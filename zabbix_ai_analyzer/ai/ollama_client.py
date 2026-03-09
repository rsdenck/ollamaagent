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
        
        # Evita transbordamento do Context Window do LLM e longos Timeouts com dados massivos
        if len(data_str) > 12000:
            data_str = data_str[:12000] + "\n\n...[DADOS TRUNCADOS DEVIDO AO VOLUME DE ROTINAS]..."
            
        # Template estruturado para forçar uso de dados reais
        prompt_template = (
            "CONTEXTO TÉCNICO (DADOS REAIS DO ZABBIX):\n"
            "{data}\n\n"
            "INSTRUÇÕES CRÍTICAS DE ENGENHARIA SRE:\n"
            "1. Analise OBRIGATORIAMENTE: Uso de CPU (%), Memória (%) e Espaço em Disco (%).\n"
            "2. REGRA DE OURO: NUNCA USE NÚMEROS FRACIONÁRIOS (FLUTUANTES). Arredonde tudo para o NÚMERO INTEIRO mais próximo (ex: 3.99% vira 4%).\n"
            "3. CONVERSÃO DE UNIDADES: Transforme Bytes (B) em Gigabytes (GB) ou Megabytes (MB) para facilitar a leitura. Use apenas números inteiros.\n"
            "4. Se um dado não existir, use 'Dado não disponível'. NUNCA INVENTE.\n"
            "5. ESTRUTURA DA RESPOSTA:\n"
            "   **Health**: [Status CPU/RAM/Disco]\n"
            "   **Security**: [Alertas ativos ou 'Nenhum alerta']\n"
            "   **Capacity**: [Tamanhos totais/usados em GB/MB]\n"
            "6. Resposta extremamente limpa, profissional, sem emojis e sem introduções."
        ) if mode == "consolidated" else PROMPTS.get(mode, PROMPTS.get("health", "{data}")).format(data=data_str)
        
        prompt = prompt_template if mode == "consolidated" else prompt_template
        
        if mode == "consolidated":
            prompt = prompt_template.format(data=data_str)

        logger.info("Analise IA: modo=%s, tamanho_dado=%d chars", mode, len(data_str))
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system", 
                    "content": "Você é um Engenheiro SRE sênior. Sua tarefa é extrair fatos numéricos Puros de JSONs do Zabbix. Proibido alucinar. Proibido emojis. Se a métrica não existe no JSON, não comente sobre ela ou use 'N/A'."
                },
                {"role": "user", "content": prompt},
            ],
            "stream": False
        }
        url = f"{self.address}/api/chat"
        logger.debug("Enviando req para Ollama em %s", url)
        r = requests.post(url, json=payload, timeout=300)
        r.raise_for_status()
        data_out = r.json()
        logger.debug(
            "Resposta Ollama recebida: status=%s", getattr(r, "status_code", "NA")
        )

        # Try robust extraction
        def _extract(d):
            if isinstance(d, dict):
                # Formato nativo do Ollama (/api/chat)
                msg = d.get("message")
                if isinstance(msg, dict):
                    return msg.get("content")
                # Formato OpenAI Compatible (/v1/chat/completions)
                ch = d.get("choices")
                if isinstance(ch, list) and ch:
                    m = ch[0].get("message")
                    if isinstance(m, dict):
                        return m.get("content")

        txt = _extract(data_out)
        if isinstance(txt, str):
            return txt.strip()
        return json.dumps(data_out)
