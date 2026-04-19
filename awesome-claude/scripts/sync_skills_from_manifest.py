#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "skills.manifest.json"
DEFAULT_DEST = ROOT / "skills"
DEFAULT_INSTALLER = (
    Path.home()
    / ".codex/skills/.system/skill-installer/scripts/install-skill-from-github.py"
)
DEFAULT_NPX_CANDIDATES = [
    Path("/opt/homebrew/bin/npx"),
    Path("/usr/local/bin/npx"),
]
PROJECT_AGENT_DIRS = {
    "codex": ".agents/skills",
    "claude-code": ".claude/skills",
    "github-copilot": ".agents/skills",
    "cursor": ".agents/skills",
}


@dataclass(frozen=True)
class SkillSpec:
    name: str
    source: str
    skill_id: str | None = None
    install_name: str | None = None
    agent: str | None = None

    @property
    def is_local(self) -> bool:
        return self.source == "local"

    @property
    def resolved_remote(self) -> bool:
        return self.source != "local" and bool(self.skill_id)

    @property
    def repo_url(self) -> str:
        if self.is_local:
            raise ValueError(f"Local skill '{self.name}' has no repo URL")
        return f"https://github.com/{self.source}"


def derive_source_from_repo_url(repo_url: str) -> str:
    match = re.match(r"^https://github\.com/([^/]+/[^/]+)/?$", repo_url.rstrip(".git"))
    if not match:
        raise ValueError(f"Unsupported GitHub repo URL: {repo_url}")
    return match.group(1)


def load_manifest(path: Path) -> list[SkillSpec]:
    data = json.loads(path.read_text())
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise ValueError("Manifest must contain a top-level 'skills' array")

    result: list[SkillSpec] = []
    for raw in skills:
        if not isinstance(raw, dict):
            raise ValueError("Each manifest skill entry must be an object")
        name = raw.get("name")
        source = raw.get("source")
        if not isinstance(name, str) or not name:
            raise ValueError("Each skill entry requires a non-empty string 'name'")
        if source not in {"local", "remote"}:
            if not isinstance(source, str) or "/" not in source:
                raise ValueError(f"Skill '{name}' has invalid source: {source!r}")
        result.append(
            SkillSpec(
                name=name,
                source=source,
                skill_id=raw.get("skillId"),
                install_name=raw.get("installName"),
                agent=raw.get("agent"),
            )
        )
    return result


def filter_skills(skills: Iterable[SkillSpec], names: set[str] | None) -> list[SkillSpec]:
    if not names:
        return list(skills)
    return [skill for skill in skills if skill.name in names]


def parse_skills_add_command(tokens: list[str]) -> dict[str, str]:
    if not tokens:
        raise ValueError("No command provided. Paste the full 'npx skills add ... --skill ...' command.")

    filtered = [token for token in tokens if token not in {"\\", "\n"}]

    while filtered and filtered[0] in {"npx", "skills", "add"}:
        filtered.pop(0)
        if filtered[:2] == ["skills", "add"]:
            filtered = filtered[2:]
            break

    if not filtered:
        raise ValueError("Could not find the repo URL in the add command.")

    repo_url = None
    skill_id = None
    i = 0
    while i < len(filtered):
        token = filtered[i]
        if token.startswith("https://github.com/"):
            repo_url = token
        elif token == "--skill":
            if i + 1 >= len(filtered):
                raise ValueError("Missing value after --skill")
            skill_id = filtered[i + 1]
            i += 1
        i += 1

    if not repo_url:
        raise ValueError("Could not find a GitHub repo URL in the add command.")
    if not skill_id:
        raise ValueError("Could not find '--skill <id>' in the add command.")

    return {"source": derive_source_from_repo_url(repo_url), "skillId": skill_id}


def add_remote_skill_to_manifest(path: Path, repo_source: str, skill_id: str) -> dict[str, str]:
    data = json.loads(path.read_text())
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise ValueError("Manifest must contain a top-level 'skills' array")

    entry_name = skill_id
    for skill in skills:
        if not isinstance(skill, dict):
            continue
        if skill.get("name") == entry_name:
            skill["source"] = repo_source
            skill["skillId"] = skill_id
            data["skills"] = skills
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
            return skill

    entry = {"name": entry_name, "source": repo_source, "skillId": skill_id}
    skills.append(entry)
    data["skills"] = skills
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    return entry


def discover_npx() -> Path:
    for candidate in DEFAULT_NPX_CANDIDATES:
        if candidate.exists():
            return candidate
    found = shutil.which("npx")
    if found:
        return Path(found)
    raise FileNotFoundError("Could not find npx in PATH or default Homebrew locations")


def project_agent_skill_dir(root: Path, agent: str) -> Path:
    rel = PROJECT_AGENT_DIRS.get(agent)
    if not rel:
        raise ValueError(f"Unsupported agent for skills_cli transport: {agent!r}")
    return root / rel


