#!/usr/bin/env python3
"""Setup script for git-commit-visualization-utilities MCP server."""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="git-commit-visualization-utilities",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="A comprehensive toolkit for analyzing and visualizing Git commit patterns with MCP server support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alyshia Ledlie",
    author_email="alyshia@inventoryai.com",
    url="https://github.com/alyshialedlie/RepoViz",
    packages=find_packages(),
    py_modules=["schemas", "schema_org", "enhanced_plot_scripts", "database_schema", "enhanced_mcp_server"],
    include_package_data=True,
    package_data={
        "": ["*.sh", "*.txt", "*.json", "*.jsonld", "*.md"],
    },
    install_requires=requirements,
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "git-viz=enhanced_plot_scripts:main",
            "git-viz-server=enhanced_mcp_server:main",
        ],
        "mcp.servers": [
            "git-visualization=enhanced_mcp_server:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Tools",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities",
    ],
    keywords="git commit-analysis data-visualization charts development-tools repository-analytics matplotlib python mcp-server pydantic schema-org",
)