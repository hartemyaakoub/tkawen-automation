#!/usr/bin/env python3
"""Push sitemap URLs to Bing + Yandex IndexNow.

Usage:
    indexnow_push.py <host> <key> <sitemap_url> [--since-hours N]

Without --since-hours: submits every <loc> in the sitemap (full daily push).
With --since-hours N: submits ONLY URLs whose <lastmod> is within the last N
hours — this is the "fresh content" mode that avoids re-pinging the entire
site every few hours. URLs with no <lastmod> are skipped in this mode (we
can't tell whether they changed, so we don't spam IndexNow with them).
"""
import sys, json, gzip
import urllib.request as ur
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

# ---- arg parsing (positional host/key/sitemap + optional --since-hours) ----
args = sys.argv[1:]
since_hours: int | None = None
if "--since-hours" in args:
    i = args.index("--since-hours")
    try:
        since_hours = int(args[i + 1])
    except (IndexError, ValueError):
        print("--since-hours needs an integer"); sys.exit(2)
    del args[i:i + 2]

if len(args) < 3:
    print("usage: indexnow_push.py <host> <key> <sitemap_url> [--since-hours N]")
    sys.exit(2)
host, key, sitemap = args[0], args[1], args[2]

# Recursive sitemap fetch — handles sitemap-index.xml that points to other sitemaps
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def fetch(url: str) -> bytes:
    req = ur.Request(url, headers={"User-Agent": "TKAWEN-IndexNow/1.0"})
    data = ur.urlopen(req, timeout=20).read()
    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data


def parse_urls(xml_bytes: bytes) -> list[tuple[str, str | None]]:
    """Return (loc, lastmod) pairs, recursing into sub-sitemaps."""
    out: list[tuple[str, str | None]] = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        print(f"parse error: {e}", file=sys.stderr); return out
    tag = root.tag.split('}', 1)[-1]
    if tag == "sitemapindex":
        for sm in root.findall("sm:sitemap/sm:loc", NS):
            try:
                out.extend(parse_urls(fetch(sm.text.strip())))
            except Exception as e:
                print(f"sub-sitemap failed {sm.text}: {e}", file=sys.stderr)
    elif tag == "urlset":
        for u in root.findall("sm:url", NS):
            loc = u.find("sm:loc", NS)
            if loc is None or not loc.text:
                continue
            lm = u.find("sm:lastmod", NS)
            out.append((loc.text.strip(),
                        lm.text.strip() if lm is not None and lm.text else None))
    return out


def is_fresh(lastmod: str | None, cutoff: datetime) -> bool:
    if not lastmod:
        return False
    try:
        dt = datetime.fromisoformat(lastmod.replace("Z", "+00:00"))
    except ValueError:
        return False
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt >= cutoff


def push(endpoint: str, urls: list[str]) -> tuple[int, str]:
    payload = json.dumps({
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": urls,
    }).encode()
    req = ur.Request(endpoint, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        r = ur.urlopen(req, timeout=30)
        return r.status, r.read().decode()[:200]
    except Exception as e:
        return 0, str(e)


def main():
    print(f"sitemap: {sitemap}")
    pairs = parse_urls(fetch(sitemap))
    print(f"collected {len(pairs)} URLs")

    if since_hours is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)
        urls = [loc for loc, lm in pairs if is_fresh(lm, cutoff)]
        print(f"fresh-mode: {len(urls)} URLs modified in last {since_hours}h")
    else:
        urls = [loc for loc, _ in pairs]

    if not urls:
        print("nothing to push"); return 0

    # IndexNow allows up to 10000 URLs per request; we're well under that.
    s_b, msg_b = push("https://api.indexnow.org/indexnow", urls)
    s_y, msg_y = push("https://yandex.com/indexnow", urls)
    print(f"Bing   → HTTP {s_b}")
    print(f"Yandex → HTTP {s_y}")
    # 200/202 are both success in IndexNow protocol
    return 0 if (s_b in (200, 202) and s_y in (200, 202)) else 1


if __name__ == "__main__":
    sys.exit(main())
