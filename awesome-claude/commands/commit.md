---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
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
3. Confirm the branch name and commit result

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
