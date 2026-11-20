#!/usr/bin/env python3
"""Install every repo of OWNER tagged with TOPIC into the agents on this machine.

Per repo, by what it ships:
  .claude-plugin/marketplace.json   -> claude plugin marketplace add + install each plugin
  .github/plugin/marketplace.json   -> copilot plugin marketplace add + install each plugin
  .agents/plugins/marketplace.json  -> codex plugin marketplace add (install from /plugins)
  SKILL.md files, no plugin above   -> npx skills add OWNER/REPO -g --all (every detected agent)
A host that is not on PATH is skipped. A failed step warns and the rest continue.

Usage: install_repos.py [--owner bcmyguest] [--topic claude-memory] [--dry-run]
Env: CLAUDE_MEMORY_OWNER, CLAUDE_MEMORY_TOPIC, GITHUB_TOKEN (optional; only the topic search
uses the GitHub API, once per run). Repo contents are read with a blobless git clone.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request

API = "https://api.github.com"
SELF = "claude-memory"
CLAUDE_MP = ".claude-plugin/marketplace.json"
COPILOT_MP = ".github/plugin/marketplace.json"
CODEX_MP = ".agents/plugins/marketplace.json"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "claude-memory"})
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and url.startswith(API):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def discover(owner, topic, get=fetch_json):
    """Full names of OWNER's repos tagged TOPIC, excluding this repo and archived ones."""
    data = get(f"{API}/search/repositories?q=user:{owner}+topic:{topic}+archived:false&per_page=100")
    return sorted(i["full_name"] for i in data["items"] if i["name"] != SELF)


def git_files(repo, base="https://github.com"):
    """Return (paths, read) for REPO's default branch via a blobless clone; no API calls."""
    tmp = tempfile.mkdtemp(prefix="claude-memory-")
    try:
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--no-checkout",
                        f"{base}/{repo}", tmp], check=True, capture_output=True)
        out = subprocess.run(["git", "-C", tmp, "ls-tree", "-r", "--name-only", "HEAD"],
                             check=True, capture_output=True, text=True).stdout
        cache = {}
        for path in (CLAUDE_MP, COPILOT_MP):
            r = subprocess.run(["git", "-C", tmp, "show", f"HEAD:{path}"], capture_output=True, text=True)
            if r.returncode == 0:
                cache[path] = json.loads(r.stdout)
        return set(out.split()), cache.__getitem__
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def plan(repo, files=git_files, have=shutil.which):
    """Commands that install REPO, as (description, argv) pairs."""
    paths, read = files(repo)
    has_skills = any(p == "SKILL.md" or p.endswith("/SKILL.md") for p in paths)
    steps = []

    def plugins(path):
        mp = read(path)
        return mp["name"], [p["name"] for p in mp.get("plugins", [])]

    if CLAUDE_MP in paths and have("claude"):
        name, names = plugins(CLAUDE_MP)
        steps.append(("claude marketplace", ["claude", "plugin", "marketplace", "add", repo]))
        steps.append(("claude marketplace update", ["claude", "plugin", "marketplace", "update", name]))
        steps += [(f"claude plugin {p}", ["claude", "plugin", "install", f"{p}@{name}"]) for p in names]
    if COPILOT_MP in paths and have("copilot"):
        name, names = plugins(COPILOT_MP)
        steps.append(("copilot marketplace", ["copilot", "plugin", "marketplace", "add", repo]))
        steps += [(f"copilot plugin {p}", ["copilot", "plugin", "install", f"{p}@{name}"]) for p in names]
    if CODEX_MP in paths and have("codex"):
        steps.append(("codex marketplace (then install from /plugins)", ["codex", "plugin", "marketplace", "add", repo]))
    if has_skills and CLAUDE_MP not in paths and have("npx"):
        steps.append(("skills, every detected agent", ["npx", "-y", "skills", "add", repo, "-g", "--all"]))
    return steps


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--owner", default=os.environ.get("CLAUDE_MEMORY_OWNER", "bcmyguest"))
    ap.add_argument("--topic", default=os.environ.get("CLAUDE_MEMORY_TOPIC", "claude-memory"))
    ap.add_argument("--dry-run", action="store_true", help="print the commands without running them")
    args = ap.parse_args(argv)

    try:
        repos = discover(args.owner, args.topic)
    except Exception as e:  # network or rate limit: the rest of install.sh still runs
        print(f"warning: could not list {args.owner} repos tagged {args.topic}: {e}", file=sys.stderr)
        return 0
    print(f"{len(repos)} {args.owner} repos tagged {args.topic}: {', '.join(repos) or 'none'}")
    failed = 0
    for repo in repos:
        try:
            steps = plan(repo)
        except Exception as e:
            print(f"warning: {repo}: {e}", file=sys.stderr)
            failed += 1
            continue
        if not steps:
            print(f"{repo}: nothing to install for the agents on PATH")
        for desc, cmd in steps:
            print(f"{repo}: {desc}: {' '.join(cmd)}")
            if args.dry_run:
                continue
            if subprocess.run(cmd).returncode != 0 and "update" not in desc and "marketplace" not in desc:
                print(f"warning: {repo}: {desc} failed", file=sys.stderr)
                failed += 1
    if failed:
        print(f"{failed} step(s) failed; see warnings above", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
