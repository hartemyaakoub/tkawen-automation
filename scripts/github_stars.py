#!/usr/bin/env python3
"""Snapshot stars/forks/watchers for every public TKAWEN repo."""

import json
import os
import sys
import urllib.request as ur
from datetime import datetime

REPOS = [
    "hartemyaakoub/tkawen-automation",
    "hartemyaakoub/seo-toolkit",
    "hartemyaakoub/mystoq-js-sdk",
    "hartemyaakoub/mystoq-php-sdk",
    "hartemyaakoub/mystoq-python-sdk",
    "hartemyaakoub/mystoq-themes",
    "hartemyaakoub/mystoq-openapi",
    "hartemyaakoub/mystoq-cli",
    "hartemyaakoub/mystoq-examples",
    "hartemyaakoub/awesome-mystoq",
    "hartemyaakoub/mystoq-status",
    "hartemyaakoub/mystoq-postman",
    "hartemyaakoub/mystoq-mcp-server",
    "hartemyaakoub/mystoq-wilayas-dataset",
    "hartemyaakoub/mystoq-react-components",
    "hartemyaakoub/mystoq-fakeshield-rules",
    "hartemyaakoub/mystoq-yalidine-bridge",
    "hartemyaakoub/mystoq-maystro-bridge",
    "hartemyaakoub/mystoq-whatsapp-bridge",
    "hartemyaakoub/mystoq-webhook-tester",
    "hartemyaakoub/mystoq-discord-bot",
    "hartemyaakoub/mystoq-zapier",
]

UA = "TKAWEN-GitHubStars/1.0"
TIMEOUT = 15
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")


def fetch_repo(name: str) -> dict | None:
    url = f"https://api.github.com/repos/{name}"
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    try:
        req = ur.Request(url, headers=headers)
        with ur.urlopen(req, timeout=TIMEOUT) as r:
            return json.load(r)
    except Exception as e:
        print(f"failed {name}: {e}", file=sys.stderr)
        return None


def main() -> None:
    rows = []
    total_stars = 0
    total_forks = 0
    total_watchers = 0
    for r in REPOS:
        info = fetch_repo(r)
        if not info:
            continue
        stars = info.get("stargazers_count", 0)
        forks = info.get("forks_count", 0)
        watchers = info.get("subscribers_count", 0)
        rows.append({
            "name": r,
            "stars": stars,
            "forks": forks,
            "watchers": watchers,
            "open_issues": info.get("open_issues_count", 0),
            "pushed_at": info.get("pushed_at"),
        })
        total_stars += stars
        total_forks += forks
        total_watchers += watchers

    print(json.dumps({
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "total_repos": len(rows),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "total_watchers": total_watchers,
        },
        "repos": rows,
    }, indent=2))


if __name__ == "__main__":
    main()
