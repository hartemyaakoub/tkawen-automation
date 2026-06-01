# TKAWEN Automation

> The always-on growth engine for the [TKAWEN ecosystem](https://hartem.tkawen.com) — **22 scheduled jobs** that keep every platform fast, indexed, and visible, running **free** on GitHub Actions.

This repository is a serverless cron platform. Every workflow is a self-contained, zero-cost task that watches, measures, or promotes the TKAWEN products on a fixed schedule and reports anomalies to Telegram. No servers to pay for, no dashboards to babysit — the public-repo GitHub Actions minutes do the work, and every result is committed back as an auditable JSON trail under `.data/`.

## Platforms covered

| Platform | URL |
|----------|-----|
| Mystoq — e‑commerce builder | [mystoq.com](https://mystoq.com) |
| LIQAA — video meetings | [liqaa.io](https://liqaa.io) |
| AlgeriaCertify — credential verification | [algeriacertify.com](https://algeriacertify.com) |
| PharmaPro — pharmacy management | [pharmapro.tkawen.com](https://pharmapro.tkawen.com) |
| Catalogue — training catalogue | [catalogue.tkawen.com](https://catalogue.tkawen.com) |
| TKAWEN — parent platform | [tkawen.com](https://tkawen.com) |
| Track — GPS fleet | [track.tkawen.com](https://track.tkawen.com) |
| Trust — verified badges | [trust.tkawen.com](https://trust.tkawen.com) |
| Brand — design system | [brand.tkawen.com](https://brand.tkawen.com) |
| Hartem — founder hub | [hartem.tkawen.com](https://hartem.tkawen.com) |

## What runs, and when

### Uptime & health
| Workflow | Schedule | What it does |
|----------|----------|--------------|
| `uptime-monitor` | every 15 min | Pings every site, logs downtime to `.data/uptime/`, alerts Telegram. |
| `health-check` | every 30 min | Hits each homepage and reports failures to the founder chat. |

### Search indexing & SEO plumbing
| Workflow | Schedule | What it does |
|----------|----------|--------------|
| `indexnow-daily` | daily 06:00 | Submits every sitemap URL to Bing + Yandex via IndexNow. |
| `fresh-content-ping` | every 4h | IndexNows only URLs whose sitemap `<lastmod>` is fresh — fast re-crawl. |
| `sitemap-rebuilder` | daily 02:00 | SSHes to the VPS and rebuilds each Laravel app's `sitemap.xml`. |
| `llms-txt-refresher` | daily 03:30 | Regenerates `llms.txt` for every site so AI crawlers stay current. |
| `schema-validator` | daily 08:45 | Extracts and validates JSON-LD across top URLs; flags broken schema. |
| `programmatic-pages-generator` | weekly (Thu) | Builds long-tail keyword landing pages, one per term. |

### Performance & hygiene
| Workflow | Schedule | What it does |
|----------|----------|--------------|
| `pagespeed-monitor` | daily 10:00 | Pulls Core Web Vitals (mobile + desktop) from PageSpeed Insights. |
| `broken-links-check` | weekly (Mon) | Crawls a sample of pages and reports dead `<a href>` links. |

### Rank & competitive intelligence
| Workflow | Schedule | What it does |
|----------|----------|--------------|
| `serp-position-monitor` | daily 12:30 | Tracks where each brand ranks for its target keywords. |
| `sr-rank-monitor` | weekly (Mon) | Records StartupRanking score (SR Web + SR Social) to a public JSON. |
| `competitor-sitemap-watcher` | daily 07:00 | Diffs competitors' sitemaps day-over-day to surface their new pages. |
| `backlink-prospector` | weekly (Wed) | Finds backlink opportunities via web search. |

### Brand presence & answer-engine optimization
| Workflow | Schedule | What it does |
|----------|----------|--------------|
| `ai-citation-watcher` | daily 11:15 | Probes AI search surfaces to see when they cite TKAWEN brands. |
| `news-mentions-watcher` | daily 15:00 | Polls Google News RSS for every brand keyword. |
| `wikipedia-watcher` | daily 05:30 | Watches Wikipedia + Wikidata for fresh brand mentions. |

### Ecosystem & distribution signals
| Workflow | Schedule | What it does |
|----------|----------|--------------|
| `github-pulse` | daily 04:23 | Keeps public repos warm with a tiny last-updated commit. |
| `github-stars-snapshot` | daily 14:00 | Snapshots stars / forks / watchers across all public repos. |
| `npm-downloads-monitor` | daily 13:00 | Records daily download counts for the `@mystoq/*` packages. |
| `readme-promoter` | weekly (Tue) | Refreshes cross-promotion links in repo READMEs. |
| `postiz-social-poster` | every 8h | Drains a social-post queue to the self-hosted Postiz instance. |

Every job also accepts a manual `workflow_dispatch` run from the **Actions** tab.

## Configuration

Set under **Settings → Secrets and variables → Actions**:

| Secret | Used by |
|--------|---------|
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | all alerting workflows |
| `VPS_SSH_KEY` | `sitemap-rebuilder`, `llms-txt-refresher` |
| `PULSE_TOKEN` | `github-pulse`, `github-stars-snapshot` (cross-repo writes) |
| `POSTIZ_API_TOKEN` | `postiz-social-poster` |
| `GITHUB_TOKEN` | provided automatically by Actions |

## Design principles

- **Free by construction** — public-repo Actions minutes only; no paid infra.
- **Auditable** — results are committed as JSON under `.data/`, so anything claimed can be checked.
- **Resilient** — concurrency guards and rebase-retry on push so concurrent runs never lose a commit.
- **No silent failures** — anything that breaks pings Telegram.

## License

[AGPL-3.0](LICENSE) — open by design, so any TKAWEN customer can audit exactly what runs against their properties.

---

Built and maintained by [Hartem Yaakoub](https://hartem.tkawen.com) for the TKAWEN ecosystem.
