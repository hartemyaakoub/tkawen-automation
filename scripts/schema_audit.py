#!/usr/bin/env python3
"""Crawl 30 URLs per TKAWEN site, extract JSON-LD, validate.

Output:
  {
    "scanned_at": "...",
    "summary": {pages_scanned, errors_total, pages_without_schema},
    "by_site": [{host, pages, errors, missing, samples: [...]}]
  }
"""

import json
import re
import sys
import urllib.request as ur
import xml.etree.ElementTree as ET
from datetime import datetime

SITES = [
    "https://mystoq.com/sitemap.xml",
    "https://algeriacertify.com/sitemap.xml",
    "https://tkawen.com/sitemap.xml",
    "https://liqaa.io/sitemap.xml",
    "https://pharmapro.tkawen.com/sitemap.xml",
    "https://catalogue.tkawen.com/sitemap.xml",
]
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
UA = "TKAWEN-SchemaAudit/1.0 (+https://tkawen.com)"
PAGES_PER_SITE = 30
TIMEOUT = 20

SCRIPT_RE = re.compile(
    r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)


def fetch(url: str) -> str:
    req = ur.Request(url, headers={"User-Agent": UA})
    with ur.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_bytes(url: str) -> bytes:
    req = ur.Request(url, headers={"User-Agent": UA})
    return ur.urlopen(req, timeout=TIMEOUT).read()


def list_urls(sitemap_url: str, limit: int) -> list[str]:
    try:
        root = ET.fromstring(fetch_bytes(sitemap_url))
    except Exception:
        return []
    tag = root.tag.split("}", 1)[-1]
    if tag == "urlset":
        return [u.text.strip() for u in root.findall("sm:url/sm:loc", NS) if u.text][:limit]
    if tag == "sitemapindex":
        urls: list[str] = []
        for sm in root.findall("sm:sitemap/sm:loc", NS):
            if not sm.text:
                continue
            try:
                urls.extend(list_urls(sm.text.strip(), limit - len(urls)))
            except Exception:
                continue
            if len(urls) >= limit:
                break
        return urls[:limit]
    return []


def validate_jsonld(blob: str) -> tuple[bool, str]:
    try:
        doc = json.loads(blob)
    except json.JSONDecodeError as e:
        return False, f"invalid JSON: {e}"
    if isinstance(doc, list):
        docs = doc
    else:
        docs = [doc]
    for d in docs:
        if not isinstance(d, dict):
            return False, "not an object"
        if "@context" not in d:
            return False, "missing @context"
        if "@type" not in d and "@graph" not in d:
            return False, "missing @type/@graph"
    return True, ""


def audit_site(sitemap_url: str) -> dict:
    host = sitemap_url.split("/", 3)[2]
    urls = list_urls(sitemap_url, PAGES_PER_SITE)
    pages = 0
    errors = 0
    missing = 0
    samples: list[dict] = []

    for u in urls:
        try:
            html = fetch(u)
        except Exception as e:
            samples.append({"url": u, "error": f"fetch failed: {e}"})
            continue
        pages += 1
        scripts = SCRIPT_RE.findall(html)
        if not scripts:
            missing += 1
            continue
        for s in scripts:
            ok, msg = validate_jsonld(s.strip())
            if not ok:
                errors += 1
                samples.append({"url": u, "error": msg})

    return {
        "host": host,
        "pages": pages,
        "errors": errors,
        "missing": missing,
        "samples": samples[:10],
    }


def main() -> None:
    by_site = []
    pages_total = 0
    errors_total = 0
    missing_total = 0
    for sm in SITES:
        try:
            result = audit_site(sm)
        except Exception as e:
            result = {"host": sm, "error": str(e), "pages": 0, "errors": 0, "missing": 0, "samples": []}
        by_site.append(result)
        pages_total += result.get("pages", 0)
        errors_total += result.get("errors", 0)
        missing_total += result.get("missing", 0)

    out = {
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "pages_scanned": pages_total,
            "errors_total": errors_total,
            "pages_without_schema": missing_total,
        },
        "by_site": by_site,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
