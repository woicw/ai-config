# Skills Sync Split — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Move remote skill materialization out of `ai-config` into `wr-ai` (`wrs`), so `ai-config` only vendors hand-authored local skills while `wrs` resolves `skills.manifest.json` at sync time — local skills from the ai-config clone, remote skills from `npx skills add` with a per-user cache.

**Architecture:** `wrs sync` reads `awesome-claude/skills.manifest.json` from the cloned ai-config repo (still at `~/.wrs/templates/woicw_ai-config/`), classifies each entry by `source`, and resolves the source path: `local` → inside the clone; remote → `~/.wrs/cache/skills/<id>/` (materialized via `npx skills add` with `cwd=~/.wrs/cache/stage/`). Both paths feed the existing `syncSkillDirectory` copy logic, keeping target distribution unchanged.

**Tech Stack:** Node.js ESM (`"type": "module"`), `commander`, `@inquirer/prompts`, `ora`, `yoctocolors`. Tests via Node built-in test runner (`node --test tests/**/*.test.js`). External: `npx skills add` (Anthropic CLI).

**Reference:** Design doc — [`docs/plans/2026-04-21-skills-sync-split-design.md`](./2026-04-21-skills-sync-split-design.md)

**Working directories:**
- Phase 1 runs in `/Users/woic/woicw/wr-ai/`
- Phase 2 runs in `/Users/woic/woicw/ai-config/`
- Phase 3 spans both

---

## Phase 1 — `wr-ai` manifest-aware sync (additive)

**Preconditions:** `cd /Users/woic/woicw/wr-ai`. `ai-config` is left untouched; after Phase 1, both old (vendored) and new (manifest) paths must coexist.

### Task 1.1: Add cache & manifest constants

**Files:**
- Modify: `src/utils/constants.js`

**Step 1: Open the file** — it currently exports `EXCLUDE_LIST`, `DEFAULT_SOURCE`, `MAX_DISPLAY_ITEMS`, `TEMPLATES_DIR`.

**Step 2: Append new exports**

```javascript
export const CACHE_DIR = path.join(os.homedir(), '.wrs', 'cache');
export const CACHE_SKILLS_DIR = path.join(CACHE_DIR, 'skills');
export const CACHE_STAGE_DIR = path.join(CACHE_DIR, 'stage');
export const MANIFEST_REL_PATH = path.join('awesome-claude', 'skills.manifest.json');
```

**Step 3: Smoke-check** — `node -e "import('./src/utils/constants.js').then(m => console.log(m.CACHE_SKILLS_DIR))"` → prints `/Users/<you>/.wrs/cache/skills`.

**Step 4: Commit**

```bash
git add src/utils/constants.js
git commit -m "feat(wrs): add cache and manifest path constants"
```

---

### Task 1.2: Write failing test for manifest loader

**Files:**
- Create: `tests/lib/manifest.test.js`

**Step 1: Write the test**

```javascript
import { test } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { loadManifest, classifyBySource } from '../../src/lib/manifest.js';

function writeManifest(root, payload) {
  const file = path.join(root, 'awesome-claude', 'skills.manifest.json');
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(payload));
  return root;
}

function tmp(prefix) {
  return fs.mkdtempSync(path.join(os.tmpdir(), prefix));
}

test('loadManifest - parses local and remote entries', () => {
  const root = writeManifest(tmp('wrs-manifest-'), {
    version: 2,
    skills: [
      { name: 'woic', source: 'local' },
      { name: 'vite', source: 'antfu/skills', skillId: 'vite' },
      { name: 'skill-creator-anthropics', source: 'anthropics/skills', skillId: 'skill-creator', installName: 'skill-creator-anthropics' },
    ],
  });
  try {
    const entries = loadManifest(root);
    assert.strictEqual(entries.length, 3);
    assert.strictEqual(entries[0].source, 'local');
    assert.strictEqual(entries[1].repoUrl, 'https://github.com/antfu/skills');
    assert.strictEqual(entries[2].installName, 'skill-creator-anthropics');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('classifyBySource - splits local vs remote', () => {
  const entries = [
    { name: 'a', source: 'local' },
    { name: 'b', source: 'x/y', skillId: 'b' },
  ];
  const { local, remote } = classifyBySource(entries);
  assert.deepStrictEqual(local.map((e) => e.name), ['a']);
  assert.deepStrictEqual(remote.map((e) => e.name), ['b']);
});

test('loadManifest - throws on malformed source', () => {
  const root = writeManifest(tmp('wrs-manifest-bad-'), {
    version: 2,
    skills: [{ name: 'oops', source: 'not-a-repo' }],
  });
  try {
    assert.throws(() => loadManifest(root), /invalid source/);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
```

