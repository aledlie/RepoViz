#!/usr/bin/env python3
"""
Enhanced setup script for Git Commit Visualization Utilities.

This script sets up the enhanced version with Pydantic schemas,
schema.org structured data, and database support.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_git_repository():
    """Check if we're in a git repository."""
    try:
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository detected")
            return True
        else:
            print("⚠️  Not in a git repository - some features may not work")
            return False
    except FileNotFoundError:
        print("❌ Git not found - please install Git")
        return False


def create_virtual_environment():
    """Create and activate virtual environment."""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def get_pip_command():
    """Get the appropriate pip command for the platform."""
    if os.name == 'nt':  # Windows
        return [".venv/Scripts/python", "-m", "pip"]
    else:  # Unix-like
        return [".venv/bin/python", "-m", "pip"]


def install_dependencies():
    """Install required dependencies."""
    pip_cmd = get_pip_command()
    
    # Upgrade pip first
    try:
        print("📦 Upgrading pip...")
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], check=True)
        print("✅ Pip upgraded")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Failed to upgrade pip: {e}")
    
    # Install requirements
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        try:
            print("📦 Installing dependencies from requirements.txt...")
            subprocess.run(pip_cmd + ["install", "-r", "requirements.txt"], check=True)
            print("✅ Dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    else:
        # Install core dependencies manually
        core_deps = [
            "pydantic>=2.0.0",
            "matplotlib>=3.7.0", 
            "numpy>=1.24.0",
            "mcp[cli]>=0.1.0",
            "sqlalchemy>=2.0.0"
        ]
        
        try:
            print("📦 Installing core dependencies...")
            subprocess.run(pip_cmd + ["install"] + core_deps, check=True)
            print("✅ Core dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install core dependencies: {e}")
            return False


def create_directory_structure():
    """Create necessary directories."""
    directories = [
        "Generated Data",
        "Generated Data/schemas",
        "examples",
        "examples/configs",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")


def make_scripts_executable():
    """Make shell scripts executable on Unix-like systems."""
    if os.name != 'nt':  # Not Windows
        shell_scripts = [
            "commit_history.sh",
            "commits_by_hour.sh", 
            "commits_by_day.sh",
            "commits_by_month.sh",
            "get_repo_name.sh",
            "convert_kebab_to_snake.sh",
            "convert_snake_to_kebab.sh"
        ]
        
        for script in shell_scripts:
            script_path = Path(script)
            if script_path.exists():
                try:
                    subprocess.run(["chmod", "+x", str(script_path)], check=True)
                    print(f"✅ Made executable: {script}")
                except subprocess.CalledProcessError:
                    print(f"⚠️  Could not make executable: {script}")


def test_imports():
    """Test that all enhanced modules can be imported."""
    python_cmd = get_pip_command()[0]  # Get python executable
    
    modules_to_test = [
        "schemas",
        "schema_org", 
        "enhanced_plot_scripts",
        "database_schema"
    ]
    
    print("🧪 Testing module imports...")
    
    for module in modules_to_test:
        try:
            result = subprocess.run([python_cmd, "-c", f"import {module}; print('✅ {module}')"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout.strip())
            else:
                print(f"❌ Failed to import {module}: {result.stderr.strip()}")
                return False
        except Exception as e:
            print(f"❌ Error testing {module}: {e}")
            return False
    
    return True


def initialize_database():
    """Initialize the SQLite database."""
    python_cmd = get_pip_command()[0]
    
    try:
        print("🗄️  Initializing database...")
        result = subprocess.run([
            python_cmd, "-c",
            "from database_schema import initialize_database; "
            "db = initialize_database(); "
            "print('Database initialized successfully')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database initialized")
            return True
        else:
            print(f"❌ Database initialization failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False


def generate_example_configs():
    """Generate example configuration files."""
    python_cmd = get_pip_command()[0]
    
    try:
        print("📝 Generating example configurations...")
        result = subprocess.run([
            python_cmd, "examples/example_configs.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Example configurations generated")
            return True
        else:
            print(f"⚠️  Could not generate examples: {result.stderr}")
            return False
    except Exception as e:
        print(f"⚠️  Error generating examples: {e}")
        return False


def create_activation_script():
    """Create convenience script for activating environment."""
    if os.name == 'nt':  # Windows
        activate_script = """@echo off
echo Activating Git Visualization Utilities environment...
call .venv\\Scripts\\activate.bat
echo Environment activated! You can now run:
echo   python enhanced_mcp_server.py
echo   python enhanced_plot_scripts.py --help
echo   python examples/example_configs.py
"""
        script_name = "activate.bat"
    else:  # Unix-like
        activate_script = """#!/bin/bash
echo "Activating Git Visualization Utilities environment..."
source .venv/bin/activate
echo "Environment activated! You can now run:"
echo "  python enhanced_mcp_server.py"
echo "  python enhanced_plot_scripts.py --help"
echo "  python examples/example_configs.py"
"""
        script_name = "activate.sh"
    
    with open(script_name, "w") as f:
        f.write(activate_script)
    
    if os.name != 'nt':
        subprocess.run(["chmod", "+x", script_name])
    
    print(f"✅ Created activation script: {script_name}")


def create_config_file():
    """Create default configuration file."""
    config = {
        "version": "2.0.0",
        "enhanced_features": True,
        "default_plot_config": {
            "dpi": 300,
            "figsize": [12, 8],
            "color_primary": "#4e79a7",
            "color_secondary": "#2e4977",
            "font_size": 12,
            "title_fontsize": 16,
            "grid_alpha": 0.3
        },
        "paths": {
            "data_source": "./Generated Data/",
            "output": "./Generated Data/",
            "schemas": "./Generated Data/schemas/"
        },
        "database": {
            "url": "sqlite:///./Generated Data/git_viz.db",
            "enabled": True
        },
        "mcp_server": {
            "name": "git-visualization-server",
            "version": "1.0.0"
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created default configuration file: config.json")


def print_success_message():
    """Print setup completion message."""
    print("\n" + "=" * 60)
    print("🎉 Enhanced Git Commit Visualization Utilities Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Activate the environment:")
    if os.name == 'nt':
        print("   activate.bat")
    else:
        print("   source activate.sh")
    print()
    print("2. Generate your first chart:")
    print("   python enhanced_plot_scripts.py --type hour_bar")
    print()
    print("3. Start the MCP server:")
    print("   python enhanced_mcp_server.py")
    print()
    print("4. Explore examples:")
    print("   python examples/example_configs.py")
    print()
    print("5. Check the documentation:")
    print("   - README.md for basic usage")
    print("   - examples/configs/ for configuration examples")
    print("   - Generated Data/schemas/ for schema.org data")
    print()
    print("Features enabled:")
    print("✅ Pydantic data validation")
    print("✅ Schema.org structured data")
    print("✅ Enhanced MCP server")
    print("✅ SQLite database support")
    print("✅ Advanced plotting configurations")


def main():
    """Run the complete setup process."""
    print("Git Commit Visualization Utilities - Enhanced Setup")
    print("=" * 60)
    
    success = True
    
    # Check prerequisites
    if not check_python_version():
        success = False
    
    check_git_repository()  # Warning only, not required
    
    # Setup steps
    if success and not create_virtual_environment():
        success = False
    
    if success and not install_dependencies():
        success = False
    
    if success:
        create_directory_structure()
        make_scripts_executable()
        create_config_file()
        create_activation_script()
    
    # Test installation
    if success and not test_imports():
        print("⚠️  Some modules failed to import - check dependencies")
        success = False
    
    # Optional steps
    if success:
        initialize_database()  # Continue even if this fails
        generate_example_configs()  # Continue even if this fails
    
    if success:
        print_success_message()
    else:
        print("\n❌ Setup failed - please check the errors above")
        sys.exit(1)


if __name__ == "__main__":
    main()
