#!/usr/bin/env python3
"""
Git Commit Helper Script
Automatically generates standardized commit messages based on staged changes.
"""

import subprocess
import sys
import os
from typing import Dict, List, Tuple

class GitCommitHelper:
    def __init__(self):
        self.commit_types = {
            'feat': 'A new feature',
            'fix': 'A bug fix',
            'docs': 'Documentation changes',
            'style': 'Code style changes (formatting, missing semi colons, etc)',
            'refactor': 'Code refactoring',
            'test': 'Adding or modifying tests',
            'chore': 'Maintenance tasks, build process, dependencies'
        }

    def run_git_command(self, command: List[str]) -> Tuple[bool, str]:
        """Execute a git command and return success status and output."""
        try:
            result = subprocess.run(
                ['git'] + command,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, e.stderr.strip()

    def get_staged_changes(self) -> Dict[str, List[str]]:
        """Get detailed information about staged changes."""
        changes = {
            'added': [],
            'modified': [],
            'deleted': [],
            'renamed': []
        }

        # Get staged files status
        success, status_output = self.run_git_command(['status', '--porcelain'])
        if not success:
            return changes

        for line in status_output.split('\n'):
            if not line.strip():
                continue

            status = line[:2].strip()
            filename = line[3:].strip()

            if status == 'A' or status.startswith('A'):
                changes['added'].append(filename)
            elif status == 'M' or status.startswith('M'):
                changes['modified'].append(filename)
            elif status == 'D' or status.startswith('D'):
                changes['deleted'].append(filename)
            elif status == 'R' or status.startswith('R'):
                changes['renamed'].append(filename)

        return changes

    def get_staged_diff(self) -> str:
        """Get the diff of staged changes."""
        success, diff_output = self.run_git_command(['diff', '--staged'])
        if not success:
            return ""
        return diff_output

    def analyze_changes(self, changes: Dict[str, List[str]], diff: str) -> Dict:
        """Analyze staged changes to determine commit type and scope."""
        analysis = {
            'type': 'chore',  # default type
            'scope': None,
            'description': '',
            'details': []
        }

        # Analyze file patterns to determine scope
        scopes = []
        for files in changes.values():
            for file_path in files:
                # Extract directory/scope from file path
                dir_name = os.path.dirname(file_path)
                if dir_name and dir_name != '.':
                    # Take the first meaningful directory as scope
                    scope_candidate = dir_name.split('/')[0]
                    if scope_candidate not in ['src', 'lib', 'test', 'tests', 'docs']:
                        scopes.append(scope_candidate)

        # Determine scope (most common or specific)
        if scopes:
            # Get most frequent scope
            analysis['scope'] = max(set(scopes), key=scopes.count)

        # Determine type based on file patterns and diff content
        all_files = (changes['added'] + changes['modified'] +
                    changes['deleted'] + changes['renamed'])

        # Check for test files
        if any('test' in f.lower() or 'spec' in f.lower() for f in all_files):
            analysis['type'] = 'test'

        # Check for documentation files
        elif any(f.endswith(('.md', '.rst', '.txt')) or 'doc' in f.lower() for f in all_files):
            analysis['type'] = 'docs'

        # Check for feature additions (new files with meaningful content)
        elif changes['added'] and len(diff) > 100:  # Substantial new code
            analysis['type'] = 'feat'

        # Check for bug fixes (error handling, null checks, etc)
        elif ('fix' in diff.lower() or 'error' in diff.lower() or
              'null' in diff.lower() or 'exception' in diff.lower()):
            analysis['type'] = 'fix'

        # Check for refactoring (structural changes without new features)
        elif ('refactor' in diff.lower() or 'cleanup' in diff.lower() or
              'reorganize' in diff.lower()):
            analysis['type'] = 'refactor'

        # Generate description based on changes
        if changes['added']:
            analysis['details'].append(f"Add {len(changes['added'])} new file(s)")
        if changes['modified']:
            analysis['details'].append(f"Modify {len(changes['modified'])} file(s)")
        if changes['deleted']:
            analysis['details'].append(f"Delete {len(changes['deleted'])} file(s)")

        return analysis

    def generate_commit_message(self, analysis: Dict) -> str:
        """Generate a standardized commit message."""
        type_desc = self.commit_types.get(analysis['type'], 'Maintenance tasks')

        # Build the main message line
        if analysis['scope']:
            main_line = f"{analysis['type']}({analysis['scope']}): {type_desc.lower()}"
        else:
            main_line = f"{analysis['type']}: {type_desc.lower()}"

        # Build the body with details
        message_lines = [main_line, ""]  # Empty line after subject

        if analysis['details']:
            message_lines.extend([f"- {detail}" for detail in analysis['details']])

        return '\n'.join(message_lines)

    def create_commit(self, message: str) -> bool:
        """Create a git commit with the given message."""
        # Use heredoc format for proper message handling
        success, output = self.run_git_command([
            'commit', '-m', message
        ])

        if success:
            print(f"✓ Commit created successfully")
            print(f"Commit message:\n{message}")
        else:
            print(f"✗ Failed to create commit: {output}")

        return success

def main():
    """Main function to execute the git commit workflow."""
    helper = GitCommitHelper()

    # Check if we're in a git repository
    success, _ = helper.run_git_command(['rev-parse', '--git-dir'])
    if not success:
        print("Error: Not a git repository")
        sys.exit(1)

    # Check for staged changes
    changes = helper.get_staged_changes()
    total_changes = sum(len(files) for files in changes.values())

    if total_changes == 0:
        print("No staged changes found. Please stage some files first.")
        print("You can stage files using: git add <files>")
        sys.exit(1)

    print(f"Found {total_changes} staged changes:")
    for category, files in changes.items():
        if files:
            print(f"  {category}: {len(files)} files")

    # Analyze changes and generate commit message
    diff = helper.get_staged_diff()
    analysis = helper.analyze_changes(changes, diff)
    commit_message = helper.generate_commit_message(analysis)

    print("\nGenerated commit message:")
    print("-" * 50)
    print(commit_message)
    print("-" * 50)

    # Create commit directly
    success = helper.create_commit(commit_message)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()