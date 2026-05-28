#!/usr/bin/env python3
"""Hit every TKAWEN platform homepage. Telegram-alert any failure."""
import os, sys, json, time
import urllib.request as ur

PLATFORMS = [
    ("Mystoq",          "https://mystoq.com/"),
    ("LIQAA",           "https://liqaa.io/"),
    ("Algeria Certify", "https://algeriacertify.com/"),
    ("PharmaPro",       "https://pharmapro.tkawen.com/"),
    ("Catalogue",       "https://catalogue.tkawen.com/"),
    ("TKAWEN.com",      "https://tkawen.com/"),
    ("TKAWEN Track",    "https://track.tkawen.com/"),
    ("Brand",           "https://brand.tkawen.com/"),
    ("Trust",           "https://trust.tkawen.com/"),
    ("Studio",          "https://studio.tkawen.com/"),
    ("Hartem",          "https://hartem.tkawen.com/"),
]
TOKEN = os.environ.get("TOKEN", "")
CHAT  = os.environ.get("CHAT", "")


def probe(url: str) -> tuple[int, float]:
    t = time.monotonic()
    try:
        r = ur.urlopen(ur.Request(url, headers={"User-Agent": "TKAWEN-Health/1.0"}), timeout=12)
        return r.status, time.monotonic() - t
    except Exception:
        return 0, time.monotonic() - t


def tg(msg: str) -> None:
    if not (TOKEN and CHAT):
        return
    import urllib.parse as up
    ur.urlopen(ur.Request(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data=up.urlencode({"chat_id": CHAT, "text": msg, "parse_mode": "Markdown"}).encode()
    ), timeout=15)


failures = []
lines = ["TKAWEN platforms health probe", ""]
for name, url in PLATFORMS:
    code, dur = probe(url)
    icon = "✅" if 200 <= code < 400 else "❌"
    line = f"{icon} {name:<18} HTTP {code:<4} {int(dur*1000):>4}ms"
    print(line); lines.append(line)
    if not (200 <= code < 400):
        failures.append((name, url, code, dur))

if failures:
    msg = "🚨 *TKAWEN Health Alert*\n\n" + "\n".join(
        f"❌ *{n}* → {u}\n   HTTP {c} after {int(d*1000)}ms"
        for n, u, c, d in failures
    )
    tg(msg)
    sys.exit(1)
print("\nAll healthy.")
