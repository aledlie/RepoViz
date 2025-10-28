"""
Unit tests for installation and setup functionality.
"""

import pytest
import subprocess
import os
from pathlib import Path


class TestInstallScript:
    """Tests for the install.sh script."""

    def test_install_script_exists(self):
        """Verify that the install script exists and is executable."""
        script_path = Path(__file__).parent.parent / "install.sh"
        assert script_path.exists(), "install.sh should exist"
        assert os.access(script_path, os.X_OK), "install.sh should be executable"

    def test_install_script_has_shebang(self):
        """Verify that the install script has a proper shebang."""
        script_path = Path(__file__).parent.parent / "install.sh"
        with open(script_path, 'r') as f:
            first_line = f.readline().strip()
        assert first_line == "#!/bin/bash", "install.sh should have bash shebang"

    def test_install_script_syntax(self):
        """Verify that the install script has valid bash syntax."""
        script_path = Path(__file__).parent.parent / "install.sh"
        result = subprocess.run(
            ["bash", "-n", str(script_path)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"install.sh has syntax errors: {result.stderr}"


class TestRequirements:
    """Tests for requirements files."""

    def test_core_requirements_exist(self):
        """Verify that requirements.txt exists."""
        req_path = Path(__file__).parent.parent / "requirements.txt"
        assert req_path.exists(), "requirements.txt should exist"

    def test_test_requirements_exist(self):
        """Verify that requirements-test.txt exists."""
        req_path = Path(__file__).parent.parent / "requirements-test.txt"
        assert req_path.exists(), "requirements-test.txt should exist"

    def test_core_requirements_content(self):
        """Verify that core requirements contains expected dependencies."""
        req_path = Path(__file__).parent.parent / "requirements.txt"
        with open(req_path, 'r') as f:
            content = f.read()

        required_packages = ['pydantic', 'matplotlib', 'numpy', 'mcp', 'python-dateutil']
        for package in required_packages:
            assert package in content, f"{package} should be in requirements.txt"

    def test_requirements_minimal(self):
        """Verify that requirements.txt only has core dependencies (no dev tools)."""
        req_path = Path(__file__).parent.parent / "requirements.txt"
        with open(req_path, 'r') as f:
            content = f.read()

        # These should NOT be in core requirements
        dev_packages = ['pytest', 'black', 'mypy', 'flake8', 'sphinx']
        for package in dev_packages:
            assert package not in content, f"{package} should not be in core requirements.txt"


class TestProjectStructure:
    """Tests for overall project structure."""

    def test_pyproject_toml_exists(self):
        """Verify that pyproject.toml exists."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml should exist"

    def test_readme_exists(self):
        """Verify that README.md exists."""
        readme_path = Path(__file__).parent.parent / "README.md"
        assert readme_path.exists(), "README.md should exist"

    def test_quickstart_exists(self):
        """Verify that QUICKSTART.md exists."""
        quickstart_path = Path(__file__).parent.parent / "QUICKSTART.md"
        assert quickstart_path.exists(), "QUICKSTART.md should exist"

    def test_activate_script_exists(self):
        """Verify that activate.sh exists."""
        activate_path = Path(__file__).parent.parent / "activate.sh"
        assert activate_path.exists(), "activate.sh should exist"


class TestMCPServerEntry:
    """Tests for MCP server entry point."""

    def test_enhanced_mcp_server_exists(self):
        """Verify that enhanced_mcp_server.py exists."""
        server_path = Path(__file__).parent.parent / "enhanced_mcp_server.py"
        assert server_path.exists(), "enhanced_mcp_server.py should exist"

    def test_enhanced_mcp_server_has_main(self):
        """Verify that enhanced_mcp_server.py has a main function."""
        server_path = Path(__file__).parent.parent / "enhanced_mcp_server.py"
        with open(server_path, 'r') as f:
            content = f.read()
        assert 'def main(' in content, "enhanced_mcp_server.py should have a main function"


class TestDocumentation:
    """Tests for documentation completeness."""

    def test_readme_has_installation_section(self):
        """Verify that README has installation instructions."""
        readme_path = Path(__file__).parent.parent / "README.md"
        with open(readme_path, 'r') as f:
            content = f.read()
        assert '## Quick Start' in content or '## Installation' in content, \
            "README should have installation section"

    def test_quickstart_has_installation(self):
        """Verify that QUICKSTART has installation instructions."""
        quickstart_path = Path(__file__).parent.parent / "QUICKSTART.md"
        with open(quickstart_path, 'r') as f:
            content = f.read()
        assert 'Installation' in content, "QUICKSTART should have installation section"
        assert 'uvx' in content, "QUICKSTART should mention uvx installation"

    def test_readme_mentions_uvx(self):
        """Verify that README mentions uvx installation method."""
        readme_path = Path(__file__).parent.parent / "README.md"
        with open(readme_path, 'r') as f:
            content = f.read()
        assert 'uvx' in content, "README should mention uvx installation method"
