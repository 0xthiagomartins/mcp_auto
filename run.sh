#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"
PYTHON="${VENV_DIR}/bin/python"
PIP="${VENV_DIR}/bin/pip"

if [[ ! -d "$VENV_DIR" ]] || [[ ! -x "$PYTHON" ]]; then
  echo "Ambiente não encontrado. Criando venv com $(python3 --version)..."
  python3 -m venv "$VENV_DIR"
fi

echo "Instalando/atualizando dependências..."
"$PIP" install --upgrade pip -q
"$PIP" install -e . -q

echo "Garantindo banco populado..."
"$PYTHON" scripts/seed_vehicles.py

if [[ "${1:-}" == "cli" ]]; then
  echo "Iniciando CLI (chat no terminal)..."
  exec "$PYTHON" cli.py "${@:2}"
fi

echo "Iniciando aplicação Streamlit..."
exec "$VENV_DIR/bin/streamlit" run app_streamlit.py "$@"