**Step 2: Run to confirm failure**

```bash
node --test tests/lib/manifest.test.js
```

Expected: FAIL with `Cannot find module '.../src/lib/manifest.js'`.

---

### Task 1.3: Implement manifest loader

**Files:**
- Create: `src/lib/manifest.js`

**Step 1: Implementation**

```javascript
import fs from 'node:fs';
import path from 'node:path';
import { MANIFEST_REL_PATH } from '../utils/constants.js';

function parseEntry(raw) {
  if (!raw || typeof raw !== 'object') {
    throw new Error('each manifest skill entry must be an object');
  }
  const { name, source } = raw;
  if (typeof name !== 'string' || name.length === 0) {
    throw new Error('each skill entry requires a non-empty string name');
  }
  if (source !== 'local' && (typeof source !== 'string' || !source.includes('/'))) {
    throw new Error(`skill '${name}' has invalid source: ${JSON.stringify(source)}`);
  }
  return {
    name,
    source,
    skillId: raw.skillId ?? null,
    installName: raw.installName ?? null,
    agent: raw.agent ?? null,
    isLocal: source === 'local',
    repoUrl: source === 'local' ? null : `https://github.com/${source}`,
  };
}

export function loadManifest(sourcePath) {
  const file = path.join(sourcePath, MANIFEST_REL_PATH);
  const data = JSON.parse(fs.readFileSync(file, 'utf-8'));
  if (!Array.isArray(data.skills)) {
    throw new Error('manifest must contain a top-level skills array');
  }
  return data.skills.map(parseEntry);
}

export function classifyBySource(entries) {
  const local = [];
  const remote = [];
  for (const entry of entries) {
    (entry.isLocal ? local : remote).push(entry);
  }
  return { local, remote };
}

export function filterByName(entries, names) {
  if (!names || names.length === 0) return entries;
  const set = new Set(names);
  return entries.filter((entry) => set.has(entry.name));
}

export function getTargetName(entry) {
  return entry.installName ?? entry.name;
}
```

**Step 2: Run tests**

```bash
node --test tests/lib/manifest.test.js
```

Expected: 3 pass.

**Step 3: Commit**

```bash
git add src/lib/manifest.js tests/lib/manifest.test.js
git commit -m "feat(wrs): add manifest loader with source classification"
```

---

### Task 1.4: Write failing test for cache layout helper

**Files:**
- Create: `tests/lib/installer.test.js`

**Step 1: Write the test**

```javascript
import { test } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { resolveSkillSource } from '../../src/lib/installer.js';

function scratch(prefix) {
  return fs.mkdtempSync(path.join(os.tmpdir(), prefix));
}

test('resolveSkillSource - returns local clone path for local entries', () => {
  const cloneRoot = scratch('wrs-clone-');
  const skillDir = path.join(cloneRoot, 'awesome-claude', 'skills', 'woic');
  fs.mkdirSync(skillDir, { recursive: true });
  fs.writeFileSync(path.join(skillDir, 'SKILL.md'), '# woic');
  try {
    const resolved = resolveSkillSource({ isLocal: true, name: 'woic' }, { cloneRoot, cacheDir: '/unused' });
    assert.strictEqual(resolved, skillDir);
  } finally {
    fs.rmSync(cloneRoot, { recursive: true, force: true });
  }
});

test('resolveSkillSource - returns cache path for remote entries', () => {
  const cacheDir = scratch('wrs-cache-');
  const entry = { isLocal: false, name: 'vite', skillId: 'vite', installName: null };
  const resolved = resolveSkillSource(entry, { cloneRoot: '/unused', cacheDir });
  assert.strictEqual(resolved, path.join(cacheDir, 'skills', 'vite'));
});

