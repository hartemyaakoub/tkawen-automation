#!/usr/bin/env python3
"""Search Wikipedia (all languages) + Wikidata for TKAWEN brand mentions.

Outputs JSON with structure:
  {
    "scanned_at": "2026-05-28T22:00:00Z",
    "queries": [...],
    "results": [{title, url, snippet, query, lang}],
    "new": [...]   # diff vs previous run
  }
"""

import json
import os
import sys
import urllib.parse as up
import urllib.request as ur
from datetime import datetime
from pathlib import Path

BRANDS = [
    "Mystoq",
    "TKAWEN",
    "Algeria Certify",
    "LIQAA",
    "PharmaPro Algeria",
    "Hartem Yaakoub",
    "حرتام يعقوب",
    "ميستوك",
]

LANGS = ["en", "ar", "fr"]
TIMEOUT = 20
UA = "TKAWEN-WikipediaWatcher/1.0 (+https://tkawen.com)"


def search_wikipedia(query: str, lang: str) -> list[dict]:
    url = (
        f"https://{lang}.wikipedia.org/w/api.php?"
        f"action=query&format=json&list=search&srlimit=10"
        f"&srsearch={up.quote(query)}"
    )
    req = ur.Request(url, headers={"User-Agent": UA})
    try:
        with ur.urlopen(req, timeout=TIMEOUT) as r:
            data = json.load(r)
    except Exception as e:
        print(f"wikipedia search failed for {query}@{lang}: {e}", file=sys.stderr)
        return []
    out = []
    for hit in data.get("query", {}).get("search", []):
        title = hit.get("title", "")
        snippet = hit.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
        out.append({
            "title": title,
            "url": f"https://{lang}.wikipedia.org/wiki/{up.quote(title.replace(' ', '_'))}",
            "snippet": snippet,
            "query": query,
            "lang": lang,
        })
    return out


def load_previous() -> set[str]:
    data_dir = Path(".data")
    if not data_dir.exists():
        return set()
    files = sorted(data_dir.glob("wikipedia-mentions-*.json"))
    if len(files) < 1:
        return set()
    previous = set()
    for f in files[-7:]:
        try:
            doc = json.loads(f.read_text())
            for r in doc.get("results", []):
                previous.add(r["url"])
        except Exception:
            continue
    return previous


def main() -> None:
    all_results: list[dict] = []
    for query in BRANDS:
        for lang in LANGS:
            hits = search_wikipedia(query, lang)
            all_results.extend(hits)

    previous = load_previous()
    new_results = [r for r in all_results if r["url"] not in previous]

    output = {
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "queries": BRANDS,
        "languages": LANGS,
        "results": all_results,
        "new": new_results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
