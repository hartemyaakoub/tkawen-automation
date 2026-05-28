#!/usr/bin/env python3
"""Free-tier backlink prospector. Queries DuckDuckGo HTML for brand mentions
without ours-domain links, then emits a JSON prospect list.

Output:
  {
    "summary": {total_prospects, total_queries},
    "prospects": [{url, title, query, snippet}]
  }
"""

import json
import re
import sys
import urllib.parse as up
import urllib.request as ur
from datetime import datetime

QUERIES = [
    # Brand + non-domain mentions
    '"Algeria Certify" -site:algeriacertify.com',
    '"Mystoq" -site:mystoq.com -site:mystoq.online',
    '"TKAWEN" -site:tkawen.com -site:tkawen.online',
    '"LIQAA" -site:liqaa.io',
    '"PharmaPro Algeria" -site:pharmapro.tkawen.com',
    # Topical mentions where we should be cited
    "e-commerce Algeria cash on delivery",
    "Algeria certification platform digital credentials",
    "Algeria video conferencing platform",
    "MENA e-commerce platform",
    "Algerian SaaS startup",
]

UA = "Mozilla/5.0 (compatible; TKAWEN-BacklinkProspector/1.0)"
TIMEOUT = 30
RESULT_RE = re.compile(
    r'<a\s+rel="nofollow"\s+class="result__a"\s+href="([^"]+)"[^>]*>(.*?)</a>',
    re.DOTALL | re.IGNORECASE,
)


def query_ddg(q: str) -> list[dict]:
    url = f"https://html.duckduckgo.com/html/?q={up.quote(q)}"
    req = ur.Request(url, headers={"User-Agent": UA})
    try:
        with ur.urlopen(req, timeout=TIMEOUT) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"ddg query failed for {q}: {e}", file=sys.stderr)
        return []

    out: list[dict] = []
    for m in RESULT_RE.finditer(html):
        href, title_html = m.groups()
        # DDG wraps with /l/?uddg=...
        parsed = up.urlparse(href)
        qs = up.parse_qs(parsed.query)
        real = qs.get("uddg", [href])[0]
        title = re.sub(r"<[^>]+>", "", title_html).strip()
        # Skip our own
        if any(d in real for d in [
            "tkawen.com", "tkawen.online", "mystoq.com", "algeriacertify.com",
            "liqaa.io", "pharmapro.tkawen.com",
        ]):
            continue
        out.append({"url": real, "title": title[:200], "query": q})
    return out[:30]


def main() -> None:
    seen: set[str] = set()
    prospects: list[dict] = []
    for q in QUERIES:
        for hit in query_ddg(q):
            if hit["url"] in seen:
                continue
            seen.add(hit["url"])
            prospects.append(hit)

    out = {
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "summary": {"total_prospects": len(prospects), "total_queries": len(QUERIES)},
        "prospects": prospects,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
