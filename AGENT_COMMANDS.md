OllamaAgent - Guia de Uso (Comandos)

Este arquivo descreve como usar o OllamaAgent a partir do código Python (programático) com o Ollama Server remoto. Também cobre opções de configuração, verificação de conectividade e comandos úteis.

1) Pré-requisitos
- Ollama Server ativo em https://10.1.254.32:11434 (ou outro host/porta que você use)
- Python 3.8+
- Dependências instaladas: pip install -e .; pip install pytest (opcional para testes)
- Opcional: ADK do Google (google-adk) se desejar orquestrar agentes no futuro

2) Configuração básica
- Endereço do Ollama (remoto) pode ser fornecido por:
  - Variável de ambiente: OLLAMA_ADDRESS=http://10.1.254.32:11434
  - Código: Config(address="http://10.1.254.32:11434")
- Modelo: gemma3 (exemplo)
- Modo rápido (short_mode=True) para respostas curtas e rápidas

3) Uso programático (Python)
```python
from ollama_agent.config import Config
from ollama_agent.agent import OllamaAgent

# Configura para apontar ao Ollama remoto
cfg = Config(address="http://10.1.254.32:11434", model="gemma3", short_mode=True)
agent = OllamaAgent(cfg)

# Envia uma pergunta e imprime a resposta
resp = agent.ask("Por que o céu é azul?")
print(resp)

print("Conectado?", agent.connected)
```

4) Verificação de Conexão
- Ao criar o OllamaAgent, ele tenta realizar connect() automaticamente.
- Propriedade connected indica se a conexão com o Ollama foi estabelecida com sucesso.
- Em falhas de rede ou servidor indisponível, a conexão falha e você receberá uma exceção ao inicializar.

5) Enviando consultas
- Para enviar uma pergunta: agent.ask("Sua pergunta aqui?")
- O agent irá usar a API oficial Ollama Python (se disponível) ou REST (/v1/chat) como fallback.

6) Checagem rápida com REST (sem CLI)
- Endpoint REST padrão de chat: POST http://10.1.254.32:11434/v1/chat
- Payload típico (exemplo):
  {
    "model": "gemma3",
    "messages": [
      {"role": "system", "content": "You are a concise assistant."},
      {"role": "user", "content": "Oi"}
    ]
  }
- A resposta é extraída de forma robusta, independentemente do formato de retorno.

7) Testes de integração (local)
- pytest -q (com pytest instalado)
- O conjunto de testes já cobre criação de agent, conectividade simulada e parsing de REST.
- Testes de CLI interativo são opcionais/condicionais (dependem do Ollama CLI estar instalado no ambiente de CI).

8) Observações finais
- Ó README principal no root já cobre instruções; este arquivo fornece comandos diretos.
- Para ADK, ative e configure conforme necessidade (adk_enabled no Config).
