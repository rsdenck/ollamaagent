#!/usr/bin/env bash
set -euo pipefail

BRANCH_MAIN="main"
BRANCH_MASTER="master"
REPO="https://github.com/rsdenck/ollamaagent.git"

echo "Starting consolidation: main <- master"
git fetch origin
git checkout "$BRANCH_MAIN"
git pull origin "$BRANCH_MAIN"

# Merge origin/master into main if master exists on remote
if git ls-remote --heads origin "$BRANCH_MASTER" | grep -w "$BRANCH_MASTER" >/dev/null 2>&1; then
  echo "Merging origin/master into main..."
  git merge "origin/$BRANCH_MASTER" --no-ff -m "Merge origin/master into main: consolidar alterações"
else
  echo "origin/master não existe no remoto; pulando merge."
fi

echo "Push da main..."
git push origin "$BRANCH_MAIN"

# Delete remote master if exists
if git ls-remote --heads origin "$BRANCH_MASTER" | grep -w "$BRANCH_MASTER" >/dev/null 2>&1; then
  echo "Deletando remote master..."
  git push origin --delete "$BRANCH_MASTER" || true
else
  echo "Remote master já não existe."
fi

echo "Definindo main como default no GitHub (via gh se disponível)"
if command -v gh >/dev/null 2>&1; then
  if [ -n "${GH_TOKEN:-}" ]; then
    echo "Autenticando gh com GH_TOKEN..."
    gh auth login --with-token <<< "$GH_TOKEN"
  fi
  gh repo edit rsdenck/ollamaagent --default-branch "$BRANCH_MAIN" || true
else
  echo "gh não está instalado; altere o default pela UI: GitHub -> Settings -> Branches -> Default branch -> main"
fi

echo "Limpeza de refs remotos e locais..."
git fetch --prune
git remote prune origin
echo "Branches remotas após limpeza (deve mostrar origin/main):"
git branch -r

echo "Removendo branch master local (se existir)"
git branch -D "$BRANCH_MASTER" || true

echo "Concluído. Verifique no GitHub se apenas 'main' existe como branch e se 'main' é o default."
