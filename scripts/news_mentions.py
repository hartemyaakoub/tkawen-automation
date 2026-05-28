#!/usr/bin/env python3
"""Poll Google News RSS for TKAWEN brand mentions. Diff vs the previous 7 days
of snapshots to identify fresh press."""

import json
import sys
import urllib.parse as up
import urllib.request as ur
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

BRANDS = [
    "Mystoq",
    "TKAWEN",
    "Algeria Certify",
    "LIQAA",
    "PharmaPro Algeria",
    "Hartem Yaakoub",
]
LANGS = [
    ("en", "US"),
    ("ar", "DZ"),
    ("fr", "FR"),
]
UA = "TKAWEN-NewsWatcher/1.0"
TIMEOUT = 25
DATA_DIR = Path(".data/news")


def fetch_rss(query: str, lang: str, country: str) -> list[dict]:
    url = (
        f"https://news.google.com/rss/search?"
        f"q={up.quote(query)}&hl={lang}&gl={country}&ceid={country}:{lang}"
    )
    try:
        req = ur.Request(url, headers={"User-Agent": UA})
        with ur.urlopen(req, timeout=TIMEOUT) as r:
            xml = r.read()
    except Exception as e:
        print(f"rss failed {query}@{lang}-{country}: {e}", file=sys.stderr)
        return []
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return []
    out = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        source = item.find("source")
        src = source.text.strip() if (source is not None and source.text) else ""
        if title and link:
            out.append({
                "title": title,
                "link": link,
                "published": pub,
                "source": src,
                "query": query,
                "lang": f"{lang}-{country}",
            })
    return out[:25]


def previous_links() -> set[str]:
    if not DATA_DIR.exists():
        return set()
    files = sorted(DATA_DIR.glob("mentions-*.json"))[-7:]
    seen: set[str] = set()
    for f in files:
        try:
            doc = json.loads(f.read_text())
            for r in doc.get("results", []):
                seen.add(r["link"])
        except Exception:
            continue
    return seen


def main() -> None:
    all_results: list[dict] = []
    for brand in BRANDS:
        for lang, country in LANGS:
            all_results.extend(fetch_rss(brand, lang, country))

    seen = previous_links()
    new = [r for r in all_results if r["link"] not in seen]

    print(json.dumps({
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "total": len(all_results),
            "new_today": len(new),
            "brands": BRANDS,
            "lang_country_pairs": LANGS,
        },
        "results": all_results,
        "new": new,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
