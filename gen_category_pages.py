"""批量生成澳洲 + 欧洲 城市×品类 双语品类页（复用美国精简模板）"""
import json, os
from data_regions import TIERS, CITIES, build_items, get_verdict

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"
SITE = "https://subaog.com"
LASTMOD = "2026-09-05"

# ============ 复用美国精简模板的 CSS ============
CSS_EN = """:root{--primary:#0066CC;--primary-dark:#004C99;--primary-light:#E6F0FA;--green:#00B900;--bg:#F5F7FA;--text:#1A1A2E;--text-secondary:#64748B;--border:#E2E8F0;--radius-lg:16px;--radius-pill:24px;--nav-height:68px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;color:var(--text);line-height:1.7;font-size:16px;background:var(--bg)}
a{text-decoration:none;color:inherit}
.container{max-width:1100px;margin:0 auto;padding:0 24px}
.header{position:fixed;top:0;left:0;right:0;height:var(--nav-height);background:rgba(255,255,255.96);backdrop-filter:blur(12px);z-index:1000;box-shadow:0 1px 3px rgba(0,0,0.05)}
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
.footer{background:#1A1A2E;color:#fff;padding:40px 24px;text-align:center}
.footer a{color:#999}"""

CSS_ZH = CSS_EN.replace("'Segoe UI',Arial", "'PingFang SC','Microsoft YaHei'")


def build_faq_json(qa_list):
    """构造 FAQPage JSON-LD"""
    main_entity = []
    for q, a in qa_list:
        main_entity.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity,
    }, ensure_ascii=False, separators=(",", ":"))


def build_breadcrumb_json(items):
    """构造 BreadcrumbList JSON-LD"""
    lst = []
    for i, (name, url) in enumerate(items, start=1):
        lst.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": lst,
    }, ensure_ascii=False, separators=(",", ":"))


