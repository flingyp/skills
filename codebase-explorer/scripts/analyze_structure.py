#!/usr/bin/env python3
"""
Project Structure Analyzer

Analyzes a project directory structure and generates:
- Directory tree representation
- File statistics (counts, line counts)
- Mermaid-compatible tree format
- Identification of key directories

Usage:
    analyze_structure.py [project_path] [--max-depth N] [--include-hidden]
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import json


# Common key directory patterns
KEY_DIRECTORIES = {
    'src': 'Source code',
    'lib': 'Library code',
    'app': 'Application code',
    'components': 'UI components',
    'pages': 'Page components',
    'views': 'View components',
    'api': 'API endpoints',
    'routes': 'Route definitions',
    'controllers': 'Controller logic',
    'services': 'Business logic services',
    'models': 'Data models',
    'utils': 'Utility functions',
    'helpers': 'Helper functions',
    'config': 'Configuration files',
    'tests': 'Test files',
    'test': 'Test files',
    '__tests__': 'Test files',
    'spec': 'Test specifications',
    'docs': 'Documentation',
    'assets': 'Static assets',
    'public': 'Public files',
    'static': 'Static files',
    'styles': 'Stylesheets',
    'scripts': 'Build/deploy scripts',
    'dist': 'Distribution files',
    'build': 'Build output',
    'node_modules': 'Node dependencies',
    '.git': 'Git version control',
    'vendor': 'Third-party dependencies',
}

# File extensions to count as code
CODE_EXTENSIONS = {
    'py', 'js', 'ts', 'jsx', 'tsx', 'vue', 'svelte',
    'java', 'kt', 'kts', 'go', 'rs', 'c', 'cpp', 'h', 'hpp',
    'cs', 'swift', 'rb', 'php', 'scala', 'dart',
    'html', 'css', 'scss', 'sass', 'less',
    'json', 'yaml', 'yml', 'xml', 'toml', 'ini',
}


def count_lines(file_path: Path) -> int:
    """Count lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def analyze_directory(
    root_path: Path,
    max_depth: int = 3,
    include_hidden: bool = False,
    current_depth: int = 0
) -> Dict:
    """
    Recursively analyze directory structure.

    Returns dict with:
    - name: Directory/file name
    - type: 'dir' or 'file'
    - path: Relative path from root
    - children: List of child items (for directories)
    - line_count: Line count (for code files)
    - is_key: Whether this is a key directory
    """
    if current_depth > max_depth:
        return None

    result = {
        'name': root_path.name,
        'type': 'dir' if root_path.is_dir() else 'file',
        'path': str(root_path),
        'children': [],
        'line_count': 0,
        'is_key': False,
    }

    if root_path.is_dir():
        # Check if this is a key directory
        result['is_key'] = root_path.name.lower() in KEY_DIRECTORIES

        # Skip hidden directories unless requested
        if not include_hidden and root_path.name.startswith('.') and root_path.name != '.':
            return None

        # Skip common generated directories
        skip_dirs = {'node_modules', '__pycache__', '.git', 'dist', 'build', '.next', '.nuxt'}
        if root_path.name in skip_dirs:
            result['children'] = ['<skipped>']
            return result

        # Process children
        try:
            items = sorted(root_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            for item in items:
                child = analyze_directory(item, max_depth, include_hidden, current_depth + 1)
                if child:
                    result['children'].append(child)
                    result['line_count'] += child.get('line_count', 0)
        except PermissionError:
            result['children'] = ['<permission denied>']
    else:
        # Count lines for code files
        ext = root_path.suffix.lstrip('.').lower()
        if ext in CODE_EXTENSIONS:
            result['line_count'] = count_lines(root_path)

    return result


def generate_text_tree(structure: Dict, prefix: str = '', is_last: bool = True) -> str:
    """Generate ASCII directory tree."""
    lines = []
    connector = '└── ' if is_last else '├── '
    lines.append(f"{prefix}{connector}{structure['name']}")

    # Add metadata for directories
    if structure['type'] == 'dir':
        if structure['is_key']:
            key_desc = KEY_DIRECTORIES.get(structure['name'].lower(), '')
            lines.append(f"{prefix}{'    ' if is_last else '│   '}# {key_desc}")

    # Process children
    children = structure.get('children', [])
    extension = '    ' if is_last else '│   '

    for i, child in enumerate(children):
        if isinstance(child, str):
            # Special markers like '<skipped>'
            lines.append(f"{prefix}{extension}{child}")
        else:
            is_last_child = (i == len(children) - 1)
            lines.append(generate_text_tree(child, prefix + extension, is_last_child))

    return '\n'.join(lines)


def generate_mermaid_tree(structure: Dict, indent: int = 0) -> str:
    """Generate Mermind tree diagram."""
    lines = []
    prefix = '  ' * indent

    if structure['type'] == 'dir':
        lines.append(f"{prefix}{structure['name']}")
        for child in structure.get('children', []):
            if isinstance(child, str):
                continue  # Skip special markers
            lines.append(generate_mermaid_tree(child, indent + 1))
    else:
        # Add line count for code files
        line_info = f" ({structure['line_count']} lines)" if structure['line_count'] > 0 else ''
        lines.append(f"{prefix}{structure['name']}{line_info}")

    return '\n'.join(lines)


def calculate_stats(structure: Dict) -> Dict:
    """Calculate file statistics."""
    stats = {
        'total_files': 0,
        'code_files': 0,
        'total_lines': 0,
        'directories': 0,
        'by_language': {},
    }

    def traverse(node):
        if isinstance(node, str):
            return

        if node['type'] == 'dir':
            stats['directories'] += 1
            for child in node.get('children', []):
                traverse(child)
        else:
            stats['total_files'] += 1
            if node['line_count'] > 0:
                stats['code_files'] += 1
                stats['total_lines'] += node['line_count']

                ext = Path(node['path']).suffix.lstrip('.').lower()
                stats['by_language'][ext] = stats['by_language'].get(ext, 0) + node['line_count']

    traverse(structure)
    return stats


def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_structure.py [project_path] [--max-depth N] [--include-hidden]")
        print("\nExample:")
        print("  analyze_structure.py .")
        print("  analyze_structure.py ./my-project --max-depth 2")
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()
    max_depth = 3
    include_hidden = False

    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--max-depth' and i + 1 < len(sys.argv):
            max_depth = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--include-hidden':
            include_hidden = True
            i += 1
        else:
            i += 1

    if not project_path.exists():
        print(f"Error: Path not found: {project_path}")
        sys.exit(1)

    print(f"📁 Analyzing: {project_path}\n")

    # Analyze structure
    structure = analyze_directory(project_path, max_depth, include_hidden)

    # Calculate statistics
    stats = calculate_stats(structure)

    # Output results
    print("=" * 60)
    print("PROJECT STATISTICS")
    print("=" * 60)
    print(f"Total directories: {stats['directories']}")
    print(f"Total files: {stats['total_files']}")
    print(f"Code files: {stats['code_files']}")
    print(f"Total lines of code: {stats['total_lines']}")
    print(f"\nLines by language:")
    for lang, lines in sorted(stats['by_language'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {lang}: {lines:,} lines")

    print("\n" + "=" * 60)
    print("DIRECTORY TREE")
    print("=" * 60)
    print(generate_text_tree(structure))

    print("\n" + "=" * 60)
    print("MERMAID TREE DIAGRAM")
    print("=" * 60)
    print("```mermaid")
    print("graph TD")
    print(generate_mermaid_tree(structure))
    print("```")

    # Also output as JSON for programmatic use
    output_file = project_path / '.codebase-structure.json'
    with open(output_file, 'w') as f:
        json.dump({
            'structure': structure,
            'stats': stats
        }, f, indent=2)

    print(f"\n✅ Structure saved to: {output_file}")


if __name__ == "__main__":
    main()
