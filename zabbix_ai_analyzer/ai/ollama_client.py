import json
import requests
import logging

from .prompts import PROMPTS
from tenacity import retry, stop_after_attempt, wait_fixed

logger = logging.getLogger("zabbix_ai_analyzer.ai.ollama_client")


class OllamaClient:
    def __init__(self, address: str, model: str = "gemma3", short_mode: bool = True):
        self.address = address.rstrip("/")
        self.model = model
        self.short_mode = short_mode

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        before_sleep=lambda retry_state: logger.warning(
            "Falha ao comunicar com Ollama para análise. Tentando novamente: %s", 
            retry_state.outcome.exception()
        )
    )
    def analyze(self, mode: str, data: dict) -> str:
        # Build prompt from data
        data_str = json.dumps(data, indent=2)
        template = PROMPTS.get(mode, PROMPTS["health"])
        prompt = template.format(data=data_str)
        logger.info("Analise IA: modo=%s, tamanho_dado=%d chars", mode, len(data_str))
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a concise Zabbix AI Copilot."},
                {"role": "user", "content": prompt},
            ],
        }
        url = f"{self.address}/v1/chat"
        logger.debug("Enviando req para Ollama em %s", url)
        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()
        data_out = r.json()
        logger.debug(
            "Resposta Ollama recebida: status=%s", getattr(r, "status_code", "NA")
        )

        # Try robust extraction
        def _extract(d):
            if isinstance(d, dict):
                ch = d.get("choices")
                if isinstance(ch, list) and ch:
                    m = ch[0].get("message")
                    if isinstance(m, dict):
                        return m.get("content")

        txt = _extract(data_out)
        if isinstance(txt, str):
            return txt.strip()
        return json.dumps(data_out)
