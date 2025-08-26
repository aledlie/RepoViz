#!/usr/bin/env python3
"""
Example configurations and usage patterns for Git Commit Visualization Utilities.

This module demonstrates how to use the Pydantic schemas and enhanced plotting
functionality with various configuration options.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas import (
    ChartConfig, PlotConfig, ChartType, VisualizationConfig,
    create_default_chart_config, ChartRequest, MCPToolResponse
)
from schema_org import (
    get_software_application_schema, get_dataset_schema,
    generate_all_schemas
)
from enhanced_plot_scripts import create_chart_from_config


def example_basic_configuration():
    """Example: Basic chart configuration."""
    print("=== Basic Configuration Example ===")
    
    # Create a simple hourly bar chart configuration
    config = ChartConfig(
        title="My Project Commits by Hour",
        output_filename="my_project_hourly",
        chart_type=ChartType.HOUR_BAR,
        repository_name="MyProject"
    )
    
    print("Basic Configuration:")
    print(config.json(indent=2))
    return config


def example_custom_styling():
    """Example: Custom styling configuration."""
    print("\n=== Custom Styling Example ===")
    
    # Create custom plot configuration
    custom_plot_config = PlotConfig(
        dpi=600,  # High resolution
        figsize=(16, 10),  # Large figure
        color_primary="#2E8B57",  # Sea green
        color_secondary="#228B22",  # Forest green
        font_size=14,
        title_fontsize=20,
        grid_alpha=0.5
    )
    
    # Create chart configuration with custom styling
    config = ChartConfig(
        title="High-Resolution Commit Analysis",
        output_filename="high_res_commits",
        chart_type=ChartType.DAY_MONTH_COMBINED,
        repository_name="HighResProject",
        plot_config=custom_plot_config
    )
    
    print("Custom Styling Configuration:")
    print(config.json(indent=2))
    return config


def example_mcp_request():
    """Example: MCP server request configuration."""
    print("\n=== MCP Request Example ===")
    
    # Create MCP chart request
    request = ChartRequest(
        chart_type=ChartType.DAY_PIE,
        repository_name="MCPExample",
        output_filename="mcp_day_chart",
        title="MCP Generated Day Chart",
        plot_config=PlotConfig(
            color_primary="#FF6B6B",  # Coral red
            color_secondary="#4ECDC4"  # Turquoise
        )
    )
    
    print("MCP Request Configuration:")
    print(request.json(indent=2))
    return request


def example_visualization_config():
    """Example: Overall visualization toolkit configuration."""
    print("\n=== Visualization Config Example ===")
    
    # Create comprehensive visualization configuration
    viz_config = VisualizationConfig(
        data_source_path="./data/",
        output_path="./charts/",
        default_plot_config=PlotConfig(
            dpi=300,
            color_primary="#1f77b4",  # Matplotlib default blue
            color_secondary="#ff7f0e"  # Matplotlib default orange
        ),
        supported_formats=["png", "pdf", "svg"],
        auto_detect_repo=True
    )
    
    print("Visualization Configuration:")
    print(viz_config.json(indent=2))
    return viz_config


def example_schema_org_generation():
    """Example: Generate schema.org structured data."""
    print("\n=== Schema.org Generation Example ===")
    
    # Generate software application schema
    app_schema = get_software_application_schema(
        repository_name="ExampleRepo",
        version="2.0.0",
        author_name="John Developer",
        author_email="john@example.com"
    )
    
    print("Software Application Schema (first 500 chars):")
    schema_str = json.dumps(app_schema, indent=2)
    print(schema_str[:500] + "..." if len(schema_str) > 500 else schema_str)
    
    # Generate dataset schema
    dataset_schema = get_dataset_schema(
        data_type="hourly",
        repository_name="ExampleRepo",
        record_count=24
    )
    
    print("\nDataset Schema (first 300 chars):")
    dataset_str = json.dumps(dataset_schema, indent=2)
    print(dataset_str[:300] + "..." if len(dataset_str) > 300 else dataset_str)
    
    return app_schema, dataset_schema


def example_configuration_validation():
    """Example: Configuration validation and error handling."""
    print("\n=== Configuration Validation Example ===")
    
    try:
        # This should work fine
        valid_config = ChartConfig(
            title="Valid Configuration",
            output_filename="valid_chart",
            chart_type=ChartType.HOUR_BAR
        )
        print("✓ Valid configuration created successfully")
        
        # This should raise validation errors
        try:
            invalid_config = ChartConfig(
                title="",  # Empty title - should fail
                output_filename="invalid/filename",  # Invalid characters
                chart_type="invalid_type"  # Invalid chart type
            )
        except Exception as e:
            print(f"✗ Invalid configuration caught: {type(e).__name__}")
            print(f"  Error details: {str(e)[:100]}...")
        
        # Test plot config validation
        try:
            invalid_plot = PlotConfig(
                dpi=50,  # Too low DPI
                color_primary="not-a-color",  # Invalid color format
                grid_alpha=1.5  # Invalid alpha value
            )
        except Exception as e:
            print(f"✗ Invalid plot config caught: {type(e).__name__}")
            print(f"  Error details: {str(e)[:100]}...")
            
    except Exception as e:
        print(f"Unexpected error: {e}")


def example_json_export_import():
    """Example: Export and import configurations as JSON."""
    print("\n=== JSON Export/Import Example ===")
    
    # Create configuration
    config = create_default_chart_config(
        ChartType.MONTH_PIE,
        repo_name="JSONExample"
    )
    
    # Export to JSON
    config_json = config.json(indent=2)
    print("Exported Configuration:")
    print(config_json)
    
    # Save to file
    os.makedirs("./examples/configs", exist_ok=True)
    with open("./examples/configs/example_config.json", "w") as f:
        f.write(config_json)
    
    # Import from JSON
    with open("./examples/configs/example_config.json", "r") as f:
        imported_data = json.load(f)
    
    imported_config = ChartConfig(**imported_data)
    print(f"\n✓ Successfully imported configuration: {imported_config.title}")
    
    return imported_config


def example_batch_chart_generation():
    """Example: Generate multiple charts with different configurations."""
    print("\n=== Batch Chart Generation Example ===")
    
    # Define multiple chart configurations
    chart_configs = [
        {
            "title": "Morning Commits (6AM-12PM)",
            "filename": "morning_commits",
            "type": ChartType.HOUR_BAR,
            "color": "#FFD700"  # Gold
        },
        {
            "title": "Weekend vs Weekday Activity",
            "filename": "weekend_activity", 
            "type": ChartType.DAY_PIE,
            "color": "#9370DB"  # Medium purple
        },
        {
            "title": "Seasonal Commit Patterns",
            "filename": "seasonal_patterns",
            "type": ChartType.MONTH_PIE,
            "color": "#20B2AA"  # Light sea green
        }
    ]
    
    generated_configs = []
    
    for chart_def in chart_configs:
        plot_config = PlotConfig(color_primary=chart_def["color"])
        
        config = ChartConfig(
            title=chart_def["title"],
            output_filename=chart_def["filename"],
            chart_type=chart_def["type"],
            repository_name="BatchExample",
            plot_config=plot_config
        )
        
        generated_configs.append(config)
        print(f"✓ Created config: {config.title}")
    
    print(f"\nGenerated {len(generated_configs)} chart configurations")
    return generated_configs


def example_mcp_response_handling():
    """Example: Handle MCP tool responses."""
    print("\n=== MCP Response Handling Example ===")
    
    # Simulate successful response
    success_response = MCPToolResponse(
        success=True,
        message="Chart generated successfully",
        output_file="./Generated Data/example_chart.png",
        chart_config=create_default_chart_config(ChartType.HOUR_BAR, "ResponseExample")
    )
    
    print("Success Response:")
    print(success_response.json(indent=2))
    
    # Simulate error response
    error_response = MCPToolResponse(
        success=False,
        message="Failed to generate chart",
        error_details="Data file not found: commit_counts.txt"
    )
    
    print("\nError Response:")
    print(error_response.json(indent=2))
    
    return success_response, error_response


def save_all_examples():
    """Save all example configurations to files."""
    print("\n=== Saving All Examples ===")
    
    os.makedirs("./examples/configs", exist_ok=True)
    
    examples = {
        "basic_config": example_basic_configuration(),
        "custom_styling": example_custom_styling(),
        "mcp_request": example_mcp_request(),
        "visualization_config": example_visualization_config()
    }
    
    for name, config in examples.items():
        filename = f"./examples/configs/{name}.json"
        with open(filename, "w") as f:
            f.write(config.json(indent=2))
        print(f"✓ Saved {filename}")
    
    # Save schema.org examples
    app_schema, dataset_schema = example_schema_org_generation()
    
    with open("./examples/configs/schema_org_app.jsonld", "w") as f:
        json.dump(app_schema, f, indent=2)
    
    with open("./examples/configs/schema_org_dataset.jsonld", "w") as f:
        json.dump(dataset_schema, f, indent=2)
    
    print("✓ Saved schema.org examples")


def main():
    """Run all examples."""
    print("Git Commit Visualization Utilities - Configuration Examples")
    print("=" * 60)
    
    try:
        example_basic_configuration()
        example_custom_styling()
        example_mcp_request()
        example_visualization_config()
        example_schema_org_generation()
        example_configuration_validation()
        example_json_export_import()
        example_batch_chart_generation()
        example_mcp_response_handling()
        save_all_examples()
        
        print("\n" + "=" * 60)
        print("✓ All examples completed successfully!")
        print("Check ./examples/configs/ for saved configuration files")
        
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
