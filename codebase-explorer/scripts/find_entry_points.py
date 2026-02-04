#!/usr/bin/env python3
"""
Entry Point Finder

Finds entry points and key configuration files in a project:
- Main entry files (main.py, index.js, App.vue, etc.)
- Route definitions
- Configuration files
- API endpoints

Usage:
    find_entry_points.py [project_path]
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple


# Common entry point file patterns
ENTRY_POINT_PATTERNS = {
    'Python': {
        'main': ['main.py', 'app.py', 'run.py', 'server.py', 'wsgi.py', '__main__.py'],
        'cli': ['cli.py'],
    },
    'JavaScript/TypeScript': {
        'main': ['index.js', 'index.ts', 'main.js', 'main.ts', 'app.js', 'app.ts'],
        'server': ['server.js', 'server.ts'],
        'cli': ['cli.js', 'cli.ts'],
    },
    'React': {
        'root': ['App.jsx', 'App.tsx', 'index.jsx', 'index.tsx'],
        'entry': ['src/index.js', 'src/index.tsx', 'src/main.jsx', 'src/main.tsx'],
    },
    'Vue': {
        'root': ['App.vue', 'main.js', 'main.ts'],
        'entry': ['src/main.js', 'src/main.ts'],
    },
    'Next.js': {
        'pages': ['pages/index.js', 'pages/index.tsx', 'pages/_app.js', 'pages/_app.tsx'],
        'app': ['app/page.js', 'app/page.tsx', 'app/layout.js', 'app/layout.tsx'],
    },
    'Nuxt': {
        'pages': ['pages/index.vue'],
        'app': ['app.vue'],
    },
    'Go': {
        'main': ['main.go', 'cmd/*/main.go'],
    },
    'Rust': {
        'main': ['main.rs', 'src/main.rs'],
    },
    'Java': {
        'main': ['src/main/java/*/Main.java', 'src/main/java/*/Application.java'],
    },
}


# Configuration file patterns
CONFIG_PATTERNS = {
    'General': ['.env*', '*.config.js', '*.config.ts'],
    'JavaScript/TypeScript': ['tsconfig.json', 'jsconfig.json', '.eslintrc*', '.prettierrc*'],
    'Python': ['setup.py', 'pyproject.toml', 'pytest.ini', 'tox.ini', '.flake8'],
    'Go': ['go.mod', 'go.sum'],
    'Rust': ['Cargo.toml', 'Cargo.lock'],
    'Java': ['pom.xml', 'build.gradle', 'application.properties', 'application.yml'],
    'Testing': ['jest.config.*', 'vitest.config.*', 'cypress.config.*', 'playwright.config.*'],
    'Docker': ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml'],
    'CI/CD': ['.gitlab-ci.yml', '.github/workflows/*.yml', '.travis.yml', 'circleci'],
}


def find_files_by_pattern(project_path: Path, patterns: List[str]) -> List[Path]:
    """Find files matching glob patterns."""
    found = []

    for pattern in patterns:
        # Handle patterns with directory structure
        if '/' in pattern:
            # Pattern includes directory (e.g., 'src/index.js')
            parts = pattern.split('/')
            base_pattern = '/'.join(parts[:-1])
            file_pattern = parts[-1]

            base_dir = project_path
            for part in base_pattern.split('/'):
                if part == '*':
                    # Wildcard directory
                    if base_dir.exists() and base_dir.is_dir():
                        matching_dirs = [d for d in base_dir.iterdir() if d.is_dir()]
                        for md in matching_dirs:
                            found.extend(md.glob(file_pattern))
                    break
                else:
                    base_dir = base_dir / part
                    if not base_dir.exists():
                        break
            else:
                if base_dir.exists():
                    found.extend(base_dir.glob(file_pattern))
        else:
            # Simple file pattern
            found.extend(project_path.rglob(pattern))

    return sorted(set(found))


def find_entry_points(project_path: Path) -> Dict[str, List[Path]]:
    """Find entry points in the project."""
    entry_points = {}

    for category, patterns in ENTRY_POINT_PATTERNS.items():
        for subcategory, file_patterns in patterns.items():
            key = f"{category} - {subcategory}"
            found = find_files_by_pattern(project_path, file_patterns)
            if found:
                entry_points[key] = found

    return entry_points


def find_config_files(project_path: Path) -> Dict[str, List[Path]]:
    """Find configuration files in the project."""
    config_files = {}

    for category, patterns in CONFIG_PATTERNS.items():
        found = find_files_by_pattern(project_path, patterns)
        if found:
            config_files[category] = found

    return config_files


def find_routes(project_path: Path) -> Dict[str, List[Path]]:
    """Find route definition files."""
    routes = {}

    # Common route file patterns
    route_patterns = [
        # Python
        'routes.py', 'urls.py', 'views.py', 'app/routes.py',
        # JavaScript/TypeScript
        'routes.js', 'routes.ts', 'router.js', 'router.ts',
        # Next.js
        'pages/**/*.js', 'pages/**/*.tsx', 'app/**/page.js', 'app/**/page.tsx',
        # Nuxt
        'pages/**/*.vue',
        # React Router
        '**/routes.js', '**/routes.tsx',
        # Vue Router
        'router/*.js', 'router/*.ts',
    ]

    found = find_files_by_pattern(project_path, route_patterns)
    if found:
        routes['Route definitions'] = found

    return routes


def find_api_endpoints(file_path: Path) -> List[Dict[str, str]]:
    """Extract API endpoint definitions from code files."""
    endpoints = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Python Flask/Django/FastAPI patterns
        python_patterns = [
            r'@app\.route\([\'"]([^\'"]+)[\'"]',
            r'@bp\.route\([\'"]([^\'"]+)[\'"]',
            r'@router\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]',
            r'@api\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]',
            r'path\([\'"]([^\'"]+)[\'"]',
            r'url\(r[\'"]([^\'"]+)[\'"]',
        ]

        for pattern in python_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    endpoint = match[1] if len(match) > 1 else match[0]
                else:
                    endpoint = match
                endpoints.append({
                    'method': 'GET',  # Default, could be refined
                    'path': endpoint,
                    'source': str(file_path.relative_to(file_path.parents[-2])),
                })

        # JavaScript/TypeScript Express patterns
        js_patterns = [
            r'app\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]',
            r'router\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]',
        ]

        for pattern in js_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                method = match[0].upper()
                path = match[1]
                endpoints.append({
                    'method': method,
                    'path': path,
                    'source': str(file_path.relative_to(file_path.parents[-2])),
                })

    except Exception:
        pass

    return endpoints


def analyze_routes(project_path: Path, route_files: List[Path]) -> Dict:
    """Analyze route files and extract endpoints."""
    endpoints = []

    for file_path in route_files[:10]:  # Limit to first 10 files
        file_endpoints = find_api_endpoints(file_path)
        endpoints.extend(file_endpoints)

    return {
        'total': len(endpoints),
        'endpoints': endpoints[:20],  # Return first 20
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: find_entry_points.py [project_path]")
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()

    if not project_path.exists():
        print(f"Error: Path not found: {project_path}")
        sys.exit(1)

    print(f"🎯 Finding entry points: {project_path}\n")

    # Find entry points
    entry_points = find_entry_points(project_path)

    print("=" * 60)
    print("ENTRY POINTS")
    print("=" * 60)
    if entry_points:
        for category, files in entry_points.items():
            print(f"\n{category}:")
            for file in files:
                rel_path = file.relative_to(project_path)
                print(f"  • {rel_path}")
    else:
        print("  No entry points detected")

    # Find config files
    config_files = find_config_files(project_path)

    print("\n" + "=" * 60)
    print("CONFIGURATION FILES")
    print("=" * 60)
    if config_files:
        for category, files in config_files.items():
            print(f"\n{category}:")
            for file in files[:5]:  # Limit to 5 per category
                rel_path = file.relative_to(project_path)
                print(f"  • {rel_path}")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more")
    else:
        print("  No config files detected")

    # Find routes
    routes = find_routes(project_path)

    print("\n" + "=" * 60)
    print("ROUTE DEFINITIONS")
    print("=" * 60)
    if routes:
        for category, files in routes.items():
            print(f"\n{category}:")
            for file in files[:10]:  # Limit to 10
                rel_path = file.relative_to(project_path)
                print(f"  • {rel_path}")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more")

        # Analyze endpoints
        route_files = routes['Route definitions']
        endpoints_info = analyze_routes(project_path, route_files)

        if endpoints_info['endpoints']:
            print(f"\nDetected API Endpoints ({endpoints_info['total']} total, showing first 20):")
            for ep in endpoints_info['endpoints']:
                print(f"  {ep['method']} {ep['path']}")
                print(f"    → {ep['source']}")
    else:
        print("  No route definitions detected")

    # Save to JSON
    output_file = project_path / '.codebase-entry-points.json'
    import json
    with open(output_file, 'w') as f:
        json.dump({
            'entry_points': {k: [str(v) for v in vals] for k, vals in entry_points.items()},
            'config_files': {k: [str(v) for v in vals] for k, vals in config_files.items()},
            'routes': {k: [str(v) for v in vals] for k, vals in routes.items()},
        }, f, indent=2)

    print(f"\n✅ Entry points saved to: {output_file}")


if __name__ == "__main__":
    main()
