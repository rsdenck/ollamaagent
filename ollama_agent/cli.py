#!/usr/bin/env python3
"""Simple CLI for interacting with OllamaAgent.

Usage:
  python -m ollama_agent.cli [--address URL] [--model NAME] [--short] [--system "PROMPT"]
"""

from __future__ import annotations

import argparse
import os

from .config import Config
from .agent import OllamaAgent


def _build_config_from_args(args: argparse.Namespace) -> Config:
    # Prioritize explicit arg, then environment variable, then a testing default.
    # For testing, default to the user's provided Ollama Server at 10.1.254.32:11434
    address = args.address or os.environ.get(
        "OLLAMA_ADDRESS", "http://10.1.254.32:11434"
    )
    model = args.model or os.environ.get("OLLAMA_MODEL", "gemma3")
    system_prompt = args.system
    short_mode = True if args.short else False
    conf = Config(
        address=address,
        model=model,
        system_prompt=system_prompt,
        short_mode=short_mode,
        timeout=args.timeout or 5,
    )
    return conf


def run():
    parser = argparse.ArgumentParser(description="OllamaAgent CLI (Python)")
    parser.add_argument(
        "--address", help="Ollama server base URL (default: http://127.0.0.1:11434)"
    )
    parser.add_argument("--model", help="Model name (default: gemma3)")
    parser.add_argument("--system", help="System prompt to guide the assistant")
    parser.add_argument(
        "--short", action="store_true", help="Use concise prompts for speed"
    )
    parser.add_argument(
        "--timeout", type=int, help="HTTP request timeout in seconds (default: 5)"
    )
    args = parser.parse_args()

    config = _build_config_from_args(args)
    agent = OllamaAgent(config)

    print("OllamaAgent CLI. Type 'exit' or 'quit' to end.")
    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user.strip().lower() in {"exit", "quit"}:
            break
        try:
            resp = agent.ask(user)
            print(f"Ollama: {resp}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    run()
