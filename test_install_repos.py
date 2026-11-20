#!/usr/bin/env python3
"""Tests for install_repos.py with fake search results and repo files: discovery and the install plan."""

import unittest

import install_repos as ir

API = ir.API


def fake_search(repos):
    def get(url):
        topic = url.split("topic:")[1].split("+")[0]
        return {"items": [{"full_name": n, "name": n.split("/")[1]} for n, r in repos.items() if topic in r["topics"]]}
    return get


def fake_files(repos):
    def files(repo):
        f = repos[repo]["files"]
        return set(f), f.__getitem__
    return files


MP = {"name": "oncebitten", "plugins": [{"name": "oncebitten"}]}
REPOS = {
    "o/oncebitten": {"topics": ["claude-memory"], "files": {
        ir.CLAUDE_MP: MP, ir.COPILOT_MP: MP, ir.CODEX_MP: MP, "README.md": None}},
    "o/personal-skills": {"topics": ["claude-memory", "skills"], "files": {
        "skills/a/SKILL.md": None, "skills/b/SKILL.md": None}},
    "o/claude-memory": {"topics": ["claude-memory"], "files": {"MEMORY.md": None}},
    "o/other": {"topics": ["misc"], "files": {"skills/x/SKILL.md": None}},
    "o/docs": {"topics": ["claude-memory"], "files": {"README.md": None}},
}
ALL = lambda _: True  # noqa: E731


class GitFiles(unittest.TestCase):
    def test_reads_tree_and_marketplace_from_a_local_repo(self):
        import pathlib, subprocess, tempfile
        with tempfile.TemporaryDirectory() as d:
            src = pathlib.Path(d, "o", "r")
            (src / ".claude-plugin").mkdir(parents=True)
            (src / ".claude-plugin" / "marketplace.json").write_text('{"name": "m", "plugins": [{"name": "p"}]}')
            (src / "skills" / "a").mkdir(parents=True)
            (src / "skills" / "a" / "SKILL.md").write_text("x")
            for cmd in (["init", "-q"], ["add", "."], ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "commit", "-qm", "i"]):
                subprocess.run(["git", "-C", str(src), *cmd], check=True)
            paths, read = ir.git_files("o/r", base=f"file://{d}")
            self.assertEqual(paths, {".claude-plugin/marketplace.json", "skills/a/SKILL.md"})
            self.assertEqual(read(ir.CLAUDE_MP)["name"], "m")


class Discover(unittest.TestCase):
    def test_topic_filters_and_skips_self(self):
        self.assertEqual(ir.discover("o", "claude-memory", fake_search(REPOS)), ["o/docs", "o/oncebitten", "o/personal-skills"])


class Plan(unittest.TestCase):
    def cmds(self, repo, have=ALL):
        return [" ".join(c) for _, c in ir.plan(repo, fake_files(REPOS), have)]

    def test_plugin_repo_installs_into_each_host(self):
        self.assertEqual(self.cmds("o/oncebitten"), [
            "claude plugin marketplace add o/oncebitten",
            "claude plugin marketplace update oncebitten",
            "claude plugin install oncebitten@oncebitten",
            "copilot plugin marketplace add o/oncebitten",
            "copilot plugin install oncebitten@oncebitten",
            "codex plugin marketplace add o/oncebitten",
        ])

    def test_skills_repo_uses_npx_skills(self):
        self.assertEqual(self.cmds("o/personal-skills"), ["npx -y skills add o/personal-skills -g --all"])

    def test_missing_hosts_are_skipped(self):
        self.assertEqual(self.cmds("o/oncebitten", have=lambda c: c == "codex"), ["codex plugin marketplace add o/oncebitten"])
        self.assertEqual(self.cmds("o/personal-skills", have=lambda c: False), [])

    def test_repo_without_skills_or_plugins_plans_nothing(self):
        self.assertEqual(self.cmds("o/docs"), [])


if __name__ == "__main__":
    unittest.main()
