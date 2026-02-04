#!/usr/bin/env python3
"""
Tech Stack Detector

Detects the technology stack of a project by analyzing:
- Dependency files (package.json, requirements.txt, etc.)
- Configuration files
- File extensions and directory structure
- Build tools and frameworks

Usage:
    detect_tech_stack.py [project_path]
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set


# Dependency file patterns and their package managers
DEPENDENCY_FILES = {
    'package.json': 'npm/yarn/pnpm',
    'package-lock.json': 'npm',
    'yarn.lock': 'yarn',
    'pnpm-lock.yaml': 'pnpm',
    'requirements.txt': 'pip',
    'setup.py': 'pip',
    'pyproject.toml': 'pip/pep518',
    'Pipfile': 'pipenv',
    'poetry.lock': 'poetry',
    'go.mod': 'go modules',
    'go.sum': 'go modules',
    'Cargo.toml': 'cargo',
    'Cargo.lock': 'cargo',
    'pom.xml': 'maven',
    'build.gradle': 'gradle',
    'build.gradle.kts': 'gradle',
    'Gemfile': 'bundler',
    'Gemfile.lock': 'bundler',
    'composer.json': 'composer',
}


# Common framework/library detection patterns
FRAMEWORK_PATTERNS = {
    # JavaScript/TypeScript
    'react': ['react', '@types/react'],
    'vue': ['vue', '@vue/*'],
    'angular': ['@angular/*'],
    'svelte': ['svelte'],
    'next.js': ['next'],
    'nuxt': ['nuxt'],
    'gatsby': ['gatsby'],
    'express': ['express'],
    'koa': ['koa'],
    'nest': ['@nestjs/*'],
    'remix': ['@remix-run/*'],
    'astro': ['astro'],
    'solid': ['solid-js'],
    'preact': ['preact'],
    'vite': ['vite'],
    'webpack': ['webpack'],
    'rollup': ['rollup'],
    'esbuild': ['esbuild'],
    'tailwind': ['tailwindcss', '@tailwindcss/*'],
    'bootstrap': ['bootstrap'],
    'material-ui': ['@mui/*', '@material-ui/*'],
    'ant-design': ['antd'],
    'chakra-ui': ['@chakra-ui/*'],

    # Python
    'django': ['django'],
    'flask': ['flask'],
    'fastapi': ['fastapi'],
    'tornado': ['tornado'],
    'pyramid': ['pyramid'],
    'sanic': ['sanic'],
    'aiohttp': ['aiohttp'],
    'celery': ['celery'],
    'sqlalchemy': ['sqlalchemy'],
    'pandas': ['pandas'],
    'numpy': ['numpy'],
    'scikit-learn': ['scikit-learn', 'sklearn'],
    'pytest': ['pytest'],
    'black': ['black'],
    'mypy': ['mypy'],

    # Go
    'gin': ['github.com/gin-gonic/gin'],
    'echo': ['github.com/labstack/echo'],
    'fiber': ['github.com/gofiber/fiber'],
    'gorilla': ['github.com/gorilla/*'],

    # Rust
    'actix': ['actix-web', 'actix-*'],
    'rocket': ['rocket'],
    'tokio': ['tokio'],
    'serde': ['serde'],

    # Java/Kotlin
    'spring': ['org.springframework.*'],
    'spring-boot': ['org.springframework.boot'],
    'hibernate': ['org.hibernate'],
    'junit': ['junit'],
    'mockito': ['org.mockito'],

    # Ruby
    'rails': ['rails'],
    'sinatra': ['sinatra'],
    'rspec': ['rspec'],
    'rubocop': ['rubocop'],

    # PHP
    'laravel': ['laravel/*'],
    'symfony': ['symfony/*'],
    'wordpress': ['wordpress'],
}


# Language detection by file extension
LANGUAGE_EXTENSIONS = {
    'py': 'Python',
    'js': 'JavaScript',
    'jsx': 'JavaScript (React)',
    'ts': 'TypeScript',
    'tsx': 'TypeScript (React)',
    'vue': 'Vue',
    'go': 'Go',
    'rs': 'Rust',
    'java': 'Java',
    'kt': 'Kotlin',
    'kts': 'Kotlin',
    'c': 'C',
    'cpp': 'C++',
    'h': 'C',
    'hpp': 'C++',
    'cs': 'C#',
    'swift': 'Swift',
    'rb': 'Ruby',
    'php': 'PHP',
    'scala': 'Scala',
    'dart': 'Dart',
    'lua': 'Lua',
    'r': 'R',
    'm': 'Objective-C',
    'mm': 'Objective-C++',
    'swift': 'Swift',
    'sql': 'SQL',
    'sh': 'Shell',
    'bash': 'Bash',
    'zsh': 'Zsh',
    'ps1': 'PowerShell',
}


def detect_languages(project_path: Path) -> Dict[str, int]:
    """Detect languages by counting file extensions."""
    language_counts = {}

    for root, dirs, files in os.walk(project_path):
        # Skip common ignore directories
        dirs[:] = [d for d in dirs if d not in {
            'node_modules', '__pycache__', '.git', 'vendor',
            'dist', 'build', '.next', '.nuxt', 'target', 'bin'
        }]

        for file in files:
            ext = Path(file).suffix.lstrip('.').lower()
            if ext in LANGUAGE_EXTENSIONS:
                lang = LANGUAGE_EXTENSIONS[ext]
                language_counts[lang] = language_counts.get(lang, 0) + 1

    return language_counts


def parse_package_json(file_path: Path) -> Dict:
    """Parse package.json and extract dependencies."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        deps = {}
        for key in ['dependencies', 'devDependencies', 'peerDependencies']:
            if key in data:
                deps.update(data[key])

        return deps
    except Exception:
        return {}


