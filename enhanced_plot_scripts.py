#!/usr/bin/env python3
"""
Enhanced plotting scripts with Pydantic configuration support.

This module provides enhanced versions of the plotting scripts that use
Pydantic models for configuration and validation.
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Optional
import json

# Add current directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from schemas import (
        ChartConfig, PlotConfig, CommitCount, ChartType,
        create_default_chart_config, validate_commit_data_file
    )
    from schema_org import get_creative_work_schema, save_structured_data
except ImportError:
    print("Error: Local schema modules not found. Ensure schemas.py and schema_org.py are present.")
    sys.exit(1)


class EnhancedPlotter:
    """Enhanced plotter with Pydantic configuration support."""
    
    def __init__(self, config: ChartConfig):
        """Initialize plotter with validated configuration."""
        self.config = config
        self.plot_config = config.plot_config
        
        # Set matplotlib parameters
        plt.rcParams['figure.dpi'] = self.plot_config.dpi
        plt.rcParams['font.size'] = self.plot_config.font_size
        plt.rcParams['axes.titlesize'] = self.plot_config.title_fontsize
    
    def load_commit_data(self, data_type: str) -> List[CommitCount]:
        """Load and validate commit data."""
        file_mapping = {
            "hour": "./Generated Data/commit_counts.txt",
            "day": "./Generated Data/commit_counts_day.txt",
            "month": "./Generated Data/commit_counts_month.txt"
        }
        
        file_path = file_mapping.get(data_type)
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        return validate_commit_data_file(file_path)
    
    def create_hour_bar_chart(self) -> str:
        """Create hourly bar chart with enhanced configuration."""
        commit_data = self.load_commit_data("hour")
        
        # Prepare data
        hours = [cc.period for cc in commit_data]
        counts = [cc.count for cc in commit_data]
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.plot_config.figsize)
        
        # Create bar chart
        bars = ax.bar(hours, counts, color=self.plot_config.color_primary, 
                     edgecolor=self.plot_config.color_secondary, linewidth=0.5)
        
        # Customize chart
        ax.set_xlabel('Hour of Day', fontsize=self.plot_config.font_size)
        ax.set_ylabel('Number of Commits', fontsize=self.plot_config.font_size)
        ax.set_title(self.config.title, fontsize=self.plot_config.title_fontsize, pad=20)
        
        # Set x-axis ticks
        ax.set_xticks(range(0, 24, 2))
        ax.set_xlim(-0.5, 23.5)
        
        # Add grid
        ax.grid(True, alpha=self.plot_config.grid_alpha, linestyle='--')
        ax.set_axisbelow(True)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            if count > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                       str(count), ha='center', va='bottom', 
                       fontsize=self.plot_config.font_size - 2)
        
        # Save chart
        output_path = f"./Generated Data/{self.config.output_filename}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.plot_config.dpi, bbox_inches='tight')
        plt.close()
        
        # Generate and save schema.org data
        self._save_chart_schema("hour_bar", output_path)
        
        return output_path
    
    def create_day_pie_chart(self) -> str:
        """Create day of week pie chart with enhanced configuration."""
        commit_data = self.load_commit_data("day")
        
        # Prepare data
        day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 
                    'Thursday', 'Friday', 'Saturday']
        
        # Create full data array (some days might have 0 commits)
        day_counts = [0] * 7
        for cc in commit_data:
            day_counts[cc.period] = cc.count
        
        # Filter out days with no commits for cleaner pie chart
        filtered_days = []
        filtered_counts = []
        for i, count in enumerate(day_counts):
            if count > 0:
                filtered_days.append(day_names[i])
                filtered_counts.append(count)
        
        if not filtered_counts:
            raise ValueError("No commit data found for any day")
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.plot_config.figsize)
        
        # Generate colors
        colors = self._generate_pie_colors(len(filtered_counts))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            filtered_counts, 
            labels=filtered_days,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': self.plot_config.font_size}
        )
        
        # Customize chart
        ax.set_title(self.config.title, fontsize=self.plot_config.title_fontsize, pad=20)
        
        # Enhance text appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Save chart
        output_path = f"./Generated Data/{self.config.output_filename}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.plot_config.dpi, bbox_inches='tight')
        plt.close()
        
        # Generate and save schema.org data
        self._save_chart_schema("day_pie", output_path)
        
        return output_path
    
    def create_month_pie_chart(self) -> str:
        """Create monthly pie chart with enhanced configuration."""
        commit_data = self.load_commit_data("month")
        
        # Prepare data
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        # Create full data array
        month_counts = [0] * 12
        for cc in commit_data:
            month_counts[cc.period - 1] = cc.count  # Months are 1-indexed
        
        # Filter out months with no commits
        filtered_months = []
        filtered_counts = []
        for i, count in enumerate(month_counts):
            if count > 0:
                filtered_months.append(month_names[i])
                filtered_counts.append(count)
        
        if not filtered_counts:
            raise ValueError("No commit data found for any month")
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.plot_config.figsize)
        
        # Generate colors
        colors = self._generate_pie_colors(len(filtered_counts))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            filtered_counts,
            labels=filtered_months,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': self.plot_config.font_size}
        )
        
        # Customize chart
        ax.set_title(self.config.title, fontsize=self.plot_config.title_fontsize, pad=20)
        
        # Enhance text appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Save chart
        output_path = f"./Generated Data/{self.config.output_filename}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.plot_config.dpi, bbox_inches='tight')
        plt.close()
        
        # Generate and save schema.org data
        self._save_chart_schema("month_pie", output_path)
        
        return output_path
    
    def create_combined_day_month_chart(self) -> str:
        """Create combined day and month pie charts."""
        day_data = self.load_commit_data("day")
        month_data = self.load_commit_data("month")
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Day of week chart (left)
        day_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        day_counts = [0] * 7
        for cc in day_data:
            day_counts[cc.period] = cc.count
        
        filtered_days = []
        filtered_day_counts = []
        for i, count in enumerate(day_counts):
            if count > 0:
                filtered_days.append(day_names[i])
                filtered_day_counts.append(count)
        
        if filtered_day_counts:
            colors1 = self._generate_pie_colors(len(filtered_day_counts))
            wedges1, texts1, autotexts1 = ax1.pie(
                filtered_day_counts,
                labels=filtered_days,
                colors=colors1,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': self.plot_config.font_size - 2}
            )
            
            for autotext in autotexts1:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        
        ax1.set_title('By Day of Week', fontsize=self.plot_config.title_fontsize - 2)
        
        # Month chart (right)
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_counts = [0] * 12
        for cc in month_data:
            month_counts[cc.period - 1] = cc.count
        
        filtered_months = []
        filtered_month_counts = []
        for i, count in enumerate(month_counts):
            if count > 0:
                filtered_months.append(month_names[i])
                filtered_month_counts.append(count)
        
        if filtered_month_counts:
            colors2 = self._generate_pie_colors(len(filtered_month_counts))
            wedges2, texts2, autotexts2 = ax2.pie(
                filtered_month_counts,
                labels=filtered_months,
                colors=colors2,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': self.plot_config.font_size - 2}
            )
            
            for autotext in autotexts2:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        
        ax2.set_title('By Month', fontsize=self.plot_config.title_fontsize - 2)
        
        # Overall title
        fig.suptitle(self.config.title, fontsize=self.plot_config.title_fontsize, y=0.95)
        
        # Save chart
        output_path = f"./Generated Data/{self.config.output_filename}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.plot_config.dpi, bbox_inches='tight')
        plt.close()
        
        # Generate and save schema.org data
        self._save_chart_schema("day_month_combined", output_path)
        
        return output_path
    
    def _generate_pie_colors(self, count: int) -> List[str]:
        """Generate a list of colors for pie charts."""
        base_color = self.plot_config.color_primary
        secondary_color = self.plot_config.color_secondary
        
        if count == 1:
            return [base_color]
        elif count == 2:
            return [base_color, secondary_color]
        else:
            # Generate gradient colors
            colors = []
            for i in range(count):
                # Interpolate between primary and secondary colors
                ratio = i / (count - 1) if count > 1 else 0
                
                # Convert hex to RGB
                primary_rgb = tuple(int(base_color[j:j+2], 16) for j in (1, 3, 5))
                secondary_rgb = tuple(int(secondary_color[j:j+2], 16) for j in (1, 3, 5))
                
                # Interpolate
                interpolated_rgb = tuple(
                    int(primary_rgb[k] + (secondary_rgb[k] - primary_rgb[k]) * ratio)
                    for k in range(3)
                )
                
                # Convert back to hex
                color = f"#{interpolated_rgb[0]:02x}{interpolated_rgb[1]:02x}{interpolated_rgb[2]:02x}"
                colors.append(color)
            
            return colors
    
    def _save_chart_schema(self, chart_type: str, output_path: str) -> None:
        """Save schema.org structured data for the chart."""
        try:
            schema_data = get_creative_work_schema(
                chart_type, 
                self.config.repository_name, 
                output_path
            )
            
            schema_filename = f"{self.config.output_filename}_schema.jsonld"
            schema_path = f"./Generated Data/schemas/{schema_filename}"
            
            os.makedirs(os.path.dirname(schema_path), exist_ok=True)
            save_structured_data(schema_data, schema_path)
            
        except Exception as e:
            print(f"Warning: Failed to save schema data: {e}")


def create_chart_from_config(config: ChartConfig) -> str:
    """Create a chart based on configuration."""
    plotter = EnhancedPlotter(config)
    
    if config.chart_type == ChartType.HOUR_BAR:
        return plotter.create_hour_bar_chart()
    elif config.chart_type == ChartType.DAY_PIE:
        return plotter.create_day_pie_chart()
    elif config.chart_type == ChartType.MONTH_PIE:
        return plotter.create_month_pie_chart()
    elif config.chart_type == ChartType.DAY_MONTH_COMBINED:
        return plotter.create_combined_day_month_chart()
    else:
        raise ValueError(f"Unsupported chart type: {config.chart_type}")


def create_chart_from_env() -> str:
    """Create chart using environment variables for configuration."""
    # Get configuration from environment
    chart_type_str = os.environ.get('CHART_TYPE', 'hour_bar')
    title = os.environ.get('CHART_TITLE', 'Git Commit Analysis')
    output_filename = os.environ.get('OUTPUT_FILENAME', 'commit_chart')
    repo_name = os.environ.get('REPOSITORY_NAME')
    
    # Parse chart type
    try:
        chart_type = ChartType(chart_type_str)
    except ValueError:
        chart_type = ChartType.HOUR_BAR
    
    # Create plot configuration from environment
    plot_config = PlotConfig()
    
    if os.environ.get('DPI'):
        try:
            plot_config.dpi = int(os.environ['DPI'])
        except ValueError:
            pass
    
    if os.environ.get('COLOR_PRIMARY'):
        plot_config.color_primary = os.environ['COLOR_PRIMARY']
    
    if os.environ.get('COLOR_SECONDARY'):
        plot_config.color_secondary = os.environ['COLOR_SECONDARY']
    
    # Create chart configuration
    config = ChartConfig(
        title=title,
        output_filename=output_filename,
        chart_type=chart_type,
        repository_name=repo_name,
        plot_config=plot_config
    )
    
    return create_chart_from_config(config)


def main():
    """Main function for standalone script execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Git Commit Visualization')
    parser.add_argument('--type', choices=['hour_bar', 'day_pie', 'month_pie', 'day_month_combined'],
                       default='hour_bar', help='Chart type to generate')
    parser.add_argument('--title', default='Git Commit Analysis', help='Chart title')
    parser.add_argument('--output', default='commit_chart', help='Output filename (without extension)')
    parser.add_argument('--repo', help='Repository name')
    parser.add_argument('--dpi', type=int, default=300, help='Chart resolution')
    parser.add_argument('--color', default='#4e79a7', help='Primary color')
    parser.add_argument('--config', help='JSON configuration file')
    
    args = parser.parse_args()
    
    if args.config and os.path.exists(args.config):
        # Load configuration from file
        with open(args.config, 'r') as f:
            config_data = json.load(f)
        config = ChartConfig(**config_data)
    else:
        # Create configuration from arguments
        plot_config = PlotConfig(dpi=args.dpi, color_primary=args.color)
        config = ChartConfig(
            title=args.title,
            output_filename=args.output,
            chart_type=ChartType(args.type),
            repository_name=args.repo,
            plot_config=plot_config
        )
    
    try:
        output_path = create_chart_from_config(config)
        print(f"Chart saved to: {output_path}")
        
        # Print configuration used
        print(f"\nConfiguration used:")
        print(config.json(indent=2))
        
    except Exception as e:
        print(f"Error creating chart: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
