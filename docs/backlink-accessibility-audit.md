# استطلاع عميق: المواقع التي تذكر منظومة TKAWEN ويصعب الوصول إليها من غوغل

> تاريخ الاستطلاع: 2026-06-03 · الفرع: `claude/backlink-accessibility-audit`
> المُخرَج المرافق: سكربت `scripts/backlink_accessibility_audit.py` + بيانات حيّة تحت `.data/backlinks/audit-*.json`

هذا تقرير بحثي متعدّد المصادر يجيب على السؤال: **مَن يتحدّث عن علاماتك على الويب، ولماذا لا يظهر ذلك (أو يُدفَن) في نتائج غوغل، وكيف نُصلحه؟**

اعتمد على: (1) بحث ميداني عبر عدة محركات وأكثر من 190 استعلاماً بثلاث لغات، (2) تشغيل حيّ لسكربت التدقيق الجديد، (3) عمود تحليلي موثّق من وثائق غوغل الرسمية ومصادر SEO معتمدة (Ahrefs، Onely، Search Engine Land).

---

## 0. الخلاصة التنفيذية (اقرأ هذا أولاً)

| الحقيقة | الأثر |
|---|---|
| **معظم ما يُذكر عن علاماتك ليس تغطية مستقلة** — بل محتوى تنشره أنت: بيانات صحفية مدفوعة (OpenPR، IssueWire)، مقالات بتوقيع المؤسس (Vocal.media، Medium)، ونطاقات مملوكة (tkawen.online). | غوغل يعامل هذا كمحتوى ترويجي/مكرّر منخفض القيمة، فيدفنه. |
| **TKAWEN** وحدها لها حضور خارجي حقيقي (Crunchbase, Tracxn, StartupRanking, elioplus). | هذه أقوى روابطك — لكنها أدلّة تلقائية رقيقة. |
| **AlgeriaCertify** حضورها كله ذاتي النشر، لا تغطية صحفية مستقلة واحدة. | لا رصيد روابط مستقل. |
| **Mystoq، LIQAA، PharmaPro**: صفر إشارات خارجية مستقلة مؤكَّدة. | غير مرئية عضوياً خارج موقعها. |
| **تضارب أسماء خطير**: «Mystoq» يتطابق مع تطبيق إدارة بضائع أمريكي + لاعب Minecraft؛ «LIQAA» يتطابق مع منصّة *Liqaa* السعودية (Wamid/تداول). | غوغل يرتّب الاسم الأقدم/الأقوى فوقك، فيصعّب إيجادك أنت تحديداً. |
| **الفجوة غوغل ↔ Bing/DuckDuckGo حقيقية**: عدة صفحات تظهر في DuckDuckGo (فهرس Bing) وهي ضعيفة/غائبة في غوغل. | لأن Bing يبتلع الروابط فوراً عبر IndexNow، بينما غوغل يؤجّل الزحف للمواقع الصغيرة. |

**أهم توصية واحدة:** مشكلتك ليست «روابط مدفونة» بقدر ما هي **غياب تغطية مستقلة أصلاً**. الأولوية: (أ) تحويل الإشارات المملوكة إلى روابط نظيفة ومفهرسة، (ب) كسب تغطية مستقلة حقيقية، (ج) حلّ تضارب الأسماء.

---

## 1. جرد الإشارات المكتشَفة (مصنّفة حسب صعوبة الوصول من غوغل)

> ✅ = مؤكَّد بجلب الصفحة وقراءة النص · 🔎 = ظهر باستمرار في نتائج عدة محركات لكن المضيف يحظر الجلب الآلي (403) فتعذّر اقتباسه حرفياً

### المجموعة أ — مدفونة/ضعيفة في غوغل رغم وجودها في Bing/DuckDuckGo

