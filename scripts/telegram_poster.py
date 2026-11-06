#!/usr/bin/env python3
"""Forward the automation's social-post queue to the founder's Telegram chat.

Reads .data/queue/social-posts.json — every entry { platform, message, link,
image_url } gets delivered to the Telegram chat so the founder sees exactly
what the machine is queuing/publishing.

This consumer is NON-DESTRUCTIVE: it does not drain the shared queue (Postiz
owns that). Instead it records a content hash of every delivered post in
.data/queue/telegram-sent.json, so scheduled runs never double-send and never
race the Postiz drain. Set TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID to authorize.
"""

import hashlib
import json
import os
import sys
import urllib.parse as up
import urllib.request as ur
from pathlib import Path

QUEUE = Path(".data/queue/social-posts.json")
STATE = Path(".data/queue/telegram-sent.json")
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT = os.environ.get("TELEGRAM_CHAT_ID", "")
MAX_STATE = 2000  # keep the de-dupe ledger from growing forever

PLATFORM_ICON = {
    "facebook": "📘",
    "instagram": "📸",
    "linkedin": "💼",
    "telegram": "✈️",
    "x": "✖️",
}


def post_hash(entry: dict) -> str:
    key = "|".join([
        str(entry.get("platform", "")),
        str(entry.get("message", "")),
        str(entry.get("link", "")),
        str(entry.get("image_url", "")),
    ])
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def render(entry: dict) -> str:
    platform = str(entry.get("platform", "")).lower()
    icon = PLATFORM_ICON.get(platform, "📝")
    header = f"{icon} *{platform.upper() or 'POST'}*"
    parts = [header, ""]
    msg = entry.get("message")
    if msg:
        parts.append(msg)
    link = entry.get("link")
    if link:
        parts.append(f"\n🔗 {link}")
    return "\n".join(parts)


def tg_send(entry: dict) -> tuple[bool, str]:
    if not (TOKEN and CHAT):
        return False, "missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID"
    image_url = entry.get("image_url")
    caption = render(entry)
    try:
        if image_url:
            url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
            data = up.urlencode({
                "chat_id": CHAT,
                "photo": image_url,
                "caption": caption,
                "parse_mode": "Markdown",
            }).encode()
        else:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            data = up.urlencode({
                "chat_id": CHAT,
                "text": caption,
                "parse_mode": "Markdown",
                "disable_web_page_preview": "false",
            }).encode()
        with ur.urlopen(ur.Request(url, data=data), timeout=20) as r:
            return 200 <= r.status < 300, f"http {r.status}"
    except Exception as e:
        return False, str(e)


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def main() -> None:
    items = load_json(QUEUE, [])
    if not isinstance(items, list):
        items = []

    already = set(load_json(STATE, []))

    pending = [e for e in items if isinstance(e, dict) and post_hash(e) not in already]

    if not (TOKEN and CHAT):
        print("missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID — skipping", file=sys.stderr)
        Path("/tmp/telegram_result.json").write_text(json.dumps({"sent": 0, "skipped": True}))
        return

    sent = 0
    failed = 0
    for entry in pending:
        ok, msg = tg_send(entry)
        if ok:
            sent += 1
            already.add(post_hash(entry))
            print(f"sent {entry.get('platform')}: {msg}")
        else:
            failed += 1
            print(f"FAILED {entry.get('platform')}: {msg}", file=sys.stderr)

    # Persist the de-dupe ledger (most-recent kept)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(list(already)[-MAX_STATE:], indent=2))

    Path("/tmp/telegram_result.json").write_text(json.dumps({
        "sent": sent,
        "failed": failed,
        "pending_before": len(pending),
    }))
    print(f"telegram: sent {sent} / failed {failed} / pending {len(pending)}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
