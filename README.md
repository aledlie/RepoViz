# RepoViz MCP Server

**Code Observability Utils** - Bringing professional data validation, structured metadata, and advanced configuration to your Git/mercurial analytics workflow.
Provides a comprehensive toolkit for structuring, storing, analyzing, and visualizing your repo code & commit patterns through schematization & interactive charts and graphs.

## Features

-**Pydantic data validation**

-**schema.org structured data** & **database support**

-**an advanced MCP server for programmatic access.**

## Installation

### Generate logs.txt from commit data

#### For git:
```bash
git log -v > logs.txt
```
#### For mercurial:
```bash
hg log -v > logs.txt
```
### 🎯 Warning: Run as a scheduled task if large (e.g. chron)

The output will look ~like this for every git commit:
```txt
commit db89c01b219253e21310cd40353e3025089ea601
Author: My Name <myemail@my_cool_domain.mcp>
Date:   Mon Aug 25 06:38:24 2025 -0500

    Your Commit Message
```
And like ~this for hg:
```txt
  changeset:   59:783a1a00679c0i
  user:        My Name <user@university.edu>
  date:        Tue Jan 07 08:35:49 2024 -0500
  files:       apply_laplacian.f90
  description: debug_master
  Topic: Fixed minor error in Laplacian.
  Description:
  * Factor of two error incorrect in the Laplacian.
```

## MCP Server Installation
### Easy Install:
```bash
# Clone the repository
git clone https://github.com/aledlie/RepoViz.git
cd RepoViz

# Run the setup script
python setup_enhanced.py

```
### Manual Install:
```bash
# Activate the environment
source activate.sh  # On macOS/Linux
# or
activate.bat       # On Windows

# or create virtual environment
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Make scripts executable (Unix-like systems)
chmod +x *.sh
```
## Usage

### With Claude Desktop

Add this to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "RepoViz": {
      "command": "python",
      "args": ["/path/to/RepoViz/mcp_server.py"]
    }
  }
}
```

## MCP Capabilities

### Key Functions

- **`create_default_chart_config()`**: Generate default configurations
- **`validate_commit_data_file()`**: Validate and parse data files
- **`generate_all_schemas()`**: Create schema.org structured data
- **`create_chart_from_config()`**: Generate charts from configuration

### ✨ Data Validation
- **Pydantic Models**: Type-safe data structures with automatic validation
- **Configuration Management**: Structured chart and plot configurations
- **Error Handling**: Comprehensive validation with detailed error messages

### 🏗️ Schema.org Integration
- **Structured Data**: JSON-LD schemas for SEO and discoverability
- **Software Application Schema**: Proper metadata for the toolkit
- **Dataset Schemas**: Structured data for commit analysis datasets
- **Creative Work Schemas**: Metadata for generated charts

### 🗄️ Database Support
- **SQLAlchemy ORM**: Optional database storage for commit data
- **Aggregated Statistics**: Pre-computed summaries by hour/day/month
- **Chart Metadata**: Track generated visualizations
- **Data Integrity**: Constraints and indexes for performance

### 🔧 Advanced MCP Server
- **Enhanced Tools**: Validated input/output with Pydantic
- **Configuration Support**: Custom styling and parameters
- **Schema Generation**: Automatic structured data creation
- **Error Handling**: Detailed error responses and validation

## 🎯 Quick Start

### 1. Generate Basic Charts
```bash
# Using the enhanced plotting script
github repo
python enhanced_plot_scripts.py --type hour_bar --title "My Project Commits"

# Using configuration file
python enhanced_plot_scripts.py --config examples/configs/custom_styling.json
```

### 2. Start MCP Server
```bash
# Start the enhanced MCP server
python enhanced_mcp_server.py
```

### 3. Explore Examples
```bash
# Run example configurations
python examples/example_configs.py
```

## 📊 Chart Types

| Chart Type | Description | Configuration |
|------------|-------------|---------------|
| `hour_bar` | Hourly commit distribution (bar chart) | `ChartType.HOUR_BAR` |
| `day_pie` | Day of week patterns (pie chart) | `ChartType.DAY_PIE` |
| `month_pie` | Monthly activity (pie chart) | `ChartType.MONTH_PIE` |
| `day_month_combined` | Combined day/month visualization | `ChartType.DAY_MONTH_COMBINED` |

## 🔧 Configuration

### Pydantic Models

```python
from schemas import ChartConfig, PlotConfig, ChartType

