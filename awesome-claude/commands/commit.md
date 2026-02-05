---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*), Bash(git log:*)
description: Create a git commit and push to remote (without Co-authored-by)
---

## Context

- **Current branch**: !`git branch --show-current`
- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.

### Process

1. Run `git add .` to stage all changes (including untracked files)
2. Create commit with appropriate message
3. **Immediately remove Co-authored-by line** (see below)
4. Confirm the branch name and commit result
5. Push to remote repository using `git push origin <branch-name>`
6. Confirm the push result

### Remove Co-authored-by

**CRITICAL**: After creating commit, immediately remove any Co-authored-by line that Cursor may have added:

```bash
# Get commit message without Co-authored-by lines
CLEAN_MSG=$(git log -1 --pretty=%B | grep -v "^Co-authored-by:" | grep -v "^Co-authored-by: Cursor" | grep -v "cursoragent@cursor.com")
# Amend commit with clean message
git commit --amend -m "$CLEAN_MSG" --no-edit
```

**Important**: Always check and remove Co-authored-by lines before confirming commit result.

### Commit message format

Follow **Conventional Commits** specification:

```
<type>: <subject>

<body>
```

### Commit types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries
- **ci**: Changes to CI configuration files and scripts
- **build**: Changes that affect the build system or external dependencies

### Examples

- `feat: add user authentication`
- `fix: resolve memory leak in data processing`
- `style: format code with prettier`
- `chore: update dependencies`
- `docs: update README with installation steps`

### Push behavior

- Push to the current branch's upstream: `git push origin <branch-name>`
- If push fails due to remote changes, inform the user (do not force push automatically)
- Confirm successful push with branch name and commit hash

### Important Notes

- **Never include Co-authored-by**: The commit message must NOT contain any Co-authored-by lines, especially from Cursor
- **Verify before push**: Always verify the commit message is clean before pushing
- If Co-authored-by appears, use `git commit --amend` to remove it immediately
