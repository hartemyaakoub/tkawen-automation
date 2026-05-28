#!/usr/bin/env python3
"""Sample 10 pages per site, extract anchors, HEAD-check each, report 4xx/5xx."""

import json
import re
import sys
import urllib.parse as up
import urllib.request as ur
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
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
UA = "TKAWEN-LinkChecker/1.0 (+https://tkawen.com)"
PAGES_PER_SITE = 10
TIMEOUT = 15
HREF_RE = re.compile(r'<a\s+[^>]*href="([^"#?]+)[^"]*"', re.IGNORECASE)


def fetch_bytes(url: str) -> bytes:
    req = ur.Request(url, headers={"User-Agent": UA})
    return ur.urlopen(req, timeout=TIMEOUT).read()


def fetch_text(url: str) -> str:
    return fetch_bytes(url).decode("utf-8", errors="replace")


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


def extract_links(html: str, base: str) -> set[str]:
    out: set[str] = set()
    for href in HREF_RE.findall(html):
        if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
            continue
        if href.startswith("//"):
            href = "https:" + href
        if not href.startswith("http"):
            href = up.urljoin(base, href)
        if href.startswith("http"):
            out.add(href.split("#")[0].split("?")[0])
    return out


def check(url: str) -> tuple[str, int | None, str | None]:
    try:
        req = ur.Request(url, headers={"User-Agent": UA}, method="HEAD")
        with ur.urlopen(req, timeout=TIMEOUT) as r:
            return url, r.status, None
    except ur.HTTPError as e:
        return url, e.code, str(e.reason)
    except Exception as e:
        return url, None, str(e)


def main() -> None:
    all_links: set[str] = set()

    for sm in SITES:
        pages = list_urls(sm, PAGES_PER_SITE)
        for p in pages:
            try:
                html = fetch_text(p)
            except Exception:
                continue
            all_links |= extract_links(html, p)

    checked: list[dict] = []
    broken: list[dict] = []

    with ThreadPoolExecutor(max_workers=20) as ex:
        for fut in as_completed(ex.submit(check, u) for u in list(all_links)[:300]):
            url, code, err = fut.result()
            rec = {"url": url, "code": code, "error": err}
            checked.append(rec)
            if code is None or (code and code >= 400):
                broken.append(rec)

    print(json.dumps({
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "summary": {"checked": len(checked), "broken": len(broken)},
        "broken_links": broken[:100],
    }, indent=2))


if __name__ == "__main__":
    main()
