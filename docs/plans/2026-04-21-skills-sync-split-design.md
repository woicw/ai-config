# Skills Sync Split — Design

**Date:** 2026-04-21
**Status:** Approved (design phase)
**Scope:** `ai-config` + `wr-ai` (`wrs`) joint refactor

## Problem

`ai-config/awesome-claude/skills/` currently vendors **both** 7 hand-written local skills and 28 remote skills (pulled from various upstream repos via `scripts/sync_skills_from_manifest.py`). The remote copies are committed to git. Consequences:

- Noisy diffs whenever any upstream skill changes
- `ai-config` repo grows with material it doesn't own
- Two sources of drift: manifest vs. vendored directory
- Consumer (`wrs`) treats local and remote as an undifferentiated flat pool, hiding provenance

## Goal

Split responsibilities cleanly:

- `ai-config` maintains only what it authors (local skills) and declares what it recommends (manifest)
- `wrs` (the consumer CLI) materializes remote skills on demand using `npx skills add`, caches them per user, and merges both categories into the user's workspace at `wrs sync` time

## Scope Boundaries

| | `ai-config` | `wr-ai` (`wrs`) |
|---|---|---|
| Core asset | `skills.manifest.json` + `awesome-claude/skills/<local>/` (7 dirs only) | CLI tool |
| Responsibility | Declares the recommended skill set; hosts local skill sources | Reads manifest → classifies by source → materializes remote skills via `npx skills add` → distributes to user workspace |
| Removed | `scripts/sync_skills_from_manifest.py`, `skills-lock.json`, all 28 vendored remote skill directories | — |
| Added | — | Manifest-aware loader, `npx skills add` orchestration, per-user cache, `--refresh` flag, `wrs cache clean` subcommand |

## Architecture

### Directory layout on user machine

```text
~/.wrs/
├── config.json
├── templates/
│   └── woicw_ai-config/                 # ai-config clone (existing)
│       └── awesome-claude/
│           ├── skills.manifest.json     # wrs reads this as source of truth
│           └── skills/<local>/          # local skills live here
└── cache/
    ├── stage/                           # scratch project for `npx skills add`
    │   └── .claude/skills/<id>/         # npx drops output here, then moved out
    └── skills/
        └── <remote-id>/                 # materialized remote skills (cache)
```

### `wrs sync` data flow

1. `git clone/pull` ai-config → `~/.wrs/templates/woicw_ai-config/` (existing `cloneOrUpdateRepo`)
2. Load `awesome-claude/skills.manifest.json`; partition entries by `source`
3. For each selected entry:
   - `source: "local"` → resolve source path inside the cloned ai-config
   - otherwise (remote `owner/repo`) → check `~/.wrs/cache/skills/<id>/`; if missing or `--refresh`, run `npx skills add <repo_url> --skill <id> --agent claude-code --copy -y` with `cwd=~/.wrs/cache/stage/`, then move the resulting `.claude/skills/<id>/` to `~/.wrs/cache/skills/<id>/` and clean stage
4. Feed the resolved source directory to `syncSkillDirectory()`, which copies into the target workspace (`./.claude/skills/<id>/` or `~/.claude/skills/<id>/`). Multi-target + agent-dir-detection logic is shared across both categories.

### Cache refresh strategy

| Invocation | Behavior |
|---|---|
| `wrs sync` | ai-config: `git pull`. Remote: **use cache if present**, else materialize via `npx`. |
| `wrs sync --refresh` | ai-config: `git pull`. Remote: **purge all of `cache/skills/`**, re-materialize everything. |
| `wrs sync --refresh <name>` | Refresh only the named skill's cache entry. |
| `wrs cache clean` | `rm -rf ~/.wrs/cache/` (manual escape hatch). |

### `wrs list` output

Change from "scan `skills/` directory" to "parse manifest, group by source":

```text
📦 ai-config

Local (7)
  ├─ ahooks
  ├─ antd
  └─ …

Remote (28)
  ├─ vite            ← antfu/skills
  ├─ vue             ← antfu/skills
  ├─ shadcn          ← shadcn/ui
  └─ …
```

### `wrs add <name>`

Looks up the entry by name in the manifest and takes the corresponding branch (local copy vs. npx-materialize-then-copy). Transparent to the user; no new flags.

### Last-selection compatibility

`lastSelection.skills` remains a string array (skill names). Manifest changes preserve name-level identity, so existing history records continue to work. Missing names fall back to interactive selection, as today.

## Implementation Phases

### Phase 1 — `wr-ai` gains manifest-aware sync (additive)

