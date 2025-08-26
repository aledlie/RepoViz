"""
Pydantic schemas for Git Commit Visualization Utilities.

This module defines data models for commit data, chart configurations,
and MCP server requests to ensure type safety and data validation.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal, Tuple
from datetime import datetime
from enum import Enum


class ChartType(str, Enum):
    """Supported chart types."""
    HOUR_BAR = "hour_bar"
    DAY_PIE = "day_pie"
    MONTH_PIE = "month_pie"
    DAY_MONTH_COMBINED = "day_month_combined"


class PeriodType(str, Enum):
    """Time period types for commit analysis."""
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"


class CommitData(BaseModel):
    """Individual commit data model."""
    timestamp: datetime
    hour: int = Field(..., ge=0, le=23, description="Hour of commit (0-23)")
    day_of_week: int = Field(..., ge=0, le=6, description="Day of week (0=Sunday, 6=Saturday)")
    month: int = Field(..., ge=1, le=12, description="Month of commit (1-12)")
    author: str = Field(..., min_length=1, description="Commit author name")
    message: str = Field(..., min_length=1, description="Commit message")
    repository: Optional[str] = Field(None, description="Repository name")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CommitCount(BaseModel):
    """Aggregated commit count for a specific time period."""
    period: int = Field(..., description="Time period value")
    count: int = Field(..., ge=0, description="Number of commits in this period")
    period_type: PeriodType = Field(..., description="Type of time period")

    @validator('period')
    def validate_period_range(cls, v, values):
        """Validate period value based on period type."""
        period_type = values.get('period_type')
        if period_type == PeriodType.HOUR and not (0 <= v <= 23):
            raise ValueError('Hour must be between 0 and 23')
        elif period_type == PeriodType.DAY and not (0 <= v <= 6):
            raise ValueError('Day must be between 0 and 6')
        elif period_type == PeriodType.MONTH and not (1 <= v <= 12):
            raise ValueError('Month must be between 1 and 12')
        return v


class PlotConfig(BaseModel):
    """Configuration for plot generation."""
    dpi: int = Field(300, ge=72, le=600, description="Plot resolution in DPI")
    figsize: Tuple[float, float] = Field((12, 8), description="Figure size (width, height)")
    color_primary: str = Field("#4e79a7", description="Primary color for charts")
    color_secondary: str = Field("#2e4977", description="Secondary color for charts")
    font_size: int = Field(12, ge=8, le=24, description="Base font size")
    grid_alpha: float = Field(0.3, ge=0.0, le=1.0, description="Grid transparency")
    title_fontsize: int = Field(16, ge=10, le=32, description="Title font size")
    
    @validator('color_primary', 'color_secondary')
    def validate_hex_color(cls, v):
        """Validate hex color format."""
        if not v.startswith('#') or len(v) != 7:
            raise ValueError('Color must be in hex format (#RRGGBB)')
        try:
            int(v[1:], 16)
        except ValueError:
            raise ValueError('Invalid hex color format')
        return v


class ChartConfig(BaseModel):
    """Configuration for individual chart generation."""
    title: str = Field(..., min_length=1, description="Chart title")
    output_filename: str = Field(..., min_length=1, description="Output filename (without extension)")
    chart_type: ChartType = Field(..., description="Type of chart to generate")
    repository_name: Optional[str] = Field(None, description="Repository name for title/filename")
    plot_config: PlotConfig = Field(default_factory=PlotConfig, description="Plot styling configuration")
    
    @validator('output_filename')
    def validate_filename(cls, v):
        """Ensure filename doesn't contain invalid characters."""
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        if any(char in v for char in invalid_chars):
            raise ValueError(f'Filename cannot contain: {", ".join(invalid_chars)}')
        return v


class ChartRequest(BaseModel):
    """MCP server chart generation request."""
    chart_type: ChartType = Field(..., description="Type of chart to generate")
    repository_name: Optional[str] = Field(None, description="Repository name")
    output_filename: Optional[str] = Field(None, description="Custom output filename")
    title: Optional[str] = Field(None, description="Custom chart title")
    plot_config: Optional[PlotConfig] = Field(None, description="Custom plot configuration")