# Create plot configuration
plot_config = PlotConfig(
    dpi=600,
    figsize=(16, 10),
    color_primary="#2E8B57",
    color_secondary="#228B22",
    font_size=14
)

# Create chart configuration
config = ChartConfig(
    title="High-Resolution Commit Analysis",
    output_filename="high_res_commits",
    chart_type=ChartType.HOUR_BAR,
    repository_name="MyProject",
    plot_config=plot_config
)
```

### JSON Configuration
```json
{
  "title": "Custom Commit Analysis",
  "output_filename": "custom_chart",
  "chart_type": "day_pie",
  "repository_name": "MyRepo",
  "plot_config": {
    "dpi": 300,
    "figsize": [12, 8],
    "color_primary": "#4e79a7",
    "color_secondary": "#2e4977",
    "font_size": 12
  }
}
```

## 🌐 Schema.org Integration

### Generate Structured Data
```python
from schema_org import generate_all_schemas

# Generate all schema.org files
schema_files = generate_all_schemas(
    repository_name="MyProject",
    output_dir="./Generated Data/schemas/"
)
```

### HTML Integration
```python
from schema_org import get_jsonld_script_tag, get_software_application_schema

# Get schema data
schema = get_software_application_schema("MyProject")

# Generate HTML script tag
html_tag = get_jsonld_script_tag(schema)
```

## 🗄️ Database Support

### Initialize Database
```python
from database_schema import initialize_database

# Create database with all tables
db_manager = initialize_database()

# Add repository
repo = db_manager.get_or_create_repository("MyProject")

# Import commit data
db_manager.update_commit_summaries(repo.id)
```

### Query Statistics
```python
# Get comprehensive statistics
stats = db_manager.get_commit_statistics(repo.id)
print(f"Total commits: {stats['total_commits']}")
print(f"Hourly distribution: {stats['hourly_distribution']}")
```

## 🔌 MCP Server Tools

The enhanced MCP server provides these validated tools:

### `generate_hour_bar_chart`
```json
{
  "repository_name": "MyProject",
  "title": "Custom Hourly Analysis",
  "dpi": 600,
  "color_primary": "#FF6B6B"
}
```

### `generate_day_pie_chart`
```json
{
  "repository_name": "MyProject",
  "output_filename": "custom_day_chart"
}
```

### `generate_month_pie_chart`
```json
{
  "repository_name": "MyProject",
  "title": "Monthly Commit Patterns"
}
```

### `generate_combined_day_month_chart`
```json
{
  "repository_name": "MyProject",
  "dpi": 300
}
```

### `validate_commit_data`
```json
{
  "data_type": "hour"
}
```

### `generate_schema_org_data`
```json
{
  "repository_name": "MyProject",
  "include_charts": true
}
```

## 📁 Appendix
### Project Structure
```
RepoViz/
├── README.md                  # This file
├── requirements.txt           # Enhanced dependencies
├── pyproject.toml             # Complete project configuration
├── config.json                # Default configuration
├── setup_enhanced.py          # Enhanced setup script
├── activate.sh/.bat           # Environment activation
│
├── Core Enhanced Modules/
│   ├── schemas.py             # Pydantic data models
│   ├── schema_org.py          # Schema.org structured data
│   ├── enhanced_mcp_server.py # Advanced MCP server
│   ├── enhanced_plot_scripts.py # Enhanced plotting
│   └── database_schema.py     # SQLAlchemy database models
│
├── Examples and Documentation/
│   ├── examples/
│   │   ├── example_configs.py # Configuration examples
│   │   └── configs/           # Example JSON configs
│   └── Generated Data/
│       ├── schemas/           # Schema.org JSON-LD files
│       └── git_viz.db        # SQLite database
│
└── Original Scripts/          # All original functionality preserved
    ├── commit_history.sh
    ├── commits_by_*.sh
    ├── plot_*.py
    └── get_repo_name.sh
