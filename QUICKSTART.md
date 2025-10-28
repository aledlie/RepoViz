# RepoViz MCP Quick Start

## Installation (30 seconds)

### Method 1: One-Command Install with uvx (Recommended)
```bash
uvx git-commit-visualization-utilities
```

### Method 2: Clone and Run
```bash
git clone https://github.com/aledlie/RepoViz.git
cd RepoViz && ./install.sh
```

## Configure Claude Desktop

After installation, copy the config shown in your terminal to:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

## Start Using

1. In any git repository, generate the data:
   ```bash
   git log -v > logs.txt
   ```

2. Ask Claude to visualize your commits:
   - "Show me my commit patterns by hour"
   - "Create a pie chart of commits by day of week"
   - "Generate all visualization schemas"

## Available MCP Tools

- `generate_hour_bar_chart` - Hourly commit patterns
- `generate_day_pie_chart` - Day of week distribution
- `generate_month_pie_chart` - Monthly activity
- `generate_combined_day_month_chart` - Combined visualizations
- `validate_commit_data` - Validate your data files
- `generate_schema_org_data` - Create structured metadata

## Troubleshooting

**"Python not found"**: Install Python 3.11+
```bash
# macOS
brew install python@3.11

# Linux
sudo apt install python3.11
```

**"Module not found"**: Reinstall dependencies
```bash
pip install -e .
```

**Need help?** [Open an issue](https://github.com/aledlie/RepoViz/issues)