def parse_requirements_txt(file_path: Path) -> Dict:
    """Parse requirements.txt and extract packages."""
    deps = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name (before version specifiers)
                    package = re.split(r'[<>=!~\s]', line)[0].lower()
                    if package:
                        deps[package] = line
    except Exception:
        pass
    return deps


def parse_go_mod(file_path: Path) -> Dict:
    """Parse go.mod and extract dependencies."""
    deps = {}
    try:
        with open(file_path, 'r') as f:
            in_require = False
            for line in f:
                line = line.strip()
                if line.startswith('require'):
                    in_require = True
                    continue
                if in_require:
                    if line == ')':
                        break
                    # Parse: package version
                    parts = line.split()
                    if len(parts) >= 2:
                        deps[parts[0]] = parts[1]
    except Exception:
        pass
    return deps


def parse_cargo_toml(file_path: Path) -> Dict:
    """Parse Cargo.toml and extract dependencies."""
    deps = {}
    try:
        with open(file_path, 'r') as f:
            in_deps = False
            for line in f:
                line = line.strip()
                if line.startswith('[dependencies]'):
                    in_deps = True
                    continue
                if in_deps:
                    if line.startswith('['):
                        break
                    # Parse: package = "version"
                    match = re.match(r'^(\w+)\s*=\s*["\']', line)
                    if match:
                        deps[match.group(1)] = line
    except Exception:
        pass
    return deps


def detect_frameworks(dependencies: Dict) -> List[str]:
    """Detect frameworks from dependencies."""
    frameworks = []

    for framework, patterns in FRAMEWORK_PATTERNS.items():
        for pattern in patterns:
            # Pattern can be exact match or wildcard
            if '*' in pattern:
                prefix = pattern.replace('*', '')
                if any(dep.startswith(prefix) for dep in dependencies.keys()):
                    frameworks.append(framework)
                    break
            else:
                if pattern in dependencies:
                    frameworks.append(framework)
                    break

    return sorted(set(frameworks))


def detect_package_manager(project_path: Path) -> str:
    """Detect the package manager in use."""
    for file, manager in DEPENDENCY_FILES.items():
        if (project_path / file).exists():
            return manager
    return 'Unknown'


def analyze_project(project_path: Path) -> Dict:
    """Analyze the project and return tech stack information."""
    result = {
        'package_manager': detect_package_manager(project_path),
        'languages': detect_languages(project_path),
        'dependencies': {},
        'frameworks': [],
        'build_tools': [],
    }

    # Parse dependencies based on package manager
    if (project_path / 'package.json').exists():
        result['dependencies'] = parse_package_json(project_path / 'package.json')
    elif (project_path / 'requirements.txt').exists():
        result['dependencies'] = parse_requirements_txt(project_path / 'requirements.txt')
    elif (project_path / 'go.mod').exists():
        result['dependencies'] = parse_go_mod(project_path / 'go.mod')
    elif (project_path / 'Cargo.toml').exists():
        result['dependencies'] = parse_cargo_toml(project_path / 'Cargo.toml')

    # Detect frameworks
    result['frameworks'] = detect_frameworks(result['dependencies'])

    # Detect build tools
    build_tool_indicators = {
        'webpack': ['webpack', 'webpack-cli'],
        'rollup': ['rollup'],
        'vite': ['vite'],
        'esbuild': ['esbuild'],
        'parcel': ['parcel'],
        'turbopack': ['turbo'],
        'gulp': ['gulp'],
        'grunt': ['grunt'],
        'babel': ['@babel/core', 'babel-core'],
        'typescript': ['typescript'],
        'jest': ['jest'],
        'cypress': ['cypress'],
        'playwright': ['@playwright/test'],
    }

    for tool, patterns in build_tool_indicators.items():
        if any(pattern in result['dependencies'] for pattern in patterns):
            result['build_tools'].append(tool)

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: detect_tech_stack.py [project_path]")
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()

    if not project_path.exists():
        print(f"Error: Path not found: {project_path}")
        sys.exit(1)

    print(f"🔍 Analyzing tech stack: {project_path}\n")

    tech_stack = analyze_project(project_path)

    print("=" * 60)
    print("PACKAGE MANAGER")
    print("=" * 60)
    print(tech_stack['package_manager'])

    print("\n" + "=" * 60)
    print("LANGUAGES")
    print("=" * 60)
    if tech_stack['languages']:
        for lang, count in sorted(tech_stack['languages'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {lang}: {count} files")
    else:
        print("  No code files detected")

    print("\n" + "=" * 60)
    print("FRAMEWORKS")
    print("=" * 60)
    if tech_stack['frameworks']:
        for framework in tech_stack['frameworks']:
            print(f"  • {framework}")
    else:
        print("  No frameworks detected")

    print("\n" + "=" * 60)
    print("BUILD TOOLS")
    print("=" * 60)
    if tech_stack['build_tools']:
        for tool in tech_stack['build_tools']:
            print(f"  • {tool}")
    else:
        print("  No build tools detected")

    print("\n" + "=" * 60)
    print("TOP DEPENDENCIES")
    print("=" * 60)
    # Show top 20 dependencies
    sorted_deps = sorted(tech_stack['dependencies'].items(), key=lambda x: x[0])
    for dep, version in sorted_deps[:20]:
        print(f"  • {dep}: {version}")

    if len(sorted_deps) > 20:
        print(f"  ... and {len(sorted_deps) - 20} more")

    # Save to JSON
    output_file = project_path / '.codebase-tech-stack.json'
    with open(output_file, 'w') as f:
        json.dump(tech_stack, f, indent=2)

    print(f"\n✅ Tech stack saved to: {output_file}")


if __name__ == "__main__":
    main()
