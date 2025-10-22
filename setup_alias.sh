#!/bin/bash

SHELL_CONFIG=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bash_profile"
fi

if [ -z "$SHELL_CONFIG" ]; then
    echo "❌ Неподдерживаемая оболочка"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ALIAS_LINE="alias calk='cd \"$SCRIPT_DIR\" && source .venv/bin/activate && streamlit run app.py'"

if grep -q "alias calk=" "$SHELL_CONFIG"; then
    echo "✅ Алиас 'calk' уже установлен"
else
    echo "" >> "$SHELL_CONFIG"
    echo "# UniCheck alias" >> "$SHELL_CONFIG"
    echo "$ALIAS_LINE" >> "$SHELL_CONFIG"
    echo "✅ Алиас 'calk' добавлен в $SHELL_CONFIG"
fi

source "$SHELL_CONFIG"
echo "🚀 Можешь использовать команду: calk"
