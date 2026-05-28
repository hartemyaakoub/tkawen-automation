#!/usr/bin/env python3
"""Send a weekly Telegram report comparing latest SR snapshot to last week's."""
import json, os
import urllib.request as ur
import urllib.parse as up
from pathlib import Path

TOKEN = os.environ.get("TOKEN", "")
CHAT  = os.environ.get("CHAT", "")
DATA  = Path("data/sr-history.json")


def fmt_delta(now: int | None, prev: int | None) -> str:
    if now is None: return "—"
    if prev is None or now == prev: return f"{now}"
    sign = "▲" if now > prev else "▼"
    return f"{now} ({sign}{abs(now - prev)})"


def main() -> int:
    if not DATA.exists() or not (TOKEN and CHAT):
        return 0
    hist = json.loads(DATA.read_text())
    if not hist:
        return 0
    cur = hist[-1]
    prev = hist[-2] if len(hist) > 1 else {}
    msg = (
        "📊 *StartupRanking — تقرير أسبوعي*\n\n"
        f"🌍 Global Rank: {fmt_delta(cur.get('global_rank'), prev.get('global_rank'))}\n"
        f"🇩🇿 Algeria Rank: {fmt_delta(cur.get('algeria_rank'), prev.get('algeria_rank'))}\n"
        f"⭐ SR Score: {fmt_delta(cur.get('sr_score'), prev.get('sr_score'))}\n"
        f"🔗 SR Web: {fmt_delta(cur.get('sr_web'), prev.get('sr_web'))}\n"
        f"📱 SR Social: {fmt_delta(cur.get('sr_social'), prev.get('sr_social'))}\n\n"
        f"https://www.startupranking.com/startup/mystoq"
    )
    ur.urlopen(ur.Request(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data=up.urlencode({"chat_id": CHAT, "text": msg, "parse_mode": "Markdown"}).encode()
    ), timeout=15)
    return 0


if __name__ == "__main__":
    main()
