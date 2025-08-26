"""
Schema.org structured data definitions for Git Commit Visualization Utilities.

This module provides JSON-LD structured data for SEO and discoverability,
following schema.org standards for software applications and datasets.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os


def get_software_application_schema(
    repository_name: Optional[str] = None,
    version: Optional[str] = None,
    author_name: str = "Alyshia Ledlie",
    author_email: str = "alyshialedlie@example.com"
) -> Dict[str, Any]:
    """Generate schema.org SoftwareApplication structured data."""
    
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Git Commit Visualization Utilities",
        "description": "A comprehensive toolkit for analyzing and visualizing Git commit patterns through interactive charts and graphs",
        "applicationCategory": "DeveloperApplication",
        "applicationSubCategory": "Data Visualization",
        "operatingSystem": ["macOS", "Linux", "Windows"],
        "programmingLanguage": ["Python", "Bash"],
        "runtimePlatform": "Python 3.13+",
        "softwareRequirements": [
            "Python 3.13+",
            "Git",
            "Bash shell",
            "matplotlib",
            "numpy",
            "mcp[cli]"
        ],
        "author": {
            "@type": "Person",
            "name": author_name,
            "email": author_email
        },
        "creator": {
            "@type": "Person", 
            "name": author_name,
            "email": author_email
        },
        "license": "https://opensource.org/licenses/MIT",
        "url": "https://github.com/alyshialedlie/RepoViz",
        "downloadUrl": "https://github.com/alyshialedlie/RepoViz/archive/main.zip",
        "installUrl": "https://github.com/alyshialedlie/RepoViz#installation",
        "screenshot": [],  # Add screenshot URLs when available
        "featureList": [
            "Commit Analysis by Time Patterns",
            "Hourly commit distribution (bar charts)",
            "Day of week commit patterns (pie charts)", 
            "Monthly commit activity (pie charts)",
            "Combined day/month visualizations",
            "High-resolution PNG charts (300 DPI)",
            "Repository-specific file naming",
            "MCP Server Integration",
            "Programmatic access to visualization functions"
        ],
        "softwareVersion": version or "1.0.0",
        "dateCreated": "2024-01-01",  # Update with actual creation date
        "dateModified": datetime.now().isoformat(),
        "keywords": [
            "git",
            "commit analysis", 
            "data visualization",
            "charts",
            "development tools",
            "repository analytics",
            "matplotlib",
            "python",
            "MCP server"
        ],
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock"
        }
    }
    
    if repository_name:
        schema["name"] = f"Git Commit Visualization Utilities - {repository_name}"
        schema["description"] = f"Commit pattern analysis and visualization for {repository_name} repository"
    
    return schema


def get_dataset_schema(
    data_type: str = "commit_analysis",
    repository_name: Optional[str] = None,
    file_path: Optional[str] = None,
    record_count: Optional[int] = None
) -> Dict[str, Any]:
    """Generate schema.org Dataset structured data for commit data."""
    
    dataset_names = {
        "commit_analysis": "Git Commit Analysis Data",
        "hourly": "Hourly Commit Distribution Data",
        "daily": "Daily Commit Pattern Data", 
        "monthly": "Monthly Commit Activity Data"
    }
    
    dataset_descriptions = {
        "commit_analysis": "Structured commit data extracted from Git repositories for pattern analysis",
        "hourly": "Commit frequency data aggregated by hour of day (0-23)",
        "daily": "Commit frequency data aggregated by day of week (Sunday-Saturday)",
        "monthly": "Commit frequency data aggregated by month (January-December)"
    }
    
    name = dataset_names.get(data_type, "Git Repository Data")
    description = dataset_descriptions.get(data_type, "Git repository analysis data")
    
    if repository_name:
        name = f"{name} - {repository_name}"
        description = f"{description} for {repository_name} repository"
    
    schema = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": name,
        "description": description,
        "keywords": [
            "git commits",
            "version control",
            "software development",
            "time series data",
            "repository analytics"
        ],
        "creator": {
            "@type": "Person",
            "name": "Alyshia Ledlie",
            "email": "alyshialedlie@example.com"
        },
        "dateCreated": datetime.now().isoformat(),
        "dateModified": datetime.now().isoformat(),
        "license": "https://opensource.org/licenses/MIT",
        "encodingFormat": "text/plain",
        "temporalCoverage": "2024/..",  # Update based on actual data range
        "spatialCoverage": "Global",
        "variableMeasured": [
            {
                "@type": "PropertyValue",
                "name": "commit_timestamp",
                "description": "Timestamp of git commit"
            },
            {
                "@type": "PropertyValue", 
                "name": "commit_hour",
                "description": "Hour of day when commit was made (0-23)"
            },
            {
                "@type": "PropertyValue",
                "name": "commit_day",
                "description": "Day of week when commit was made (0-6)"
            },
            {
                "@type": "PropertyValue",
                "name": "commit_month", 
                "description": "Month when commit was made (1-12)"
            }
        ]
    }
    
    if file_path and os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        schema["distribution"] = {
            "@type": "DataDownload",
            "encodingFormat": "text/plain",
            "contentSize": f"{file_size} bytes",
            "contentUrl": file_path
        }
    
    if record_count:
        schema["distribution"]["numberOfRecords"] = record_count
    
    return schema


def get_creative_work_schema(
    chart_type: str,
    repository_name: Optional[str] = None,
    file_path: Optional[str] = None
) -> Dict[str, Any]:
    """Generate schema.org CreativeWork structured data for generated charts."""
    
    chart_names = {
        "hour_bar": "Hourly Commit Distribution Chart",
        "day_pie": "Daily Commit Pattern Chart",
        "month_pie": "Monthly Commit Activity Chart", 
        "day_month_combined": "Combined Day/Month Commit Chart"
    }
    
    chart_descriptions = {
        "hour_bar": "Bar chart showing commit frequency by hour of day",
        "day_pie": "Pie chart showing commit distribution by day of week",
        "month_pie": "Pie chart showing commit distribution by month",
        "day_month_combined": "Combined visualization of daily and monthly commit patterns"
    }
    
    name = chart_names.get(chart_type, "Git Commit Visualization")
    description = chart_descriptions.get(chart_type, "Git repository commit pattern visualization")
    
    if repository_name:
        name = f"{name} - {repository_name}"
        description = f"{description} for {repository_name} repository"
    
    schema = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": name,
        "description": description,
        "creator": {
            "@type": "Person",
            "name": "Alyshia Ledlie",
            "email": "alyshialedlie@example.com"
        },
        "dateCreated": datetime.now().isoformat(),
        "license": "https://opensource.org/licenses/MIT",
        "encodingFormat": "image/png",
        "genre": "Data Visualization",
        "keywords": [
            "data visualization",
            "git commits",
            "charts",
            "repository analytics",
            "software development metrics"
        ],
        "isBasedOn": {
            "@type": "Dataset",
            "name": f"Git Commit Data - {repository_name}" if repository_name else "Git Commit Data"
        }
    }
    
    if file_path and os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        schema["contentSize"] = f"{file_size} bytes"
        schema["contentUrl"] = file_path
    
    return schema


def get_mcp_server_schema() -> Dict[str, Any]:
    """Generate schema.org structured data for the MCP server component."""
    
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Git Visualization MCP Server",
        "description": "Model Context Protocol server for programmatic access to git commit visualization tools",
        "applicationCategory": "DeveloperApplication",
        "applicationSubCategory": "API Server",
        "programmingLanguage": "Python",
        "runtimePlatform": "Python 3.13+",
        "author": {
            "@type": "Person",
            "name": "Alyshia Ledlie",
            "email": "alyshialedlie@example.com"
        },
        "softwareRequirements": [
            "Python 3.13+",
            "mcp[cli]",
            "matplotlib",
            "numpy"
        ],
        "featureList": [
            "generate_hour_bar_chart() - Create hourly bar chart",
            "generate_day_pie_chart() - Create day of week pie chart",
            "generate_month_pie_chart() - Create monthly pie chart"
        ],
        "license": "https://opensource.org/licenses/MIT",
        "dateCreated": datetime.now().isoformat(),
        "keywords": [
            "MCP server",
            "Model Context Protocol", 
            "API",
            "git visualization",
            "automation tools"
        ]
    }


def save_structured_data(schema_data: Dict[str, Any], output_path: str) -> None:
    """Save structured data to JSON-LD file."""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(schema_data, f, indent=2, ensure_ascii=False)


def generate_all_schemas(
    repository_name: Optional[str] = None,
    output_dir: str = "./Generated Data/schemas/"
) -> Dict[str, str]:
    """Generate all schema.org structured data files."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    schemas = {
        "software_application": get_software_application_schema(repository_name),
        "commit_dataset": get_dataset_schema("commit_analysis", repository_name),
        "hourly_dataset": get_dataset_schema("hourly", repository_name),
        "daily_dataset": get_dataset_schema("daily", repository_name),
        "monthly_dataset": get_dataset_schema("monthly", repository_name),
        "mcp_server": get_mcp_server_schema()
    }
    
    file_paths = {}
    
    for schema_name, schema_data in schemas.items():
        filename = f"{schema_name}.jsonld"
        if repository_name:
            filename = f"{schema_name}_{repository_name.lower().replace(' ', '_')}.jsonld"
        
        file_path = os.path.join(output_dir, filename)
        save_structured_data(schema_data, file_path)
        file_paths[schema_name] = file_path
    
    return file_paths


