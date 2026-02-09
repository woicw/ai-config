---
allowed-tools: Bash(wr-server:*), Bash(which:*), Bash(test:*), Bash(node:*), Bash(printenv:*)
description: Deploy frontend project to remote server via wr-server-cli
---

## Context

- **wr-server-cli installed**: !`which wr-server 2>/dev/null && echo "✅" || echo "❌ not installed"`
- **Config file**: !`test -f deploy.config.mjs && echo "✅ deploy.config.mjs" || echo "❌ not found"`
- **Environments**: !`node -e "import('./deploy.config.mjs').then(m=>{const c=m.default;Object.keys(c).filter(k=>!['projectName','readyTimeout'].includes(k)).forEach(k=>console.log(k+': '+c[k].name+' ('+c[k].host+')'))}).catch(()=>{})" 2>/dev/null`

## Pre-flight Checks

Run all checks. If any fails, STOP and show the fix:

1. `which wr-server` — if missing, prompt `npm install -g wr-server-cli`
2. `test -f deploy.config.mjs` — if missing, prompt to create the config file
3. `printenv WR_SERVER_CODE_<ENV>` — if unset, prompt `export WR_SERVER_CODE_<ENV>=password`

## Deploy

All checks pass → directly execute:

```bash
# Full deploy
wr-server deploy -m <env> --auto

```

If user did not specify environment, list available environments and ask.
