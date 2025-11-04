#!/bin/bash

ENV_FILE="$(dirname "$0")/.env"

set_env_var() {
    local var_name="$1"
    local var_value="$2"
    if grep -q "^export $var_name=" "$ENV_FILE" 2>/dev/null; then
        sed -i "s|^export $var_name=.*$|export $var_name=\"$var_value\"|" "$ENV_FILE"
    else
        echo "export $var_name=\"$var_value\"" >> "$ENV_FILE"
    fi
}

if [ ! -f "$ENV_FILE" ]; then
    touch "$ENV_FILE"
    echo "# Automatically generated .env file" > "$ENV_FILE"
    echo "" >> "$ENV_FILE"
fi

if ! grep -q '^export GEMINI_API_KEY=' "$ENV_FILE"; then
    echo "Gemini API key not found."
    read -p "Enter your Gemini API key: " GEMINI_API_KEY
    set_env_var "GEMINI_API_KEY" "$GEMINI_API_KEY"
    echo "API key saved."
fi

HOME_PATH="$HOME"
BIN_PATH="$(command -v python3 | xargs dirname)"

set_env_var "HOME_PATH" "$HOME_PATH"
set_env_var "BIN_PATH" "$BIN_PATH"

set -a
source "$ENV_FILE"
set +a

echo "Using environment:"
echo "  GEMINI_API_KEY=${GEMINI_API_KEY:0:6}******"
echo "  HOME_PATH=$HOME_PATH"
echo "  BIN_PATH=$BIN_PATH"
echo ""

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

if [ -f "$(dirname "$0")/requirements.txt" ]; then
    echo "Installing/updating Python dependencies..."
    pip install --upgrade pip >/dev/null
    pip install -r "$(dirname "$0")/requirements.txt"
fi

exec python3 -u -m app.main "$@"