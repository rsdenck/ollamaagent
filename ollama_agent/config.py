from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    # Ollama server base address. Pode ser override via GPIO env var OLLAMA_ADDRESS
    # Default is local Ollama, but can be overridden for testing (ex.: 10.1.254.32:11434)
    address: Optional[str] = None
    # Model name to query
    model: str = "gemma3"
    # Optional system prompt to guide the assistant
    system_prompt: Optional[str] = None
    # If True, use a concise prompt to maximize speed
    short_mode: bool = True
    # Optional generation controls; may be ignored by some backends
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    # Optional ADK usage flag (for future extension)
    adk_enabled: bool = False
    # Verbose logging to stdout
    verbose: bool = False
    # Request timeout for network calls (seconds)
    timeout: int = 5
