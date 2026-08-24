#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen-pairwise-compare.py
========================
生成 3 个中美快递「两两对比」落地页（zh-cn + en 各一份，共 6 页）：
  1. USPS vs UPS   -> usps-vs-ups-china.html
  2. FedEx vs UPS  -> fedex-vs-ups-china.html
  3. DHL vs USPS   -> dhl-vs-usps-china.html

模板对齐现有 dhl-vs-fedex-vs-ups-china.html（内联 CSS / FAQ 折叠 / BreadcrumbList /
Article+FAQPage+Person Schema / hreflang 三件套 / Salesmartly CTA）。
"""
import json
from pathlib import Path

ROOT = Path("/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com")
ZH_BLOG = ROOT / "zh-cn" / "blog"
EN_BLOG = ROOT / "en" / "blog"
DATE = "2026-08-23"
SALESMARTLY = "https://d.salesmartly.com/fuxikn"
GA = "G-DJGPMS9MOB"

CSS = """:root{--primary:#0066CC;--primary-dark:#004C99;--primary-light:#E6F0FA;--green:#00B900;--bg:#F5F7FA;--text:#1A1A2E;--text-secondary:#64748B;--border:#E2E8F0;--radius-lg:16px;--radius-pill:24px;--nav-height:68px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:var(--text);line-height:1.7;font-size:16px;background:var(--bg)}
a{text-decoration:none;color:inherit}
.container{max-width:1100px;margin:0 auto;padding:0 24px}
.header{position:fixed;top:0;left:0;right:0;height:var(--nav-height);background:rgba(255,255,255,.96);backdrop-filter:blur(12px);z-index:1000;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.header .container{display:flex;align-items:center;justify-content:space-between;height:100%}
.logo{font-size:20px;font-weight:700;color:var(--primary)}
.nav{display:flex;align-items:center;gap:2px}
.nav a{padding:7px 13px;font-size:13px;font-weight:500;color:var(--text-secondary);border-radius:var(--radius-pill);white-space:nowrap}
.nav a:hover{color:var(--primary);background:var(--primary-light)}
.lang-switch{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;font-size:13px;font-weight:600;color:var(--primary);border:1.5px solid var(--primary-light);border-radius:var(--radius-pill);background:#fff}
@media(max-width:768px){.nav{display:none}}
.hero{background:linear-gradient(135deg,#0066CC,#004C99);color:#fff;padding:110px 24px 56px}
.hero h1{font-size:clamp(1.5rem,2.6vw,2.1rem);font-weight:700;margin-bottom:10px}
.hero .subtitle{font-size:15px;opacity:.92}
.section{padding:48px 0}
.section-title{text-align:center;margin-bottom:24px}
.section-title h2{font-size:1.5rem;font-weight:700}
.faq-item{border-bottom:1px solid var(--border)}
.faq-q{width:100%;padding:16px 0;text-align:left;background:none;border:none;font-size:15px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;font-family:inherit;color:var(--text)}
.faq-a{padding:0 0 16px;font-size:14px;color:var(--text-secondary);line-height:1.7;display:none}
.faq-a.show{display:block}
.cta-section{background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;padding:64px 24px;text-align:center;border-radius:var(--radius-lg);margin:0 24px}
@media(min-width:1200px){.cta-section{margin:0}}
.cta-section h2{font-size:1.6rem;margin-bottom:12px}
.cta-section p{opacity:.9;margin-bottom:24px;max-width:500px;margin-left:auto;margin-right:auto}
.btn-primary{display:inline-flex;align-items:center;gap:6px;background:#fff;color:var(--primary);padding:14px 34px;border-radius:var(--radius-pill);font-weight:700;font-size:15px}
.footer{background:#1A1A2E;color:#fff;padding:40px 24px;text-align:center}
.footer a{color:#999}
"""

GTAG = f"""  <script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA}');</script>"""

PERSON_JSON = """{"@context": "https://schema.org", "@type": "Person", "name": "速豹国际物流编辑团队", "jobTitle": "跨境物流内容编辑", "description": "12年国际及跨境物流经验", "knowsAbout": ["国际物流", "中美物流", "关税清关"]}"""

# 对比页集群（5 个中美快递对比页互链）
CLUSTER_ORDER = [
    "usps-vs-fedex-vs-chinese-courier",
    "dhl-vs-fedex-vs-ups-china",
    "usps-vs-ups-china",
    "fedex-vs-ups-china",
    "dhl-vs-usps-china",
]
CLUSTER_TITLES = {
    "zh": {
        "usps-vs-fedex-vs-chinese-courier": "USPS vs FedEx vs 华人快递 寄中国对比",
        "dhl-vs-fedex-vs-ups-china": "DHL vs FedEx vs UPS 寄中国对比",
        "usps-vs-ups-china": "USPS vs UPS 寄中国对比",
        "fedex-vs-ups-china": "FedEx vs UPS 寄中国对比",
        "dhl-vs-usps-china": "DHL vs USPS 寄中国对比",
    },
    "en": {
        "usps-vs-fedex-vs-chinese-courier": "USPS vs FedEx vs Chinese Courier to China",
        "dhl-vs-fedex-vs-ups-china": "DHL vs FedEx vs UPS to China",
        "usps-vs-ups-china": "USPS vs UPS to China",
        "fedex-vs-ups-china": "FedEx vs UPS to China",
        "dhl-vs-usps-china": "DHL vs USPS to China",
    },
}


def render(lang, slug, d):
    is_zh = lang == "zh"
    canon = f"https://subaog.com/{ 'zh-cn' if is_zh else 'en' }/blog/{slug}"
    # 对比页集群互链（排除自身）
    cluster_titles = CLUSTER_TITLES[lang]
    cluster_links = "".join(
        f'<a href="/{ "zh-cn" if is_zh else "en" }/blog/{s}.html" style="display:block;font-size:14px;font-weight:600;color:var(--primary);margin:5px 0">{cluster_titles[s]} →</a>'
        for s in CLUSTER_ORDER if s != slug
    )
    cluster_box = f'''    <div style="background:#fff;border:1px solid var(--border);border-radius:12px;padding:20px 24px;margin:24px 0">
      <div style="font-size:14px;font-weight:700;color:var(--primary-dark);margin-bottom:8px">{'🔍 更多中美快递两两对比' if is_zh else '🔍 More carrier head-to-head comparisons'}</div>
      {cluster_links}
    </div>'''
    other = f"https://subaog.com/{ 'en' if is_zh else 'zh-cn' }/blog/{slug}"
    home = "https://subaog.com/zh-cn/" if is_zh else "https://subaog.com/en/"
    logo_home = "/zh-cn/" if is_zh else "/en/"
    blog_idx = "/zh-cn/blog/" if is_zh else "/en/blog/"
    switch_target = other
    switch_label = "🌐 中文 / English" if is_zh else "🌐 English / 中文"
    switch_hreflang = "en" if is_zh else "zh-CN"

    # 章节
    sections_html = "\n".join(
        f'    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">{s["h"]}</h2><p style="color:var(--text-secondary);line-height:1.9">{s["p"]}</p></div>'
        for s in d["sections"]
    )

    # FAQ
    faq_html = "".join(
        f'<div class="faq-item"><button class="faq-q">{q}<span>▼</span></button><div class="faq-a">{a}</div></div>'
        for q, a in d["faqs"].items()
    )
    faq_json = json.dumps(
        [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faqs"].items()],
        ensure_ascii=False,
    )

    related_box = d["related_box"]
    article_json = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": d["headline"], "description": d["desc"],
        "datePublished": DATE, "dateModified": DATE,
        "author": {"@type": "Person", "name": "速豹国际物流编辑团队"}
    }, ensure_ascii=False)
    breadcrumb_json = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": home},
            {"@type": "ListItem", "position": 2, "name": "攻略", "item": blog_idx},
            {"@type": "ListItem", "position": 3, "name": d["headline"], "item": canon},
        ]
    }, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="{ 'zh-CN' if is_zh else 'en' }">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{d['title']}</title>
  <meta name="description" content="{d['desc']}">
  <link rel="alternate" hreflang="zh-CN" href="https://subaog.com/zh-cn/blog/{slug}">
  <link rel="alternate" hreflang="en" href="https://subaog.com/en/blog/{slug}">
  <link rel="alternate" hreflang="x-default" href="https://subaog.com/zh-cn/blog/{slug}">
  <link rel="canonical" href="{canon}">
  <meta property="og:title" content="{d['og_title']}">
  <meta property="og:description" content="{d['og_desc']}">
  <meta property="og:url" content="{canon}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://subaog.com/assets/images/og-image.jpg">
  <meta property="og:locale" content="{'zh_CN' if is_zh else 'en_US'}">
  <meta name="lastmod" content="{DATE}">
  <script type="application/ld+json">{article_json}</script>
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": {faq_json}}}</script>
  <script type="application/ld+json">{PERSON_JSON}</script>
  {GTAG}
  <style>{CSS}</style>
  <script type="application/ld+json">{breadcrumb_json}</script>
</head>
<body>
  <header class="header"><div class="container">
    <a href="{logo_home}" class="logo">速豹回国物流<span style="font-size:11px;color:var(--text-secondary);margin-left:8px">{'美国寄中国' if is_zh else 'USA to China'}</span></a>
    <nav class="nav">
      <a href="{logo_home}">{'首页' if is_zh else 'Home'}</a><a href="{ '/zh-cn/usa-to-china/' if is_zh else '/en/usa-to-china/' }">{'美国寄中国' if is_zh else 'USA to China'}</a>
      <a href="{blog_idx}" class="active">{'攻略' if is_zh else 'Guides'}</a>
      <a href="{switch_target}" class="lang-switch" hreflang="{switch_hreflang}">{switch_label}</a>
    </nav>
  </div></header>
  <section class="hero"><div class="container"><h1>{d['h1']}</h1><p class="subtitle">{d['subtitle']}</p></div></section>
  <section class="section"><div class="container" style="max-width:820px">
    {sections_html}
    <div style="background:var(--primary-light);border:1px solid #CDE3F5;border-radius:12px;padding:20px 24px;margin:32px 0">
      <div style="font-size:14px;font-weight:700;color:var(--primary-dark);margin-bottom:6px">📦 {related_box['title']}</div>
      <a href="{related_box['url']}" style="font-size:15px;font-weight:700;color:var(--primary);text-decoration:underline">{related_box['link']} →</a>
      <p style="font-size:13px;color:var(--text-secondary);margin-top:4px">{related_box['note']}</p>
    </div>
    {cluster_box}
    <div class="section-title" style="margin-top:44px"><h2>{d['faq_title']}</h2></div>
    {faq_html}
    <div style="max-width:800px;margin:32px auto 0;padding:0 24px;font-size:13px;color:#64748B">{'作者：' if is_zh else 'Author: '}<strong>速豹国际物流编辑团队</strong> · {'12年国际物流经验' if is_zh else '12 years international shipping'} · <a href="{ '/zh-cn/about.html' if is_zh else '/en/about.html' }" style="color:#0066CC">{'关于我们' if is_zh else 'About us'}</a></div>
  </div></section>
  <section class="cta-section"><div class="container">
    <h2>{d['cta_h']}</h2>
    <p>{d['cta_p']}</p>
    <a href="{SALESMARTLY}" class="btn-primary" target="_blank" rel="noopener">💬 {'免费咨询' if is_zh else 'Free Consultation'}</a>
  </div></section>
  <footer class="footer"><div class="container">© 2026 速豹回国物流 | <a href="{logo_home}">{'首页' if is_zh else 'Home'}</a> · <a href="/sitemap.xml">Sitemap</a></div></footer>
  <script>
    document.querySelectorAll('.faq-q').forEach(function(q){{q.addEventListener('click',function(){{var a=q.nextElementSibling;a.classList.toggle('show');q.querySelector('span').textContent=a.classList.contains('show')?'▲':'▼';}});}});
  </script>
</body>
</html>
"""
    return html


# ============ 内容数据 ============
PAGES = {}

# ---------- 1. USPS vs UPS ----------
PAGES["usps-vs-ups-china"] = {
    "zh": {
        "title": "USPS vs UPS 寄中国对比 2026｜费用时效谁更省",
        "desc": "USPS 与 UPS 寄中国全面对比：First Class/Priority 与 UPS Worldwide Saver 的 1磅/5磅/10磅价格表、时效、清关税费，行李与大件怎么选更划算 | 速豹回国物流",
        "og_title": "USPS vs UPS 寄中国，谁更省？",
        "og_desc": "USPS First Class/Priority 与 UPS Worldwide Saver 寄中国费用时效全面对比：价格表、清关税费、行李大件怎么选 | 速豹回国物流",
        "headline": "USPS vs UPS 寄中国，谁更省？",
        "h1": "USPS vs UPS 寄中国，谁更省？",
        "subtitle": "USPS First Class/Priority 与 UPS Worldwide Saver 费用时效全面对比：1磅/5磅/10磅价格表、清关税费规则、行李大件怎么选",
        "sections": [
            {"h": "费用对比（2026 实测价）", "p": "同样从美国寄 1 磅到中国：USPS Priority 约 $66-73（6-10 天），UPS Worldwide Saver 约 $67.75（3-6 天）。小件走 USPS First Class 仅约 $29.9，但慢（15 天）、限 4 磅内。5 磅：USPS Priority $93、UPS $98.96；10 磅：USPS $107、UPS 约 $130+。结论：轻小件 USPS 更便宜，急件 UPS 更快但略贵（数据源：USPS/UPS 官网 2026 费率）。"},
            {"h": "时效对比", "p": "USPS First Class 12-20 天、Priority 6-10 天；UPS Worldwide Saver 3-6 个工作日，明显更快更稳定。赶时间、发样品合同选 UPS；不急且求便宜选 USPS Priority。"},
            {"h": "清关与关税", "p": "两者都是商业清关，超 ¥1000 部分收 13% VAT + 10% 美货附加关税，收件人自行缴税。华人专线双清包税，税费已含在运费里，适合个人行李。"},
            {"h": "什么情况选 USPS", "p": "4 磅内轻小件求便宜、非紧急文件/衣物/零食、发往个人地址且能配合缴税。USPS 网点多、面单简单、丢件理赔流程成熟。"},
            {"h": "什么情况选 UPS", "p": "急件（3-6 天）、高价值小件要可靠追踪与保险、发往公司可对公开票、批量代购要稳定时效。UPS 上门取件与轨迹比 USPS 更稳。"},
            {"h": "终极对比表", "p": "维度 | USPS | UPS：1磅价 $29.9-$73 | $67.75；5磅价 $93 | $98.96；时效 6-20天 | 3-6天；清关 收件人缴税 | 收件人缴税；行李大件 不划算 | 不划算；敏感货 不支持 | 不支持。行李/大件/敏感货都建议走华人专线双清包税。"},
        ],
        "faqs": {
            "USPS 寄中国最便宜的是哪种？": "First Class 1 磅约 $29.9，但限 4 磅内、时效 15 天上下，适合轻小非急件。",
            "UPS 寄中国要多久？": "UPS Worldwide Saver 3-6 个工作日门到门，比 USPS Priority 快且轨迹更稳。",
            "USPS 和 UPS 哪个会被税？": "都会。两者默认商业清关，超 ¥1000 部分收 13% VAT + 10% 美货附加关税，收件人付。",
            "行李用 USPS 还是 UPS 寄？": "都不划算（30kg 约 $400-600+）。行李搬家建议华人专线双清包税，省 40-60%。",
            "化妆品能走 USPS/UPS 吗？": "不建议，液体/粉末查验率高易退运，走华人敏感货专线更稳。",
            "代购发货用哪个？": "日常代购走华人专线（$5-8/lb）；只有急件才用 UPS，USPS 性价比偏低。",
            "UPS 有保险吗？": "有，按申报价值收保费（约 1-3%），理赔相对规范。",
            "最划算的寄中国方式？": "21kg+ 行李/大件走华人专线（¥70-80/kg 双清包税），比 USPS/UPS 省 40-60%。",
        },
        "related_box": {"title": "📦 相关服务", "url": "/zh-cn/usa-to-china/", "link": "美国寄中国专线", "note": "比国际快递省 40-60% 的美国寄中国专线"},
        "faq_title": "常见问题", "cta_h": "30 分钟出方案，免费上门估价", "cta_p": "双清包税门到门 · 全美免费取件 · 全程可追踪",
    },
    "en": {
        "title": "USPS vs UPS Shipping to China 2026 | Cost & Speed Comparison",
        "desc": "USPS vs UPS shipping to China: First Class/Priority vs UPS Worldwide Saver prices (1/5/10 lb), transit times, customs & duty, and which is cheaper for luggage & heavy items | Subao",
        "og_title": "USPS vs UPS to China: Which Is Cheaper?",
        "og_desc": "USPS First Class/Priority vs UPS Worldwide Saver shipping to China: price table, transit times, customs & duty, best choice for luggage | Subao",
        "headline": "USPS vs UPS Shipping to China: Which Is Cheaper?",
        "h1": "USPS vs UPS Shipping to China: Which Is Cheaper?",
        "subtitle": "Full cost & speed comparison of USPS First Class/Priority vs UPS Worldwide Saver: 1/5/10 lb price table, customs rules, and when to choose each",
        "sections": [
            {"h": "Cost Comparison (2026 rates)", "p": "Shipping 1 lb from the US to China: USPS Priority ~$66-73 (6-10 days), UPS Worldwide Saver ~$67.75 (3-6 days). For light items, USPS First Class is only ~$29.9 but slow (15 days) and capped at 4 lb. 5 lb: USPS Priority $93, UPS $98.96; 10 lb: USPS $107, UPS $130+. Verdict: USPS is cheaper for light parcels, UPS is faster but slightly pricier (source: USPS/UPS 2026 rates)."},
            {"h": "Transit Time", "p": "USPS First Class 12-20 days, Priority 6-10 days; UPS Worldwide Saver 3-6 business days, clearly faster and more reliable. Choose UPS for urgent samples/contracts; USPS Priority when cost matters more than speed."},
            {"h": "Customs & Duty", "p": "Both use commercial clearance; shipments over ¥1000 incur 13% VAT + 10% US-goods tariff, paid by the receiver. Chinese consolidation lines offer DDP (tax included), ideal for personal luggage."},
            {"h": "When to Choose USPS", "p": "Light non-urgent items under 4 lb, documents/clothes/snacks, shipping to a residential address that can handle customs payment. USPS has wide drop-off, simple labels, and mature claim process."},
            {"h": "When to Choose UPS", "p": "Urgent shipments (3-6 days), high-value small items needing reliable tracking & insurance, business deliveries needing invoices, or bulk daigou needing stable schedules. UPS pickup and tracking are steadier than USPS."},
            {"h": "Ultimate Comparison Table", "p": "Metric | USPS | UPS: 1 lb $29.9-$73 | $67.75; 5 lb $93 | $98.96; transit 6-20 days | 3-6 days; clearance receiver pays | receiver pays; luggage/heavy not cost-effective | not cost-effective; sensitive goods unsupported | unsupported. For luggage/heavy/sensitive, use a Chinese DDP line."},
        ],
        "faqs": {
            "What is the cheapest USPS option to China?": "First Class at ~$29.9/lb (under 4 lb), but 15-day transit — best for light, non-urgent parcels.",
            "How long does UPS take to China?": "UPS Worldwide Saver delivers in 3-6 business days, faster and more trackable than USPS Priority.",
            "Do USPS and UPS get taxed?": "Yes. Both use commercial clearance; over ¥1000 incurs 13% VAT + 10% US-goods tariff, paid by the receiver.",
            "Ship luggage via USPS or UPS?": "Neither is cost-effective (30kg ~$400-600+). Use a Chinese DDP line for luggage, saving 40-60%.",
            "Can cosmetics go via USPS/UPS?": "Not recommended — liquids/powders face high inspection and may be returned. Use a sensitive-goods line.",
            "Which for daigou shipping?": "Daily daigou uses a Chinese line ($5-8/lb); only urgent items use UPS. USPS offers weak value.",
            "Does UPS offer insurance?": "Yes, ~1-3% of declared value, with a relatively standardized claim process.",
            "Cheapest way to ship to China?": "For 21kg+ luggage/heavy items, a Chinese DDP line (¥70-80/kg) saves 40-60% vs USPS/UPS.",
        },
        "related_box": {"title": "📦 Related Service", "url": "/en/usa-to-china/", "link": "USA to China Shipping Line", "note": "Ship from the US to China for 40-60% less than express carriers"},
        "faq_title": "FAQ", "cta_h": "Get a Plan in 30 Minutes — Free Pickup Estimate", "cta_p": "Door-to-door DDP · Free US pickup · Full tracking",
    },
}

# ---------- 2. FedEx vs UPS ----------
PAGES["fedex-vs-ups-china"] = {
    "zh": {
        "title": "FedEx vs UPS 寄中国对比 2026｜费用时效谁更划算",
        "desc": "FedEx 与 UPS 寄中国全面对比：FedEx Priority/International 与 UPS Worldwide Saver 的 1磅/5磅/10磅价格表、时效、清关税费，急件与大件怎么选 | 速豹回国物流",
        "og_title": "FedEx vs UPS 寄中国，谁更划算？",
        "og_desc": "FedEx Priority/International 与 UPS Worldwide Saver 寄中国费用时效全面对比：价格表、清关税费、急件大件怎么选 | 速豹回国物流",
        "headline": "FedEx vs UPS 寄中国，谁更划算？",
        "h1": "FedEx vs UPS 寄中国，谁更划算？",
        "subtitle": "FedEx Priority/International 与 UPS Worldwide Saver 费用时效全面对比：1磅/5磅/10磅价格表、清关税费规则、急件大件怎么选",
        "sections": [
            {"h": "费用对比（2026 实测价）", "p": "同样从美国寄 1 磅到中国：FedEx Priority 约 $73.18、UPS Worldwide Saver 约 $67.75。5 磅：FedEx $93.35、UPS $98.96；10 磅：FedEx 约 $107、UPS 约 $130+。两者价格高度接近，FedEx 在 1-5 磅段略贵、10 磅段反而更便宜；UPS 大件涨幅更陡（数据源：Shippo/MyUS 2026-05）。"},
            {"h": "时效对比", "p": "FedEx Priority 3-6 天、UPS Worldwide Saver 3-6 天，几乎并列。实际稳定性看取件点与航线：美国西岸 FedEx 略快，东岸 UPS 网络更密。两者都比华人专线快（7-10 天）。"},
            {"h": "清关与关税", "p": "都是商业清关，超 ¥1000 部分收 13% VAT + 10% 美货附加关税，收件人付。华人渠道双清包税，税费含运费。急件要时效就接受商业清关，个人行李走专线更稳。"},
            {"h": "什么情况选 FedEx", "p": "西岸取件、文件/样品急件、对 FedEx 账号有协议价、要国际优先（IP）全球网络。FedEx 在亚太航线密度高，部分城市清关更快。"},
            {"h": "什么情况选 UPS", "p": "东岸/中部取件、要更稳的地面+空运衔接、公司件要对公开票、批量代购要稳定排期。UPS 在美国本土地面网络最强。"},
            {"h": "终极对比表", "p": "维度 | FedEx | UPS：1磅价 $73.18 | $67.75；5磅价 $93.35 | $98.96；10磅价 ~$107 | $130+；时效 3-6天 | 3-6天；清关 收件人缴税 | 收件人缴税；行李大件 不划算 | 不划算。行李/大件/敏感货均建议华人专线双清包税。"},
        ],
        "faqs": {
            "FedEx 和 UPS 寄中国哪个便宜？": "1-5 磅 UPS 略便宜，10 磅起 FedEx 反而更便宜；整体价格高度接近，差几美元。",
            "FedEx 寄中国要多久？": "FedEx Priority 3-6 个工作日，与 UPS 几乎并列。",
            "UPS 寄中国多少钱？": "1 磅约 $67.75、5 磅约 $98.96、10 磅约 $130+（Worldwide Saver）。",
            "两者会被税吗？": "会。商业清关，超 ¥1000 部分收 13% VAT + 10% 美货附加关税，收件人付。",
            "行李用 FedEx 还是 UPS？": "都不划算（30kg 约 $500-650）。行李搬家走华人专线双清包税，省 40-60%。",
            "化妆品能走这两家吗？": "不建议，液体/敏感货查验率高易退运，走华人敏感货专线。",
            "代购发货用哪个？": "日常代购走华人专线（$5-8/lb）；急件才用 FedEx/UPS，两者差不大。",
            "最划算的寄中国方式？": "21kg+ 行李/大件走华人专线（¥70-80/kg 双清包税），比 FedEx/UPS 省 40-60%。",
        },
        "related_box": {"title": "📦 相关服务", "url": "/zh-cn/usa-to-china/", "link": "美国寄中国专线", "note": "比国际快递省 40-60% 的美国寄中国专线"},
        "faq_title": "常见问题", "cta_h": "30 分钟出方案，免费上门估价", "cta_p": "双清包税门到门 · 全美免费取件 · 全程可追踪",
    },
    "en": {
        "title": "FedEx vs UPS Shipping to China 2026 | Cost & Speed Comparison",
        "desc": "FedEx vs UPS shipping to China: FedEx Priority/International vs UPS Worldwide Saver prices (1/5/10 lb), transit times, customs & duty, and which is better for urgent & heavy items | Subao",
        "og_title": "FedEx vs UPS to China: Which Is Better?",
        "og_desc": "FedEx Priority/International vs UPS Worldwide Saver shipping to China: price table, transit times, customs & duty, best for urgent/heavy | Subao",
        "headline": "FedEx vs UPS Shipping to China: Which Is Better?",
        "h1": "FedEx vs UPS Shipping to China: Which Is Better?",
        "subtitle": "Full cost & speed comparison of FedEx Priority/International vs UPS Worldwide Saver: 1/5/10 lb price table, customs rules, and when to choose each",
        "sections": [
            {"h": "Cost Comparison (2026 rates)", "p": "Shipping 1 lb from the US to China: FedEx Priority ~$73.18, UPS Worldwide Saver ~$67.75. 5 lb: FedEx $93.35, UPS $98.96; 10 lb: FedEx ~$107, UPS $130+. Prices are very close — FedEx is slightly pricier at 1-5 lb but cheaper at 10 lb, while UPS rises more steeply for heavy items (source: Shippo/MyUS 2026-05)."},
            {"h": "Transit Time", "p": "FedEx Priority 3-6 days, UPS Worldwide Saver 3-6 days — essentially tied. Real-world stability depends on pickup location and routes: FedEx is slightly faster on the US West Coast, UPS denser in the East. Both beat Chinese lines (7-10 days)."},
            {"h": "Customs & Duty", "p": "Both use commercial clearance; over ¥1000 incurs 13% VAT + 10% US-goods tariff, paid by the receiver. Chinese DDP lines include tax in freight. Accept commercial clearance for urgent items; use a line for personal luggage."},
            {"h": "When to Choose FedEx", "p": "West Coast pickups, urgent documents/samples, negotiated FedEx account rates, or International Priority global network. FedEx has dense Asia-Pacific routes, faster clearance in some cities."},
            {"h": "When to Choose UPS", "p": "East Coast/Central pickups, stronger ground+air handoff, business invoices, or bulk daigou needing stable schedules. UPS has the strongest US domestic ground network."},
            {"h": "Ultimate Comparison Table", "p": "Metric | FedEx | UPS: 1 lb $73.18 | $67.75; 5 lb $93.35 | $98.96; 10 lb ~$107 | $130+; transit 3-6 days | 3-6 days; clearance receiver pays | receiver pays; luggage/heavy not cost-effective | not cost-effective. For luggage/heavy/sensitive, use a Chinese DDP line."},
        ],
        "faqs": {
            "Which is cheaper, FedEx or UPS to China?": "UPS is slightly cheaper at 1-5 lb; FedEx becomes cheaper at 10 lb+. Overall they differ by just a few dollars.",
            "How long does FedEx take to China?": "FedEx Priority delivers in 3-6 business days, nearly tied with UPS.",
            "How much is UPS to China?": "About $67.75/lb, $98.96/5lb, $130+/10lb (Worldwide Saver).",
            "Do both get taxed?": "Yes. Commercial clearance; over ¥1000 incurs 13% VAT + 10% US-goods tariff, paid by the receiver.",
            "Ship luggage via FedEx or UPS?": "Neither is cost-effective (30kg ~$500-650). Use a Chinese DDP line for luggage, saving 40-60%.",
            "Can cosmetics go via these carriers?": "Not recommended — liquids/sensitive goods face high inspection and may be returned. Use a sensitive-goods line.",
            "Which for daigou shipping?": "Daily daigou uses a Chinese line ($5-8/lb); only urgent items use FedEx/UPS, which are close in price.",
            "Cheapest way to ship to China?": "For 21kg+ luggage/heavy items, a Chinese DDP line (¥70-80/kg) saves 40-60% vs FedEx/UPS.",
        },
        "related_box": {"title": "📦 Related Service", "url": "/en/usa-to-china/", "link": "USA to China Shipping Line", "note": "Ship from the US to China for 40-60% less than express carriers"},
        "faq_title": "FAQ", "cta_h": "Get a Plan in 30 Minutes — Free Pickup Estimate", "cta_p": "Door-to-door DDP · Free US pickup · Full tracking",
    },
}

# ---------- 3. DHL vs USPS ----------
PAGES["dhl-vs-usps-china"] = {
    "zh": {
        "title": "DHL vs USPS 寄中国对比 2026｜时效费用怎么选",
        "desc": "DHL 与 USPS 寄中国全面对比：DHL Express 与 USPS First Class/Priority 的 1磅/5磅/10磅价格表、时效、清关税费，急件与轻小件怎么选 | 速豹回国物流",
        "og_title": "DHL vs USPS 寄中国，怎么选？",
        "og_desc": "DHL Express 与 USPS First Class/Priority 寄中国费用时效全面对比：价格表、清关税费、急件轻小件怎么选 | 速豹回国物流",
        "headline": "DHL vs USPS 寄中国，怎么选？",
        "h1": "DHL vs USPS 寄中国，怎么选？",
        "subtitle": "DHL Express 与 USPS First Class/Priority 费用时效全面对比：1磅/5磅/10磅价格表、清关税费规则、急件与轻小件怎么选",
        "sections": [
            {"h": "费用对比（2026 实测价）", "p": "同样从美国寄 1 磅到中国：DHL Express 约 $66.97（2-5 天）、USPS Priority 约 $66-73（6-10 天）、USPS First Class 仅 $29.9（15 天，限 4 磅内）。5 磅：DHL $94.12、USPS Priority $93；10 磅：DHL 约 $107、USPS $107。轻小件 USPS First Class 最便宜，急件 DHL 最快（数据源：Shippo/MyUS 2026-05）。"},
            {"h": "时效对比", "p": "DHL Express 2-5 个工作日最快；USPS Priority 6-10 天；USPS First Class 12-20 天。DHL 比 USPS 快 1 倍不止，但价格也高——First Class 除外（便宜但慢）。"},
            {"h": "清关与关税", "p": "都是商业清关，超 ¥1000 部分收 13% VAT + 10% 美货附加关税，收件人付。华人渠道双清包税。DHL 清关专业但税费照收，USPS 面单简单但同样商业清关。"},
            {"h": "什么情况选 DHL", "p": "真急件（2-5 天）、高价值小件要保险与可靠追踪、文件/合同/样品、发往公司可对公开票。DHL 全球清关网络最强。"},
            {"h": "什么情况选 USPS", "p": "轻小非急件求便宜（First Class $29.9）、个人地址能配合缴税、发衣物零食等低值品。USPS 面单简单、网点多。"},
            {"h": "终极对比表", "p": "维度 | DHL | USPS：1磅价 $66.97 | $29.9-$73；5磅价 $94.12 | $93；时效 2-5天 | 6-20天；清关 收件人缴税 | 收件人缴税；行李大件 不划算 | 不划算；敏感货 不支持 | 不支持。行李/大件/敏感货建议华人专线双清包税。"},
        ],
        "faqs": {
            "DHL 寄中国要多久？": "DHL Express 2-5 个工作日门到门，最快但最贵。",
            "USPS 寄中国最便宜的是哪种？": "First Class 1 磅约 $29.9，限 4 磅内、约 15 天，适合轻小非急件。",
            "DHL 和 USPS 哪个会被税？": "都会。商业清关，超 ¥1000 部分收 13% VAT + 10% 美货附加关税，收件人付。",
            "行李用 DHL 还是 USPS？": "都不划算（30kg DHL $600+、USPS 也贵）。行李走华人专线双清包税，省 40-60%。",
            "化妆品能走 DHL/USPS 吗？": "不建议，液体/敏感货查验率高易退运，走华人敏感货专线。",
            "代购发货用哪个？": "日常代购走华人专线（$5-8/lb）；急件才用 DHL，USPS 性价比偏低。",
            "DHL 有保险吗？": "有，按申报价值收保费（约 3%），理赔流程规范。",
            "最划算的寄中国方式？": "21kg+ 行李/大件走华人专线（¥70-80/kg 双清包税），比 DHL/USPS 省 40-60%。",
        },
        "related_box": {"title": "📦 相关服务", "url": "/zh-cn/usa-to-china/", "link": "美国寄中国专线", "note": "比国际快递省 40-60% 的美国寄中国专线"},
        "faq_title": "常见问题", "cta_h": "30 分钟出方案，免费上门估价", "cta_p": "双清包税门到门 · 全美免费取件 · 全程可追踪",
    },
    "en": {
        "title": "DHL vs USPS Shipping to China 2026 | Cost & Speed Comparison",
        "desc": "DHL vs USPS shipping to China: DHL Express vs USPS First Class/Priority prices (1/5/10 lb), transit times, customs & duty, and which to choose for urgent vs light items | Subao",
        "og_title": "DHL vs USPS to China: Which to Choose?",
        "og_desc": "DHL Express vs USPS First Class/Priority shipping to China: price table, transit times, customs & duty, best for urgent vs light items | Subao",
        "headline": "DHL vs USPS Shipping to China: Which to Choose?",
        "h1": "DHL vs USPS Shipping to China: Which to Choose?",
        "subtitle": "Full cost & speed comparison of DHL Express vs USPS First Class/Priority: 1/5/10 lb price table, customs rules, and when to choose each",
        "sections": [
            {"h": "Cost Comparison (2026 rates)", "p": "Shipping 1 lb from the US to China: DHL Express ~$66.97 (2-5 days), USPS Priority ~$66-73 (6-10 days), USPS First Class only $29.9 (15 days, under 4 lb). 5 lb: DHL $94.12, USPS Priority $93; 10 lb: DHL ~$107, USPS $107. USPS First Class is cheapest for light items; DHL is fastest for urgent ones (source: Shippo/MyUS 2026-05)."},
            {"h": "Transit Time", "p": "DHL Express 2-5 business days (fastest); USPS Priority 6-10 days; USPS First Class 12-20 days. DHL is more than twice as fast as USPS, but costs more — except First Class, which is cheap but slow."},
            {"h": "Customs & Duty", "p": "Both use commercial clearance; over ¥1000 incurs 13% VAT + 10% US-goods tariff, paid by the receiver. Chinese DDP lines include tax. DHL clears professionally but still charges duty; USPS labels are simpler but equally commercial."},
            {"h": "When to Choose DHL", "p": "Truly urgent (2-5 days), high-value small items needing insurance & reliable tracking, documents/contracts/samples, or business deliveries needing invoices. DHL has the strongest global clearance network."},
            {"h": "When to Choose USPS", "p": "Light non-urgent items on a budget (First Class $29.9), residential addresses that can handle customs, low-value clothes/snacks. USPS has simple labels and wide drop-off."},
            {"h": "Ultimate Comparison Table", "p": "Metric | DHL | USPS: 1 lb $66.97 | $29.9-$73; 5 lb $94.12 | $93; transit 2-5 days | 6-20 days; clearance receiver pays | receiver pays; luggage/heavy not cost-effective | not cost-effective; sensitive goods unsupported | unsupported. For luggage/heavy/sensitive, use a Chinese DDP line."},
        ],
        "faqs": {
            "How long does DHL take to China?": "DHL Express delivers in 2-5 business days door-to-door — fastest but priciest.",
            "What is the cheapest USPS option to China?": "First Class at ~$29.9/lb (under 4 lb), ~15-day transit — best for light, non-urgent parcels.",
            "Do DHL and USPS get taxed?": "Yes. Both use commercial clearance; over ¥1000 incurs 13% VAT + 10% US-goods tariff, paid by the receiver.",
            "Ship luggage via DHL or USPS?": "Neither is cost-effective (30kg DHL $600+, USPS also pricey). Use a Chinese DDP line, saving 40-60%.",
            "Can cosmetics go via DHL/USPS?": "Not recommended — liquids/sensitive goods face high inspection and may be returned. Use a sensitive-goods line.",
            "Which for daigou shipping?": "Daily daigou uses a Chinese line ($5-8/lb); only urgent items use DHL. USPS offers weak value.",
            "Does DHL offer insurance?": "Yes, ~3% of declared value, with a standardized claim process.",
            "Cheapest way to ship to China?": "For 21kg+ luggage/heavy items, a Chinese DDP line (¥70-80/kg) saves 40-60% vs DHL/USPS.",
        },
        "related_box": {"title": "📦 Related Service", "url": "/en/usa-to-china/", "link": "USA to China Shipping Line", "note": "Ship from the US to China for 40-60% less than express carriers"},
        "faq_title": "FAQ", "cta_h": "Get a Plan in 30 Minutes — Free Pickup Estimate", "cta_p": "Door-to-door DDP · Free US pickup · Full tracking",
    },
}


def main():
    for slug, langs in PAGES.items():
        for lang, d in langs.items():
            out = (ZH_BLOG if lang == "zh" else EN_BLOG) / f"{slug}.html"
            out.write_text(render(lang, slug, d), encoding="utf-8")
            print(f"✅ {out}")
    print(f"\n共生成 {len(PAGES)*2} 个页面")


if __name__ == "__main__":
    main()
