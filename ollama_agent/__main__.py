def main():
    # Standalone entry: initialize an OllamaAgent and verify connectivity without a CLI loop
    from .config import Config
    from .agent import OllamaAgent
    import os

    address = os.environ.get("OLLAMA_ADDRESS", "http://10.1.254.32:11434")
    cfg = Config(address=address, model="gemma3", short_mode=True)
    try:
        agent = OllamaAgent(cfg)
        # If we reached here, connection succeeded
        print(f"OllamaAgent conectado com sucesso em {address}")
    except Exception as e:
        print(f"Falha ao conectar ao Ollama: {e}")
        raise


if __name__ == "__main__":  # pragma: no cover
    main()