def run_skills_cli_install(root: Path, dest: Path, skill: SkillSpec) -> None:
    npx = discover_npx()
    agent = skill.agent or "codex"
    install_name = skill.install_name or skill.name
    skill_id = skill.skill_id or skill.name
    source_dir = project_agent_skill_dir(root, agent) / skill_id
    if dest.joinpath(install_name).exists():
        shutil.rmtree(dest / install_name)

    cmd = [
        str(npx),
        "skills",
        "add",
        skill.repo_url,
        "--skill",
        skill_id,
        "--agent",
        agent,
        "--copy",
        "-y",
    ]
    print("$ " + " ".join(cmd))
    subprocess.run(cmd, cwd=root, check=True)
    if not source_dir.exists():
        raise FileNotFoundError(
            f"skills_cli install did not create expected project skill dir: {source_dir}"
        )
    shutil.copytree(source_dir, dest / install_name)


def existing_names(dest: Path) -> set[str]:
    if not dest.exists():
        return set()
    return {item.name for item in dest.iterdir() if item.is_dir()}


def run_check(skills: list[SkillSpec], dest: Path) -> int:
    installed = existing_names(dest)
    local = [skill.name for skill in skills if skill.is_local]
    resolved = [skill.name for skill in skills if skill.resolved_remote]
    unresolved = [skill.name for skill in skills if not skill.is_local and not skill.resolved_remote]

    print("Manifest summary")
    print(f"- local: {len(local)}")
    print(f"- resolved remote: {len(resolved)}")
    print(f"- unresolved remote: {len(unresolved)}")

    missing = [name for name in resolved if name not in installed]
    extras = sorted(installed - {skill.name for skill in skills})

    if missing:
        print("\nMissing resolved skills:")
        for name in missing:
            print(f"- {name}")

    if unresolved:
        print("\nUnresolved remote skills:")
        for name in unresolved:
            print(f"- {name}")

    if extras:
        print("\nInstalled but not in manifest:")
        for name in extras:
            print(f"- {name}")

    return 1 if missing or unresolved else 0


def run_sync(
    skills: list[SkillSpec],
    dest: Path,
    update_existing_only: bool,
) -> int:
    installed = existing_names(dest)
    unresolved = [skill.name for skill in skills if not skill.is_local and not skill.resolved_remote]
    if unresolved:
        print("Skipping unresolved remote skills:")
        for name in unresolved:
            print(f"- {name}")

    resolved = [skill for skill in skills if skill.resolved_remote]
    if update_existing_only:
        resolved = [skill for skill in resolved if skill.name in installed]

    if not resolved:
        print("No resolved remote skills selected for sync.")
        return 0

    for skill in resolved:
        print(f"\nSyncing {skill.name}")
        run_skills_cli_install(ROOT.parent, dest, skill)

    return 0


def run_list(skills: list[SkillSpec]) -> int:
    for skill in skills:
        if skill.is_local:
            print(f"{skill.name}\tlocal")
        elif skill.resolved_remote:
            print(
                f"{skill.name}\tremote\tresolved\tskills_cli\t{skill.repo_url}\t{skill.skill_id}"
            )
        else:
            print(f"{skill.name}\tremote\tunresolved")
    return 0


def run_add(manifest: Path, tokens: list[str]) -> int:
    parsed = parse_skills_add_command(tokens)
    entry = add_remote_skill_to_manifest(
        manifest,
        repo_source=parsed["source"],
        skill_id=parsed["skillId"],
    )
    print("Added remote skill to manifest")
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    print("\nNext step:")
    print(f"bash ./sync-skills sync {entry['name']}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync awesome-claude skills from a manifest.")
    parser.add_argument(
        "command",
        choices=["list", "check", "sync", "add"],
        help="Action to perform",
    )
    parser.add_argument(
        "names",
        nargs="*",
        help="Optional skill names to limit the action to",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Path to the manifest file",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEFAULT_DEST,
        help="Destination skills directory",
    )
    parser.add_argument(
        "--update-existing-only",
        action="store_true",
        help="Sync only resolved remote skills that already exist in the destination",
    )
    args, unknown = parser.parse_known_args(argv)
    if args.command == "add":
        args.names.extend(unknown)
        return args
    if unknown:
        parser.error(f"unrecognized arguments: {' '.join(unknown)}")
    return args


def main() -> int:
    args = parse_args()
    skills = load_manifest(args.manifest)
    selected = filter_skills(skills, set(args.names) if args.names else None)

    if args.command == "list":
        return run_list(selected)
    if args.command == "check":
        return run_check(selected, args.dest)
    if args.command == "sync":
        return run_sync(selected, args.dest, args.update_existing_only)
    if args.command == "add":
        return run_add(args.manifest, args.names)
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
