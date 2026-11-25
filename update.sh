#!/usr/bin/env bash
set -e

# CleanMyOS Self-Updater (Fetches from original repository)
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORIGINAL_REPO="https://github.com/All3yp/cleanmyos.git"

echo -e "${CYAN}==============================================${NC}"
echo -e "${CYAN}        CleanMyOS Updater                    ${NC}"
echo -e "${CYAN}==============================================${NC}"

cd "$SCRIPT_DIR"

if [ ! -d ".git" ]; then
    echo -e "${RED}[✘] Erro: Este diretório não é um repositório git.${NC}"
    exit 1
fi

# Ensure remote is configured
REMOTES="$(git remote -v)"
TARGET_REMOTE="origin"

if [[ "$REMOTES" == *"$ORIGINAL_REPO"* ]]; then
    for r in $(git remote); do
        if [[ "$(git remote get-url "$r" 2>/dev/null)" == "$ORIGINAL_REPO" ]]; then
            TARGET_REMOTE="$r"
            break
        fi
    done
else
    if git remote | grep -q "^upstream$"; then
        git remote set-url upstream "$ORIGINAL_REPO"
    else
        git remote add upstream "$ORIGINAL_REPO"
    fi
    TARGET_REMOTE="upstream"
fi

echo -e "${YELLOW}[*] Buscando atualizações de ${CYAN}$TARGET_REMOTE ($ORIGINAL_REPO)...${NC}"
git fetch "$TARGET_REMOTE" main

LOCAL_HASH="$(git rev-parse HEAD)"
REMOTE_HASH="$(git rev-parse "$TARGET_REMOTE/main")"

if [ "$LOCAL_HASH" = "$REMOTE_HASH" ]; then
    echo -e "${GREEN}[✔] Você já está na versão mais recente!${NC}"
    exit 0
fi

echo -e "${YELLOW}[*] Baixando novidades...${NC}"
git pull --rebase "$TARGET_REMOTE" main

echo -e "${YELLOW}[*] Reinstalando nova versão no sistema...${NC}"
chmod +x install.sh
./install.sh "$@"

echo -e "${GREEN}[✔] CleanMyOS atualizado com sucesso!${NC}"
