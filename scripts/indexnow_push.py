#!/usr/bin/env python3
"""Push every URL of a sitemap to Bing + Yandex IndexNow."""
import sys, json, gzip, io
import urllib.request as ur
import xml.etree.ElementTree as ET

if len(sys.argv) < 4:
    print("usage: indexnow_push.py <host> <key> <sitemap_url>"); sys.exit(2)
host, key, sitemap = sys.argv[1], sys.argv[2], sys.argv[3]

# Recursive sitemap fetch — handles sitemap-index.xml that points to other sitemaps
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def fetch(url: str) -> bytes:
    req = ur.Request(url, headers={"User-Agent": "TKAWEN-IndexNow/1.0"})
    data = ur.urlopen(req, timeout=20).read()
    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data


def parse_urls(xml_bytes: bytes) -> list[str]:
    """Return all <loc> values, recursing into sub-sitemaps."""
    out: list[str] = []
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
        for u in root.findall("sm:url/sm:loc", NS):
            if u.text:
                out.append(u.text.strip())
    return out


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
    urls = parse_urls(fetch(sitemap))
    print(f"collected {len(urls)} URLs")
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