| الرابط | العلامة | النوع | لماذا يصعب الوصول من غوغل |
|---|---|---|---|
| `registry.npmjs.org/@mystoq/sdk` (+6 حِزَم `@mystoq/*`) | Mystoq ✅ | حزم npm (ذاتية النشر) | لا تترتّب لاسم العلامة في غوغل؛ تُكتشف فقط عبر واجهة npm. صفحات رقيقة + سلطة منخفضة. |
| `github.com/mystoq-cloud`, `github.com/topics/mystoq`, `github.com/TKAWEN`, `github.com/ALGERIACERTIFY` | Mystoq/TKAWEN/AlgeriaCertify ✅ | مستودعات GitHub | حيّة (200) لكن صفحات منظمات GitHub فارغة المحتوى الزاحف → «Discovered – currently not indexed». |
| `issuewire.com/tkawen-a-revolutionary-digital-ecosystem-...` | TKAWEN ✅ | توزيع بيان صحفي | محتوى مُتزامَن (syndicated) مكرّر على عشرات النطاقات → غوغل يطوي النسخ. |
| `algeriaculturedaily.com/article/...tkawen-global-certification...` · `algeriaindustryjournal.com/article/...` · `meatechwatch.com/2025/01/20/tkawen-...` | TKAWEN / Algeria Certify ✅ | شبكة نشر إقليمية | نفس المقال منسوخ عبر نطاقات شبكة واحدة → محتوى مكرّر منخفض الثقة. |
| `elioplus.com/profiles/channel-partners/218656/tkawen` | TKAWEN ✅ | دليل شركاء قنوات | صفحة عميقة في دليل B2B متخصّص؛ سلطة صفحة منخفضة. |

### المجموعة ب — منصّات يضعّفها غوغل بطبيعتها (UGC / بيانات صحفية / أدلّة رقيقة)

| الرابط | العلامة | لماذا يدفنها غوغل |
|---|---|---|
| `vocal.media/education/algeria-certify-transforming-...` · `vocal.media/education/tkawen-...` | AlgeriaCertify / TKAWEN ✅ | منصّة نشر مفتوحة، المقال **بتوقيع المؤسس** Yaakoub Hartem → ترويج ذاتي. |
| `medium.com/@yaakoub.hartem/...` (عدة مقالات) | TKAWEN / AlgeriaCertify ✅ | مدوّنة ذاتية، روابط UGC/nofollow غالباً. |
| `openpr.com/news/3954870/algeriacertify-...` · `/4399739/...` · `/3818914/tkawen-...` | AlgeriaCertify / TKAWEN 🔎 | بيانات صحفية مدفوعة/مُرسَلة ذاتياً؛ غوغل يخصم قيمتها. |
| `crunchbase.com/organization/tkawen` · `/organization/mystoq` · `/person/yaakoub-hartem` | TKAWEN / Mystoq 🔎 | ملفّات قاعدة بيانات رقيقة؛ تُفهرَس لكن تترتّب ضعيفاً. (ملاحظة: قد يكون ملف mystoq لشركة مختلفة — انظر §3.) |
| `tracxn.com/d/companies/tkawen/...` · `startupranking.com/startup/tkawen` | TKAWEN 🔎 | أدلّة شركات ناشئة، صفحات شبه تلقائية. |
| `f6s.com/company/algeria-certify` | Algeria Certify ✅ | دليل شركات ناشئة منخفض الترتيب. |
| `facebook.com/AlgeriaCertify/` · `linkedin.com/company/tkawen` · `linkedin.com/pulse/engineering-trust-...-hartem-cgbcf` | AlgeriaCertify / TKAWEN ✅ | محتوى سوشيال؛ غوغل يفهرسه جزئياً ويرتّبه منخفضاً. |
| `youtube.com/watch?v=r6Ympn75Pi8` | AlgeriaCertify ✅ (حيّ، يحظر الفحص الآلي 429) | فيديو منفرد دون سلطة قناة. |

### المجموعة ج — روابط معطّلة / يتيمة / تضارب أسماء

| العنصر | الحالة | الملاحظة |
|---|---|---|
| `liqaa.com` | مركونة/للبيع | ليست لك (نطاقك `liqaa.io`). |
| `liqaa.net` | محتوى عربي غير ذي صلة | تضارب اسم. |
| `catpvp.xyz/player/mystoq` | حيّ لكنه **ليس علامتك** | لاعب Minecraft اسمه mystoq — ضجيج يلتقطه البحث عن «Mystoq». |
| روابط داخلية مكسورة (29) | 404/timeout | من `.data/links/report-2026-06-01.json` — مثل `trust.tkawen.com/docs` وصفحات مدرّبين على algeriacertify. أصلِحها فهي تُهدر زحف غوغل (انظر §4، السبب 2). |

> **حول جسّ فهرسة غوغل:** السكربت يحاول التحقّق هل كل رابط مفهرس في غوغل، لكن غوغل يحظر الكشط من عناوين مراكز البيانات (CI)، فيسجّل `inconclusive` بأمانة بدل تخمين. تحديد «مدفون في غوغل تحديداً» أعلاه استُنتج من البحث الميداني اليدوي عبر المحركات، لا من الجسّ الآلي.

