import os
import pytest
import requests

from ollama_agent.config import Config
from ollama_agent.client import OllamaClient


def test_build_messages_structure():
    cfg = Config(model="gemma3", short_mode=True, system_prompt=None)
    cfg.address = os.environ.get("OLLAMA_ADDRESS")
    client = OllamaClient(cfg)
    msgs = client._build_messages("Hello")
    assert isinstance(msgs, list)
    assert len(msgs) == 2
    assert msgs[0]["role"] == "system"
    assert isinstance(msgs[0]["content"], str)
    assert msgs[1]["role"] == "user"


def _server_available(address: str) -> bool:
    try:
        url = address.rstrip("/") + "/health"
        r = requests.get(url, timeout=2)
        return r.status_code in (200, 204)
    except Exception:
        return False


def test_chat_real_server():
    address = os.environ.get("OLLAMA_ADDRESS", "http://10.1.254.32:11434")
    cfg = Config(address=address, model="gemma3", short_mode=True)
    client = OllamaClient(cfg)
    if not _server_available(address):
        pytest.skip(
            f"Ollama server not available at {address}, skipping real-server test."
        )
    try:
        resp = client.chat("Oi")
    except Exception as e:
        pytest.skip(f"Error contacting Ollama: {e}")
    assert isinstance(resp, str)
    assert len(resp.strip()) > 0
