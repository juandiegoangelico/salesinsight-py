#!/usr/bin/env bash
# Cria o histórico Git com branches por funcionalidade e envia para o GitHub.
# Uso:  bash publicar_github.sh https://github.com/SEU_USUARIO/salesinsight-py.git
set -e

URL_REMOTO="$1"

if [ -d .git ]; then
  echo "[ERRO] Já existe um repositório Git nesta pasta. Apague a pasta .git para recomeçar."
  exit 1
fi

git init -b main

# 1. Estrutura inicial
git add README.md .gitignore
git commit -m "chore: cria estrutura inicial do projeto e README"

# 2. Dataset, leitura e limpeza
git checkout -b feature/dataset-e-limpeza
git add modulo_vendas.py vendas.csv
git commit -m "feat: adiciona geração, leitura, inspeção e limpeza do dataset"
git checkout main
git merge --no-ff feature/dataset-e-limpeza -m "merge: integra feature/dataset-e-limpeza"

# 3. Pipeline principal
git checkout -b feature/pipeline-main
git add main.py
git commit -m "feat: implementa pipeline principal com métricas e segmentação"
git checkout main
git merge --no-ff feature/pipeline-main -m "merge: integra feature/pipeline-main"

# 4. Relatórios exportados
git checkout -b feature/exportacao
git add outputs/
git commit -m "feat: adiciona relatórios exportados em CSV e JSON"
git checkout main
git merge --no-ff feature/exportacao -m "merge: integra feature/exportacao"

# 5. Script de publicação
git checkout -b docs/publicacao
git add publicar_github.sh
git commit -m "docs: adiciona script de versionamento e publicação"
git checkout main
git merge --no-ff docs/publicacao -m "merge: integra docs/publicacao"

echo
git log --oneline --graph --all

if [ -n "$URL_REMOTO" ]; then
  git remote add origin "$URL_REMOTO"
  git push -u origin --all
  echo "[OK] Projeto enviado para $URL_REMOTO"
else
  echo
  echo "[INFO] Histórico criado. Para enviar ao GitHub, rode:"
  echo "  git remote add origin https://github.com/SEU_USUARIO/salesinsight-py.git"
  echo "  git push -u origin --all"
fi