test('resolveSkillSource - honors installName for remote entries', () => {
  const cacheDir = scratch('wrs-cache-');
  const entry = { isLocal: false, name: 'skill-creator-anthropics', skillId: 'skill-creator', installName: 'skill-creator-anthropics' };
  const resolved = resolveSkillSource(entry, { cloneRoot: '/unused', cacheDir });
  assert.strictEqual(resolved, path.join(cacheDir, 'skills', 'skill-creator-anthropics'));
});
```

**Step 2: Run**

```bash
node --test tests/lib/installer.test.js
```

Expected: FAIL with `Cannot find module '.../src/lib/installer.js'`.

---

### Task 1.5: Implement `resolveSkillSource` (pure)

**Files:**
- Create: `src/lib/installer.js`

**Step 1: Minimal implementation (pure function first, remote materialization comes next)**

```javascript
import fs from 'node:fs';
import path from 'node:path';
import { CACHE_SKILLS_DIR } from '../utils/constants.js';

export function resolveSkillSource(entry, { cloneRoot, cacheDir }) {
  if (entry.isLocal) {
    return path.join(cloneRoot, 'awesome-claude', 'skills', entry.name);
  }
  const targetName = entry.installName ?? entry.name;
  return path.join(cacheDir, 'skills', targetName);
}

export function defaultCacheDir() {
  return path.dirname(CACHE_SKILLS_DIR);
}

export function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}
```

**Step 2: Run tests**

```bash
node --test tests/lib/installer.test.js
```

Expected: 3 pass.

**Step 3: Commit**

```bash
git add src/lib/installer.js tests/lib/installer.test.js
git commit -m "feat(wrs): add resolveSkillSource for local/remote dispatch"
```

---

### Task 1.6: Write failing test for `ensureRemoteInCache`

**Files:**
- Modify: `tests/lib/installer.test.js` (append cases)

**Step 1: Append**

```javascript
import { ensureRemoteInCache } from '../../src/lib/installer.js';

test('ensureRemoteInCache - skips npx when cache already populated', async () => {
  const cacheDir = scratch('wrs-cache-hit-');
  const existing = path.join(cacheDir, 'skills', 'vite');
  fs.mkdirSync(existing, { recursive: true });
  fs.writeFileSync(path.join(existing, 'SKILL.md'), '# vite');
  let called = false;
  await ensureRemoteInCache(
    { isLocal: false, name: 'vite', skillId: 'vite', repoUrl: 'https://github.com/antfu/skills' },
    { cacheDir, refresh: false, runNpxSkillsAdd: async () => { called = true; } }
  );
  assert.strictEqual(called, false);
  assert.strictEqual(fs.existsSync(path.join(existing, 'SKILL.md')), true);
});

test('ensureRemoteInCache - invokes npx when cache missing', async () => {
  const cacheDir = scratch('wrs-cache-miss-');
  const calls = [];
  await ensureRemoteInCache(
    { isLocal: false, name: 'vite', skillId: 'vite', repoUrl: 'https://github.com/antfu/skills' },
    {
      cacheDir,
      refresh: false,
      runNpxSkillsAdd: async ({ stageDir, skillId, repoUrl }) => {
        calls.push({ stageDir, skillId, repoUrl });
        // Simulate npx output landing under stage/.claude/skills/<id>/
        const fake = path.join(stageDir, '.claude', 'skills', skillId);
        fs.mkdirSync(fake, { recursive: true });
        fs.writeFileSync(path.join(fake, 'SKILL.md'), '# vite upstream');
      },
    }
  );
  assert.strictEqual(calls.length, 1);
  assert.strictEqual(calls[0].repoUrl, 'https://github.com/antfu/skills');
  assert.strictEqual(
    fs.readFileSync(path.join(cacheDir, 'skills', 'vite', 'SKILL.md'), 'utf-8'),
    '# vite upstream'
  );
});

test('ensureRemoteInCache - refresh=true rebuilds even when cache present', async () => {
  const cacheDir = scratch('wrs-cache-refresh-');
  const existing = path.join(cacheDir, 'skills', 'vite');
  fs.mkdirSync(existing, { recursive: true });
  fs.writeFileSync(path.join(existing, 'SKILL.md'), '# stale');
  await ensureRemoteInCache(
    { isLocal: false, name: 'vite', skillId: 'vite', repoUrl: 'https://github.com/antfu/skills' },
    {
      cacheDir,
      refresh: true,
      runNpxSkillsAdd: async ({ stageDir, skillId }) => {
        const fake = path.join(stageDir, '.claude', 'skills', skillId);
        fs.mkdirSync(fake, { recursive: true });
        fs.writeFileSync(path.join(fake, 'SKILL.md'), '# fresh');
      },
    }
  );
  assert.strictEqual(
    fs.readFileSync(path.join(cacheDir, 'skills', 'vite', 'SKILL.md'), 'utf-8'),
    '# fresh'
  );
});
```

**Step 2: Run**

```bash
node --test tests/lib/installer.test.js
```

Expected: FAIL with `ensureRemoteInCache is not a function`.

---

### Task 1.7: Implement `ensureRemoteInCache`

**Files:**
- Modify: `src/lib/installer.js`

**Step 1: Add the function (inject `runNpxSkillsAdd` for testability)**

```javascript
import { spawn } from 'node:child_process';

