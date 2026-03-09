from __future__ import annotations

import json
import time
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_fixed
import logging

logger = logging.getLogger(__name__)

try:
    # Preferred path: Ollama Python client
    from ollama import chat as _ollama_chat  # type: ignore
    from ollama import ChatResponse as _ChatResponse  # type: ignore

    _HAS_OLLAMA_LIB = True
except Exception:
    _HAS_OLLAMA_LIB = False

import os
import requests

from .config import Config


class OllamaClient:
    def __init__(self, config: Config):
        # Resolve address: explicit config, environment variable, then default local
        self.address = (
            (config.address or os.environ.get("OLLAMA_ADDRESS"))
            or "http://127.0.0.1:11434"
        ).rstrip("/")
        self.model = config.model or "gemma3"
        self.system_prompt = config.system_prompt
        self.short_mode = bool(config.short_mode)
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens
        self.timeout = int(config.timeout) if config.timeout is not None else 5
        self.verbose = bool(config.verbose)

        # Ensure a default concise system prompt if none provided
        if not self.system_prompt and self.short_mode:
            self.system_prompt = (
                "You are a concise assistant. Respond briefly to maximize speed."
            )
        # Fallback: If ADK is desired in the future, expose a flag here
        self._has_ollama_lib = _HAS_OLLAMA_LIB
        self._connected = False

    def _test_connection(self) -> bool:
        # Try a lightweight probe against the server
        probes = [
            f"{self.address}/v1/models",
            f"{self.address}/health",
            f"{self.address}/healthz",
            self.address,
            f"{self.address}/",
        ]
        for url in probes:
            try:
                r = requests.get(url, timeout=self.timeout)
                if 200 <= r.status_code < 300:
                    return True
            except Exception:
                continue
        return False

    def connect(self) -> bool:
        if self._test_connection():
            self._connected = True
            return True
        raise ConnectionError(f"Não foi possível conectar ao Ollama em {self.address}")

    def _build_messages(self, user_input: str) -> List[Dict[str, str]]:
        msgs: List[Dict[str, str]] = []
        if self.system_prompt:
            msgs.append({"role": "system", "content": self.system_prompt})
        else:
            # Always include a minimal system prompt to set tone
            msgs.append({"role": "system", "content": "You are a helpful assistant."})
        msgs.append({"role": "user", "content": user_input})
        return msgs

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        before_sleep=lambda retry_state: logger.warning(
            "Falha ao conversar com Ollama: %s. Tentando novamente...", 
            retry_state.outcome.exception()
        )
    )
    def chat(self, user_input: str) -> str:
        messages = self._build_messages(user_input)

        # Try using the official Ollama Python client if available
        if self._has_ollama_lib:
            try:
                # NOTE: signatures may vary by library version
                resp = _ollama_chat(model=self.model, messages=messages)  # type: ignore
                # Support both new and old return formats
                content = None
                if hasattr(resp, "message") and isinstance(
                    getattr(resp, "message"), dict
                ):
                    content = resp.message.get("content")  # type: ignore
                elif hasattr(resp, "content"):
                    content = getattr(resp, "content")  # type: ignore
                elif isinstance(resp, str):
                    content = resp
                if isinstance(content, str) and content.strip():
                    return content.strip()
            except Exception:
                # Fall back to REST API if the library call fails
                pass

        # Fallback: direct REST API call to Ollama server with endpoint fallbacks
        payload = {"model": self.model, "messages": messages, "stream": False}
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens

        endpoints = ["/api/chat", "/v1/chat/completions"]
        last_error: Optional[Exception] = None
        for ep in endpoints:
            url = f"{self.address}{ep}"
            try:
                r = requests.post(url, json=payload, timeout=self.timeout)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                last_error = e
                continue
            else:
                # Try to extract content robustly
                def _content_from(d) -> Optional[str]:
                    if isinstance(d, dict):
                        # Native
                        m_native = d.get("message")
                        if isinstance(m_native, dict):
                            txt = m_native.get("content")
                            if isinstance(txt, str):
                                return txt
                        # OpenAI format
                        ch = d.get("choices")
                        if isinstance(ch, list) and ch:
                            m = (
                                ch[0].get("message")
                                if isinstance(ch[0], dict)
                                else None
                            )
                            if isinstance(m, dict):
                                txt = m.get("content")
                                if isinstance(txt, str):
                                    return txt
                        resp = d.get("response")
                        if isinstance(resp, dict):
                            txt = resp.get("content")
                            if isinstance(txt, str):
                                return txt
                        if isinstance(d.get("content"), str):
                            return d["content"]
                    return None

                content = _content_from(data)
                if isinstance(content, str) and content.strip():
                    return content.strip()
                try:
                    return json.dumps(data)
                except Exception:
                    return str(data)
        if last_error:
            raise RuntimeError(
                f"Ollama REST call failed on all endpoints: {last_error}"
            )
        raise RuntimeError("Ollama REST call failed on all endpoints")
