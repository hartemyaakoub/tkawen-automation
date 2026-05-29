#!/usr/bin/env python3
"""Scrape Mystoq's public StartupRanking page and append to history."""
import json, re, sys, datetime
import urllib.request as ur
from pathlib import Path

URL = "https://www.startupranking.com/startup/mystoq"
DATA = Path(".data/sr/history.json")
DATA.parent.mkdir(parents=True, exist_ok=True)


def fetch() -> str:
    req = ur.Request(URL, headers={"User-Agent": "Mozilla/5.0 TKAWEN-SR/1.0"})
    return ur.urlopen(req, timeout=20).read().decode("utf-8", errors="ignore")


def parse(html: str) -> dict:
    """Best-effort extraction of the 4 main metrics from SR's HTML."""
    def num(pat: str) -> int | None:
        m = re.search(pat, html, re.S)
        if not m:
            return None
        return int(re.sub(r"[^\d]", "", m.group(1)))

    return {
        "ts": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "global_rank":  num(r"Startup Ranking[^\d]*([\d,]+)"),
        "algeria_rank": num(r"Algeria\s*([\d,]+)"),
        "sr_score":     num(r"SR Score[^\d]*([\d,]+)"),
        "sr_web":       num(r"SR Web[^\d]*([\d,]+)"),
        "sr_social":    num(r"SR Social[^\d]*([\d,]+)"),
    }


def main() -> int:
    snapshot = parse(fetch())
    history = []
    if DATA.exists():
        try:
            history = json.loads(DATA.read_text())
        except json.JSONDecodeError:
            history = []
    history.append(snapshot)
    DATA.write_text(json.dumps(history, indent=2, ensure_ascii=False))
    print(json.dumps(snapshot, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
