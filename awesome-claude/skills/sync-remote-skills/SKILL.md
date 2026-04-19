---
name: sync-remote-skills
description: Sync remote-managed skills in awesome-claude from a local manifest file. Use when updating skills to their latest upstream versions, checking which skills are unresolved, or refreshing a single managed skill without touching local-only skills.
---

# Sync Remote Skills

Use the manifest at `awesome-claude/skills.manifest.json` as the source of truth.

## When to Use

- Refresh all remote-managed skills to the latest upstream version
- Update one specific remote-managed skill
- Check which skills are unresolved and still need source mapping
- Verify that installed skills match the manifest

## Commands

### List all managed skills

```bash
python3 awesome-claude/scripts/sync_skills_from_manifest.py list
```

### Check manifest health

```bash
python3 awesome-claude/scripts/sync_skills_from_manifest.py check
```

### Sync every resolved remote skill

```bash
python3 awesome-claude/scripts/sync_skills_from_manifest.py sync
```

### Sync only one skill

```bash
python3 awesome-claude/scripts/sync_skills_from_manifest.py sync zustand
```

### Update only skills that already exist locally

```bash
python3 awesome-claude/scripts/sync_skills_from_manifest.py sync --update-existing-only
```

## Rules

- Do not add local-only skills to the remote sync path.
- Add or update upstream mappings in `skills.manifest.json` before syncing.
- If a skill is marked unresolved, do not guess a repo or path during sync; resolve the mapping first.
- Keep `install_name` aligned with the directory name in `awesome-claude/skills/` when the upstream path basename differs.
