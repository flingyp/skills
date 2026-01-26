---
name: git-commit
description: Generate standardized commit messages and commit staged changes to the local repository. Use when you need to create professional git commits with conventional commit format.
---

# Git Commit Standardizer

## Instructions

When invoked, this skill will:

1. **Check git status**: Verify there are staged changes ready for commit
2. **Analyze staged changes**: Review the git diff to understand what changes are being committed
3. **Generate standardized commit message**: Create a commit message following conventional commit format
   - **Format**: `<type>(<scope>): <description>`
   - **Types**: feat, fix, docs, style, refactor, test, chore
   - **Description**: Use imperative mood, concise and clear
   - **Requirements**: Both `type` and `scope` are **required** for all commits
4. **Commit the changes**: Execute the git commit with the generated message

## Conventional Commit Format

The generated commit messages follow this format:

```
type(scope): description

[optional body]

[optional footer(s)]
```

**Important**: Both `type` and `scope` are **required** and must be present in every commit message.

**Common types:**

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semi colons, etc)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks, build process, dependencies

## Requirements

- Git must be installed and configured
- User must have a git repository initialized
- There must be staged changes ready to commit
- scope is required for all commits

## Examples

### Example 1: Feature Addition

```
feat(auth): add user registration functionality

- Implement user registration API endpoint
- Add password hashing and validation
- Create user registration form component
```

### Example 2: Bug Fix

```
fixed(api): fix null pointer exception in user service

- Add null checks for user object
- Handle user not found scenarios gracefully
- Add test cases for edge conditions
```

### Example 3: Documentation Update

```
docs(readme): update installation instructions

- Add npm installation steps
- Include environment setup guide
- Update troubleshooting section
```
