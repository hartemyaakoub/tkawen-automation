#!/usr/bin/env python3
"""Snapshot 5+ competitor sitemaps; diff vs yesterday; emit JSON.

Output structure:
  {
    "scanned_at": "...",
    "total_new": int,
    "total_seen": int,
    "by_competitor": [
      {"name": "...", "sitemap": "...", "new": [...], "removed": [...], "count": int}
    ]
  }
"""

import gzip
import json
import sys
import urllib.request as ur
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

COMPETITORS = [
    # e-commerce / Mystoq competitors
    {"name": "youcan",      "sitemap": "https://youcan.shop/sitemap.xml"},
    {"name": "shopify",     "sitemap": "https://www.shopify.com/sitemap.xml"},
    # credentialing / Algeria Certify competitors
    {"name": "accredible",  "sitemap": "https://www.accredible.com/sitemap.xml"},
    {"name": "credly",      "sitemap": "https://info.credly.com/sitemap.xml"},
    # video conferencing / LIQAA competitors
    {"name": "daily",       "sitemap": "https://www.daily.co/sitemap.xml"},
    {"name": "agora",       "sitemap": "https://www.agora.io/en/sitemap.xml"},
]

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
UA = "TKAWEN-CompetitorWatcher/1.0 (+https://tkawen.com)"
DATA_DIR = Path(".data/competitors")


def fetch(url: str) -> bytes:
    req = ur.Request(url, headers={"User-Agent": UA})
    data = ur.urlopen(req, timeout=25).read()
    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data


def parse_urls(xml_bytes: bytes, depth: int = 0) -> set[str]:
    """Return all <loc> values, recursing into sub-sitemaps up to depth 2."""
    out: set[str] = set()
    if depth > 2:
        return out
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return out
    tag = root.tag.split("}", 1)[-1]
    if tag == "urlset":
        for url in root.findall("sm:url/sm:loc", NS):
            if url.text:
                out.add(url.text.strip())
    elif tag == "sitemapindex":
        for sm in root.findall("sm:sitemap/sm:loc", NS):
            if sm.text:
                try:
                    out |= parse_urls(fetch(sm.text.strip()), depth + 1)
                except Exception:
                    continue
    return out


def previous_snapshot(name: str) -> set[str]:
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    p = DATA_DIR / f"snapshot-{name}-{yesterday}.json"
    if not p.exists():
        # fall back to most recent
        snaps = sorted(DATA_DIR.glob(f"snapshot-{name}-*.json"))
        if not snaps:
            return set()
        p = snaps[-1]
    try:
        return set(json.loads(p.read_text()))
    except Exception:
        return set()


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    by_competitor = []
    total_new = 0
    total_seen = 0

    for c in COMPETITORS:
        try:
            current = parse_urls(fetch(c["sitemap"]))
        except Exception as e:
            print(f"failed {c['name']}: {e}", file=sys.stderr)
            current = set()

        previous = previous_snapshot(c["name"])
        new = sorted(current - previous)
        removed = sorted(previous - current)
        total_new += len(new)
        total_seen += len(current)

        # Persist today's snapshot
        snap = DATA_DIR / f"snapshot-{c['name']}-{today}.json"
        snap.write_text(json.dumps(sorted(current), indent=2))

        by_competitor.append({
            "name": c["name"],
            "sitemap": c["sitemap"],
            "count": len(current),
            "new": new[:50],
            "removed": removed[:50],
        })

    output = {
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "total_new": total_new,
        "total_seen": total_seen,
        "by_competitor": by_competitor,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
