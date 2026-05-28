# 🤖 TKAWEN Automation

> Free cron server for the TKAWEN ecosystem, powered by GitHub Actions.

This repository runs automated tasks on a schedule, **completely free** thanks
to GitHub Actions' unlimited public-repo minutes. It keeps the 11 platforms
of the [TKAWEN ecosystem](https://hartem.tkawen.com) healthy and visible.

## 🛰 Platforms monitored

| Platform | URL | Sitemap |
|----------|-----|---------|
| Mystoq | [mystoq.com](https://mystoq.com) | [sitemap](https://mystoq.com/sitemap.xml) |
| LIQAA | [liqaa.io](https://liqaa.io) | [sitemap](https://liqaa.io/sitemap.xml) |
| Algeria Certify | [algeriacertify.com](https://algeriacertify.com) | [sitemap](https://algeriacertify.com/sitemap.xml) |
| PharmaPro | [pharmapro.tkawen.com](https://pharmapro.tkawen.com) | [sitemap](https://pharmapro.tkawen.com/sitemap.xml) |
| Catalogue | [catalogue.tkawen.com](https://catalogue.tkawen.com) | [sitemap](https://catalogue.tkawen.com/sitemap.xml) |
| TKAWEN.com | [tkawen.com](https://tkawen.com) | [sitemap](https://tkawen.com/sitemap.xml) |
| TKAWEN Track | [track.tkawen.com](https://track.tkawen.com) | — |
| Brand | [brand.tkawen.com](https://brand.tkawen.com) | — |
| Trust | [trust.tkawen.com](https://trust.tkawen.com) | — |
| Studio | [studio.tkawen.com](https://studio.tkawen.com) | — |
| Hartem | [hartem.tkawen.com](https://hartem.tkawen.com) | — |

## ⚙️ Workflows

### 🔍 `indexnow-daily.yml`
Pings Bing + Yandex with every sitemap URL across the 11 platforms. Runs **daily at 06:00 UTC**.
Boosts SEO fresh-crawl signal for all properties.

### 🩺 `health-check.yml`
Hits every platform's homepage. Reports failures to Telegram (founder chat).
Runs every **30 minutes**.

### 📊 `sr-rank-track.yml`
Scrapes [StartupRanking](https://www.startupranking.com/startup/mystoq) weekly and
commits the rank + SR Web + SR Social to a public JSON file. Visualisable.

### 📈 `mystoq-stats-snapshot.yml`
Daily snapshot of public Mystoq metrics committed to `data/mystoq-stats.json`.
Mystoq.com can fetch this file to render a live "trust" widget.

## 🔐 Secrets used

| Secret | Purpose |
|--------|---------|
| `TELEGRAM_BOT_TOKEN` | sending alerts to founder |
| `TELEGRAM_CHAT_ID` | recipient chat |

(set via GitHub repo → Settings → Secrets and variables → Actions)

## 📜 License

AGPL-3.0 · open-source so every TKAWEN customer can audit what runs.

— Built by [Hartem Yaakoub](https://hartem.tkawen.com) for the TKAWEN ecosystem.