class VisualizationConfig(BaseModel):
    """Overall configuration for the visualization toolkit."""
    data_source_path: str = Field("./Generated Data/", description="Path to data files")
    output_path: str = Field("./Generated Data/", description="Path for output files")
    default_plot_config: PlotConfig = Field(default_factory=PlotConfig)
    supported_formats: List[str] = Field(["png", "pdf", "svg"], description="Supported output formats")
    auto_detect_repo: bool = Field(True, description="Automatically detect repository name")


class RepositoryInfo(BaseModel):
    """Repository information for chart generation."""
    name: str = Field(..., min_length=1, description="Repository name")
    remote_url: Optional[str] = Field(None, description="Git remote URL")
    branch: Optional[str] = Field(None, description="Current branch")
    total_commits: Optional[int] = Field(None, ge=0, description="Total number of commits")
    date_range: Optional[Tuple[datetime, datetime]] = Field(None, description="Commit date range")


class DataFile(BaseModel):
    """Data file information."""
    filename: str = Field(..., description="Data file name")
    path: str = Field(..., description="Full file path")
    format: Literal["txt", "csv", "json"] = Field("txt", description="File format")
    last_modified: Optional[datetime] = Field(None, description="Last modification time")
    record_count: Optional[int] = Field(None, ge=0, description="Number of records")


class MCPToolResponse(BaseModel):
    """Response from MCP tool execution."""
    success: bool = Field(..., description="Whether the operation succeeded")
    message: str = Field(..., description="Response message")
    output_file: Optional[str] = Field(None, description="Generated output file path")
    chart_config: Optional[ChartConfig] = Field(None, description="Configuration used")
    error_details: Optional[str] = Field(None, description="Error details if failed")


# Validation helper functions
def validate_commit_data_file(file_path: str) -> List[CommitCount]:
    """Validate and parse commit count data from file."""
    import os
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    commit_counts = []
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                parts = line.split()
                if len(parts) != 2:
                    raise ValueError(f"Invalid format at line {line_num}: expected 'period count'")
                
                period, count = int(parts[0]), int(parts[1])
                
                # Determine period type based on filename
                if 'hour' in file_path:
                    period_type = PeriodType.HOUR
                elif 'day' in file_path:
                    period_type = PeriodType.DAY
                elif 'month' in file_path:
                    period_type = PeriodType.MONTH
                else:
                    raise ValueError("Cannot determine period type from filename")
                
                commit_counts.append(CommitCount(
                    period=period,
                    count=count,
                    period_type=period_type
                ))
                
            except ValueError as e:
                raise ValueError(f"Error parsing line {line_num}: {e}")
    
    return commit_counts


# Example usage and factory functions
def create_default_chart_config(chart_type: ChartType, repo_name: Optional[str] = None) -> ChartConfig:
    """Create a default chart configuration."""
    type_titles = {
        ChartType.HOUR_BAR: "Commits by Hour",
        ChartType.DAY_PIE: "Commits by Day of Week",
        ChartType.MONTH_PIE: "Commits by Month",
        ChartType.DAY_MONTH_COMBINED: "Commits by Day and Month"
    }
    
    type_filenames = {
        ChartType.HOUR_BAR: "commits_by_hour",
        ChartType.DAY_PIE: "commits_by_day",
        ChartType.MONTH_PIE: "commits_by_month",
        ChartType.DAY_MONTH_COMBINED: "commits_by_day_month"
    }
    
    title = type_titles[chart_type]
    filename = type_filenames[chart_type]
    
    if repo_name:
        title = f"{title} - {repo_name}"
        filename = f"{filename}_{repo_name.lower().replace(' ', '_').replace('-', '_')}"
    
    return ChartConfig(
        title=title,
        output_filename=filename,
        chart_type=chart_type,
        repository_name=repo_name
    )