# HTML integration helpers
def get_jsonld_script_tag(schema_data: Dict[str, Any]) -> str:
    """Generate HTML script tag for JSON-LD structured data."""
    
    json_str = json.dumps(schema_data, indent=2, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{json_str}\n</script>'


def get_meta_tags(schema_data: Dict[str, Any]) -> List[str]:
    """Generate HTML meta tags from schema data."""
    
    meta_tags = []
    
    if "name" in schema_data:
        meta_tags.append(f'<meta property="og:title" content="{schema_data["name"]}">')
        meta_tags.append(f'<meta name="twitter:title" content="{schema_data["name"]}">')
    
    if "description" in schema_data:
        meta_tags.append(f'<meta name="description" content="{schema_data["description"]}">')
        meta_tags.append(f'<meta property="og:description" content="{schema_data["description"]}">')
        meta_tags.append(f'<meta name="twitter:description" content="{schema_data["description"]}">')
    
    if "keywords" in schema_data:
        keywords = ", ".join(schema_data["keywords"])
        meta_tags.append(f'<meta name="keywords" content="{keywords}">')
    
    if "author" in schema_data and isinstance(schema_data["author"], dict):
        author_name = schema_data["author"].get("name", "")
        if author_name:
            meta_tags.append(f'<meta name="author" content="{author_name}">')
    
    return meta_tags