async function defaultRunNpxSkillsAdd({ stageDir, repoUrl, skillId, agent = 'claude-code' }) {
  await new Promise((resolve, reject) => {
    const child = spawn(
      'npx',
      ['skills', 'add', repoUrl, '--skill', skillId, '--agent', agent, '--copy', '-y'],
      { cwd: stageDir, stdio: 'inherit' }
    );
    child.on('error', reject);
    child.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(`npx skills add failed with exit code ${code}`));
    });
  });
}

export async function ensureRemoteInCache(entry, options) {
  const {
    cacheDir,
    refresh = false,
    runNpxSkillsAdd = defaultRunNpxSkillsAdd,
    agent = 'claude-code',
  } = options;

  const targetName = entry.installName ?? entry.name;
  const cachePath = path.join(cacheDir, 'skills', targetName);
  const stageDir = path.join(cacheDir, 'stage');

  if (fs.existsSync(cachePath) && !refresh) return cachePath;
  if (fs.existsSync(cachePath)) fs.rmSync(cachePath, { recursive: true, force: true });

  // Scrub stage before use to avoid cross-skill leftovers
  fs.rmSync(stageDir, { recursive: true, force: true });
  fs.mkdirSync(stageDir, { recursive: true });

  await runNpxSkillsAdd({ stageDir, repoUrl: entry.repoUrl, skillId: entry.skillId, agent });

  const produced = path.join(stageDir, '.claude', 'skills', entry.skillId);
  if (!fs.existsSync(produced)) {
    throw new Error(`npx skills add did not produce expected dir: ${produced}`);
  }

  fs.mkdirSync(path.dirname(cachePath), { recursive: true });
  fs.renameSync(produced, cachePath);
  fs.rmSync(stageDir, { recursive: true, force: true });

  return cachePath;
}
```

**Step 2: Run tests**

```bash
node --test tests/lib/installer.test.js
```

Expected: 6 pass (3 from Task 1.5 + 3 new).

**Step 3: Commit**

```bash
git add src/lib/installer.js tests/lib/installer.test.js
git commit -m "feat(wrs): materialize remote skills via npx into per-user cache"
```

---

### Task 1.8: Write failing test for manifest-aware skill listing

**Files:**
- Create: `tests/utils/parser-manifest.test.js`

**Step 1: Write the test** (keeps the old `readSkillList` test file untouched; adds the new API alongside)

```javascript
import { test } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { readManifestEntries } from '../../src/utils/parser.js';

function buildClone(entries) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'wrs-parser-manifest-'));
  const file = path.join(root, 'awesome-claude', 'skills.manifest.json');
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify({ version: 2, skills: entries }));
  return root;
}

