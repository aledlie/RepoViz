"""
Unit tests for the enhanced plotting scripts.
"""

import pytest
import os
from unittest.mock import patch

from enhanced_plot_scripts import create_chart_from_config
from schemas import ChartConfig, ChartType, PlotConfig, CommitCount, PeriodType

@pytest.fixture
def mock_commit_data():
    """Fixture to provide mock commit data for different period types."""
    return {
        "hour": [CommitCount(period=h, count=h % 6, period_type=PeriodType.HOUR) for h in range(24)],
        "day": [CommitCount(period=d, count=d * 2, period_type=PeriodType.DAY) for d in range(7)],
        "month": [CommitCount(period=m, count=m * 5, period_type=PeriodType.MONTH) for m in range(1, 13)],
    }

@pytest.mark.parametrize("chart_type", [
    ChartType.HOUR_BAR,
    ChartType.DAY_PIE,
    ChartType.MONTH_PIE,
    ChartType.DAY_MONTH_COMBINED,
])
def test_create_chart_from_config(chart_type, tmp_path, mock_commit_data):
    """
    Test that each chart type can be generated without errors and creates an output file.
    """
    # --- Arrange ---
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend for testing

    # Create a temporary Generated Data directory
    generated_data_dir = tmp_path / "Generated Data"
    generated_data_dir.mkdir()

    output_filename = f"test_chart_{chart_type.value}"

    config = ChartConfig(
        title=f"Test {chart_type.value}",
        output_filename=output_filename,
        chart_type=chart_type,
        repository_name="TestRepo",
        plot_config=PlotConfig(dpi=72) # Use low DPI for speed
    )

    # --- Act & Assert ---
    # Patch the data loading and schema saving methods
    with patch('enhanced_plot_scripts.EnhancedPlotter.load_commit_data', side_effect=lambda dtype: mock_commit_data[dtype]) as mock_load:
        with patch('enhanced_plot_scripts.EnhancedPlotter._save_chart_schema'):
            # Change working directory temporarily to use our tmp_path
            original_cwd = os.getcwd()
            try:
                os.chdir(tmp_path)
                result_path = create_chart_from_config(config)
            except Exception as e:
                pytest.fail(f"create_chart_from_config raised an unexpected exception: {e}")
            finally:
                os.chdir(original_cwd)

    # --- Assert ---
    # Verify that the data loading was attempted for the correct data types
    if chart_type == ChartType.HOUR_BAR:
        mock_load.assert_called_once_with("hour")
    elif chart_type == ChartType.DAY_PIE:
        mock_load.assert_called_once_with("day")
    elif chart_type == ChartType.MONTH_PIE:
        mock_load.assert_called_once_with("month")
    elif chart_type == ChartType.DAY_MONTH_COMBINED:
        assert mock_load.call_count == 2
        mock_load.assert_any_call("day")
        mock_load.assert_any_call("month")

    # Verify that the output file was created
    expected_path = generated_data_dir / f"{output_filename}.png"
    assert expected_path.exists(), f"Output file was not created at {expected_path}"
