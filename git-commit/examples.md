# Git Commit Skill - Usage Examples

## Basic Usage

When you have staged changes in your git repository, Claude will automatically use this skill to generate a standardized commit message and commit the changes.

## Example Scenarios

### 1. Adding New Features

**Situation**: You've added a new authentication module

**Staged files**:
- `src/auth/register.js`
- `src/auth/login.js`
- `tests/auth.test.js`

**Generated commit message**:
```
feat(auth): a new feature

- Add 3 new file(s)
```

### 2. Fixing Bugs

**Situation**: You've fixed a null pointer exception in the API

**Staged files**:
- `src/api/userService.js`
- `tests/api/userService.test.js`

**Generated commit message**:
```
fix(api): a bug fix

- Modify 2 file(s)
```

### 3. Documentation Updates

**Situation**: You've updated the README and added API documentation

**Staged files**:
- `README.md`
- `docs/api.md`

**Generated commit message**:
```
docs: documentation changes

- Modify 2 file(s)
```

### 4. Code Refactoring

**Situation**: You've restructured the project layout

**Staged files**:
- `src/components/Button.js` → `src/ui/Button.js`
- `src/components/Input.js` → `src/ui/Input.js`

**Generated commit message**:
```
refactor(ui): code refactoring

- Rename 2 file(s)
```

## Manual Execution

You can also run the helper script manually:

```bash
python scripts/commit_helper.py
```

## Integration with Claude Code

When Claude detects that you have staged changes and need to create a commit, it will:

1. Automatically analyze the staged changes
2. Generate an appropriate commit message
3. Ask for confirmation before committing
4. Execute the git commit command

This ensures consistent, professional commit messages across your project.