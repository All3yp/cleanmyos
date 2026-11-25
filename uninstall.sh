#!/usr/bin/env bash
set -e

# CleanMyOS Uninstaller Script (JSON Locales)
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$HOME/.config/cleanmyos/config.json"
LANG_PREF="pt_BR"

if [ -f "$CONFIG_FILE" ]; then
    if grep -q '"en_US"' "$CONFIG_FILE" 2>/dev/null; then
        LANG_PREF="en_US"
    fi
fi

# Locate JSON file
LOCALE_FILE="$SCRIPT_DIR/locales/${LANG_PREF}.json"
if [ ! -f "$LOCALE_FILE" ]; then
    LOCALE_FILE="$HOME/.local/share/cleanmyos/locales/${LANG_PREF}.json"
fi

get_msg() {
    local key="$1"
    python3 -c "
import json
try:
    with open('$LOCALE_FILE', 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(data.get('uninstaller', {}).get('$key', '$key'))
except Exception:
    print('$key')
" 2>/dev/null
}

echo -e "${CYAN}$(get_msg "header")${NC}"

rm -f "$HOME/.local/bin/cleanmyos"
rm -f "$HOME/.local/bin/clean"
rm -rf "$HOME/.local/share/cleanmyos"

echo -e "${GREEN}[✔] $(get_msg "removed")${NC}"