test('readManifestEntries - returns parsed entries in manifest order', () => {
  const root = buildClone([
    { name: 'woic', source: 'local' },
    { name: 'vite', source: 'antfu/skills', skillId: 'vite' },
  ]);
  try {
    const entries = readManifestEntries(root);
    assert.deepStrictEqual(entries.map((e) => e.name), ['woic', 'vite']);
    assert.strictEqual(entries[0].isLocal, true);
    assert.strictEqual(entries[1].repoUrl, 'https://github.com/antfu/skills');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
```

**Step 2: Run**

```bash
node --test tests/utils/parser-manifest.test.js
```

Expected: FAIL with `readManifestEntries is not a function`.

---

### Task 1.9: Add `readManifestEntries` to `parser.js`

**Files:**
- Modify: `src/utils/parser.js`

**Step 1: Append the export (keep existing `readSkillList` untouched for now — Phase 1 keeps both paths alive)**

```javascript
import { loadManifest } from '../lib/manifest.js';

export function readManifestEntries(sourcePath) {
  return loadManifest(sourcePath);
}
```

**Step 2: Run new + existing tests**

```bash
node --test tests/utils/parser.test.js tests/utils/parser-manifest.test.js
```

Expected: all pass.

**Step 3: Commit**

```bash
git add src/utils/parser.js tests/utils/parser-manifest.test.js
git commit -m "feat(wrs): expose readManifestEntries alongside directory scan"
```

---

### Task 1.10: Update `list.js` to group local vs remote from manifest

**Files:**
- Modify: `src/commands/list.js`
- Modify: `tests/commands/list.test.js` (add a grouping case)

**Step 1: Add a grouping-output test**

Inspect `tests/commands/list.test.js` to match existing style. Append a `describe` block:

```javascript
import { formatManifestListOutput } from '../../src/commands/list.js';

describe('formatManifestListOutput', () => {
  it('groups entries into Local and Remote sections', () => {
    const output = formatManifestListOutput('ai-config', [
      { name: 'woic', source: 'local', isLocal: true },
      { name: 'vite', source: 'antfu/skills', skillId: 'vite', isLocal: false },
      { name: 'vue', source: 'antfu/skills', skillId: 'vue', isLocal: false },
    ]);
    assert.match(output, /Local \(1\)/);
    assert.match(output, /Remote \(2\)/);
    assert.match(output, /vite.*antfu\/skills/);
  });
});
```

**Step 2: Run — should fail** (`formatManifestListOutput is not defined`).

**Step 3: Implement formatter** at the top of `src/commands/list.js`

```javascript
import { readManifestEntries } from '../utils/parser.js';
import { classifyBySource } from '../lib/manifest.js';

export function formatManifestListOutput(sourceDir, entries) {
  const { local, remote } = classifyBySource(entries);
  const lines = [
    c.bold(`📦 ${sourceDir}`),
    '',
    c.bold(c.green(`Local (${local.length})`)),
  ];
  local.forEach((entry, idx) => {
    const prefix = idx === local.length - 1 ? '└─' : '├─';
    lines.push(`${prefix} ${c.green(entry.name)}`);
  });
  lines.push('', c.bold(c.cyan(`Remote (${remote.length})`)));
  remote.forEach((entry, idx) => {
    const prefix = idx === remote.length - 1 ? '└─' : '├─';
    lines.push(`${prefix} ${c.cyan(entry.name)}  ${c.dim(`← ${entry.source}`)}`);
  });
  return lines.join('\n');
}
```

**Step 4: Switch `handleList` to use the new formatter**

```javascript
const entries = readManifestEntries(sourcePath);
console.log();
console.log(formatManifestListOutput(sourceDir, entries));
```

Remove/replace the old `readSkillList` + `formatSkillListOutput` call path inside `handleList` (keep `formatSkillListOutput` export for now — removed in Phase 2).

**Step 5: Run full test suite**

```bash
node --test tests/**/*.test.js
```

Expected: all pass.

**Step 6: Commit**

```bash
git add src/commands/list.js tests/commands/list.test.js
git commit -m "feat(wrs): list groups local and remote skills from manifest"
```

---

### Task 1.11: Update `sync.js` to consume manifest entries and accept `--refresh`

**Files:**
- Modify: `src/commands/sync.js`

**Step 1: Refactor `handleSync`** to:

1. After `resolveSource(origin, spinner)` returns `sourcePath`, call `readManifestEntries(sourcePath)` to get entries.
2. Keep `lastSelection.skills` as **names** — `resolveSkillsToSync` now filters `entries` by those names.
3. For interactive prompt, pass entry names to `buildPromptChoices`.
4. In the inner loop (for each target dir), iterate over **selected entries**:

```javascript
for (const entry of selectedEntries) {
  if (!entry.isLocal) {
    await ensureRemoteInCache(entry, { cacheDir: CACHE_DIR, refresh: options.refresh === true });
  }
  const sourceDir = resolveSkillSource(entry, { cloneRoot: sourcePath, cacheDir: CACHE_DIR });
  const targetName = entry.installName ?? entry.name;
  const status = syncSkillDirectoryFromPath(sourceDir, targetName, target.claudeDir);
  // bucket into addedSkills/updatedSkills as today
}
```

(`sourcePath` is the ai-config clone root; `cloneRoot` for `resolveSkillSource` expects that path.)

**Step 2: Add helper** `syncSkillDirectoryFromPath(sourceDir, targetName, claudeDir)` in `src/utils/merger.js` — a thin variant of the current `syncSkillDirectory` that takes a direct source path instead of `(skillsDir, name)`. Reuse internally.

```javascript
export function syncSkillDirectoryFromPath(sourceDir, targetName, claudeDir) {
  if (!fs.existsSync(sourceDir) || !fs.statSync(sourceDir).isDirectory()) {
    throw new Error(`source skill dir missing: ${sourceDir}`);
  }
  const skillsTargetDir = path.join(claudeDir, 'skills');
  const destPath = path.join(skillsTargetDir, targetName);
  const exists = fs.existsSync(destPath);
  fs.mkdirSync(skillsTargetDir, { recursive: true });
  if (exists) fs.rmSync(destPath, { recursive: true, force: true });
  copyFileOrDir(sourceDir, destPath);
  return exists ? 'updated' : 'added';
}
```

**Step 3: Add a unit test for the helper**

Append to `tests/utils/merger.test.js`:

```javascript
import { syncSkillDirectoryFromPath } from '../../src/utils/merger.js';

test('syncSkillDirectoryFromPath - copies a source dir into <claudeDir>/skills/<name>', () => {
  const src = fs.mkdtempSync(path.join(os.tmpdir(), 'wrs-merger-src-'));
  fs.writeFileSync(path.join(src, 'SKILL.md'), '# test');
  const claudeDir = fs.mkdtempSync(path.join(os.tmpdir(), 'wrs-merger-dst-'));
  try {
    const status = syncSkillDirectoryFromPath(src, 'vite', claudeDir);
    assert.strictEqual(status, 'added');
    assert.strictEqual(
      fs.readFileSync(path.join(claudeDir, 'skills', 'vite', 'SKILL.md'), 'utf-8'),
      '# test'
    );
  } finally {
    fs.rmSync(src, { recursive: true, force: true });
    fs.rmSync(claudeDir, { recursive: true, force: true });
  }
});
```

**Step 4: Run all tests**

```bash
node --test tests/**/*.test.js
```

Expected: all pass.

**Step 5: Commit**

```bash
git add src/commands/sync.js src/utils/merger.js tests/utils/merger.test.js
git commit -m "feat(wrs): sync routes through manifest entries with --refresh support"
```

---

### Task 1.12: Register `--refresh` flag in the commander setup

**Files:**
- Modify: `src/index.js`

**Step 1: Add the option**

```javascript
program
  .command('sync')
  .description('同步上次选择的技能')
  .option('-g, --global', '同步全局配置')
  .option('-p, --platform <platform>', '指定平台目录')
  .option('--refresh', '忽略缓存，从上游重新拉取所有远程 skill')
  .action(handleSync);
```

**Step 2: Smoke test**

```bash
node src/index.js sync --help | grep -- '--refresh'
```

Expected: line showing `--refresh` option.

**Step 3: Commit**

```bash
git add src/index.js
git commit -m "feat(wrs): expose --refresh flag on sync command"
```

---

### Task 1.13: Add `wrs cache clean` subcommand

**Files:**
- Create: `src/commands/cache.js`
- Modify: `src/index.js`

**Step 1: Failing test**

Create `tests/commands/cache.test.js`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { cleanCacheDir } from '../../src/commands/cache.js';

test('cleanCacheDir - removes the cache directory', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'wrs-cache-clean-'));
  const nested = path.join(root, 'skills', 'vite');
  fs.mkdirSync(nested, { recursive: true });
  fs.writeFileSync(path.join(nested, 'SKILL.md'), '# x');
  cleanCacheDir(root);
  assert.strictEqual(fs.existsSync(root), false);
});

test('cleanCacheDir - no-op when cache absent', () => {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), 'wrs-cache-clean-miss-'));
  const missing = path.join(parent, 'does-not-exist');
  try {
    cleanCacheDir(missing);
    assert.strictEqual(fs.existsSync(missing), false);
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});
```

**Step 2: Run — should fail**

```bash
node --test tests/commands/cache.test.js
```

**Step 3: Implement**

```javascript
// src/commands/cache.js
import fs from 'node:fs';
import { CACHE_DIR } from '../utils/constants.js';
import { log } from '../utils/logger.js';

export function cleanCacheDir(dir) {
  if (!fs.existsSync(dir)) return;
  fs.rmSync(dir, { recursive: true, force: true });
}

export async function handleCacheClean() {
  cleanCacheDir(CACHE_DIR);
  log.info(`已清空缓存: ${CACHE_DIR}`);
}
```

**Step 4: Wire in `src/index.js`**

```javascript
import { handleCacheClean } from './commands/cache.js';

const cacheCommand = program.command('cache').description('管理 wrs 本地缓存');
cacheCommand.command('clean').description('清空远程 skill 缓存').action(handleCacheClean);
```

**Step 5: Tests + smoke**

```bash
node --test tests/**/*.test.js
node src/index.js cache clean --help
```

Expected: all tests pass; help shows `clean` subcommand.

**Step 6: Commit**

```bash
git add src/commands/cache.js src/index.js tests/commands/cache.test.js
git commit -m "feat(wrs): add 'cache clean' subcommand"
```

---

### Task 1.14: Preflight check for `npx` availability

**Files:**
- Modify: `src/lib/installer.js`

**Step 1: Add a helper**

```javascript
import { execSync } from 'node:child_process';

export function assertNpxAvailable() {
  try {
    execSync('command -v npx', { stdio: 'ignore', shell: '/bin/sh' });
  } catch {
    throw new Error('Missing npx. Install Node.js (ships with npx) before running wrs sync.');
  }
}
```

**Step 2: Call it in `sync.js`** before the loop, only when any entry needs materialization:

```javascript
if (selectedEntries.some((e) => !e.isLocal)) {
  assertNpxAvailable();
}
```

**Step 3: Smoke check**

```bash
node --test tests/**/*.test.js
```

Expected: all pass.

**Step 4: Commit**

```bash
git add src/lib/installer.js src/commands/sync.js
git commit -m "feat(wrs): preflight check for npx before materializing remote skills"
```

---

### Task 1.15: End-to-end dry run against live ai-config

**Files:** (no code change — verification only)

**Step 1:** Wipe local state to force a clean run

```bash
rm -rf ~/.wrs/templates ~/.wrs/cache
```

**Step 2:** Run sync against a scratch project

```bash
SCRATCH=$(mktemp -d)
cd "$SCRATCH"
node /Users/woic/woicw/wr-ai/src/index.js list
node /Users/woic/woicw/wr-ai/src/index.js sync --refresh --platform claude
```

**Step 3:** Verify results

- `$SCRATCH/.claude/skills/` must contain all 35 skills from the manifest.
- `~/.wrs/cache/skills/` must contain the 28 remote ones (no local).
- Compare file counts against the pre-refactor workspace to confirm parity.

**Step 4:** If verification passes, Phase 1 is complete. **Do not** commit this step (it's validation only).

---

## Phase 2 — `ai-config` slims down (destructive)

**Preconditions:** Phase 1 has landed in `wr-ai` and users are on the updated CLI. `cd /Users/woic/woicw/ai-config`.

### Task 2.1: Remove vendored remote skill directories

**Files:**
- Delete (via `git rm -r`): every directory under `awesome-claude/skills/` whose name is NOT one of the 7 locals (`ahooks`, `antd`, `react-router`, `react-webapp-builder`, `screenshot-ui-restore`, `sync-remote-skills`, `woic`). The authoritative list is the set of entries in `skills.manifest.json` where `source !== "local"`.

**Step 1:** Generate the removal list

```bash
python3 -c "
import json
data = json.load(open('awesome-claude/skills.manifest.json'))
remotes = [s.get('installName') or s['name'] for s in data['skills'] if s.get('source') != 'local']
for name in remotes: print(f'awesome-claude/skills/{name}')
"
```

**Step 2:** `git rm -r` every path from the list (verify each exists first)

**Step 3:** Confirm local dirs still present

```bash
ls awesome-claude/skills/ | sort
```

Expected: exactly 7 entries matching the locals list above.

**Step 4:** Commit

```bash
git commit -m "chore(ai-config): remove vendored remote skills (now materialized by wrs)"
```

---

### Task 2.2: Remove the old sync script and related artifacts

**Files:**
- Delete: `awesome-claude/scripts/sync_skills_from_manifest.py`
- Delete: `awesome-claude/tests/` (only if its entire contents covered the removed script — inspect first)
- Delete: `skills-lock.json`
- Modify: `package.json` — drop `skills:add`, `skills:sync`, `skills:sync:existing` scripts; keep `skills:list`/`skills:check` only if they remain meaningful after Phase 2 (likely drop all).

**Step 1:** Inspect `awesome-claude/tests/` — if every test is keyed to the Python script, remove the directory.

**Step 2:** Delete files

```bash
git rm awesome-claude/scripts/sync_skills_from_manifest.py
git rm skills-lock.json
git rm -r awesome-claude/tests  # only if audit confirms
```

**Step 3:** Update `package.json` — simplest is to remove the 5 skills:* scripts entirely:

```json
"scripts": {
  "test": "echo \"Error: no test specified\" && exit 1"
}
```

**Step 4:** Commit

```bash
git add package.json
git commit -m "chore(ai-config): drop legacy sync script and npm aliases"
```

---

### Task 2.3: Update `README.md`

**Files:**
- Modify: `README.md`

**Step 1:** Rewrite the "远程 Skills 同步"/"同步命令"/"新增远程 Skill"/"同步策略" sections into one short section: "远程 Skills 由 [wrs](https://github.com/woicw/wr-ai) 完成同步。" — include the minimal user-facing snippet:

```bash
pnpm add -g wrs
wrs set github woicw/ai-config
wrs sync            # 首次交互选择；之后会记住
wrs sync --refresh  # 强制拉取最新远程 skill
```

**Step 2:** Remove obsolete references to `sync_skills_from_manifest.py`, `skills-lock.json`, `pnpm run skills:*`.

**Step 3:** Keep the "添加本地 Skill"/"添加 Command"/"MCP 配置" sections — those still apply.

**Step 4:** Commit

```bash
git add README.md
git commit -m "docs(ai-config): point skills sync at wrs, trim legacy sections"
```

---

### Task 2.4: Post-Phase-2 regression check

**Files:** (verification only)

**Step 1:** Clean user caches

```bash
rm -rf ~/.wrs/templates ~/.wrs/cache
```

**Step 2:** Fresh sync into a scratch project

```bash
SCRATCH=$(mktemp -d) && cd "$SCRATCH"
wrs sync --refresh --platform claude
ls .claude/skills/ | wc -l
```

Expected: 35 (7 local + 28 remote, same as pre-refactor).

**Step 3:** If count and contents match Phase 1's Task 1.15 baseline, Phase 2 is complete. Otherwise debug (likely a manifest entry with a wrong `installName` or `skillId`).

---

## Phase 3 — polish (deferrable)

### Task 3.1: Publish new `wrs` version

**Files:** (wr-ai repo)
- Modify: `package.json` version → `4.1.0` (or semver-appropriate bump).
- Modify: `README.md` — document `--refresh`, `wrs cache clean`, new manifest-driven `list` output, and the requirement that the target repo expose `awesome-claude/skills.manifest.json`.

**Step 1:** Bump version, update README, commit:

```bash
git add package.json README.md
git commit -m "docs(wrs): document --refresh, cache clean, and manifest format"
```

**Step 2:** Publish (respect the repo's existing release process — check `package.json` or CI workflows before running `npm publish`).

---

### Task 3.2: Cross-link from `ai-config` README to `wrs`

**Files:**
- Modify: `ai-config/README.md`

Add a short "消费方式" bullet near the top: `skill 的分发由 [wrs](https://www.npmjs.com/package/wrs) 完成`.

Commit:

```bash
git add README.md
git commit -m "docs(ai-config): cross-link wrs consumer"
```

---

## Validation summary (end of Phase 1)

- All `node --test tests/**/*.test.js` tests pass in `wr-ai`.
- `wrs list` prints grouped Local / Remote sections sourced from the manifest.
- `wrs sync --refresh --platform claude` against a clean scratch project reproduces the pre-refactor workspace skill set (35 entries).
- `~/.wrs/cache/skills/` is populated with 28 remote skill directories; `~/.wrs/cache/stage/` is absent or empty after sync finishes.
- `wrs cache clean` wipes `~/.wrs/cache/`; subsequent `wrs sync` rebuilds it from scratch.

## Validation summary (end of Phase 2)

- `ai-config/awesome-claude/skills/` contains exactly 7 directories.
- `skills.manifest.json` unchanged; still the single source of truth.
- No `scripts/sync_skills_from_manifest.py`, no `skills-lock.json`, no `awesome-claude/tests/`.
- Fresh `wrs sync --refresh` against the slimmed ai-config still produces the full 35-skill workspace.