def generate_en(region, city_slug, city, item_slug, item, tier, verdict):
    """生成英文品类页"""
    region_en = tier["region_en"]
    price_20 = tier["price_20"]
    price_100 = tier["price_100"]
    tier_en = tier["tier_en"]

    title = f"Ship {item['en']} from {city['en']} to China | Subao Global"
    h1 = f"Ship {item['en']} from {city['en']} to China"
    meta = (
        f"Ship {item['en']} from {city['en']}, {region_en} to China: "
        f"{verdict['verdict_en']} Free pickup in {city['en']}, tax-inclusive door-to-door "
        f"in 10-15 working days, from ¥{price_20}/kg (20kg+). {city['local_en']}"
    )
    if len(meta) > 165:
        meta = meta[:162] + "…"

    # FAQ 4 问
    faq_qa = [
        (f"Can I ship {item['en'].lower()} from {city['en']} to China?", item["faq_q1_en"]),
        (f"How long does shipping from {city['en']} take?",
         f"Air freight 10-15 working days door-to-door. Free pickup across {city['en']}."),
        ("How much does it cost?",
         f"Air line from ¥{price_20}/kg (20-99kg, {tier_en}), ¥{price_100}/kg (100kg+). "
         "Volumetric weight = L×W×H (cm) ÷ 5000, charged on the larger."),
        (f"How do I book pickup in {city['en']}?",
         f"Free doorstep pickup across {city['en']} — book a window and we collect."),
    ]
    faq_json = build_faq_json(faq_qa)

    # 面包屑
    region_label = f"{region_en} to China"
    crumb = [
        ("Home", f"{SITE}/en/"),
        (region_label, f"{SITE}/en/{region}/"),
        (city["en"], f"{SITE}/en/{region}/{city_slug}/"),
        (item["en"], f"{SITE}/en/{region}/{city_slug}/{item_slug}/"),
    ]
    crumb_json = build_breadcrumb_json(crumb)

    # verdict 标题
    verdict_head = "Verdict: Allowed" if verdict["verdict_en"].startswith("Allowed") else "Verdict: Limited"

    # related service 内链
    related = (
        f'<a href="/en/{region}/{city_slug}/" style="font-size:15px;font-weight:700;color:var(--primary);text-decoration:underline">Ship from {city["en"]} to China →</a>'
    )
    if item.get("blog"):
        related += (
            f' · <a href="/en/blog/{item["blog"]}" style="font-size:15px;font-weight:700;color:var(--primary);text-decoration:underline">{item["en"]} to China guide →</a>'
        )

    # 可见 FAQ
    faq_visible = ""
    for q, a in faq_qa:
        faq_visible += (
            f'<div style="margin:16px 0"><p style="font-weight:700;margin:0 0 4px">Q: {q}</p>'
            f'<p style="margin:0;color:var(--text-secondary)">{a}</p></div>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/png" href="/assets/images/logo.png"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="applicable-device" content="pc,mobile">
  <title>{title}</title><meta name="description" content="{meta}">
  <link rel="canonical" href="{SITE}/en/{region}/{city_slug}/{item_slug}/">
  <link rel="alternate" hreflang="zh-CN" href="{SITE}/zh-cn/{region}/{city_slug}/{item_slug}/">
  <link rel="alternate" hreflang="en" href="{SITE}/en/{region}/{city_slug}/{item_slug}/">
  <link rel="alternate" hreflang="x-default" href="{SITE}/zh-cn/{region}/{city_slug}/{item_slug}/">
  <meta property="og:url" content="{SITE}/en/{region}/{city_slug}/{item_slug}/">
  <meta property="og:title" content="{h1}">
  <meta property="og:description" content="{meta}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE}/assets/images/og-image.jpg">
  <meta property="og:locale" content="en_US">
  <meta name="lastmod" content="{LASTMOD}">
  <script type="application/ld+json">{faq_json}</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-DJGPMS9MOB"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-DJGPMS9MOB');</script>
  <style>{CSS_EN}
  </style>
  <script type="application/ld+json">{crumb_json}</script>
</head>
<body>
  <header class="header"><div class="container">
    <a href="/en/" class="logo"><img src="/assets/images/logo.png" alt="Subao Global" style="height:63px;width:auto;display:block;" fetchpriority="high" decoding="async"></a>
    <nav class="nav">
      <a href="/en/">Home</a><a href="/en/{region}/">{region_en} to China</a>
      <a href="/en/tools/">Tools</a><a href="/en/blog/">Guides</a>
      <a href="{SITE}/zh-cn/{region}/{city_slug}/{item_slug}/" class="lang-switch" hreflang="zh-CN">🌐 English / 中文</a>
    </nav>
  </div></header>

  <section class="hero"><div class="container">
    <p class="hero-eyebrow" style="font-size:17px;letter-spacing:3px;opacity:.85;margin:0 0 10px;font-weight:500;text-transform:uppercase">Shipping to China</p><h1>{h1}</h1>
    <p class="subtitle">Free pickup in {city["en"]} · Tax-inclusive door-to-door · 10-15 working days</p>
  </div></section>
  <section class="section"><div class="container" style="max-width:800px">
    <div style="background:#fff;border:1px solid var(--border);border-radius:16px;padding:32px;margin-bottom:32px">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px;text-align:center">
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">¥{price_20}/kg</div><div style="font-size:12px;color:var(--text-secondary)">Air 20kg+ ({tier_en})</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">¥{price_100}/kg</div><div style="font-size:12px;color:var(--text-secondary)">100kg+</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">10-15</div><div style="font-size:12px;color:var(--text-secondary)">Working days</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">Tax-incl.</div><div style="font-size:12px;color:var(--text-secondary)">All-in price</div></div>
      </div>
    </div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">{verdict_head}</h2><p style="color:var(--text-secondary);line-height:1.9">{verdict['verdict_en']}</p></div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">Shipping from {city["en"]}</h2><p style="color:var(--text-secondary);line-height:1.9">{city['local_en']} Free doorstep pickup across {city["en"]}. Air freight with direct or connecting flights to China; first-tier cities clear fastest.</p></div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">Packing tips</h2><p style="color:var(--text-secondary);line-height:1.9">{verdict['packing_en']}</p></div>
    <div style="background:var(--primary-light);border:1px solid #CDE3F5;border-radius:12px;padding:20px 24px;margin:32px 0">
      <div style="font-size:14px;font-weight:700;color:var(--primary-dark);margin-bottom:6px">📦 Related service</div>
      {related}
    </div>
    <div class="section-title" style="margin-top:40px"><h2>Frequently asked questions</h2></div>
    {faq_visible}
    <div style="background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;padding:28px;border-radius:16px;text-align:center;margin:32px 0">
      <h3 style="font-size:1.1rem;margin-bottom:4px">Get a quote for {item["en"]} from {city["en"]}</h3>
      <p style="opacity:.85;margin-bottom:12px">30-minute proposal, free on-site estimate</p>
      <a href="https://d.salesmartly.com/fuxikn" target="_blank" rel="noopener" style="display:inline-block;background:#E65100;color:#fff;padding:12px 28px;border-radius:24px;font-weight:600" onclick="window.gtag&&gtag('event','consult_click',{{event_category:'conversion',event_label:'salesmartly',page_path:location.pathname}})">💬 Free consultation</a>
    </div>
  </div></section>
  <footer class="footer"><div class="container">© 2026 Subao Global Logistics | <a href="/en/">Home</a> · <a href="/sitemap.xml">Sitemap</a></div><div><h4>More</h4><a href="/en/routes/">All Routes</a><a href="/en/can-i-ship-index/">Can I Ship·Index</a><a href="/en/tools/customs-duty-calculator">Customs Duty</a><a href="/en/tools/volume-calculator">Volume Calc</a><a href="/en/tools/transit-time">Transit Time</a><a href="/en/tools/can-i-ship">Can I Ship?</a><a href="/en/tools/package-consolidation-calculator">Consolidation Calc</a><a href="/en/tools/shipping-calculator">Shipping Calculator</a></div>
  </footer>
</body>
</html>"""
    return html


def generate_zh(region, city_slug, city, item_slug, item, tier, verdict):
    """生成中文品类页"""
    region_zh = tier["region_zh"]
    price_20 = tier["price_20"]
    price_100 = tier["price_100"]
    tier_zh = tier["tier_zh"]

    title = f"从{city['zh']}寄{item['zh']}回国｜{region_zh}{city['zh']}到中国物流专线 | 速豹国际物流"
    h1 = f"从{city['zh']}寄{item['zh']}回国"
    meta = (
        f"从{region_zh}{city['zh']}寄{item['zh']}回国：{verdict['verdict_zh']}"
        f"{city['zh']}免费上门取件，10-15 个工作日门到门，¥{price_20}/kg 起（20-99kg）。"
        f"{city['local_zh']}"
    )
    if len(meta) > 165:
        meta = meta[:162] + "…"

    # FAQ 4 问
    faq_qa = [
        (f"从{city['zh']}寄{item['zh']}回国可以吗？", item["faq_q1_zh"]),
        (f"从{city['zh']}寄{item['zh']}要多久？",
         f"空运 10-15 个工作日门到门。{city['zh']}华人取件点覆盖广，当天可约取件。"),
        (f"从{city['zh']}寄{item['zh']}多少钱？",
         f"空运专线 20-99kg ¥{price_20}/kg（{tier_zh}），100kg+ ¥{price_100}/kg。体积重=长×宽×高÷5000，与实重取大者。"),
        (f"{city['zh']}怎么约取件？",
         f"{city['zh']}全城免费上门取件，预约时间即可，无需自送网点。"),
    ]
    faq_json = build_faq_json(faq_qa)

    # 面包屑
    crumb = [
        ("首页", f"{SITE}/zh-cn/"),
        (f"{region_zh}寄中国", f"{SITE}/zh-cn/{region}/"),
        (city["zh"], f"{SITE}/zh-cn/{region}/{city_slug}/"),
        (item["zh"], f"{SITE}/zh-cn/{region}/{city_slug}/{item_slug}/"),
    ]
    crumb_json = build_breadcrumb_json(crumb)

    # verdict 标题
    verdict_head = f"{item['zh']}寄送结论"

    # related service 内链
    related = (
        f'<a href="/zh-cn/{region}/{city_slug}/" style="font-size:15px;font-weight:700;color:var(--primary);text-decoration:underline">从{city["zh"]}寄中国 →</a>'
    )
    if item.get("blog"):
        related += (
            f' · <a href="/zh-cn/blog/{item["blog"]}" style="font-size:15px;font-weight:700;color:var(--primary);text-decoration:underline">{item["zh"]}寄中国全攻略 →</a>'
        )

    # 可见 FAQ
    faq_visible = ""
    for q, a in faq_qa:
        faq_visible += (
            f'<div style="margin:16px 0"><p style="font-weight:700;margin:0 0 4px">Q：{q}</p>'
            f'<p style="margin:0;color:var(--text-secondary)">{a}</p></div>'
        )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/png" href="/assets/images/logo.png"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="applicable-device" content="pc,mobile">
  <title>{title}</title><meta name="description" content="{meta}">
  <link rel="canonical" href="{SITE}/zh-cn/{region}/{city_slug}/{item_slug}/">
  <link rel="alternate" hreflang="zh-CN" href="{SITE}/zh-cn/{region}/{city_slug}/{item_slug}/">
  <link rel="alternate" hreflang="en" href="{SITE}/en/{region}/{city_slug}/{item_slug}/">
  <link rel="alternate" hreflang="x-default" href="{SITE}/zh-cn/{region}/{city_slug}/{item_slug}/">
  <meta property="og:url" content="{SITE}/zh-cn/{region}/{city_slug}/{item_slug}/">
  <meta property="og:title" content="{h1}">
  <meta property="og:description" content="{meta}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE}/assets/images/og-image.jpg">
  <meta property="og:locale" content="zh_CN">
  <meta name="lastmod" content="{LASTMOD}">
  <script type="application/ld+json">{faq_json}</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-DJGPMS9MOB"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-DJGPMS9MOB');</script>
  <style>{CSS_ZH}
  </style>
  <script type="application/ld+json">{crumb_json}</script>
</head>
<body>
  <header class="header"><div class="container">
    <a href="/zh-cn/" class="logo"><img src="/assets/images/logo.png" alt="速豹回国物流" style="height:63px;width:auto;display:block;" fetchpriority="high" decoding="async"></a>
    <nav class="nav">
      <a href="/zh-cn/">首页</a><a href="/zh-cn/{region}/">{region_zh}寄中国</a>
      <a href="/zh-cn/tools/">工具</a><a href="/zh-cn/blog/">攻略</a>
      <a href="{SITE}/en/{region}/{city_slug}/{item_slug}/" class="lang-switch" hreflang="en">🌐 中文 / English</a>
    </nav>
  </div></header>

  <section class="hero"><div class="container">
    <p class="hero-eyebrow" style="font-size:17px;letter-spacing:3px;opacity:.85;margin:0 0 10px;font-weight:500">各国寄中国专线</p><h1>{h1}</h1>
    <p class="subtitle">{city['zh']}免费上门取件 · 双清包税门到门 · 10-15 个工作日</p>
  </div></section>
  <section class="section"><div class="container" style="max-width:800px">
    <div style="background:#fff;border:1px solid var(--border);border-radius:16px;padding:32px;margin-bottom:32px">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px;text-align:center">
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">¥{price_20}/kg</div><div style="font-size:12px;color:var(--text-secondary)">空运 20kg+（{tier_zh}）</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">¥{price_100}/kg</div><div style="font-size:12px;color:var(--text-secondary)">100kg+</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">10-15</div><div style="font-size:12px;color:var(--text-secondary)">工作日门到门</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">双清包税</div><div style="font-size:12px;color:var(--text-secondary)">含关税</div></div>
      </div>
    </div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">{verdict_head}</h2><p style="color:var(--text-secondary);line-height:1.9"><strong>{verdict['verdict_zh']}</strong></p></div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">{city['zh']}出发：取件与航线</h2><p style="color:var(--text-secondary);line-height:1.9">{city['local_zh']}{city['zh']}全城免费上门取件，空运直飞或中转中国，一线城市清关最快。</p></div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">包装建议</h2><p style="color:var(--text-secondary);line-height:1.9">{verdict['packing_zh']}</p></div>
    <div style="background:var(--primary-light);border:1px solid #CDE3F5;border-radius:12px;padding:20px 24px;margin:32px 0">
      <div style="font-size:14px;font-weight:700;color:var(--primary-dark);margin-bottom:6px">📦 相关服务</div>
      {related}
    </div>
    <div class="section-title" style="margin-top:40px"><h2>常见问题</h2></div>
    {faq_visible}
    <div style="background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;padding:28px;border-radius:16px;text-align:center;margin:32px 0">
      <h3 style="font-size:1.1rem;margin-bottom:4px">从{city['zh']}寄{item['zh']}，立即获取报价</h3>
      <p style="opacity:.85;margin-bottom:12px">30 分钟出方案，免费上门估价</p>
      <a href="https://d.salesmartly.com/fuxikn" target="_blank" rel="noopener" style="display:inline-block;background:#E65100;color:#fff;padding:12px 28px;border-radius:24px;font-weight:600" onclick="window.gtag&&gtag('event','consult_click',{{event_category:'conversion',event_label:'salesmartly',page_path:location.pathname}})">💬 免费咨询</a>
    </div>
  </div></section>
  <footer class="footer"><div class="container">© 2026 速豹回国物流 | <a href="/zh-cn/">首页</a> · <a href="/sitemap.xml">Sitemap</a></div><div><h4>更多资源</h4><a href="/zh-cn/routes/">全部线路</a><a href="/zh-cn/can-i-ship-index/">能不能寄·分类</a><a href="/zh-cn/tools/customs-duty-calculator">关税估算</a><a href="/zh-cn/tools/volume-calculator">材积计算</a><a href="/zh-cn/tools/transit-time">时效查询</a><a href="/zh-cn/tools/can-i-ship">能不能寄</a><a href="/zh-cn/tools/package-consolidation-calculator">合箱计算</a><a href="/zh-cn/tools/shipping-calculator">运费计算</a></div>
  </footer>
</body>
</html>"""
    return html


def main():
    total = 0
    for region, tier in TIERS.items():
        items = build_items(region)
        for city_slug, city in CITIES[region].items():
            for item_slug, item_raw in items.items():
                verdict = get_verdict(region, item_slug, item_raw)
                # 生成 en
                en_dir = f"{BASE}/en/{region}/{city_slug}/{item_slug}"
                os.makedirs(en_dir, exist_ok=True)
                en_html = generate_en(region, city_slug, city, item_slug, item_raw, tier, verdict)
                with open(f"{en_dir}/index.html", "w", encoding="utf-8") as f:
                    f.write(en_html)
                # 生成 zh-cn
                zh_dir = f"{BASE}/zh-cn/{region}/{city_slug}/{item_slug}"
                os.makedirs(zh_dir, exist_ok=True)
                zh_html = generate_zh(region, city_slug, city, item_slug, item_raw, tier, verdict)
                with open(f"{zh_dir}/index.html", "w", encoding="utf-8") as f:
                    f.write(zh_html)
                total += 2
    print(f"✅ 生成完成：{total} 页（en + zh-cn）")


if __name__ == "__main__":
    main()