Goal: `wrs` can consume the manifest and route per-source even while `ai-config` still vendors the old directories. No destructive change to `ai-config` yet.

| File | Change |
|---|---|
| `src/utils/constants.js` | Add `CACHE_DIR`, `CACHE_SKILLS_DIR`, `CACHE_STAGE_DIR`, `MANIFEST_REL_PATH = "awesome-claude/skills.manifest.json"` |
| `src/lib/manifest.js` (**new**) | `loadManifest(sourcePath)`, `filterByName(entries, names)`, `classifyBySource(entries)` — port SkillSpec semantics from the Python script |
| `src/lib/installer.js` (**new**) | `ensureRemoteInCache(entry, { refresh })` runs `npx skills add <url> --skill <id> --agent claude-code --copy -y` with `cwd=~/.wrs/cache/stage/`, moves output to `~/.wrs/cache/skills/<id>/`, clears stage. `resolveSkillSource(entry)` returns the source path (local → ai-config clone path; remote → cache path). |
| `src/utils/parser.js` | `readSkillList` returns manifest entries (with `source`), not directory scan |
| `src/commands/list.js` | Group output by Local / Remote, show upstream for remote |
| `src/commands/sync.js` | Use entries (not bare names); call `resolveSkillSource` per entry; accept `--refresh` |
| `src/commands/add.js` | Resolve via manifest entry; dispatch local vs. remote |
| `src/commands/cache.js` (**new**) | `wrs cache clean` subcommand |
| `src/index.js` | Register `--refresh`, `cache` subcommand |
| `tests/**` | Unit tests (manifest parse, cache hit/miss, stage cleanup); integration test with a fixture manifest |

**Validation:** With `ai-config` untouched, `wrs sync --refresh` must produce the same on-disk skill set in the target workspace as the pre-refactor behavior. Regression is green before moving on.

### Phase 2 — `ai-config` slims down (destructive)

| Action | Detail |
|---|---|
| `git rm -r awesome-claude/skills/<28 remote names>/` | Keep only the 7 local skills + manifest |
| `rm awesome-claude/scripts/sync_skills_from_manifest.py` | Obsolete |
| `rm -r awesome-claude/tests/` | If it only covered the removed script |
| `rm skills-lock.json` | Cache replaces it |
| `package.json` scripts | Drop `skills:add` / `skills:sync` / `skills:sync:existing`; keep `skills:list` / `skills:check` only if they validate manifest semantics |
| `README.md` | Rewrite the "Sync Commands" section — point users at `wrs` |

**Validation:** After slimming, a fresh run (`rm -rf ~/.wrs/templates ~/.wrs/cache && wrs sync`) should yield a workspace skill set equivalent to the pre-refactor one.

### Phase 3 — polish (deferrable)

- Release new `wrs` version (e.g. 4.1.0); update README
- Short note in `ai-config` README pointing at `wrs`
- Friendly error surfaces when manifest is missing or malformed

## Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| `npx skills add` fails for one upstream (repo gone, renamed, offline) | One remote skill fails to sync | Per-skill `try/catch`; warn-and-continue; allow manifest `deprecated: true` to opt out |
| Users lack `node`/`npx` | First run fails | Preflight `which npx`; surface actionable message (port Python's `discover_npx`) |
| Stage directory reuse under concurrency or orphan state | Corrupt output | File lock at `~/.wrs/cache/.lock`; clean stage before every ensure |
| Cache pollution if `npx` output shape changes | Bad content in cache | `--refresh` wipes; persist `.wrs-meta.json` (upstream sha, timestamp) for health checks |
| Old `wrs` versions after Phase 2 ship | Users on stale CLI get a truncated skill set (missing the 28 remotes) | Release Phase 1 at least a week before Phase 2; bump manifest `version` to 3 so old CLIs can surface an "upgrade required" notice |
| Manifest format evolution | Forward-compat breakage | Dispatch on `version` inside the loader |

## Deferred (not in this refactor)

Manifest v3 optional fields for future-proofing reproducible sync:

- `deprecated: true`
- `ref: "v1.2.0"` — pin upstream tag/commit
- `hash` — content checksum

Reserve the `version` field now; don't wire these in yet.

## Success Criteria

- `ai-config/awesome-claude/skills/` contains only hand-authored skills
- `skills.manifest.json` is the single source of truth for the recommended set
- `wrs sync` produces the same final workspace layout as today, with local and remote materialization diverging internally
- `wrs sync --refresh` can pull the freshest upstream state without touching `ai-config`
- Cache survives normal usage; `wrs cache clean` recovers from any corrupt state