---

## 2. لماذا يصعب الوصول إليها من غوغل تحديداً؟ (الأسباب موثّقة)

> الإطار العام: نتائج DuckDuckGo مصدرها فهرس Bing أساساً. لذا «موجود في Bing/DDG وغائب عن غوغل» تعني غالباً أن الصفحة **في فهرس Bing لكن غوغل لم يزحف إليها أو لم يفهرسها أو دفنها**. وBing يبتلع الروابط فوراً عبر IndexNow (وغوغل لا يدعمه)، ما يفسّر سبق Bing.

1. **«Discovered – currently not indexed»**: غوغل يعرف الرابط لكن لم يزحفه/يفهرسه بسبب ميزانية الزحف وضعف الجودة وقلّة الروابط الداخلية ([Ahrefs](https://ahrefs.com/blog/discovered-currently-not-indexed/)).
2. **ميزانية الزحف / PageRank منخفض**: «الروابط الأكثر شعبية تُزحَف أكثر»، و«ليست كل صفحة مزحوفة ستُفهرَس» ([Google Search Central](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)). الروابط الداخلية المكسورة تُهدر هذه الميزانية.
3. **الصفحات اليتيمة**: بلا روابط داخلية «قد لا يكتشفها المحرك أبداً... وتملك سلطة ضئيلة» ([Conductor](https://www.conductor.com/academy/what-are-orphan-pages-how-to-find-fix/)).
4. **محتوى رقيق/مكرّر**: البيانات الصحفية المُتزامَنة عبر شبكة نطاقات = نسخ مكرّرة يطويها غوغل ([Ahrefs](https://ahrefs.com/blog/discovered-currently-not-indexed/)).
5. **محتوى يُحقَن بـ JavaScript**: «غوغل يحتاج 9 أضعاف الوقت لزحف JS مقابل HTML»، و5–50% من صفحات JS الجديدة تبقى غير مفهرسة بعد أسبوعين ([Onely](https://www.onely.com/blog/google-needs-9x-more-time-to-crawl-js-than-html/)).
6. **روابط nofollow/ugc/sponsored**: «لن تُتبَّع عموماً» ولا تمرّر PageRank ([Google](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)). معظم إشارات السوشيال/المنتديات من هذا النوع.
7. **تأخّر النطاق الجديد («sandbox»)**: النطاقات الحديثة «تكافح للظهور أول 3–6 أشهر» ([Search Engine Journal](https://www.searchenginejournal.com/mueller-mentions-google-sandbox-and-honeymoon-ranking-effects/408994/)).
8. **الترتيب الجغرافي/اللغوي**: صفحة عربية/فرنسية عن علامة جزائرية صغيرة تتنافس في نتائج محلية ضعيفة الثقة لدى غوغل.
9. **أدلّة سبام مُزالة من الفهرس**: إشارة تعيش فقط على دليل رديء بلا تدقيق = قيمة صفرية ([Search Engine Land](https://searchengineland.com/guide/how-to-disavow-backlinks)).
10. **تأخّر تقارير غوغل + تضارب الأسماء**: غوغل يبلّغ عن عيّنة من الروابط فقط، وقد يفهرس Bing الرابط أسرع ([Reliablesoft](https://www.reliablesoft.net/backlinks-not-showing-google-search-console/)). وعند تطابق الاسم مع علامة أقدم، يرتّبها غوغل فوقك.

---

## 3. تحذير: تضارب الأسماء (يُضعِف ظهورك في غوغل فعلياً)

- **Mystoq** ↔ `mystoq.com` يوصَف في كثير من النتائج كتطبيق **إدارة بضائع/مخزون** أمريكي لا صلة له بالجزائر/TKAWEN؛ + لاعب Minecraft باسم mystoq. تأكّد أنّ ملفّات الأدلّة (مثل Crunchbase mystoq) تخصّك فعلاً قبل المطالبة بها.
- **LIQAA** ↔ كل نتائج «Liqaa video meeting» تعود لمنصّة **Wamid السعودية** (`liqaa.wamid.sa`، مجموعة تداول)؛ + `liqaa.app` (بطاقات تعريف) + `liqaabyhebah.com` (تعلّم لغات) + `liqo.io` (Kubernetes). كلمة «لقاء» شائعة عربياً.

**الأثر:** حتى لو ذكرك أحد، يرفع غوغل الاسم الأقدم/الأقوى فوقك. الحل: ترسيخ هوية مميَّزة (مثلاً «LIQAA by TKAWEN»، «Mystoq Algeria») في كل إشارة وبيانات schema، وبناء سلطة العلامة.

---

## 4. خطّة العلاج (عملية ومرتّبة بالأولوية)

**فوري (تملك الأدوات بالفعل في هذا المستودع):**
1. **IndexNow** — لديك `indexnow-daily` و`fresh-content-ping`. وسّعهما ليشملا صفحات الإشارات المملوكة (tkawen.online، صفحات المنتجات) لإجبار Bing على الفهرسة الفورية.
2. **أصلِح الـ29 رابطاً داخلياً مكسوراً** (`.data/links/report-2026-06-01.json`) — يوقف هدر ميزانية زحف غوغل (السبب 2 و3).
3. **اطلب الفهرسة يدوياً** في Google Search Console (URL Inspection → Request Indexing) لأهمّ الإشارات: ملفّات Crunchbase/Tracxn/StartupRanking وصفحات GitHub.

**خلال شهر:**
4. **حوّل الإشارات غير المرتبطة إلى روابط**: راسِل المواقع التي تذكرك نصّياً دون رابط (شبكات الأخبار الإقليمية) لإضافة رابط نظيف dofollow.
5. **استرجاع الروابط المعطّلة/المفقودة** (link reclamation): استعد أي رابط حُذف أو صار 404 (~26% نسبة نجاح المراسلة).
6. **وحِّد بدل التكرار**: أوقف نشر نفس البيان عبر شبكة نطاقات متطابقة (محتوى مكرّر)؛ انشر أصلاً واحداً قوياً واربط الباقي إليه.

**استراتيجي (يعالج السبب الجذري):**
7. **اكسب تغطية مستقلة حقيقية** — صحافة تقنية، مدوّنون غير تابعين، مراجعات. هذه فجوتك الكبرى: تقريباً كل «إشارة» حالية تعود إليك أو إلى المؤسس.
8. **احسم تضارب الأسماء** (§3) في كل بيانات schema وملفّات الأدلّة.
9. **لا تستخدم disavow** إلا عند إجراء يدوي فعلي من غوغل؛ هو يتجاهل السبام تلقائياً.

---

## 5. الأتمتة المرافقة

أُنشئ سكربت `scripts/backlink_accessibility_audit.py` ليكرّر هذا الاستطلاع دورياً:
- يحصد الإشارات من **DuckDuckGo** (فهرس Bing = «كل شيء عدا غوغل»)؛ Bing الخام معطّل افتراضياً لأنه يخدم نتائج مشوّهة للبوتات.
- يفحص حيوية كل رابط: `live` / `redirect` / `blocked` (403/429 = حيّ لكن يحظر البوت) / `broken` (404/5xx/timeout).
- يجسّ فهرسة غوغل best-effort ويسجّل `inconclusive` بأمانة عند حظر غوغل للكاشط.
- يصنّف كل إشارة في: `broken_or_orphaned` / `not_indexed_by_google` / `low_rank_platform` / `google_inconclusive` / `visible`.
- يحفظ JSON قابلاً للتدقيق تحت `.data/backlinks/audit-YYYY-MM-DD.json`.

التشغيل: `python3 scripts/backlink_accessibility_audit.py > .data/backlinks/audit-$(date -u +%Y-%m-%d).json`

> **حدود الأداة (شفافية):** نتائج DuckDuckGo تتباين بين الطلبات (كشط مجاني)، وجسّ غوغل يرجع `inconclusive` من بيئات CI لأن غوغل يحظر مراكز البيانات. الأداة للرصد المستمر للاتجاه، لا لقياس ترتيب غوغل الدقيق — لذلك يبقى التحقّق اليدوي عبر Search Console ضرورياً للقرارات الحاسمة.

---

## 6. ملاحظات منهجية ومصداقية

- لم يُختلَق أي رابط؛ كل رابط وُجد فعلاً في نتائج محرك أو جُلب وقُرئ.
- مواقع كثيرة (Crunchbase، Tracxn، StartupRanking، OpenPR، Medium) تردّ 403 على الجلب الآلي؛ وُسِمت 🔎 واعتُمد ظهورها المتكرّر عبر استعلامات مستقلة كدليل وجود.
- عدد الإشارات في ملف `.data/backlinks/` قد يختلف عن جرد هذا التقرير لأن DuckDuckGo يعيد مجموعات نتائج متغيّرة في كل تشغيل؛ التقرير يدمج عدة جولات بحث + الجلب اليدوي.
