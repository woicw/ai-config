---
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*), ReadFile, CodebaseSearch, Grep
description: Perform comprehensive code review using code-review skill
---

# Code Review Command

## Context

- Current git status: !`git status`
- Changed files: !`git diff --name-only`
- Git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Use the **code-review** skill to perform a comprehensive code review of the changes above.

### Review process

1. **Gather context**: Understand what changed and why
2. **Security audit**: Check for vulnerabilities (injection, auth, sensitive data)
3. **Style check**: Verify naming, formatting, documentation
4. **Performance review**: Identify N+1 queries, memory issues, inefficient algorithms
5. **Best practices**: Check error handling, logging, testing, DRY principle
6. **Generate report**: Summarize findings by severity (CRITICAL, HIGH, MEDIUM, LOW, INFO)

### Output format

Provide a structured review report with:

- **Critical issues** (must fix)
- **High priority** (should fix before merge)
- **Medium priority** (consider fixing)
- **Low priority** (nice to have)
- **Info** (positive observations)

For each issue, include:

- File path and line number
- Issue description
- Suggested fix or improvement
