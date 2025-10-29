#!/usr/bin/env python3
"""
Analyze IntegrityStudioClients directory structure to find most active directories.
This will generate data for the ToolVisualizer "Most Active Directories" component.
"""

import os
import json
from pathlib import Path
from collections import defaultdict


def get_file_language(file_path):
    """Determine programming language from file extension."""
    ext_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript React',
        '.jsx': 'React',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.go': 'Go',
        '.java': 'Java',
        '.sh': 'Shell',
        '.bash': 'Shell',
        '.md': 'Markdown'
    }
    return ext_map.get(Path(file_path).suffix.lower(), 'Other')


def analyze_directory(base_path):
    """Analyze directory structure and collect statistics."""
    base = Path(base_path)

    # Skip these directories
    skip_dirs = {
        'node_modules', '__pycache__', 'venv', '.venv', 'dist',
        'build', '.git', '.next', 'coverage', '.pytest_cache',
        'vendor', 'bower_components', '.sass-cache'
    }

    directory_stats = {}

    # Analyze each subdirectory in IntegrityStudioClients
    for item in base.iterdir():
        if not item.is_dir() or item.name.startswith('.'):
            continue

        dir_name = item.name
        file_count = 0
        size_bytes = 0
        languages = defaultdict(int)

        # Walk through subdirectory
        for root, dirs, files in os.walk(item):
            # Remove skip directories from walk
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]

            for file in files:
                if file.startswith('.'):
                    continue

                file_path = Path(root) / file
                try:
                    file_size = file_path.stat().st_size
                    size_bytes += file_size
                    file_count += 1

                    # Track language
                    lang = get_file_language(file_path)
                    if lang != 'Other':
                        languages[lang] += 1
                except (OSError, PermissionError):
                    continue

        if file_count > 0:
            # Get top 3 languages
            top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
            lang_names = [lang for lang, count in top_langs]

            directory_stats[dir_name] = {
                'name': dir_name,
                'file_count': file_count,
                'size_bytes': size_bytes,
                'size_mb': round(size_bytes / (1024 * 1024), 2),
                'languages': lang_names,
                'language_str': ', '.join(lang_names) if lang_names else 'Mixed'
            }

    return directory_stats


def format_size(bytes_size):
    """Format bytes to human readable."""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.2f} KB"
    elif bytes_size < 1024 * 1024 * 1024:
        return f"{bytes_size / (1024 * 1024):.2f} MB"
    else:
        return f"{bytes_size / (1024 * 1024 * 1024):.2f} GB"


def main():
    """Generate directory analysis data."""
    base_path = Path.home() / 'code' / 'IntegrityStudioClients'

    if not base_path.exists():
        print(f"Error: {base_path} does not exist")
        return

    print(f"Analyzing {base_path}...")
    directory_stats = analyze_directory(base_path)

    # Sort by file count (most active first)
    sorted_dirs = sorted(
        directory_stats.values(),
        key=lambda x: x['file_count'],
        reverse=True
    )

    print(f"\nFound {len(sorted_dirs)} directories")
    print("\nMost Active Directories:")
    print("-" * 70)

    for i, dir_info in enumerate(sorted_dirs[:10], 1):
        print(f"{i}. {dir_info['name']}")
        print(f"   Files: {dir_info['file_count']:,}")
        print(f"   Size: {format_size(dir_info['size_bytes'])}")
        print(f"   Languages: {dir_info['language_str']}")
        print()

    # Save data to JSON for integration
    output_file = Path(__file__).parent / 'Generated Data' / 'integrity_studio_active_dirs.json'
    output_file.parent.mkdir(exist_ok=True)

    output_data = {
        'repository': 'IntegrityStudioClients',
        'analyzed_at': '2025-10-28',
        'total_directories': len(sorted_dirs),
        'directories': sorted_dirs
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"Data saved to: {output_file}")

    # Generate HTML snippet for ToolVisualizer
    print("\n" + "=" * 70)
    print("HTML snippet for ToolVisualizer index.html:")
    print("=" * 70)

    for dir_info in sorted_dirs[:5]:
        html_snippet = f'''                        <a href="directories/{dir_info['name']}.html" style="text-decoration: none; color: inherit;">
                            <div class="directory-card">
                                <h4>{dir_info['name']}</h4>
                                <p class="directory-files">{dir_info['file_count']:,} files</p>
                                <p class="directory-lang">{dir_info['language_str']}</p>
                            </div>
                        </a>'''
        print(html_snippet)


if __name__ == '__main__':
    main()
