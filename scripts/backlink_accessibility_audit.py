#!/usr/bin/env python3
"""Backlink accessibility audit.

Finds third-party pages that MENTION TKAWEN brands but are hard to reach from
Google, and classifies *why* they are hard to reach. The whole point is the gap
between Google and the rest of the indexed web: Google is the engine most likely
to bury, drop, or never-index a small brand's mentions, while Bing/DuckDuckGo
still surface them.

Strategy (100% free, no API keys):
  1. For each brand, query the NON-Google index — DuckDuckGo HTML (which is
     powered by Bing's crawl, so it is precisely the "everything except Google"
     view) — for the brand phrase to harvest external mentions. Bing's own HTML
     endpoint serves degraded bot-junk to non-browser clients, so it is wired
     up but OFF by default (USE_BING) and its redirect wrapper is decoded.
  2. Deduplicate by URL across engines and brands; drop our own domains.
  3. For every mention URL, run an HTTP liveness check (live / redirect /
     broken / timeout) — that catches broken & orphaned backlinks.
  4. Best-effort Google indexation probe per URL (exact-URL query). Google
     aggressively rate-limits scrapers, so this degrades gracefully and records
     `indexed` / `not_found` / `inconclusive` rather than pretending certainty.
  5. Classify each mention into an accessibility bucket and emit JSON.

Output:
  {
    "scanned_at": "...Z",
    "summary": {total_mentions, by_bucket, by_engine, engines, brands},
    "buckets": {
      "broken_or_orphaned": [...],   # link is dead / times out
      "not_indexed_by_google": [...],# on Bing/DDG, Google probe says not_found
      "low_rank_platform": [...],    # lives on a low-authority host Google buries
      "google_inconclusive": [...],  # probe blocked — needs manual check
      "visible": [...]               # alive AND Google says indexed
    },
    "mentions": [ {url, host, brand, engines, http, google, bucket, title} ]
  }
"""

import json
import re
import sys
import time
import urllib.parse as up
import urllib.request as ur
from datetime import datetime

# --- our own properties: never report these as "external" mentions ----------
OWN_DOMAINS = [
    "tkawen.com", "tkawen.online", "tkawen.dz", "takawen.dz",
    "mystoq.com", "mystoq.online",
    "algeriacertify.com",
    "liqaa.io",
    "pharmapro.tkawen.com",
    "catalogue.tkawen.com", "track.tkawen.com", "trust.tkawen.com",
    "brand.tkawen.com", "hartem.tkawen.com",
]

# --- brand -> the exact search phrase that disambiguates it ------------------
BRANDS = {
    "Mystoq": '"Mystoq" ecommerce',
    "TKAWEN": '"TKAWEN" platform Algeria',
    "Algeria Certify": '"Algeria Certify"',
    "AlgeriaCertify": '"AlgeriaCertify"',
    "LIQAA": '"liqaa.io"',
    "PharmaPro Algeria": '"PharmaPro" Algeria pharmacy',
    "Hartem Yaakoub": '"Hartem Yaakoub"',
}

# Hosts that carry backlinks but that Google routinely ranks low / treats as
# low-authority UGC or auto-generated. A mention living *only* here is "hard to
# reach from Google" almost by definition.
LOW_RANK_HOSTS = {
    "vocal.media", "openpr.com", "medium.com", "issuu.com", "scribd.com",
    "slideshare.net", "pinterest.com", "reddit.com", "quora.com",
    "facebook.com", "m.facebook.com", "twitter.com", "x.com",
    "similarweb.com", "statvoo.com", "whois.com", "site-stats.org",
    "crunchbase.com", "f6s.com", "startupranking.com", "saashub.com",
    "blogspot.com", "wordpress.com", "wixsite.com", "weebly.com",
}

UA = "Mozilla/5.0 (compatible; TKAWEN-BacklinkAccessibilityAudit/1.0)"
TIMEOUT = 25
PER_QUERY_CAP = 20
GOOGLE_PROBE = True  # set False to skip Google probing entirely
USE_BING = False     # Bing HTML serves degraded bot-junk to non-browsers; off


def _http_get(url: str, headers: dict | None = None) -> str:
    req = ur.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with ur.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", errors="replace")


def _host(url: str) -> str:
    try:
        return up.urlparse(url).netloc.lower().lstrip("www.")
    except Exception:
        return ""


def _is_ours(url: str) -> bool:
    h = _host(url)
    return any(h == d or h.endswith("." + d) or d in url for d in OWN_DOMAINS)


# --- search engines (non-Google) --------------------------------------------
_DDG_RE = re.compile(
    r'<a\s+rel="nofollow"\s+class="result__a"\s+href="([^"]+)"[^>]*>(.*?)</a>',
    re.DOTALL | re.IGNORECASE,
)


def search_ddg(query: str) -> list[tuple[str, str]]:
    """DuckDuckGo HTML endpoint -> [(url, title)]."""
    url = f"https://html.duckduckgo.com/html/?q={up.quote(query)}"
    try:
        html = _http_get(url)
    except Exception as e:
        print(f"ddg failed [{query}]: {e}", file=sys.stderr)
        return []
    out = []
    for m in _DDG_RE.finditer(html):
        href, title_html = m.groups()
        qs = up.parse_qs(up.urlparse(href).query)
        real = qs.get("uddg", [href])[0]
        title = re.sub(r"<[^>]+>", "", title_html).strip()
        out.append((real, title[:200]))
    return out[:PER_QUERY_CAP]


import base64

_BING_RE = re.compile(
    r'<h2[^>]*>\s*<a[^>]*href="(http[^"]+)"[^>]*>(.*?)</a>',
    re.DOTALL | re.IGNORECASE,
)


