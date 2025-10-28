#!/bin/bash
set -e

echo "🚀 Installing RepoViz MCP Server..."

# Detect installation directory
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CMD="${PYTHON:-python3}"

# Check Python version
echo "Checking Python version..."
if ! command -v "$PYTHON_CMD" &> /dev/null; then
    echo "❌ Error: Python 3.11+ is required but not found"
    exit 1
fi

# Install with uv if available (faster), otherwise use pip
if command -v uv &> /dev/null; then
    echo "📦 Installing with uv (fast mode)..."
    uv pip install --system -e .
else
    echo "📦 Installing with pip..."
    $PYTHON_CMD -m pip install -e .
fi

# Detect Claude config location
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_PATH="$HOME/.config/Claude/claude_desktop_config.json"
else
    CONFIG_PATH=""
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 To use with Claude Desktop, add this to your config:"

if [ -n "$CONFIG_PATH" ] && [ -f "$CONFIG_PATH" ]; then
    echo "   Config file: $CONFIG_PATH"
fi

echo ""
echo '{
  "mcpServers": {
    "git-visualization": {
      "command": "'"$PYTHON_CMD"'",
      "args": ["'"$REPO_DIR/enhanced_mcp_server.py"'"]
    }
  }
}'

echo ""
echo "💡 Or use uvx for easier setup:"
echo "   uvx git-commit-visualization-utilities"
