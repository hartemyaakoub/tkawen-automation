#!/usr/bin/env python3
"""Generate HTML landing pages: 58 wilayas × {bilingual intent}.

Each page is a small, fast, well-structured SEO landing page targeting one
intent in one wilaya. Pure programmatic SEO — every page is unique because the
local context (wilaya, currency, COD norms, language) differs.

Usage: python3 programmatic_pages.py <out_dir>
"""

import sys
from datetime import datetime
from pathlib import Path

# 58 Algerian wilayas — (slug, AR name, FR name)
WILAYAS = [
    ("adrar", "أدرار", "Adrar"), ("chlef", "الشلف", "Chlef"),
    ("laghouat", "الأغواط", "Laghouat"), ("oum-el-bouaghi", "أم البواقي", "Oum El Bouaghi"),
    ("batna", "باتنة", "Batna"), ("bejaia", "بجاية", "Béjaïa"),
    ("biskra", "بسكرة", "Biskra"), ("bechar", "بشار", "Béchar"),
    ("blida", "البليدة", "Blida"), ("bouira", "البويرة", "Bouira"),
    ("tamanrasset", "تمنراست", "Tamanrasset"), ("tebessa", "تبسة", "Tébessa"),
    ("tlemcen", "تلمسان", "Tlemcen"), ("tiaret", "تيارت", "Tiaret"),
    ("tizi-ouzou", "تيزي وزّو", "Tizi Ouzou"), ("alger", "الجزائر", "Algiers"),
    ("djelfa", "الجلفة", "Djelfa"), ("jijel", "جيجل", "Jijel"),
    ("setif", "سطيف", "Sétif"), ("saida", "سعيدة", "Saïda"),
    ("skikda", "سكيكدة", "Skikda"), ("sidi-bel-abbes", "سيدي بلعباس", "Sidi Bel Abbès"),
    ("annaba", "عنابة", "Annaba"), ("guelma", "قالمة", "Guelma"),
    ("constantine", "قسنطينة", "Constantine"), ("medea", "المدية", "Médéa"),
    ("mostaganem", "مستغانم", "Mostaganem"), ("msila", "المسيلة", "M'Sila"),
    ("mascara", "معسكر", "Mascara"), ("ouargla", "ورقلة", "Ouargla"),
    ("oran", "وهران", "Oran"), ("el-bayadh", "البيض", "El Bayadh"),
    ("illizi", "إليزي", "Illizi"), ("bordj-bou-arreridj", "برج بوعريريج", "Bordj Bou Arreridj"),
    ("boumerdes", "بومرداس", "Boumerdès"), ("el-tarf", "الطارف", "El Tarf"),
    ("tindouf", "تندوف", "Tindouf"), ("tissemsilt", "تيسمسيلت", "Tissemsilt"),
    ("el-oued", "الوادي", "El Oued"), ("khenchela", "خنشلة", "Khenchela"),
    ("souk-ahras", "سوق أهراس", "Souk Ahras"), ("tipaza", "تيبازة", "Tipaza"),
    ("mila", "ميلة", "Mila"), ("ain-defla", "عين الدفلى", "Aïn Defla"),
    ("naama", "النعامة", "Naâma"), ("ain-temouchent", "عين تموشنت", "Aïn Témouchent"),
    ("ghardaia", "غرداية", "Ghardaïa"), ("relizane", "غليزان", "Relizane"),
    ("timimoun", "تيميمون", "Timimoun"), ("bordj-badji-mokhtar", "برج باجي مختار", "Bordj Badji Mokhtar"),
    ("ouled-djellal", "أولاد جلال", "Ouled Djellal"), ("beni-abbes", "بني عباس", "Béni Abbès"),
    ("in-salah", "عين صالح", "In Salah"), ("in-guezzam", "عين قزام", "In Guezzam"),
    ("touggourt", "تقرت", "Touggourt"), ("djanet", "جانت", "Djanet"),
    ("el-mghair", "المغير", "El M'Ghair"), ("el-meniaa", "المنيعة", "El Meniaa"),
]

INTENTS = [
    ("start-online-store", "بدء متجر إلكتروني", "Démarrer une boutique"),
    ("cash-on-delivery", "البيع بالدفع عند الاستلام", "Vente cash à la livraison"),
    ("verify-certificate", "التحقق من شهادة", "Vérifier un certificat"),
    ("digital-credentials", "شهادات رقمية", "Certificats numériques"),
]


