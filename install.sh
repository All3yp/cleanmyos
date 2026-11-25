#!/usr/bin/env bash
set -e

# CleanMyOS Installer Script (Universal Linux + JSON Locales)
# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Determine Language Preference
SELECTED_LANG="pt_BR"

for arg in "$@"; do
    case "$arg" in
        --lang=en|--en)
            SELECTED_LANG="en_US"
            ;;
        --lang=pt|--pt)
            SELECTED_LANG="pt_BR"
            ;;
    esac
done

if [ -t 0 ] && [[ "$*" != *"--lang="* ]] && [[ "$*" != *"--pt"* ]] && [[ "$*" != *"--en"* ]]; then
    echo -e "${CYAN}==============================================${NC}"
    echo -e "${YELLOW}Escolha o idioma / Choose your language:${NC}"
    echo -e "  ${GREEN}1)${NC} Português (pt-BR) [Padrão]"
    echo -e "  ${GREEN}2)${NC} English (en-US)"
    read -r -p "Opção / Choice [1]: " LANG_CHOICE
    case "$LANG_CHOICE" in
        2|en|EN|english|English)
            SELECTED_LANG="en_US"
            ;;
        *)
            SELECTED_LANG="pt_BR"
            ;;
    esac
fi

LOCALE_FILE="$SCRIPT_DIR/locales/${SELECTED_LANG}.json"
if [ ! -f "$LOCALE_FILE" ]; then
    LOCALE_FILE="$SCRIPT_DIR/locales/pt_BR.json"
fi

# Helper to read strings directly from JSON with optional replacements
get_msg() {
    local key="$1"
    local p1="${2:-}"
    local p2="${3:-}"
    python3 -c "
import json
try:
    with open('$LOCALE_FILE', 'r', encoding='utf-8') as f:
        data = json.load(f)
        text = data.get('installer', {}).get('$key', '$key')
        text = text.replace('{shell}', '$p1').replace('{path}', '$p1').replace('{config}', '$p2')
        print(text)
except Exception:
    print('$key')
" 2>/dev/null
}

echo -e "\n${CYAN}==============================================${NC}"
echo -e "${CYAN}        $(get_msg "header")       ${NC}"
echo -e "${CYAN}==============================================${NC}"
echo -e "${GREEN}[✔] $(get_msg "lang_selected")${NC}"

# Save language preference to ~/.config/cleanmyos/config.json
CONFIG_DIR="$HOME/.config/cleanmyos"
mkdir -p "$CONFIG_DIR"
cat <<EOF > "$CONFIG_DIR/config.json"
{
  "lang": "$SELECTED_LANG"
}
EOF

# 2. Check Python3
if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${RED}[✘] $(get_msg "python_not_found")${NC}"
    exit 1
fi
echo -e "${GREEN}[✔] $(get_msg "python_detected")${NC}"

# 3. Check / Install Rich dependency
if ! python3 -c "import rich" >/dev/null 2>&1; then
    echo -e "${YELLOW}[!] $(get_msg "rich_installing")${NC}"
    if command -v pacman >/dev/null 2>&1; then
        pip install --user rich || sudo pacman -S --noconfirm python-rich || python3 -m pip install --user rich
    elif command -v apt-get >/dev/null 2>&1; then
        pip install --user rich || sudo apt-get install -y python3-rich || python3 -m pip install --user rich
    elif command -v dnf >/dev/null 2>&1; then
        pip install --user rich || sudo dnf install -y python3-rich || python3 -m pip install --user rich
    else
        python3 -m pip install --user rich
    fi
fi

if python3 -c "import rich" >/dev/null 2>&1; then
    echo -e "${GREEN}[✔] $(get_msg "rich_ready")${NC}"
else
    echo -e "${RED}[✘] $(get_msg "rich_failed")${NC}"
    exit 1
fi

# 3b. Optional uv installation
if command -v uv >/dev/null 2>&1; then
    echo -e "${GREEN}[✔] $(get_msg "uv_already")${NC}"
else
    echo -e "${YELLOW}[!] $(get_msg "uv_not_found")${NC}"
    INSTALL_UV="n"
    if [ -t 0 ]; then
        read -r -p "$(get_msg "uv_install_prompt") " INSTALL_UV
    fi
    case "$INSTALL_UV" in
        y|Y|s|S|yes|YES|sim|SIM)
            echo -e "${CYAN}[*] $(get_msg "uv_installing")${NC}"
            if command -v curl >/dev/null 2>&1; then
                curl -LsSf https://astral.sh/uv/install.sh | sh
            elif command -v wget >/dev/null 2>&1; then
                wget -qO- https://astral.sh/uv/install.sh | sh
            else
                echo -e "${RED}[✘] $(get_msg "uv_failed")${NC}"
                INSTALL_UV="n"
            fi
            if [ "$INSTALL_UV" != "n" ]; then
                export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
                if command -v uv >/dev/null 2>&1; then
                    echo -e "${GREEN}[✔] $(get_msg "uv_installed")${NC}"
                else
                    echo -e "${YELLOW}[!] $(get_msg "uv_failed")${NC}"
                fi
            fi
            ;;
        *)
            echo -e "${CYAN}[*] $(get_msg "uv_skipped")${NC}"
            ;;
    esac
