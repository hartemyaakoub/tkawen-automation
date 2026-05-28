#!/usr/bin/env python3
"""Drain .data/queue/social-posts.json into Postiz.

Each entry: {"platform": "facebook" | "instagram" | "linkedin" | "telegram" | "x",
             "message": "...", "link": "...", "image_url": "..."}.

Consumed entries get moved to .data/queue/sent/<YYYY-MM-DD-HHMM>.json so the
queue file shrinks. Set POSTIZ_API_TOKEN env to authorize."""

import json
import os
import sys
import urllib.request as ur
from datetime import datetime
from pathlib import Path

QUEUE = Path(".data/queue/social-posts.json")
SENT_DIR = Path(".data/queue/sent")
POSTIZ_BASE = os.environ.get("POSTIZ_BASE", "https://post.tkawen.com")
TOKEN = os.environ.get("POSTIZ_API_TOKEN", "")
MAX_PER_RUN = 5  # don't fire-hose if queue is huge


def post_to_postiz(entry: dict) -> tuple[bool, str]:
    if not TOKEN:
        return False, "no token"
    url = f"{POSTIZ_BASE}/api/posts"
    body = json.dumps({
        "providers": [entry.get("platform")],
        "message": entry.get("message", ""),
        "link": entry.get("link"),
        "media": [{"url": entry["image_url"]}] if entry.get("image_url") else [],
    }).encode()
    req = ur.Request(
        url, data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}",
        },
        method="POST",
    )
    try:
        with ur.urlopen(req, timeout=30) as r:
            return True, f"http {r.status}"
    except Exception as e:
        return False, str(e)


def main() -> None:
    if not QUEUE.exists():
        print(f"no queue at {QUEUE}", file=sys.stderr)
        Path("/tmp/postiz_result.json").write_text(json.dumps({"sent": 0}))
        return

    try:
        items = json.loads(QUEUE.read_text())
    except Exception as e:
        print(f"queue parse failed: {e}", file=sys.stderr)
        Path("/tmp/postiz_result.json").write_text(json.dumps({"sent": 0}))
        return

    if not isinstance(items, list):
        items = []

    sent = []
    fails = []
    for entry in items[:MAX_PER_RUN]:
        ok, msg = post_to_postiz(entry)
        if ok:
            sent.append({"entry": entry, "status": msg})
        else:
            fails.append({"entry": entry, "status": msg})

    # Persist what's left
    remaining = items[len(sent) + len(fails):] + [f["entry"] for f in fails]
    QUEUE.write_text(json.dumps(remaining, ensure_ascii=False, indent=2))

    # Snapshot what was sent
    if sent:
        SENT_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.utcnow().strftime("%Y-%m-%d-%H%M")
        (SENT_DIR / f"sent-{ts}.json").write_text(
            json.dumps(sent, ensure_ascii=False, indent=2)
        )

    Path("/tmp/postiz_result.json").write_text(json.dumps({
        "sent": len(sent),
        "failed": len(fails),
        "remaining": len(remaining),
    }))
    print(f"posted {len(sent)} / failed {len(fails)} / remaining {len(remaining)}")


if __name__ == "__main__":
    main()