def render(slug: str, wilaya_slug: str, ar: str, fr: str, intent: tuple[str, str, str]) -> str:
    intent_slug, intent_ar, intent_fr = intent
    title = f"{intent_fr} à {fr} — TKAWEN"
    description = f"{intent_fr} dans la wilaya de {fr}. Plateformes digitales TKAWEN pour entrepreneurs algériens. Mystoq · Algeria Certify · LIQAA."
    url = f"https://mystoq.com/wilaya-cod-pages/{slug}.html"

    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="alternate" hreflang="ar-DZ" href="{url}">
<link rel="alternate" hreflang="fr-DZ" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"WebPage",
  "name":"{title}",
  "url":"{url}",
  "inLanguage":["ar-DZ","fr-DZ"],
  "isPartOf":{{"@type":"WebSite","name":"TKAWEN","url":"https://tkawen.com"}},
  "mainEntity":{{
    "@type":"Service",
    "name":"{intent_fr} à {fr}",
    "areaServed":{{"@type":"AdministrativeArea","name":"{fr}, Algeria"}},
    "provider":{{"@type":"Organization","name":"TKAWEN","url":"https://tkawen.com"}}
  }}
}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#060a18;--bg-2:#0a1024;--panel:rgba(255,255,255,.04);--panel-2:rgba(255,255,255,.06);
  --line:rgba(148,163,184,.14);--line-2:rgba(148,163,184,.25);
  --ink:#f1f5f9;--ink-2:#cbd5e1;--mute:#8ea0b8;--blue-2:#60a5fa;--cyan:#22d3ee;
  --grad:linear-gradient(-92deg,#60a5fa 0%,#22d3ee 50%,#a78bfa 100%);
}}
html,body{{background:var(--bg);color:var(--ink);font-family:'Cairo',system-ui,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.7}}
a{{color:var(--blue-2);text-decoration:none}}a:hover{{text-decoration:underline}}
::selection{{background:rgba(96,165,250,.35)}}
.aurora{{position:fixed;inset:0;z-index:-1;overflow:hidden;pointer-events:none}}
.aurora::before,.aurora::after{{content:'';position:absolute;border-radius:50%;filter:blur(120px);opacity:.35}}
.aurora::before{{width:560px;height:560px;background:radial-gradient(circle,#1d4ed8 0%,transparent 70%);top:-200px;right:-120px}}
.aurora::after{{width:480px;height:480px;background:radial-gradient(circle,#0e7490 0%,transparent 70%);top:160px;left:-160px}}
.wrap{{max-width:820px;margin:0 auto;padding:40px 24px 0}}
.brand{{display:flex;align-items:center;gap:10px;margin-bottom:52px;font-weight:900;font-size:19px;letter-spacing:-.01em}}
.brand .mark{{width:26px;height:26px;border-radius:7px;background:var(--grad);box-shadow:0 4px 18px rgba(34,211,238,.35);flex-shrink:0}}
.brand span b{{color:var(--blue-2)}}
.kicker{{display:inline-flex;align-items:center;gap:8px;padding:7px 16px;background:rgba(96,165,250,.08);border:1px solid rgba(96,165,250,.25);color:var(--blue-2);border-radius:999px;font-size:11px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;margin-bottom:20px}}
h1{{font-size:clamp(30px,5.6vw,44px);font-weight:900;letter-spacing:-.02em;line-height:1.2;margin-bottom:16px}}
h1 .grad{{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}}
.lead{{font-size:18px;color:var(--mute);margin-bottom:30px;max-width:620px}}
.lead strong{{color:var(--ink)}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:16px;overflow:hidden;margin:0 0 44px}}
.stat{{background:var(--bg-2);padding:18px 12px;text-align:center}}
.stat .n{{font-size:26px;font-weight:900;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;line-height:1.2}}
.stat .l{{font-size:12px;font-weight:700;color:var(--mute);margin-top:2px}}
h2{{font-size:24px;font-weight:900;letter-spacing:-.01em;margin:40px 0 16px}}
h2 .accent{{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}}
p{{margin-bottom:14px;color:var(--ink-2)}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:24px 0}}
.card{{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px;transition:transform .2s,border-color .2s,background .2s;overflow:hidden}}
.card::before{{content:'';position:absolute;inset:0 0 auto 0;height:1px;background:var(--grad);opacity:0;transition:opacity .2s}}
.card:hover{{transform:translateY(-3px);border-color:var(--line-2);background:var(--panel-2)}}
.card:hover::before{{opacity:1}}
.card h3{{font-size:16px;font-weight:800;margin-bottom:6px;color:var(--blue-2)}}
.card p{{font-size:14px;color:var(--mute);margin:0}}
.cta-row{{display:flex;gap:14px;flex-wrap:wrap;margin-top:22px}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:14px 28px;border-radius:12px;font-weight:800;font-size:15px;text-decoration:none!important;transition:transform .15s,box-shadow .15s}}
.btn-grad{{background:var(--grad);color:#04101f;box-shadow:0 4px 24px rgba(34,211,238,.25)}}
.btn-grad:hover{{transform:translateY(-1px);box-shadow:0 8px 32px rgba(34,211,238,.35)}}
.btn-ghost{{background:var(--panel);color:var(--ink);border:1.5px solid var(--line-2)}}
.btn-ghost:hover{{border-color:var(--blue-2);transform:translateY(-1px)}}
footer{{margin-top:56px;padding:28px 0 0;border-top:1px solid var(--line);font-size:13px;color:var(--mute)}}
.strip{{height:3px;background:var(--grad);margin-top:28px}}
</style>
</head>
<body>
<div class="aurora"></div>
<div class="wrap">
<div class="brand"><div class="mark"></div><span>tk<b>awen</b></span></div>
<span class="kicker">⚡ {fr.upper()} · {ar}</span>
<h1>{intent_ar}<br><span class="grad">في ولاية {ar}</span></h1>
<p class="lead">منصّات TKAWEN الرقمية الجاهزة لرواد الأعمال في <strong>{ar}</strong> ({fr}). مجاناً لتبدأ، احترافي لتتوسّع.</p>

<div class="stats">
  <div class="stat"><div class="n">58</div><div class="l">ولاية مدعومة</div></div>
  <div class="stat"><div class="n">4+</div><div class="l">منصّات متكاملة</div></div>
  <div class="stat"><div class="n">0 دج</div><div class="l">للانطلاق</div></div>
  <div class="stat"><div class="n">24/7</div><div class="l">تعمل دائماً</div></div>
</div>

<h2>منتجاتنا في <span class="accent">{ar}</span></h2>
<div class="cards">
  <div class="card"><h3>🛒 Mystoq</h3><p>منصّة تجارة إلكترونية للدفع عند الاستلام في ولاية {ar}.</p></div>
  <div class="card"><h3>🎓 Algeria Certify</h3><p>شهادات رقمية موثّقة لكل المهنيين في {ar}.</p></div>
  <div class="card"><h3>📹 LIQAA</h3><p>اجتماعات فيديو مشفّرة للشركات في {ar}.</p></div>
  <div class="card"><h3>📚 TKAWEN Academy</h3><p>تكوينات إلكترونية + شهادات للسكان في {ar}.</p></div>
</div>

<div class="cta-row">
  <a href="https://mystoq.com/?utm_source=programmatic&amp;utm_medium=wilaya&amp;utm_campaign={slug}" class="btn btn-grad">ابدأ الآن مجاناً ←</a>
  <a href="https://tkawen.com" class="btn btn-ghost">اكتشف المنظومة</a>
</div>

<h2>لماذا TKAWEN في <span class="accent">{ar}</span>؟</h2>
<p>منظومة كاملة مفتوحة المصدر من المؤسس <a href="https://hartem.tkawen.com">حرتام يعقوب</a>. كل المنصّات تتكامل سلساً: تربط متجرك بشهاداتك بفيديو اجتماعاتك بكاتالوغك.</p>

<footer>
صفحة آلية الإنشاء — جزء من منظومة <a href="https://tkawen.com">TKAWEN</a>. آخر تحديث: {datetime.utcnow().strftime("%Y-%m-%d")}.
<br><br>
المنطقة: ولاية {ar} ({fr}, Algeria) · جميع 58 ولاية مدعومة.
<div class="strip"></div>
</footer>
</div>
</body>
</html>
"""


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("out/pages")
    out.mkdir(parents=True, exist_ok=True)
    count = 0
    for w_slug, ar, fr in WILAYAS:
        for intent in INTENTS:
            slug = f"{intent[0]}-{w_slug}"
            html = render(slug, w_slug, ar, fr, intent)
            (out / f"{slug}.html").write_text(html, encoding="utf-8")
            count += 1
    print(f"generated {count} pages → {out}")


if __name__ == "__main__":
    main()
