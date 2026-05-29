#!/usr/bin/env python3
"""Track where TKAWEN domains rank on DDG for their target keywords."""

import json
import re
import sys
import urllib.parse as up
import urllib.request as ur
from datetime import datetime

# (keyword, target_domain) — the domain we *want* to rank for that keyword
TARGETS = [
    ("Mystoq", "mystoq.com"),
    ("Mystoq Algeria", "mystoq.com"),
    ("e-commerce Algeria platform", "mystoq.com"),
    ("Algeria Certify", "algeriacertify.com"),
    ("Algeria digital credentials", "algeriacertify.com"),
    ("certificat Algerie en ligne", "algeriacertify.com"),
    ("LIQAA", "liqaa.io"),
    ("LIQAA video meeting", "liqaa.io"),
    ("liqaa.io", "liqaa.io"),
    ("PharmaPro Algeria", "pharmapro.tkawen.com"),
    ("logiciel pharmacie algerie", "pharmapro.tkawen.com"),
    ("TKAWEN group", "tkawen.com"),
    ("TKAWEN startup", "tkawen.com"),
    ("Hartem Yaakoub", "hartem.tkawen.com"),
    ("Hartem Yaakoub founder", "hartem.tkawen.com"),
    ("catalogue.tkawen.com", "catalogue.tkawen.com"),
    ("catalogue TKAWEN", "catalogue.tkawen.com"),
]

UA = "Mozilla/5.0 (compatible; TKAWEN-SERPProbe/1.0)"
TIMEOUT = 25
DDG_RE = re.compile(
    r'<a\s+rel="nofollow"\s+class="result__a"\s+href="([^"]+)"',
    re.DOTALL | re.IGNORECASE,
)


def search(q: str) -> list[str]:
    url = f"https://html.duckduckgo.com/html/?q={up.quote(q)}"
    try:
        req = ur.Request(url, headers={"User-Agent": UA})
        with ur.urlopen(req, timeout=TIMEOUT) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"search failed for {q}: {e}", file=sys.stderr)
        return []
    urls = []
    for href in DDG_RE.findall(html):
        parsed = up.urlparse(href)
        qs = up.parse_qs(parsed.query)
        urls.append(qs.get("uddg", [href])[0])
    return urls[:30]


def position_of(target: str, urls: list[str]) -> int | None:
    for i, u in enumerate(urls, 1):
        if target in u:
            return i
    return None


def main() -> None:
    tracked = []
    in_top10 = 0
    for q, target in TARGETS:
        urls = search(q)
        pos = position_of(target, urls)
        tracked.append({
            "keyword": q,
            "target": target,
            "position": pos,
            "first_result": urls[0] if urls else None,
        })
        if pos and pos <= 10:
            in_top10 += 1

    total = len(TARGETS)
    out = {
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "tracked": total,
            "in_top_10": in_top10,
            "top_10_percent": round(100 * in_top10 / max(total, 1), 1),
        },
        "tracked": tracked,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
