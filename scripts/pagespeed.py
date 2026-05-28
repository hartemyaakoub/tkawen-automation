#!/usr/bin/env python3
"""Run Google PSI on every site's homepage + one inner page (mobile + desktop).

Output:
  {
    "summary": {total, failing},
    "by_url": [{url, strategy, performance, lcp, cls, fcp, tbt, ttfb}]
  }

Failing = performance score < 0.75.
"""

import json
import os
import sys
import urllib.parse as up
import urllib.request as ur
from datetime import datetime

URLS = [
    "https://mystoq.com/",
    "https://mystoq.com/tools/",
    "https://algeriacertify.com/",
    "https://algeriacertify.com/atlas/",
    "https://tkawen.com/",
    "https://tkawen.com/research/",
    "https://liqaa.io/",
    "https://pharmapro.tkawen.com/",
    "https://catalogue.tkawen.com/",
]
STRATEGIES = ["mobile", "desktop"]
ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
TIMEOUT = 60
KEY = os.environ.get("PSI_API_KEY", "")


def measure(url: str, strategy: str) -> dict:
    qs = {
        "url": url,
        "strategy": strategy,
        "category": "performance",
    }
    if KEY:
        qs["key"] = KEY
    req_url = f"{ENDPOINT}?{up.urlencode(qs)}"
    try:
        with ur.urlopen(req_url, timeout=TIMEOUT) as r:
            data = json.load(r)
    except Exception as e:
        return {"url": url, "strategy": strategy, "error": str(e)}

    lh = data.get("lighthouseResult", {})
    audits = lh.get("audits", {})
    cat = lh.get("categories", {}).get("performance", {})

    def num(audit_id, field="numericValue"):
        a = audits.get(audit_id, {})
        v = a.get(field)
        return round(v, 2) if isinstance(v, (int, float)) else None

    return {
        "url": url,
        "strategy": strategy,
        "performance": cat.get("score"),
        "lcp": num("largest-contentful-paint"),
        "cls": num("cumulative-layout-shift"),
        "fcp": num("first-contentful-paint"),
        "tbt": num("total-blocking-time"),
        "ttfb": num("server-response-time"),
    }


def main() -> None:
    rows = []
    for u in URLS:
        for s in STRATEGIES:
            row = measure(u, s)
            rows.append(row)

    failing = sum(
        1 for r in rows
        if isinstance(r.get("performance"), (int, float)) and r["performance"] < 0.75
    )
    out = {
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "summary": {"total": len(rows), "failing": failing},
        "by_url": rows,
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
