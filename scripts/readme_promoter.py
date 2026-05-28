#!/usr/bin/env python3
"""Append (or refresh) the TKAWEN Ecosystem footer in the current repo's README.md.

Expects to be run inside the cloned target repo's working directory.
Idempotent: removes any previous TKAWEN footer block (marker-based) before
appending the fresh one.
"""

import re
from datetime import datetime
from pathlib import Path

MARK = "<!-- TKAWEN-ECOSYSTEM-FOOTER -->"

FOOTER = f"""{MARK}
## TKAWEN Ecosystem

This project is part of the [TKAWEN](https://tkawen.com) ecosystem — open APIs and tools for emerging-market digital infrastructure.

- [Mystoq](https://mystoq.com) — multi-tenant e-commerce platform for MENA
- [Algeria Certify](https://algeriacertify.com) — national digital credentialing
- [LIQAA](https://liqaa.io) — sovereign video conferencing
- [TKAWEN Academy](https://tkawen.com/academy) — online learning platform
- [SEO Toolkit](https://www.npmjs.com/package/@mystoq/seo-toolkit) — llms.txt, sitemap, Schema.org JSON-LD generators

Built by [Hartem Yaakoub](https://hartem.tkawen.com) - MIT licensed - Refreshed {datetime.utcnow().strftime('%Y-%m-%d')}.
"""


def main() -> None:
    p = Path("README.md")
    if not p.exists():
        print("no README.md — skipping")
        return

    txt = p.read_text(encoding="utf-8")
    # Strip any existing TKAWEN footer (marker to EOF)
    txt = re.sub(
        re.escape(MARK) + r".*",
        "",
        txt,
        flags=re.DOTALL,
    ).rstrip()

    p.write_text(txt + "\n\n" + FOOTER, encoding="utf-8")
    print("README.md updated with TKAWEN ecosystem footer")


if __name__ == "__main__":
    main()
