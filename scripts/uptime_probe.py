#!/usr/bin/env python3
"""Ping every TKAWEN site once. Append result to month-rolling JSON.

Output file structure (month-rolling, appended to):
  {
    "month": "2026-05",
    "sites": ["mystoq.com", ...],
    "runs": [
      {"ts": "...", "up": [...], "down": [...]}
    ]
  }

Also writes /tmp/uptime_now.json with just THIS run's summary for the workflow
to pick up output values.
"""

import json
import sys
import urllib.request as ur
from datetime import datetime
from pathlib import Path

SITES = [
    "https://mystoq.com/",
    "https://algeriacertify.com/",
    "https://tkawen.com/",
    "https://liqaa.io/",
    "https://pharmapro.tkawen.com/",
    "https://catalogue.tkawen.com/",
    "https://hartem.tkawen.com/",
    "https://brand.tkawen.com/",
    "https://trust.tkawen.com/",
    "https://design.tkawen.com/",
    "https://studio.tkawen.com/",
]

TIMEOUT = 10
UA = "TKAWEN-UptimeProbe/1.0"


def ping(url: str) -> tuple[bool, int | None]:
    try:
        req = ur.Request(url, headers={"User-Agent": UA}, method="HEAD")
        with ur.urlopen(req, timeout=TIMEOUT) as r:
            return r.status < 500, r.status
    except Exception:
        # HEAD might be blocked; fall back to GET
        try:
            req = ur.Request(url, headers={"User-Agent": UA})
            with ur.urlopen(req, timeout=TIMEOUT) as r:
                return r.status < 500, r.status
        except Exception:
            return False, None


def main() -> None:
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/uptime.json")
    now = datetime.utcnow().isoformat() + "Z"
    up: list[str] = []
    down: list[str] = []
    statuses: dict[str, int | None] = {}

    for u in SITES:
        ok, code = ping(u)
        statuses[u] = code
        if ok:
            up.append(u)
        else:
            down.append(u)

    this_run = {"ts": now, "up": up, "down": down, "statuses": statuses}

    if out_path.exists():
        try:
            doc = json.loads(out_path.read_text())
        except Exception:
            doc = {}
    else:
        doc = {}

    doc.setdefault("month", out_path.stem.replace("uptime-", ""))
    doc.setdefault("sites", SITES)
    doc.setdefault("runs", [])
    doc["runs"].append(this_run)
    # Keep file size sane: drop runs older than 31 days
    doc["runs"] = doc["runs"][-2000:]

    out_path.write_text(json.dumps(doc, indent=2))

    summary = {
        "this_run": {
            "ts": now,
            "up": len(up),
            "down": len(down),
            "down_sites": down,
        }
    }
    Path("/tmp/uptime_now.json").write_text(json.dumps(summary))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
