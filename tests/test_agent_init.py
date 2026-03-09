import pytest

from ollama_agent.config import Config
from ollama_agent.agent import OllamaAgent


def test_agent_initializes_and_connects(monkeypatch):
    # Monkeypatch connect to simulate a successful connection
    monkeypatch.setattr(
        "ollama_agent.client.OllamaClient.connect",
        lambda self: setattr(self, "_connected", True),
    )
    cfg = Config(model="gemma3", short_mode=True)
    agent = OllamaAgent(cfg)
    assert agent.connected
