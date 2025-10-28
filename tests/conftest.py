"""
Pytest configuration and shared fixtures for RepoViz tests.
"""

import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def test_data_dir(tmp_path):
    """Provide a temporary directory for test data files."""
    data_dir = tmp_path / "Generated Data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def sample_git_log():
    """Provide sample git log output for testing."""
    return """commit abc123def456
Author: Test User <test@example.com>
Date:   Mon Jan 15 14:30:00 2024 -0500

    Initial commit

commit def789ghi012
Author: Test User <test@example.com>
Date:   Tue Jan 16 09:15:00 2024 -0500

    Add feature
"""


@pytest.fixture
def sample_commit_counts():
    """Provide sample commit count data."""
    return {
        "hour": "08 10\n09 5\n10 12\n14 20\n",
        "day": "0 15\n1 20\n2 18\n3 25\n4 22\n5 10\n6 8\n",
        "month": "1 100\n2 95\n3 110\n4 105\n5 120\n6 98\n"
    }
