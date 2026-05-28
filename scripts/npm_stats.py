#!/usr/bin/env python3
"""Pull download counts for every @mystoq/* npm package via npmjs.org/downloads."""

import json
import sys
import urllib.request as ur
from datetime import datetime

PACKAGES = [
    "@mystoq/seo-toolkit",
    "@mystoq/sdk",
    "@mystoq/react",
    "@mystoq/mcp-server",
    "@mystoq/yalidine-bridge",
    "@mystoq/maystro-bridge",
    "@mystoq/whatsapp-bridge",
]

TIMEOUT = 15
UA = "TKAWEN-NpmStats/1.0"


def downloads(pkg: str, range_: str) -> int | None:
    url = f"https://api.npmjs.org/downloads/point/{range_}/{pkg}"
    try:
        req = ur.Request(url, headers={"User-Agent": UA})
        with ur.urlopen(req, timeout=TIMEOUT) as r:
            doc = json.load(r)
        return doc.get("downloads")
    except Exception as e:
        print(f"failed {pkg} {range_}: {e}", file=sys.stderr)
        return None


def main() -> None:
    rows = []
    total_30d = 0
    total_yday = 0
    for p in PACKAGES:
        yday = downloads(p, "last-day")
        m30 = downloads(p, "last-month")
        rows.append({
            "name": p,
            "downloads_yesterday": yday,
            "downloads_last_30d": m30,
        })
        if isinstance(m30, int):
            total_30d += m30
        if isinstance(yday, int):
            total_yday += yday

    print(json.dumps({
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "total_packages": len(PACKAGES),
            "downloads_yesterday": total_yday,
            "downloads_last_30d": total_30d,
        },
        "packages": rows,
    }, indent=2))


if __name__ == "__main__":
    main()
