#!/usr/bin/env node
// Audit awesome-claude/skills.manifest.json against upstream repos.
//
// Checks, per remote entry:
//   1. source repo exists, is not archived, and has not been renamed/moved
//   2. skillId matches a SKILL.md frontmatter `name` upstream
//      (the `skills` CLI that wrs shells out to matches --skill by frontmatter name)
// And per local entry: the directory exists under awesome-claude/skills/.
//
// Usage:  node awesome-claude/scripts/audit-skills.mjs
// Auth:   uses $GITHUB_TOKEN, or falls back to `gh auth token` if gh is installed.
// Exit:   0 = all good, 1 = problems found.

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const manifestPath = path.join(repoRoot, 'awesome-claude', 'skills.manifest.json');
const skillsDir = path.join(repoRoot, 'awesome-claude', 'skills');

// A repo with more SKILL.md files than this only gets a targeted check
// (dir basename match) instead of a full frontmatter scan.
const FULL_SCAN_LIMIT = 60;

function getToken() {
  if (process.env.GITHUB_TOKEN) return process.env.GITHUB_TOKEN;
  try {
    return execSync('gh auth token', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim();
  } catch {
    return null;
  }
}
const token = getToken();

async function gh(url, raw = false) {
  const res = await fetch(`https://api.github.com/${url}`, {
    headers: {
      Accept: raw ? 'application/vnd.github.raw' : 'application/vnd.github+json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`GET ${url} -> ${res.status}`);
  return raw ? res.text() : res.json();
}

function frontmatterName(text) {
  const match = text.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  const line = match[1].split('\n').find((l) => l.startsWith('name:'));
  return line ? line.slice(5).trim().replace(/^['"]|['"]$/g, '') : null;
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
const problems = [];
const notes = [];

// --- local entries ---
for (const s of manifest.skills.filter((s) => s.source === 'local')) {
  if (!fs.existsSync(path.join(skillsDir, s.name))) {
    problems.push(`[local] ${s.name}: missing directory awesome-claude/skills/${s.name}`);
  }
}

// --- remote entries, grouped by repo ---
const remote = manifest.skills.filter((s) => s.source !== 'local');
const byRepo = new Map();
for (const s of remote) {
  if (!byRepo.has(s.source)) byRepo.set(s.source, []);
  byRepo.get(s.source).push(s);
}

await Promise.all(
  [...byRepo.entries()].map(async ([repo, entries]) => {
    const info = await gh(`repos/${repo}`);
    if (!info) {
      problems.push(`[repo] ${repo}: not found (moved or deleted?)`);
      return;
    }
    if (info.archived) notes.push(`[repo] ${repo}: archived upstream (still clonable, but frozen)`);
    if (info.full_name.toLowerCase() !== repo.toLowerCase()) {
      problems.push(`[repo] ${repo}: renamed to ${info.full_name} — update "source" in the manifest`);
    }

    const tree = await gh(`repos/${repo}/git/trees/${info.default_branch}?recursive=1`);
    const skillPaths = tree.tree.filter((t) => t.path.endsWith('SKILL.md')).map((t) => t.path);

    // Small repo: resolve every frontmatter name once, then compare.
    let allNames = null;
    if (skillPaths.length <= FULL_SCAN_LIMIT) {
      allNames = new Map();
      for (const p of skillPaths) {
        const text = await gh(`repos/${repo}/contents/${p}`, true);
        const name = text && frontmatterName(text);
        if (name) allNames.set(name, p);
      }
    }

    for (const entry of entries) {
      if (allNames) {
        if (!allNames.has(entry.skillId)) {
          const hint = [...allNames.keys()].filter((n) => n.includes(entry.skillId) || entry.skillId.includes(n));
          problems.push(
            `[skillId] ${repo} :: ${entry.skillId}: no SKILL.md frontmatter name matches.` +
              (hint.length ? ` Did you mean: ${hint.join(', ')}?` : ` Available: ${[...allNames.keys()].join(', ')}`)
          );
        }
      } else {
        // Big repo: check only the SKILL.md whose directory matches the skillId.
        const p = skillPaths.find((sp) => sp === `${entry.skillId}/SKILL.md` || sp.endsWith(`/${entry.skillId}/SKILL.md`));
        if (!p) {
          problems.push(`[skillId] ${repo} :: ${entry.skillId}: no skill directory found (repo has ${skillPaths.length} skills; removed upstream?)`);
          continue;
        }
        const name = frontmatterName((await gh(`repos/${repo}/contents/${p}`, true)) ?? '');
        if (name !== entry.skillId) {
          problems.push(`[skillId] ${repo} :: ${entry.skillId}: frontmatter name is now "${name}" (${p}) — update skillId`);
        }
      }
    }
  })
);

for (const n of notes) console.log(`NOTE  ${n}`);
if (problems.length === 0) {
  console.log(`OK — ${remote.length} remote + ${manifest.skills.length - remote.length} local entries all match upstream.`);
} else {
  for (const p of problems) console.log(`FAIL  ${p}`);
  console.log(`\n${problems.length} problem(s) found.`);
  process.exit(1);
}
