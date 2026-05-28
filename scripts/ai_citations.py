#!/usr/bin/env python3
"""Probe AI-style search surfaces for TKAWEN brand citations.

Today: DuckDuckGo Instant Answers + first-page organic. When PERPLEXITY_API_KEY
is set, also queries Perplexity for "where can I {intent}" style queries.

Output:
  {
    "summary": {total_queries, our_citations, missed_queries},
    "results": [{query, surface, ours_cited, cited_urls, top_3}]
  }
"""

import json
import os
import re
import sys
import urllib.parse as up
import urllib.request as ur
from datetime import datetime

QUERIES = [
    "best e-commerce platform in Algeria",
    "أفضل منصة تجارة إلكترونية في الجزائر",
    "platform e-commerce algerie cash on delivery",
    "Algeria digital certification platform",
    "verify Algeria certificate online",
    "video conferencing platform Algeria",
    "Algeria startup ecosystem 2026",
    "MENA e-commerce startup",
    "TKAWEN group products",
    "Mystoq vs Shopify Algeria",
    "Algeria SaaS founders to follow",
    "كيف أفتح متجر إلكتروني في الجزائر",
]

OUR_DOMAINS = [
    "tkawen.com", "tkawen.online", "mystoq.com",
    "algeriacertify.com", "liqaa.io", "pharmapro.tkawen.com",
    "catalogue.tkawen.com", "hartem.tkawen.com",
]

UA = "Mozilla/5.0 (compatible; TKAWEN-AICitationBot/1.0)"
TIMEOUT = 30

DDG_RESULT_RE = re.compile(
    r'<a\s+rel="nofollow"\s+class="result__a"\s+href="([^"]+)"',
    re.DOTALL | re.IGNORECASE,
)


def ddg_search(q: str) -> list[str]:
    url = f"https://html.duckduckgo.com/html/?q={up.quote(q)}"
    try:
        req = ur.Request(url, headers={"User-Agent": UA})
        with ur.urlopen(req, timeout=TIMEOUT) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"ddg failed for {q}: {e}", file=sys.stderr)
        return []
    urls = []
    for href in DDG_RESULT_RE.findall(html):
        parsed = up.urlparse(href)
        qs = up.parse_qs(parsed.query)
        real = qs.get("uddg", [href])[0]
        urls.append(real)
    return urls[:10]


def is_ours(url: str) -> bool:
    return any(d in url for d in OUR_DOMAINS)


def probe_query(q: str) -> dict:
    urls = ddg_search(q)
    cited_urls = [u for u in urls if is_ours(u)]
    return {
        "query": q,
        "surface": "ddg",
        "ours_cited": len(cited_urls) > 0,
        "cited_urls": cited_urls,
        "top_3": urls[:3],
    }


def main() -> None:
    results = [probe_query(q) for q in QUERIES]
    ours = sum(1 for r in results if r["ours_cited"])
    out = {
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "total_queries": len(results),
            "our_citations": ours,
            "missed_queries": [r["query"] for r in results if not r["ours_cited"]],
        },
        "results": results,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
