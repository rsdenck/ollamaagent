# OllamaAgent (Python) - Integração com Ollama

Objetivo
- Criar um OllamaAgent em Python para consumir o Ollama de forma rápida, enviando inputs curtos.
- Preparar integração com o Google ADK (opcional) para orquestrar agentes.
- Tornar toda configuração completamente configurável, para apontar para o seu Ollama Server.

O que o projeto oferece
- Um pacote Python configurável (ollama_agent) com:
  - address, model, system_prompt, timeouts e modo rápido (short_mode)
  - camada de cliente que conversa com Ollama via cliente Python oficial ou REST fallback
  - CLI simples para interação local
- Preparação para integração com ADK via adk_enabled no Config (pronta para extensão)
- CI/CD básica com GitHub Actions, e templates para release no PyPI

Instalação (recomendado)
- Instalar o Ollama (server) no seu ambiente, se ainda não estiver ativo
- Dependências Python:
  - pip install ollama (client oficial Ollama, opcional)
- Instalar ADK (opcional):
  - pip install google-adk
- Preparar o repositório para deploy (além do CI): habilitar PyPI token

Configuração para testar com o seu Ollama Server
- Use o servidor Ollama em http://10.1.254.32:11434
- Defina a variável de ambiente OLLAMA_ADDRESS para apontar para o servidor remoto:
  - export OLLAMA_ADDRESS="http://10.1.254.32:11434"
- OU passe via Config.address ao criar o OllamaAgent:
  - cfg = Config(address="http://10.1.254.32:11434", model="gemma3")
- Modelo recomendado: gemma3; modo curto (short_mode) para respostas rápidas

Uso básico (exemplos)
- Via código:
  from ollama_agent import Config, OllamaAgent
  cfg = Config(address="http://10.1.254.32:11434", model="gemma3", short_mode=True)
  agent = OllamaAgent(cfg)
  print(agent.ask("Por que o céu é azul?"))
- Via CLI:
  python -m ollama_agent

Notas
- O endpoint REST pode variar; o agente já faz fallback para múltiplos caminhos (/v1/chat, /v1/chat/).
- Se quiser mudar o servidor rapidamente, use a variável OLLAMA_ADDRESS ou o Config.address.
- ADK está preparado para extensão futura; se desejar, posso implementá-la já nesta versão.

Próximos passos sugeridos
- Adicionar testes unitários e de integração com um Ollama local disponível no CI.
- Completar a integração com ADK (fluxos de tasks) conforme a sua arquitetura.
- Refinar o packaging (PyPI) e adicionar mais exemplos de uso.
