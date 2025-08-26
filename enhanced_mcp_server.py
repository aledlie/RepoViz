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
        ChartRequest, ChartConfig, ChartType, PlotConfig, MCPToolResponse,
        create_default_chart_config, validate_commit_data_file
    )
    from schema_org import (
        get_software_application_schema, get_dataset_schema, 
        get_creative_work_schema, generate_all_schemas
    )
except ImportError:
    print("Error: Local schema modules not found. Ensure schemas.py and schema_org.py are present.")
    sys.exit(1)

# Initialize MCP server
server = Server("git-visualization-server")


def get_repository_name() -> Optional[str]:
    """Get repository name from git remote."""
    try:
        result = subprocess.run(
            ["./get_repo_name.sh"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def run_data_collection_script(script_name: str) -> bool:
    """Run a data collection shell script."""
    try:
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        result = subprocess.run([script_path], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def run_visualization_script(script_name: str, config: Optional[ChartConfig] = None) -> tuple[bool, str]:
    """Run a Python visualization script with optional configuration."""
    try:
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        
        # Set environment variables for configuration if provided
        env = os.environ.copy()
        if config:
            env['CHART_TITLE'] = config.title
            env['OUTPUT_FILENAME'] = config.output_filename
            env['DPI'] = str(config.plot_config.dpi)
            env['COLOR_PRIMARY'] = config.plot_config.color_primary
            env['COLOR_SECONDARY'] = config.plot_config.color_secondary
        
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, env=env)
        
        output_file = None
        if result.returncode == 0:
            # Try to determine output filename
            if config:
                output_file = f"./Generated Data/{config.output_filename}.png"
            else:
                # Parse stdout for filename
                for line in result.stdout.split('\n'):
                    if 'saved to' in line.lower() or '.png' in line:
                        output_file = line.strip()
                        break
        
        return result.returncode == 0, output_file or ""
        
    except Exception as e:
        return False, str(e)


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="generate_hour_bar_chart",
            description="Generate a bar chart showing commit frequency by hour of day (0-23)",
            inputSchema={
                "type": "object",
                "properties": {
                    "repository_name": {
                        "type": "string",
                        "description": "Repository name for chart title and filename"
                    },
                    "title": {
                        "type": "string", 
                        "description": "Custom chart title"
                    },
                    "output_filename": {
                        "type": "string",
                        "description": "Custom output filename (without extension)"
                    },
                    "dpi": {
                        "type": "integer",
                        "description": "Chart resolution in DPI (default: 300)",
                        "minimum": 72,
                        "maximum": 600
                    },
                    "color_primary": {
                        "type": "string",
                        "description": "Primary color in hex format (default: #4e79a7)"
                    }
                }
            }
        ),
        Tool(
            name="generate_day_pie_chart", 
            description="Generate a pie chart showing commit distribution by day of week",
            inputSchema={
                "type": "object",
                "properties": {
                    "repository_name": {
                        "type": "string",
                        "description": "Repository name for chart title and filename"
                    },
                    "title": {
                        "type": "string",
                        "description": "Custom chart title"
                    },
                    "output_filename": {
                        "type": "string", 
                        "description": "Custom output filename (without extension)"
                    },
                    "dpi": {
                        "type": "integer",
                        "description": "Chart resolution in DPI (default: 300)",
                        "minimum": 72,
                        "maximum": 600
                    },
                    "color_primary": {
                        "type": "string",
                        "description": "Primary color in hex format (default: #4e79a7)"
                    }
                }
            }
        ),
        Tool(
            name="generate_month_pie_chart",
            description="Generate a pie chart showing commit distribution by month",
            inputSchema={
                "type": "object",
                "properties": {
                    "repository_name": {
                        "type": "string",
                        "description": "Repository name for chart title and filename"
                    },
                    "title": {
                        "type": "string",
                        "description": "Custom chart title"
                    },
                    "output_filename": {
                        "type": "string",
                        "description": "Custom output filename (without extension)"
                    },
                    "dpi": {
                        "type": "integer",
                        "description": "Chart resolution in DPI (default: 300)",
                        "minimum": 72,
                        "maximum": 600
                    },
                    "color_primary": {
                        "type": "string",
                        "description": "Primary color in hex format (default: #4e79a7)"
                    }
                }
            }
        ),
        Tool(
            name="generate_combined_day_month_chart",
            description="Generate combined day of week and month pie charts",
            inputSchema={
                "type": "object",
                "properties": {
                    "repository_name": {
                        "type": "string",
                        "description": "Repository name for chart title and filename"
                    },
                    "title": {
                        "type": "string",
                        "description": "Custom chart title"
                    },
                    "output_filename": {
                        "type": "string",
                        "description": "Custom output filename (without extension)"
                    },
                    "dpi": {
                        "type": "integer",
                        "description": "Chart resolution in DPI (default: 300)",
                        "minimum": 72,
                        "maximum": 600
                    },
                    "color_primary": {
                        "type": "string",
                        "description": "Primary color in hex format (default: #4e79a7)"
                    }
                }
            }
        ),
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
                    "repository_name": {
                        "type": "string",
                        "description": "Repository name for schema generation"
                    },
                    "include_charts": {
                        "type": "boolean",
                        "description": "Include schema data for generated charts",
                        "default": True
                    }
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle MCP tool calls with full validation."""
    
    try:
        if name == "generate_hour_bar_chart":
            return await handle_hour_bar_chart(arguments)
        elif name == "generate_day_pie_chart":
            return await handle_day_pie_chart(arguments)
        elif name == "generate_month_pie_chart":
            return await handle_month_pie_chart(arguments)
        elif name == "generate_combined_day_month_chart":
            return await handle_combined_chart(arguments)
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


async def handle_hour_bar_chart(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle hourly bar chart generation."""
    
    # Get repository name if not provided
    repo_name = arguments.get("repository_name") or get_repository_name()
    
    # Create plot configuration
    plot_config = PlotConfig()
    if arguments.get("dpi"):
        plot_config.dpi = arguments["dpi"]
    if arguments.get("color_primary"):
        plot_config.color_primary = arguments["color_primary"]
    
    # Create chart configuration
    config = create_default_chart_config(ChartType.HOUR_BAR, repo_name)
    config.plot_config = plot_config
    
    if arguments.get("title"):
        config.title = arguments["title"]
    if arguments.get("output_filename"):
        config.output_filename = arguments["output_filename"]
    
    # Validate configuration
    try:
        config = ChartConfig(**config.dict())
    except Exception as e:
        response = MCPToolResponse(
            success=False,
            message="Invalid configuration",
            error_details=str(e)
        )
        return [TextContent(type="text", text=response.json(indent=2))]
    
    # Collect data
    if not run_data_collection_script("./commit_history.sh"):
        response = MCPToolResponse(
            success=False,
            message="Failed to collect git log data"
        )
        return [TextContent(type="text", text=response.json(indent=2))]
    
    if not run_data_collection_script("./commits_by_hour.sh"):
        response = MCPToolResponse(
            success=False,
            message="Failed to process hourly commit data"
        )
        return [TextContent(type="text", text=response.json(indent=2))]
    
    # Generate chart
    success, output_file = run_visualization_script("plot_repo_by_hour.py", config)
    
    if success:
        # Generate schema.org data for the chart
        chart_schema = get_creative_work_schema("hour_bar", repo_name, output_file)
        
        response = MCPToolResponse(
            success=True,
            message=f"Successfully generated hourly bar chart",
            output_file=output_file,
            chart_config=config
        )
        
        return [
            TextContent(type="text", text=response.json(indent=2)),
            TextContent(type="text", text=f"\nSchema.org data:\n{json.dumps(chart_schema, indent=2)}")
        ]
    else:
        response = MCPToolResponse(
            success=False,
            message="Failed to generate chart",
            error_details=output_file
        )
        return [TextContent(type="text", text=response.json(indent=2))]


async def handle_day_pie_chart(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle day of week pie chart generation."""
    
    repo_name = arguments.get("repository_name") or get_repository_name()
    
    plot_config = PlotConfig()
    if arguments.get("dpi"):
        plot_config.dpi = arguments["dpi"]
    if arguments.get("color_primary"):
        plot_config.color_primary = arguments["color_primary"]
    
    config = create_default_chart_config(ChartType.DAY_PIE, repo_name)
    config.plot_config = plot_config
    
    if arguments.get("title"):
        config.title = arguments["title"]
    if arguments.get("output_filename"):
        config.output_filename = arguments["output_filename"]
    
    # Collect and process data
    if not run_data_collection_script("./commit_history.sh"):
        response = MCPToolResponse(success=False, message="Failed to collect git log data")
        return [TextContent(type="text", text=response.json(indent=2))]
    
    if not run_data_collection_script("./commits_by_day.sh"):
        response = MCPToolResponse(success=False, message="Failed to process daily commit data")
        return [TextContent(type="text", text=response.json(indent=2))]
    
    success, output_file = run_visualization_script("plot_pie_day.py", config)
    
    if success:
        chart_schema = get_creative_work_schema("day_pie", repo_name, output_file)
        response = MCPToolResponse(
            success=True,
            message="Successfully generated day of week pie chart",
            output_file=output_file,
            chart_config=config
        )
        
        return [
            TextContent(type="text", text=response.json(indent=2)),
            TextContent(type="text", text=f"\nSchema.org data:\n{json.dumps(chart_schema, indent=2)}")
        ]
    else:
        response = MCPToolResponse(success=False, message="Failed to generate chart", error_details=output_file)
        return [TextContent(type="text", text=response.json(indent=2))]


async def handle_month_pie_chart(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle monthly pie chart generation."""
    
    repo_name = arguments.get("repository_name") or get_repository_name()
    
    plot_config = PlotConfig()
    if arguments.get("dpi"):
        plot_config.dpi = arguments["dpi"]
    if arguments.get("color_primary"):
        plot_config.color_primary = arguments["color_primary"]
    
    config = create_default_chart_config(ChartType.MONTH_PIE, repo_name)
    config.plot_config = plot_config
    
    if arguments.get("title"):
        config.title = arguments["title"]
    if arguments.get("output_filename"):
        config.output_filename = arguments["output_filename"]
    
    # Collect and process data
    if not run_data_collection_script("./commit_history.sh"):
        response = MCPToolResponse(success=False, message="Failed to collect git log data")
        return [TextContent(type="text", text=response.json(indent=2))]
    
    if not run_data_collection_script("./commits_by_month.sh"):
        response = MCPToolResponse(success=False, message="Failed to process monthly commit data")
        return [TextContent(type="text", text=response.json(indent=2))]
    
    success, output_file = run_visualization_script("plot_pie_month.py", config)
    
    if success:
        chart_schema = get_creative_work_schema("month_pie", repo_name, output_file)
        response = MCPToolResponse(
            success=True,
            message="Successfully generated monthly pie chart",
            output_file=output_file,
            chart_config=config
        )
        
        return [
            TextContent(type="text", text=response.json(indent=2)),
            TextContent(type="text", text=f"\nSchema.org data:\n{json.dumps(chart_schema, indent=2)}")
        ]
    else:
        response = MCPToolResponse(success=False, message="Failed to generate chart", error_details=output_file)
        return [TextContent(type="text", text=response.json(indent=2))]


async def handle_combined_chart(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle combined day/month chart generation."""
    
    repo_name = arguments.get("repository_name") or get_repository_name()
    
    plot_config = PlotConfig()
    if arguments.get("dpi"):
        plot_config.dpi = arguments["dpi"]
    if arguments.get("color_primary"):
        plot_config.color_primary = arguments["color_primary"]
    
    config = create_default_chart_config(ChartType.DAY_MONTH_COMBINED, repo_name)
    config.plot_config = plot_config
    
    if arguments.get("title"):
        config.title = arguments["title"]
    if arguments.get("output_filename"):
        config.output_filename = arguments["output_filename"]
    
    # Collect and process data
    scripts = ["./commit_history.sh", "./commits_by_day.sh", "./commits_by_month.sh"]
    for script in scripts:
        if not run_data_collection_script(script):
            response = MCPToolResponse(success=False, message=f"Failed to run {script}")
            return [TextContent(type="text", text=response.json(indent=2))]
    
    success, output_file = run_visualization_script("plot_repo_by_pie.py", config)
    
    if success:
        chart_schema = get_creative_work_schema("day_month_combined", repo_name, output_file)
        response = MCPToolResponse(
            success=True,
            message="Successfully generated combined day/month chart",
            output_file=output_file,
            chart_config=config
        )
        
        return [
            TextContent(type="text", text=response.json(indent=2)),
            TextContent(type="text", text=f"\nSchema.org data:\n{json.dumps(chart_schema, indent=2)}")
        ]
    else:
        response = MCPToolResponse(success=False, message="Failed to generate chart", error_details=output_file)
        return [TextContent(type="text", text=response.json(indent=2))]


async def handle_validate_data(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle commit data validation."""
    
    data_type = arguments.get("data_type")
    if not data_type:
        response = MCPToolResponse(success=False, message="data_type is required")
        return [TextContent(type="text", text=response.json(indent=2))]
    
    file_mapping = {
        "hour": "./Generated Data/commit_counts.txt",
        "day": "./Generated Data/commit_counts_day.txt", 
        "month": "./Generated Data/commit_counts_month.txt"
    }
    
    file_path = file_mapping.get(data_type)
    if not file_path:
        response = MCPToolResponse(success=False, message=f"Invalid data_type: {data_type}")
        return [TextContent(type="text", text=response.json(indent=2))]
    
    try:
        commit_counts = validate_commit_data_file(file_path)
        
        # Calculate statistics
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
            "records": [cc.dict() for cc in commit_counts[:10]]  # First 10 records
        }
        
        response = MCPToolResponse(
            success=True,
            message=f"Successfully validated {data_type} commit data"
        )
        
        return [
            TextContent(type="text", text=response.json(indent=2)),
            TextContent(type="text", text=f"\nData Statistics:\n{json.dumps(stats, indent=2)}")
        ]
        
    except Exception as e:
        response = MCPToolResponse(
            success=False,
            message=f"Failed to validate {data_type} data",
            error_details=str(e)
        )
        return [TextContent(type="text", text=response.json(indent=2))]


async def handle_generate_schemas(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle schema.org structured data generation."""
    
    repo_name = arguments.get("repository_name") or get_repository_name()
    include_charts = arguments.get("include_charts", True)
    
    try:
        # Generate all schema files
        schema_files = generate_all_schemas(repo_name)
        
        # If include_charts is True, also generate chart schemas
        chart_schemas = {}
        if include_charts:
            chart_types = ["hour_bar", "day_pie", "month_pie", "day_month_combined"]
            for chart_type in chart_types:
                chart_schemas[chart_type] = get_creative_work_schema(chart_type, repo_name)
        
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
        response = MCPToolResponse(
            success=False,
            message="Failed to generate schema.org data",
            error_details=str(e)
        )
        return [TextContent(type="text", text=response.json(indent=2))]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="git-visualization-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
