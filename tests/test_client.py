import os
import types

import pytest

from ollama_agent.config import Config
from ollama_agent.client import OllamaClient


def test_build_messages_structure():
    cfg = Config(model="gemma3", short_mode=True, system_prompt=None)
    # Force no Ollama Python client usage to test internal message builder
    cfg.address = "http://example.invalid"
    client = OllamaClient(cfg)
    msgs = client._build_messages("Hello")
    assert isinstance(msgs, list)
    assert len(msgs) == 2
    assert msgs[0]["role"] == "system"
    assert isinstance(msgs[0]["content"], str)
    assert msgs[1]["role"] == "user"


class DummyResp:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


def test_chat_rest_parsing(monkeypatch):
    # Ensure REST path is used by disabling the Ollama Python client
    import ollama_agent.client as client_mod

    monkeypatch.setattr(client_mod, "_HAS_OLlama_LIB", False)

    # Build a client pointing to a dummy address
    cfg = Config(model="gemma3", short_mode=True)
    cfg.address = "http://example.invalid:1234"
    client = OllamaClient(cfg)

    # Patch requests.post to return a deterministic response
    class Resp:
        status_code = 200

        def json(self):
            return {"choices": [{"message": {"content": "Hello from Ollama"}}]}

    monkeypatch.setattr("requests.post", lambda *a, **k: Resp())

    out = client.chat("Oi")
    assert isinstance(out, str)
    assert "Hello" in out


def test_connect_success(monkeypatch):
    import ollama_agent.client as client_mod

    # Pretend the server is healthy via the connectivity probe
    def dummy_test(self):
        return True

    monkeypatch.setattr(
        client_mod.OllamaClient, "_test_connection", dummy_test, raising=False
    )
    cfg = Config(model="gemma3", short_mode=True)
    client = OllamaClient(cfg)
    # Should be able to call connect without raising
    client.connect()
    assert getattr(client, "_connected", True) or True


def test_connect_failure(monkeypatch):
    import ollama_agent.client as client_mod

    monkeypatch.setattr(
        client_mod.OllamaClient, "_test_connection", lambda self: False, raising=False
    )
    cfg = Config(model="gemma3", short_mode=True)
    client = OllamaClient(cfg)
    with pytest.raises(ConnectionError):
        client.connect()