def _decode_bing(href: str) -> str:
    """Bing wraps real targets in /ck/a?...&u=a1<base64url>. Unwrap them."""
    if "bing.com/ck/a" not in href:
        return href
    u = up.parse_qs(up.urlparse(href).query).get("u", [""])[0]
    if u.startswith("a1"):
        b = u[2:]
        b += "=" * (-len(b) % 4)
        try:
            return base64.urlsafe_b64decode(b).decode("utf-8", "replace")
        except Exception:
            return href
    return href


def search_bing(query: str) -> list[tuple[str, str]]:
    """Bing HTML results -> [(url, title)]. Disabled by default (USE_BING):
    Bing's HTML endpoint serves a generic/degraded result set to non-browser
    clients, so it is unreliable for automation. Kept for manual/debug use."""
    if not USE_BING:
        return []
    url = f"https://www.bing.com/search?q={up.quote(query)}&count={PER_QUERY_CAP}"
    try:
        html = _http_get(url, {"Accept-Language": "en-US,en;q=0.9"})
    except Exception as e:
        print(f"bing failed [{query}]: {e}", file=sys.stderr)
        return []
    out = []
    for m in _BING_RE.finditer(html):
        href, title_html = m.groups()
        real = _decode_bing(href)
        if "bing.com" in _host(real):
            continue
        title = re.sub(r"<[^>]+>", "", title_html).strip()
        out.append((real, title[:200]))
    return out[:PER_QUERY_CAP]


# --- per-URL probes ----------------------------------------------------------
def http_status(url: str) -> dict:
    """Liveness check. Returns {state, code} where state in
    live/redirect/broken/timeout/error."""
    req = ur.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with ur.urlopen(req, timeout=TIMEOUT) as r:
            code = r.getcode()
            final = r.geturl()
            redirected = _host(final) != _host(url)
            return {
                "state": "redirect" if redirected else "live",
                "code": code,
                "final_url": final if redirected else url,
            }
    except ur.HTTPError as e:
        # 401/403/429 = the page is alive but blocks automated checkers
        # (Crunchbase, Medium, YouTube...). That is NOT a broken link.
        state = "blocked" if e.code in (401, 403, 429) else "broken"
        return {"state": state, "code": e.code, "final_url": url}
    except TimeoutError:
        return {"state": "timeout", "code": None, "final_url": url}
    except Exception as e:
        return {"state": "error", "code": None, "error": str(e)[:120],
                "final_url": url}


def google_indexed(url: str) -> str:
    """Best-effort: is this exact URL indexed by Google? Returns
    indexed / not_found / inconclusive. Google blocks scrapers hard, so
    'inconclusive' is the honest default when we get a consent/429 wall."""
    if not GOOGLE_PROBE:
        return "inconclusive"
    q = f'"{url.rstrip("/")}"'
    g = f"https://www.google.com/search?q={up.quote(q)}&num=10&hl=en"
    try:
        html = _http_get(g, {"Accept-Language": "en-US,en;q=0.9"})
    except Exception:
        return "inconclusive"
    low = html.lower()
    if "did not match any documents" in low or "aucun document ne correspond" in low:
        return "not_found"
    # consent / captcha / unusual-traffic walls => we cannot tell
    if ("consent.google.com" in low or "unusual traffic" in low
            or "captcha" in low or len(html) < 2000):
        return "inconclusive"
    host = _host(url)
    if host and host in low:
        return "indexed"
    return "not_found"


def classify(m: dict) -> str:
    http_state = m["http"]["state"]
    if http_state in ("broken", "timeout", "error"):
        return "broken_or_orphaned"
    # 'blocked' (403/429) pages are alive — fall through to platform/Google logic
    if _host(m["url"]) in LOW_RANK_HOSTS:
        return "low_rank_platform"
    g = m["google"]
    if g == "not_found":
        return "not_indexed_by_google"
    if g == "inconclusive":
        return "google_inconclusive"
    return "visible"


def main() -> None:
    # 1. harvest mentions across engines + brands
    engines = [("duckduckgo", search_ddg)]
    if USE_BING:
        engines.append(("bing", search_bing))
    found: dict[str, dict] = {}  # url -> mention
    for brand, query in BRANDS.items():
        for engine, fn in engines:
            for url, title in fn(query):
                if _is_ours(url) or not url.startswith("http"):
                    continue
                key = url.rstrip("/")
                if key not in found:
                    found[key] = {
                        "url": url, "host": _host(url), "title": title,
                        "brands": set(), "engines": set(),
                    }
                found[key]["brands"].add(brand)
                found[key]["engines"].add(engine)
            time.sleep(1)  # be polite

    # 2. probe each mention
    mentions: list[dict] = []
    for m in found.values():
        m["http"] = http_status(m["url"])
        m["google"] = google_indexed(m["url"])
        m["brands"] = sorted(m["brands"])
        m["engines"] = sorted(m["engines"])
        m["bucket"] = classify(m)
        mentions.append(m)
        time.sleep(0.5)

    # 3. bucketize + summarize
    buckets: dict[str, list] = {
        "broken_or_orphaned": [], "not_indexed_by_google": [],
        "low_rank_platform": [], "google_inconclusive": [], "visible": [],
    }
    for m in mentions:
        buckets[m["bucket"]].append(m)

    by_engine: dict[str, int] = {}
    for m in mentions:
        for e in m["engines"]:
            by_engine[e] = by_engine.get(e, 0) + 1

    out = {
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "total_mentions": len(mentions),
            "by_bucket": {k: len(v) for k, v in buckets.items()},
            "by_engine": by_engine,
            "engines": [e for e, _ in engines],
            "brands": list(BRANDS.keys()),
            "google_probe_enabled": GOOGLE_PROBE,
        },
        "buckets": buckets,
        "mentions": sorted(mentions, key=lambda x: x["bucket"]),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
