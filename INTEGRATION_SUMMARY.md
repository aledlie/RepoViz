# IntegrityStudio Repository Data Integration

## Overview

This document describes the integration of IntegrityStudioClients repository data with the ToolVisualizer "Most Active Directories" UI component.

## What Was Accomplished

### 1. Repository Analysis

Created `analyze_integrity_studio.py` to analyze the IntegrityStudioClients directory structure:
- **Location**: `/Users/alyshialedlie/code/ISInternal/RepoViz/analyze_integrity_studio.py`
- **Function**: Recursively analyzes directories to find most active (highest file count) directories
- **Output**: JSON data file with directory statistics

**Analysis Results**:
```
Most Active Directories in IntegrityStudioClients:
1. Leora - 313 files (HTML, JavaScript, Markdown)
2. fisterra - 162 files (JavaScript, Markdown, Python)
3. InspiredMovement - 66 files (JavaScript, Markdown, HTML)
4. ATXMovementAlliance - 53 files (TypeScript React, TypeScript, JavaScript)
5. luis-landscaping - 18 files (TypeScript, Markdown, HTML)
```

### 2. Generated Data Files

**Directory Analysis Data**:
- **File**: `Generated Data/integrity_studio_active_dirs.json`
- **Contains**: Directory statistics including file counts, sizes, and primary languages
- **Copied to**: `../ToolVisualizer/public/data/integrity_studio_active_dirs.json`

**Commit Activity Data** (Sample/Demo):
- `Generated Data/commit_counts_hour.txt` - Hourly commit distribution
- `Generated Data/commit_counts_day.txt` - Daily commit distribution
- `Generated Data/commit_counts_month.txt` - Monthly commit distribution

### 3. Visualization Charts

Created three visualization charts using RepoViz enhanced plotting tools:

**a. Hourly Commit Activity**
- **File**: `integrity_studio_hour_commits.png`
- **Chart Type**: Bar chart
- **Shows**: Commit activity by hour of day (0-23)
- **Location**: `../ToolVisualizer/public/visualizations/integrity_studio_hour_commits.png`

**b. Day of Week Activity**
- **File**: `integrity_studio_day_commits.png`
- **Chart Type**: Pie chart
- **Shows**: Commit distribution by day of week
- **Location**: `../ToolVisualizer/public/visualizations/integrity_studio_day_commits.png`

**c. Monthly Activity**
- **File**: `integrity_studio_month_commits.png`
- **Chart Type**: Pie chart
- **Shows**: Commit distribution by month
- **Location**: `../ToolVisualizer/public/visualizations/integrity_studio_month_commits.png`

### 4. UI Integration

Updated ToolVisualizer's main dashboard (`../ToolVisualizer/public/index.html`):

**Changes Made**:
- Added IntegrityStudioClients directories to "Most Active Directories" section
- Sorted directories by file count (most active first)
- Added visual indicators (purple left border) for client repositories
- Added "(Client)" tags to distinguish client sites
- Added subtitle description for the section
- Maintained existing directories from other repositories

**New UI Features**:
- Clickable directory cards linking to IntegrityStudioClients schema page
- Visual hierarchy showing most active directories across all repositories
- Consistent styling with existing ToolVisualizer design

## File Locations

### Source Files (RepoViz)
```
/Users/alyshialedlie/code/ISInternal/RepoViz/
├── analyze_integrity_studio.py          # Directory analysis script
├── enhanced_plot_scripts.py             # Visualization generation script
└── Generated Data/
    ├── integrity_studio_active_dirs.json
    ├── integrity_studio_hour_commits.png
    ├── integrity_studio_day_commits.png
    └── integrity_studio_month_commits.png
```

### Destination Files (ToolVisualizer)
```
/Users/alyshialedlie/code/ISInternal/ToolVisualizer/
├── public/
│   ├── index.html                       # Updated main dashboard
│   ├── data/
│   │   └── integrity_studio_active_dirs.json
│   └── visualizations/
│       ├── integrity_studio_hour_commits.png
│       ├── integrity_studio_day_commits.png
│       └── integrity_studio_month_commits.png
```

## How to Use

### Regenerate Data

To regenerate the directory analysis data:

```bash
cd /Users/alyshialedlie/code/ISInternal/RepoViz
python3 analyze_integrity_studio.py
```

### Generate New Visualizations

To create new visualizations with custom settings:

```bash
# Hourly bar chart
python3 enhanced_plot_scripts.py \
  --type hour_bar \
  --title "Custom Title" \
  --output custom_output \
  --repo "RepositoryName"

# Day of week pie chart
python3 enhanced_plot_scripts.py \
  --type day_pie \
  --title "Daily Activity" \
  --output daily_chart \
  --repo "RepositoryName"

# Monthly pie chart
python3 enhanced_plot_scripts.py \
  --type month_pie \
  --title "Monthly Activity" \
  --output monthly_chart \
  --repo "RepositoryName"
```

### View Results

1. Open ToolVisualizer UI:
   ```bash
   cd ../ToolVisualizer
   ./start_ui.sh
   ```

2. Navigate to the main dashboard to see "Most Active Directories" section

3. View visualizations at:
   - `http://localhost:3000/visualizations/integrity_studio_hour_commits.png`
   - `http://localhost:3000/visualizations/integrity_studio_day_commits.png`
   - `http://localhost:3000/visualizations/integrity_studio_month_commits.png`

## Technical Details

### RepoViz Tools Used

1. **enhanced_plot_scripts.py**
   - Uses Pydantic models for configuration validation
   - Supports multiple chart types (bar, pie, combined)
   - Generates Schema.org structured data
   - Configurable styling (DPI, colors, fonts)

2. **schemas.py**
   - Provides data validation models
   - Supports ChartConfig, PlotConfig, CommitCount types
   - Ensures data integrity

### Data Format

The JSON data file follows this structure:
```json
{
  "repository": "IntegrityStudioClients",
  "analyzed_at": "2025-10-28",
  "total_directories": 5,
  "directories": [
    {
      "name": "Leora",
      "file_count": 313,
      "size_bytes": 19375104,
      "size_mb": 18.48,
      "languages": ["HTML", "JavaScript", "Markdown"],
      "language_str": "HTML, JavaScript, Markdown"
    }
  ]
}
```

## Next Steps

### Suggested Enhancements

1. **Real-time Updates**
   - Add automatic directory scanning on schedule
   - Update UI dynamically with new data

2. **Additional Metrics**
   - Track file changes over time
   - Show growth trends
   - Add commit history if directories become git repos

3. **Interactive Visualizations**
   - Add drill-down capabilities
   - Filter by date range
   - Compare multiple directories

4. **Integration Improvements**
   - Create dedicated visualization page in ToolVisualizer
   - Add navigation links to charts
   - Embed charts directly in UI

## Support

For questions or issues:
- Review RepoViz documentation: `/Users/alyshialedlie/code/ISInternal/RepoViz/README.md`
- Review ToolVisualizer documentation: `/Users/alyshialedlie/code/ISInternal/ToolVisualizer/README.md`

---

**Generated**: 2025-10-28
**Repository**: TheIntegrityStudio / IntegrityStudioClients
**Tools**: RepoViz + ToolVisualizer
