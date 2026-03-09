# OllamaAgent (Python) com Ollama Server remoto

Objetivo
- Criar um agent em Python que consome o Ollama de forma eficiente, conectando-se a um Ollama Server remoto e utilizando prompts curtos para acelerar respostas.
- Oferecer configuração completa via código e variáveis de ambiente, com suporte a ADK (opcional) para orquestração de agentes.
- Disponibilizar testes de integração, CI/CD e documentação em PT-BR para facilitar o uso.

Visão geral
- Este repositório implementa o OllamaAgent em Python, usando a API oficial Ollama-python quando disponível e fallback para REST (/v1/chat) caso necessário.
- Pode apontar para o Ollama Server remoto através de configuração (address) ou variável de ambiente OLLAMA_ADDRESS.
- O agent tenta estabelecer conexão com o servidor ao inicializar e disponibiliza uma API simples para enviar prompts e receber respostas.

Pré-requisitos
- Python 3.8+
- Ollama Server acessível (no seu caso: http://10.1.254.32:11434)
- Opcional: Google ADK (para integrações avançadas)

Instalação
- Instale as dependências: pip install -e .
- Opcional: pip install google-adk
- Dependência de rede: pip install requests

Configuração
- Variável de ambiente: OLLAMA_ADDRESS=http://10.1.254.32:11434
- Ou via código, por exemplo:

  from ollama_agent.config import Config
  from ollama_agent.agent import OllamaAgent

  cfg = Config(address="http://10.1.254.32:11434", model="gemma3", short_mode=True)
  agent = OllamaAgent(cfg)
  print(agent.ask("Por que o céu é azul?"))

- O endereço padrão (quando não informado) atende localmente ou a um servidor remoto configurado.

Uso básico (programático)
- Crie um Config, inicialize o OllamaAgent e chame ask:
  - resp = agent.ask("Qual é a capital do Brasil?")
  - print(resp)

- Saída rápida: usando short_mode para respostas concisas.

Testes e CI
- Os testes incluem verificação de conectividade simulada e parsing de respostas REST.
- CI com GitHub Actions executa pytest.
- Release no PyPI pode ser feito via tag vX.Y.Z.

Notas finais
- O README está em PT-BR para facilitar o onboarding.
- Se quiser, é possível adicionar um guia de integração com ADK ou ajustar o fluxo de confiança/segurança para produção.
