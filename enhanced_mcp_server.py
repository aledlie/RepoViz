#!/usr/bin/env python3
"""
Enhanced MCP Server for Git Commit Visualization Utilities.

This server provides Model Context Protocol tools for generating commit
visualizations with full Pydantic validation and schema.org structured data.
"""

import asyncio
import json
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional

# Add current directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("Error: MCP library not found. Install with: pip install mcp[cli]")
    sys.exit(1)

try:
    from schemas import (
        ChartConfig, ChartType, PlotConfig, MCPToolResponse,
        create_default_chart_config, validate_commit_data_file
    )
    from schema_org import (
        get_creative_work_schema, generate_all_schemas
    )
    # Direct import for plotting
    from enhanced_plot_scripts import create_chart_from_config
except ImportError:
    print("Error: Local schema modules not found. Ensure schemas.py, schema_org.py, and enhanced_plot_scripts.py are present.")
    sys.exit(1)

# Initialize MCP server
server = Server("git-visualization-server")


def get_repository_name() -> Optional[str]:
    """Get repository name from git remote."""
    try:
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "get_repo_name.sh")
        result = subprocess.run(
            [script_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error getting repository name: {e}")
        return None


def run_data_collection_script(script_name: str) -> bool:
    """Run a data collection shell script."""
    try:
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        result = subprocess.run([script_path], capture_output=True, text=True, check=True)
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error running data collection script {script_name}: {e.stderr}")
        return False


async def _generate_chart(chart_type: ChartType, arguments: Dict[str, Any]) -> List[TextContent]:
    """Generic chart generation handler."""
    repo_name = arguments.get("repository_name") or get_repository_name()

    # Create plot configuration from arguments
    plot_config = PlotConfig()
    if arguments.get("dpi"):
        plot_config.dpi = arguments["dpi"]
    if arguments.get("color_primary"):
        plot_config.color_primary = arguments["color_primary"]

    # Create chart configuration
    config = create_default_chart_config(chart_type, repo_name)
    config.plot_config = plot_config

    if arguments.get("title"):
        config.title = arguments["title"]
    if arguments.get("output_filename"):
        config.output_filename = arguments["output_filename"]

    # Validate the final configuration
    try:
        config = ChartConfig(**config.dict())
    except Exception as e:
        response = MCPToolResponse(success=False, message="Invalid configuration", error_details=str(e))
        return [TextContent(type="text", text=response.json(indent=2))]

    # ---
    # Data Collection
    # ---
    required_scripts = {
        ChartType.HOUR_BAR: ["./commit_history.sh", "./commits_by_hour.sh"],
        ChartType.DAY_PIE: ["./commit_history.sh", "./commits_by_day.sh"],
        ChartType.MONTH_PIE: ["./commit_history.sh", "./commits_by_month.sh"],
        ChartType.DAY_MONTH_COMBINED: ["./commit_history.sh", "./commits_by_day.sh", "./commits_by_month.sh"],
    }

    for script in required_scripts.get(chart_type, []):
        if not run_data_collection_script(script):
            response = MCPToolResponse(success=False, message=f"Failed to run data script: {script}")
            return [TextContent(type="text", text=response.json(indent=2))]

    # ---
    # Chart Generation (Direct Call)
    # ---
    try:
        output_path = create_chart_from_config(config)
        
        chart_schema = get_creative_work_schema(chart_type.value, repo_name, output_path)
        response = MCPToolResponse(
            success=True,
            message=f"Successfully generated {chart_type.value} chart",
            output_file=output_path,
            chart_config=config
        )
        
        return [
            TextContent(type="text", text=response.json(indent=2)),
            TextContent(type="text", text=f"\nSchema.org data:\n{json.dumps(chart_schema, indent=2)}")
        ]
    except Exception as e:
        response = MCPToolResponse(success=False, message="Failed to generate chart", error_details=str(e))
        return [TextContent(type="text", text=response.json(indent=2))]


@server.list_tools()
def list_tools() -> List[Tool]:
    """List available MCP tools."""
    tool_definitions = [
        ("generate_hour_bar_chart", "Generate a bar chart showing commit frequency by hour of day (0-23)"),
        ("generate_day_pie_chart", "Generate a pie chart showing commit distribution by day of week"),
        ("generate_month_pie_chart", "Generate a pie chart showing commit distribution by month"),
        ("generate_combined_day_month_chart", "Generate combined day of week and month pie charts"),
    ]

    tools = []
    for name, description in tool_definitions:
        tools.append(Tool(
            name=name,
            description=description,
            inputSchema={
                "type": "object",
                "properties": {
                    "repository_name": {"type": "string", "description": "Repository name for chart title and filename"},
                    "title": {"type": "string", "description": "Custom chart title"},
                    "output_filename": {"type": "string", "description": "Custom output filename (without extension)"},
                    "dpi": {"type": "integer", "description": "Chart resolution in DPI (default: 300)", "minimum": 72, "maximum": 600},
                    "color_primary": {"type": "string", "description": "Primary color in hex format (default: #4e79a7)"}
                }
            }
        ))

    tools.extend([
        Tool(
            name="validate_commit_data",
            description="Validate commit data files and return statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_type": {
                        "type": "string",
                        "enum": ["hour", "day", "month"],
                        "description": "Type of commit data to validate"
                    }
                },
                "required": ["data_type"]
            }
        ),
        Tool(
            name="generate_schema_org_data",
            description="Generate schema.org structured data for the project",
            inputSchema={
                "type": "object",
                "properties": {
                    "repository_name": {"type": "string", "description": "Repository name for schema generation"},
                    "include_charts": {"type": "boolean", "description": "Include schema data for generated charts", "default": True}
                }
            }
        )
    ])
    return tools


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle MCP tool calls with full validation."""
    try:
        if name == "generate_hour_bar_chart":
            return await _generate_chart(ChartType.HOUR_BAR, arguments)
        elif name == "generate_day_pie_chart":
            return await _generate_chart(ChartType.DAY_PIE, arguments)
        elif name == "generate_month_pie_chart":
            return await _generate_chart(ChartType.MONTH_PIE, arguments)
        elif name == "generate_combined_day_month_chart":
            return await _generate_chart(ChartType.DAY_MONTH_COMBINED, arguments)
        elif name == "validate_commit_data":
            return await handle_validate_data(arguments)
        elif name == "generate_schema_org_data":
            return await handle_generate_schemas(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
            
    except Exception as e:
        error_response = MCPToolResponse(
            success=False,
            message=f"Error executing {name}",
            error_details=str(e)
        )
        return [TextContent(type="text", text=error_response.json(indent=2))]


async def handle_validate_data(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle commit data validation."""
    data_type = arguments.get("data_type")
    if not data_type:
        response = MCPToolResponse(success=False, message="data_type is required")
        return [TextContent(type="text", text=response.json(indent=2))]
    
    file_mapping = {
        "hour": "./commit_counts.txt",
        "day": "./commit_counts_day.txt", 
        "month": "./commit_counts_month.txt"
    }
    
    file_path = file_mapping.get(data_type)
    if not file_path:
        response = MCPToolResponse(success=False, message=f"Invalid data_type: {data_type}")
        return [TextContent(type="text", text=response.json(indent=2))]
    
    try:
        commit_counts = validate_commit_data_file(file_path)
        
        total_commits = sum(cc.count for cc in commit_counts)
        max_count = max(cc.count for cc in commit_counts) if commit_counts else 0
        min_count = min(cc.count for cc in commit_counts) if commit_counts else 0
        avg_count = total_commits / len(commit_counts) if commit_counts else 0
        
        stats = {
            "data_type": data_type,
            "file_path": file_path,
            "total_records": len(commit_counts),
            "total_commits": total_commits,
            "max_commits_per_period": max_count,
            "min_commits_per_period": min_count,
            "avg_commits_per_period": round(avg_count, 2),
            "records": [cc.dict() for cc in commit_counts[:10]]
        }
        
        response = MCPToolResponse(success=True, message=f"Successfully validated {data_type} commit data")
        
        return [
            TextContent(type="text", text=response.json(indent=2)),
            TextContent(type="text", text=f"\nData Statistics:\n{json.dumps(stats, indent=2)}")
        ]
        
    except Exception as e:
        response = MCPToolResponse(success=False, message=f"Failed to validate {data_type} data", error_details=str(e))
        return [TextContent(type="text", text=response.json(indent=2))]


async def handle_generate_schemas(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle schema.org structured data generation."""
    repo_name = arguments.get("repository_name") or get_repository_name()
    include_charts = arguments.get("include_charts", True)
    
    try:
        schema_files = generate_all_schemas(repo_name)
        
        chart_schemas = {}
        if include_charts:
            for chart_type in ChartType:
                chart_schemas[chart_type.value] = get_creative_work_schema(chart_type.value, repo_name)
        
        response = MCPToolResponse(
            success=True,
            message=f"Successfully generated schema.org structured data",
            output_file=f"Generated {len(schema_files)} schema files"
        )
        
        result = [TextContent(type="text", text=response.json(indent=2))]
        result.append(TextContent(type="text", text=f"\nGenerated Schema Files:\n{json.dumps(schema_files, indent=2)}"))
        
        if chart_schemas:
            result.append(TextContent(type="text", text=f"\nChart Schemas:\n{json.dumps(chart_schemas, indent=2)}"))
        
        return result
        
    except Exception as e:
        response = MCPToolResponse(success=False, message="Failed to generate schema.org data", error_details=str(e))
        return [TextContent(type="text", text=response.json(indent=2))]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="git-visualization-server",
                server_version="2.0.0", # Version bump
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())