fi

# 4. Setup ~/.local/bin and ~/.local/share/cleanmyos/locales
TARGET_DIR="$HOME/.local/bin"
mkdir -p "$TARGET_DIR"

TARGET_BIN="$TARGET_DIR/cleanmyos"
TARGET_LINK="$TARGET_DIR/clean"

cp "$SCRIPT_DIR/cleanmyos" "$TARGET_BIN"
chmod +x "$TARGET_BIN"
ln -sf "$TARGET_BIN" "$TARGET_LINK"

# Install JSON locales
XDG_LOCALES="$HOME/.local/share/cleanmyos/locales"
mkdir -p "$XDG_LOCALES"
cp -r "$SCRIPT_DIR/locales/"*.json "$XDG_LOCALES/"

echo -e "${GREEN}[✔] $(get_msg "installed_in") ${CYAN}$TARGET_BIN${NC}"
echo -e "${GREEN}[✔] $(get_msg "shortcut_created") ${CYAN}$TARGET_LINK${NC}"

# 5. Detect User Shell and Configure PATH
USER_SHELL="$(basename "${SHELL:-bash}")"
echo -e "${CYAN}[*] $(get_msg "shell_detected") ${YELLOW}$USER_SHELL${NC}"

CONFIGURED=false

case "$USER_SHELL" in
    fish)
        FISH_CONFIG="$HOME/.config/fish/config.fish"
        mkdir -p "$HOME/.config/fish"
        if [ -f "$FISH_CONFIG" ]; then
            if ! grep -q "$TARGET_DIR" "$FISH_CONFIG" 2>/dev/null; then
                echo -e "\n# CleanMyOS PATH\nfish_add_path $TARGET_DIR" >> "$FISH_CONFIG"
                echo -e "${GREEN}[✔] $(get_msg "added_to" "Fish Shell" "$FISH_CONFIG")${NC}"
            else
                echo -e "${GREEN}[✔] $(get_msg "already_in" "$TARGET_DIR" "$FISH_CONFIG")${NC}"
            fi
        else
            echo -e "fish_add_path $TARGET_DIR" > "$FISH_CONFIG"
            echo -e "${GREEN}[✔] $(get_msg "added_to" "Fish Shell" "$FISH_CONFIG")${NC}"
        fi
        CONFIGURED=true
        ;;
    zsh)
        ZSH_CONFIG="$HOME/.zshrc"
        touch "$ZSH_CONFIG"
        if ! grep -q "$TARGET_DIR" "$ZSH_CONFIG" 2>/dev/null; then
            echo -e "\n# CleanMyOS PATH\nexport PATH=\"$TARGET_DIR:\$PATH\"" >> "$ZSH_CONFIG"
            echo -e "${GREEN}[✔] $(get_msg "added_to" "Zsh" "$ZSH_CONFIG")${NC}"
        else
            echo -e "${GREEN}[✔] $(get_msg "already_in" "$TARGET_DIR" "$ZSH_CONFIG")${NC}"
        fi
        CONFIGURED=true
        ;;
    bash)
        BASH_CONFIG="$HOME/.bashrc"
        touch "$BASH_CONFIG"
        if ! grep -q "$TARGET_DIR" "$BASH_CONFIG" 2>/dev/null; then
            echo -e "\n# CleanMyOS PATH\nexport PATH=\"$TARGET_DIR:\$PATH\"" >> "$BASH_CONFIG"
            echo -e "${GREEN}[✔] $(get_msg "added_to" "Bash" "$BASH_CONFIG")${NC}"
        else
            echo -e "${GREEN}[✔] $(get_msg "already_in" "$TARGET_DIR" "$BASH_CONFIG")${NC}"
        fi
        CONFIGURED=true
        ;;
esac

# Fallback for other shells: update ~/.profile
if [ "$CONFIGURED" = false ]; then
    PROFILE="$HOME/.profile"
    touch "$PROFILE"
    if ! grep -q "$TARGET_DIR" "$PROFILE" 2>/dev/null; then
        echo -e "\n# CleanMyOS PATH\nexport PATH=\"$TARGET_DIR:\$PATH\"" >> "$PROFILE"
        echo -e "${GREEN}[✔] $(get_msg "added_to_profile")${NC}"
    fi
fi

echo -e "\n${CYAN}==============================================${NC}"
echo -e "${GREEN}$(get_msg "success")${NC}"
echo -e "$(get_msg "launch_hint")"
echo -e "${CYAN}==============================================${NC}"
