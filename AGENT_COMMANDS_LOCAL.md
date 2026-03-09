# Manutenção Local do Main (sem mocks)

Objetivo: consolidar tudo na branch main no repositório remoto e remover a branch master, rodando tudo localmente com o script de manutenção.

Pré-requisitos
- Ambiente com Python 3.8+
- Git instalado e configurado com acesso ao repositório remoto
- gh (GitHub CLI) opcional, apenas se você quiser definir o default via CLI
- O Ollama Server remoto disponível (ex.: http://10.1.254.32:11434)

Passos para executar
   - git fetch origin
   - git checkout main
   - git pull origin main
   - if git ls-remote --heads origin master | grep master; then
       git merge origin/master --no-ff -m "Merge origin/master into main: consolidar alterações"
     fi

2) Enviar main para o remoto
   - git push origin main

3) Excluir master no remoto
   - git push origin --delete master
   - Verifique se a deleção ocorreu sem erros na UI do GitHub

4) Definir main como default (opcional via gh)
   - gh repo edit rsdenck/ollamaagent --default-branch main
   - Caso gh não esteja disponível, altere pela UI do GitHub: Settings > Branches > Default branch > main

5) Limpar refs
   - git fetch --prune
   - git remote prune origin
   - git branch -r  # Deve listar origin/main

6) Remover master local (caso exista)
   - git branch -D master

7) Executar script de manutenção (alternativa)
   - Este repositório já inclui o script scripts/maintain_main_local.py
   - Execute: python3 scripts/maintain_main_local.py

Observações
- Se houver políticas de branch no remoto (proteção de master), desative-as antes de deletar a branch.
- Em ambientes que não permitam automação com gh, use a UI do GitHub para definir o default.
- Este guia foca em operações reais, sem mocks ou dados simulados.
