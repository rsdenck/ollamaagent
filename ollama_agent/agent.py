from __future__ import annotations

from typing import Optional

from .config import Config
from .client import OllamaClient


class OllamaAgent:
    def __init__(self, config: Optional[Config] = None):
        if config is None:
            config = Config()
        self.config = config
        self.client = OllamaClient(config)
        # Attempt to connect to the Ollama server upon initialization
        self.client.connect()

    def ask(self, user_input: str) -> str:
        """Send a user input to Ollama and return the model's response as text."""
        return self.client.chat(user_input)

    @property
    def connected(self) -> bool:
        return bool(getattr(self.client, "_connected", False))
