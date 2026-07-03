---
name: sync-remote-skills
description: Sync remote-managed skills in awesome-claude from the manifest, and audit skillIds against upstream before syncing. Use when updating skills to their latest upstream versions, when `wrs sync` fails with "No matching skills found", or when checking manifest health.
---

# Sync Remote Skills

Use the manifest at `awesome-claude/skills.manifest.json` as the source of truth. Syncing is done by the `wrs` CLI (wr-ai, requires >= 4.2.0), which clones `woicw/ai-config` **from GitHub** — manifest fixes must be committed and pushed before they take effect.

## Commands

### Audit manifest health (run this first when sync fails)

```bash
node awesome-claude/scripts/audit-skills.mjs
```

Verifies, for every remote entry, that the source repo exists / isn't renamed, and that `skillId` matches a SKILL.md frontmatter `name` upstream. Verifies local entries have a directory under `awesome-claude/skills/`. Exits non-zero on problems with a suggested fix per finding.

### Sync all selected skills globally

```bash
wrs sync -g
```

### Force re-fetch from upstream (ignore cache)

```bash
wrs sync -g --refresh
```

## How it works (debugging knowledge)

- `wrs` runs `npx skills add <repo> --skill <skillId>` per remote entry. The `skills` CLI matches `--skill` against the SKILL.md **frontmatter `name`**, not the directory name. When upstream renames the frontmatter, sync fails with "No matching skills found" — fix `skillId` in the manifest.
- The CLI sanitizes special characters in output directory names (e.g. `stitch::react-components` → `stitch-react-components`). wr-ai >= 4.2.0 handles this; 4.1.0 does not (`npm i -g wr-ai@latest` to fix).
- Cache lives at `~/.wrs/cache/skills/<name>`. Sync without `--refresh` skips cached entries, so re-running after a failure resumes where it stopped.
- The skill selection is stored in `~/.wrs/config.json` (`lastSelection.skills`). Names missing from the manifest are silently skipped.
- `curl 18 / early EOF` while cloning large repos (e.g. `github/awesome-copilot`) is transient network failure — just re-run.

## Rules

- Do not add local-only skills to the remote sync path.
- Update `skillId`/`source` mappings in `skills.manifest.json` before syncing; run the audit script to find the correct values.
- Keep `installName` aligned with the directory name in `awesome-claude/skills/` when the upstream skill name differs from the desired install name.
- Commit and push manifest changes before re-running `wrs sync` — it reads the manifest from GitHub, not the local checkout.
