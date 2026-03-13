#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-$SCRIPT_DIR/.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "error: $PYTHON_BIN not found" >&2
  exit 1
fi

"$PYTHON_BIN" -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --no-build-isolation "$SCRIPT_DIR"
"$VENV_DIR/bin/local-websearch-mcp" --self-test

cat <<EOF

Installed local-websearch-mcp into:
  $VENV_DIR

Executable:
  $VENV_DIR/bin/local-websearch-mcp

Example MCP client config:
{
  "mcpServers": {
    "local-websearch": {
      "command": "$VENV_DIR/bin/local-websearch-mcp"
    }
  }
}
EOF