```

### 🎨 Advanced Styling

#### Custom Color Schemes
```python
# Professional blue theme
plot_config = PlotConfig(
    color_primary="#1f77b4",
    color_secondary="#ff7f0e"
)

# Nature theme
plot_config = PlotConfig(
    color_primary="#2E8B57",  # Sea green
    color_secondary="#228B22"  # Forest green
)

# Sunset theme
plot_config = PlotConfig(
    color_primary="#FF6B6B",  # Coral
    color_secondary="#4ECDC4"  # Turquoise
)
```

#### High-Resolution Output
```python
plot_config = PlotConfig(
    dpi=600,              # Print quality
    figsize=(20, 12),     # Large format
    font_size=16,         # Readable text
    title_fontsize=24     # Prominent titles
)
```

### 📈 Data Validation

#### Automatic Validation
```python
from schemas import CommitCount, PeriodType

# This will validate automatically
commit_count = CommitCount(
    period=15,                    # Hour 15 (3 PM)
    count=42,                     # 42 commits
    period_type=PeriodType.HOUR   # Hour period type
)

# This will raise validation error
try:
    invalid_count = CommitCount(
        period=25,                # Invalid hour (>23)
        count=-5,                 # Invalid count (<0)
        period_type=PeriodType.HOUR
    )
except ValidationError as e:
    print(f"Validation failed: {e}")
```

#### File Validation
```python
from schemas import validate_commit_data_file

# Validate and parse commit data
try:
    commit_data = validate_commit_data_file("./Generated Data/commit_counts.txt")
    print(f"Loaded {len(commit_data)} valid records")
except FileNotFoundError:
    print("Data file not found")
except ValueError as e:
    print(f"Data validation failed: {e}")
```

### 🔍 Error Handling

#### MCP Server Responses
```python
from schemas import MCPToolResponse

# Success response
response = MCPToolResponse(
    success=True,
    message="Chart generated successfully",
    output_file="./Generated Data/my_chart.png",
    chart_config=config
)

# Error response
response = MCPToolResponse(
    success=False,
    message="Failed to generate chart",
    error_details="Data file not found: commit_counts.txt"
)
```

### 🧪 Testing and Development

#### Run Examples
```bash
# Test all configurations
python examples/example_configs.py

# Test specific chart type
python enhanced_plot_scripts.py --type hour_bar --repo TestRepo
```

#### Validate Installation
```bash
# Test imports
python -c "import schemas, schema_org, enhanced_plot_scripts, database_schema; print('✅ All modules imported successfully')"

# Test database
python -c "from database_schema import initialize_database; db = initialize_database(); print('✅ Database initialized')"
```

### 🔧 Troubleshooting

#### Common Issues

**Import Errors**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Data File Not Found**
```bash
# Generate git log data first
./commit_history.sh
./commits_by_hour.sh
```

**Permission Denied (Unix)**
```bash
# Make scripts executable
chmod +x *.sh
```

**Database Issues**
```bash
# Reinitialize database
python -c "from database_schema import initialize_database; initialize_database()"
```

### 📚 API Reference

#### Core Classes

- **`ChartConfig`**: Main chart configuration with validation
- **`PlotConfig`**: Plot styling and appearance settings
- **`ChartRequest`**: MCP server request structure
- **`MCPToolResponse`**: Standardized response format
- **`CommitCount`**: Validated commit count data
- **`RepositoryInfo`**: Repository metadata


#### Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Type checking
mypy .
```

## 📄 License

MIT License - see [LICENSE.md](LICENSE.md) for details.

## 👤 Author

**Alyshia Ledlie**
- Email: alyshia@theintegritystudio.com

- Site: https://www.aledlie.com

- Project: Repository Structuring & Visualization

## Advanced Features
To use enhanced features:
```bash
# Use new enhanced scripts
python enhanced_plot_scripts.py

# Or keep using original scripts
python plot_commits_by_hour.py
```

## Want to contribute?  Suggested future roadmap items:

- [ ] Web dashboard interface
- [ ] Real-time commit monitoring
- [ ] Team collaboration analytics
- [ ] Integration with popular Git platforms
- [ ] Advanced statistical analysis
- [ ] Custom plugin system

---

