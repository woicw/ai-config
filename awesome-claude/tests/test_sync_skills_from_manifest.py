import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from awesome_claude_test_loader import load_sync_module


sync = load_sync_module()


class SyncSkillsFromManifestTests(unittest.TestCase):
    def write_manifest(self, data: dict) -> Path:
        tempdir = Path(tempfile.mkdtemp())
        path = tempdir / "skills.manifest.json"
        path.write_text(json.dumps(data))
        return path

    def test_load_manifest_rejects_invalid_source(self):
        manifest = self.write_manifest(
            {"skills": [{"name": "bad", "source": "mystery"}]}
        )
        with self.assertRaises(ValueError):
            sync.load_manifest(manifest)

    def test_repo_url_is_derived_from_source(self):
        skill = sync.SkillSpec(
            name="react",
            source="remote",
            skill_id="react",
        )
        self.assertEqual(
            skill.repo_url,
            "https://github.com/remote",
        )
 
    def test_repo_url_uses_source_owner_repo(self):
        skill = sync.SkillSpec(
            name="react",
            source="vercel-labs/json-render",
            skill_id="react",
        )
        self.assertEqual(skill.repo_url, "https://github.com/vercel-labs/json-render")

    def test_skills_cli_path_is_considered_resolved(self):
        skill = sync.SkillSpec(
            name="shadcn",
            source="shadcn/ui",
            skill_id="shadcn",
        )
        self.assertTrue(skill.resolved_remote)

    def test_project_agent_skill_dir_uses_codex_project_path(self):
        root = Path("/tmp/project")
        self.assertEqual(
            sync.project_agent_skill_dir(root, "codex"),
            root / ".agents/skills",
        )

    def test_filter_skills_returns_only_named_entries(self):
        skills = [
            sync.SkillSpec(name="a", source="local"),
            sync.SkillSpec(name="b", source="owner/repo", skill_id="b"),
        ]
        filtered = sync.filter_skills(skills, {"b"})
        self.assertEqual([skill.name for skill in filtered], ["b"])

    def test_parse_skills_add_command(self):
        parsed = sync.parse_skills_add_command(
            [
                "npx",
                "skills",
                "add",
                "https://github.com/vercel-labs/agent-skills",
                "--skill",
                "vercel-react-best-practices",
            ]
        )
        self.assertEqual(
            parsed,
            {
                "source": "vercel-labs/agent-skills",
                "skillId": "vercel-react-best-practices",
            },
        )

    def test_add_remote_skill_to_manifest_appends_entry(self):
        manifest = self.write_manifest({"version": 2, "skills": []})
        entry = sync.add_remote_skill_to_manifest(
            manifest,
            repo_source="vercel-labs/agent-skills",
            skill_id="vercel-react-best-practices",
        )
        self.assertEqual(
            entry,
            {
                "name": "vercel-react-best-practices",
                "source": "vercel-labs/agent-skills",
                "skillId": "vercel-react-best-practices",
            },
        )
        data = json.loads(manifest.read_text())
        self.assertEqual(data["skills"][0], entry)


if __name__ == "__main__":
    unittest.main()
