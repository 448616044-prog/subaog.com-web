#!/usr/bin/env python3
"""品类 × 城市组合页生成器
URL: /zh-cn/usa-to-china/{city}/{item}/ + /en/usa-to-china/{city}/{item}/
每页差异化：城市取件 + 品类税率/注意事项 + 价格 + FAQ + 内链（城市出发页/品类页/城市对）
"""
import json, re, importlib.util
from pathlib import Path

ROOT = Path("/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com")
DOMAIN = "https://subaog.com"
GA_ID = "G-DJGPMS9MOB"

# 导入品类数据（gen-can-i-ship.py 的 ITEMS）
spec = importlib.util.spec_from_file_location("gcis", str(ROOT / "gen-can-i-ship.py"))
gcis = importlib.util.module_from_spec(spec); spec.loader.exec_module(gcis)
ITEMS = gcis.ITEMS
print(f"品类: {len(ITEMS)} 个")

# 导入城市数据（gen-zh-usa-city.py 的 CITIES）
spec2 = importlib.util.spec_from_file_location("gzc", str(ROOT / "gen-zh-usa-city.py"))
gzc = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(gzc)
CITIES = gzc.CITIES
print(f"城市: {len(CITIES)} 个")

# 英文城市名映射
CITY_EN = {c["slug"]: c["en"] for c in CITIES}

# 品类税率标签（en）
def item_verdict_en(item):
    return item["verdict_en"]

def gen_page(lang, city, item):
    """lang: zh-cn / en"""
    cslug, cname = city["slug"], city["zh"]
    islug, izh, ien = item["slug"], item["zh"], item["en"]
    city_en = CITY_EN[cslug]
    item_slug_low = islug

    if lang == "zh-cn":
        rel = f"usa-to-china/{cslug}/{islug}/index.html"
        zh_url = f"{DOMAIN}/zh-cn/{rel}"
        en_url = f"{DOMAIN}/en/usa-to-china/{cslug}/{islug}/"
        title = f"从{cname}寄{izh}回国｜美国{cname}到中国物流专线 | 速豹国际物流"
        desc = (f"从美国{cname}寄{izh}回国：{item['verdict_zh']}，税率{item['rate']}。"
                f"{cname}免费上门取件，双清包税门到门 7-10 工作日。{item['note_zh']} | 12年国际物流经验")
        h1 = f"从{cname}寄{izh}回国"
        # FAQ
        faq = [
            (f"从{cname}寄{izh}回国可以吗？",
             f"{item['verdict_zh']}。{item['note_zh']}。超出人民币1000元免税额部分按{item['rate']}税率计税，双清包税渠道已含基础关税。"),
            (f"从{cname}寄{izh}要多久？",
             f"空运 7-10 工作日门到门。{cname}华人取件点覆盖广，当天可约取件。"),
            (f"从{cname}寄{izh}多少钱？",
             f"空运专线 21kg+ ¥80/kg 起（美国档），100kg+ ¥75/kg。体积重=长×宽×高÷5000，与实重取大者。"),
            (f"{cname}怎么约取件？",
             f"{cname}全城免费上门取件，预约时间即可，无需自送网点。"),
        ]
        faq_schema = json.dumps({"@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}, ensure_ascii=False)
        body = f"""
  <section class="hero"><div class="container">
    <h1>{h1}</h1>
    <p class="subtitle">{cname}免费上门取件 · 双清包税门到门 · 7-10 工作日</p>
  </div></section>
  <section class="section"><div class="container" style="max-width:800px">
    <div style="background:#fff;border:1px solid var(--border);border-radius:16px;padding:32px;margin-bottom:32px">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px;text-align:center">
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">¥80/kg</div><div style="font-size:12px;color:var(--text-secondary)">空运 21kg+（美国档）</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">¥75/kg</div><div style="font-size:12px;color:var(--text-secondary)">100kg+</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">7-10</div><div style="font-size:12px;color:var(--text-secondary)">工作日门到门</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">双清包税</div><div style="font-size:12px;color:var(--text-secondary)">含关税</div></div>
      </div>
    </div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">{izh}寄送结论</h2><p style="color:var(--text-secondary);line-height:1.9"><strong>{item['verdict_zh']}</strong>。{item['note_zh']}。超出人民币 1000 元免税额部分按 {item['rate']} 税率计税。</p></div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">{cname}出发：取件与航线</h2><p style="color:var(--text-secondary);line-height:1.9">{city['note']}。{cname}全城免费上门取件，空运直飞或中转中国，一线城市清关最快。</p></div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">包装建议</h2><p style="color:var(--text-secondary);line-height:1.9">{izh}建议：保留原包装、做好缓冲防压、如实申报品名避免海关延误。易碎品类务必加固+警示标识。</p></div>
    <div style="background:var(--primary-light);border:1px solid #CDE3F5;border-radius:12px;padding:20px 24px;margin:32px 0">
      <div style="font-size:14px;font-weight:700;color:var(--primary-dark);margin-bottom:6px">📦 相关服务</div>
      <a href="/zh-cn/usa-to-china/{cslug}/" style="font-size:15px;font-weight:700;color:var(--primary);text-decoration:underline">从{cname}寄中国 →</a> ·
      <a href="/zh-cn/blog/can-i-ship-{islug}-to-china.html" style="font-size:15px;font-weight:700;color:var(--primary);text-decoration:underline">{izh}寄中国全攻略 →</a>
    </div>
    <div class="section-title" style="margin-top:40px"><h2>常见问题</h2></div>
    {''.join(f'<div style="margin:16px 0"><p style="font-weight:700;margin:0 0 4px">Q：{q}</p><p style="margin:0;color:var(--text-secondary)">{a}</p></div>' for q, a in faq)}
    <div class="cta-bar" style="background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;padding:28px;border-radius:16px;text-align:center;margin:32px 0">
      <h3 style="font-size:1.1rem;margin-bottom:4px">从{cname}寄{izh}，立即获取报价</h3>
      <p style="opacity:.85;margin-bottom:12px">30 分钟出方案，免费上门估价</p>
      <a href="https://d.salesmartly.com/fuxikn" class="btn-primary" target="_blank" rel="noopener" style="display:inline-block;background:#E65100;color:#fff;padding:12px 28px;border-radius:24px;font-weight:600">💬 免费咨询</a>
    </div>
  </div></section>"""
        page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="applicable-device" content="pc,mobile">
  <title>{title}</title><meta name="description" content="{desc}">
  <link rel="alternate" hreflang="zh-CN" href="{zh_url}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="x-default" href="{zh_url}">
  <link rel="canonical" href="{zh_url}">
  <meta property="og:title" content="{h1}">
  <meta property="og:description" content="{desc[:100]}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{DOMAIN}/assets/images/og-image.jpg">
  <meta property="og:locale" content="zh_CN">
  <meta name="lastmod" content="2026-08-20">
  <script type="application/ld+json">{faq_schema}</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
  <style>
:root{{--primary:#0066CC;--primary-dark:#004C99;--primary-light:#E6F0FA;--green:#00B900;--bg:#F5F7FA;--text:#1A1A2E;--text-secondary:#64748B;--border:#E2E8F0;--radius-lg:16px;--radius-pill:24px;--nav-height:68px}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:var(--text);line-height:1.7;font-size:16px;background:var(--bg)}}
a{{text-decoration:none;color:inherit}}
.container{{max-width:1100px;margin:0 auto;padding:0 24px}}
.header{{position:fixed;top:0;left:0;right:0;height:var(--nav-height);background:rgba(255,255,255,.96);backdrop-filter:blur(12px);z-index:1000;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
.header .container{{display:flex;align-items:center;justify-content:space-between;height:100%}}
.logo{{font-size:20px;font-weight:700;color:var(--primary)}}
.nav{{display:flex;align-items:center;gap:2px}}
.nav a{{padding:7px 13px;font-size:13px;font-weight:500;color:var(--text-secondary);border-radius:var(--radius-pill);white-space:nowrap}}
.nav a:hover{{color:var(--primary);background:var(--primary-light)}}
.lang-switch{{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;font-size:13px;font-weight:600;color:var(--primary);border:1.5px solid var(--primary-light);border-radius:var(--radius-pill);background:#fff}}
@media(max-width:768px){{.nav{{display:none}}}}
.hero{{background:linear-gradient(135deg,#0066CC,#004C99);color:#fff;padding:110px 24px 56px}}
.hero h1{{font-size:clamp(1.5rem,2.6vw,2.1rem);font-weight:700;margin-bottom:10px}}
.hero .subtitle{{font-size:15px;opacity:.92}}
.section{{padding:48px 0}}
.section-title{{text-align:center;margin-bottom:24px}}
.section-title h2{{font-size:1.5rem;font-weight:700}}
.footer{{background:#1A1A2E;color:#fff;padding:40px 24px;text-align:center}}
.footer a{{color:#999}}
  </style>
</head>
<body>
  <header class="header"><div class="container">
    <a href="/zh-cn/" class="logo">速豹回国物流<span style="font-size:11px;color:var(--text-secondary);margin-left:8px">美国寄中国</span></a>
    <nav class="nav">
      <a href="/zh-cn/">首页</a><a href="/zh-cn/usa-to-china/">美国寄中国</a>
      <a href="/zh-cn/tools/">工具</a><a href="/zh-cn/blog/">攻略</a>
      <a href="{en_url}" class="lang-switch" hreflang="en">🌐 中文 / English</a>
    </nav>
  </div></header>
  {body}
  <footer class="footer"><div class="container">© 2026 速豹回国物流 | <a href="/zh-cn/">首页</a> · <a href="/sitemap.xml">Sitemap</a></div></footer>
</body>
</html>"""
        (ROOT / "zh-cn" / rel).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / "zh-cn" / rel).write_text(page, encoding="utf-8")
        return rel

    else:
        rel = f"usa-to-china/{cslug}/{islug}/index.html"
        zh_url = f"{DOMAIN}/zh-cn/usa-to-china/{cslug}/{islug}/"
        en_url = f"{DOMAIN}/en/usa-to-china/{cslug}/{islug}/"
        title = f"Ship {ien} from {city_en} to China | Subao Global"
        desc = (f"Ship {ien.lower()} from {city_en} to China: {item['verdict_en']}, duty {item['rate']}. "
                f"Free pickup in {city_en}, tax-inclusive door-to-door in 7-10 working days. {item['note_en']}")
        h1 = f"Ship {ien} from {city_en} to China"
        faq = [
            (f"Can I ship {ien.lower()} from {city_en} to China?",
             f"{item['verdict_en']}. {item['note_en']}. Duty applies above the RMB 1,000 personal allowance; our tax-inclusive line covers base duty."),
            (f"How long does shipping from {city_en} take?",
             f"Air freight 7-10 working days door-to-door. Free pickup across {city_en}."),
            (f"How much does it cost?",
             f"Air line from $11/kg (21kg+, US tier), $10.4/kg (100kg+). Volumetric weight = L×W×H (cm) ÷ 5000, charged on the larger."),
            (f"How do I book pickup in {city_en}?",
             f"Free doorstep pickup across {city_en} — book a window and we collect."),
        ]
        faq_schema = json.dumps({"@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
        body = f"""
  <section class="hero"><div class="container">
    <h1>{h1}</h1>
    <p class="subtitle">Free pickup in {city_en} · Tax-inclusive door-to-door · 7-10 working days</p>
  </div></section>
  <section class="section"><div class="container" style="max-width:800px">
    <div style="background:#fff;border:1px solid var(--border);border-radius:16px;padding:32px;margin-bottom:32px">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px;text-align:center">
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">$11/kg</div><div style="font-size:12px;color:var(--text-secondary)">Air 21kg+ (US tier)</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">$10.4/kg</div><div style="font-size:12px;color:var(--text-secondary)">100kg+</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">7-10</div><div style="font-size:12px;color:var(--text-secondary)">Working days</div></div>
        <div><div style="font-size:1.5rem;font-weight:800;color:var(--primary)">Tax-incl.</div><div style="font-size:12px;color:var(--text-secondary)">All-in price</div></div>
      </div>
    </div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">Verdict: {item['verdict_en']}</h2><p style="color:var(--text-secondary);line-height:1.9">{item['note_en']}. Duty rate {item['rate']} on value above the RMB 1,000 allowance.</p></div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">Shipping from {city_en}</h2><p style="color:var(--text-secondary);line-height:1.9">Free doorstep pickup across {city_en}. Air freight with direct or connecting flights to China; first-tier cities clear fastest.</p></div>
    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">Packing tips</h2><p style="color:var(--text-secondary);line-height:1.9">Keep original packaging, use cushioning, and declare the item accurately to avoid customs delays. Fragile items need reinforcement.</p></div>
    <div style="background:var(--primary-light);border:1px solid #CDE3F5;border-radius:12px;padding:20px 24px;margin:32px 0">
      <div style="font-size:14px;font-weight:700;color:var(--primary-dark);margin-bottom:6px">📦 Related service</div>
      <a href="/en/usa-to-china/{cslug}/" style="font-size:15px;font-weight:700;color:var(--primary);text-decoration:underline">Ship from {city_en} to China →</a> ·
      <a href="/en/blog/can-i-ship-{islug}-to-china.html" style="font-size:15px;font-weight:700;color:var(--primary);text-decoration:underline">{ien} to China guide →</a>
    </div>
    <div class="section-title" style="margin-top:40px"><h2>Frequently asked questions</h2></div>
    {''.join(f'<div style="margin:16px 0"><p style="font-weight:700;margin:0 0 4px">Q: {q}</p><p style="margin:0;color:var(--text-secondary)">{a}</p></div>' for q, a in faq)}
    <div style="background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;padding:28px;border-radius:16px;text-align:center;margin:32px 0">
      <h3 style="font-size:1.1rem;margin-bottom:4px">Get a quote for {ien} from {city_en}</h3>
      <p style="opacity:.85;margin-bottom:12px">30-minute proposal, free on-site estimate</p>
      <a href="https://d.salesmartly.com/fuxikn" target="_blank" rel="noopener" style="display:inline-block;background:#E65100;color:#fff;padding:12px 28px;border-radius:24px;font-weight:600">💬 Free consultation</a>
    </div>
  </div></section>"""
        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="applicable-device" content="pc,mobile">
  <title>{title}</title><meta name="description" content="{desc}">
  <link rel="alternate" hreflang="zh-CN" href="{zh_url}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="x-default" href="{zh_url}">
  <link rel="canonical" href="{en_url}">
  <meta property="og:title" content="{h1}">
  <meta property="og:description" content="{desc[:100]}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{DOMAIN}/assets/images/og-image.jpg">
  <meta property="og:locale" content="en_US">
  <meta name="lastmod" content="2026-08-20">
  <script type="application/ld+json">{faq_schema}</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
  <style>
:root{{--primary:#0066CC;--primary-dark:#004C99;--primary-light:#E6F0FA;--green:#00B900;--bg:#F5F7FA;--text:#1A1A2E;--text-secondary:#64748B;--border:#E2E8F0;--radius-lg:16px;--radius-pill:24px;--nav-height:68px}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;color:var(--text);line-height:1.7;font-size:16px;background:var(--bg)}}
a{{text-decoration:none;color:inherit}}
.container{{max-width:1100px;margin:0 auto;padding:0 24px}}
.header{{position:fixed;top:0;left:0;right:0;height:var(--nav-height);background:rgba(255,255,255,.96);backdrop-filter:blur(12px);z-index:1000;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
.header .container{{display:flex;align-items:center;justify-content:space-between;height:100%}}
.logo{{font-size:20px;font-weight:700;color:var(--primary)}}
.nav{{display:flex;align-items:center;gap:2px}}
.nav a{{padding:7px 13px;font-size:13px;font-weight:500;color:var(--text-secondary);border-radius:var(--radius-pill);white-space:nowrap}}
.nav a:hover{{color:var(--primary);background:var(--primary-light)}}
.lang-switch{{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;font-size:13px;font-weight:600;color:var(--primary);border:1.5px solid var(--primary-light);border-radius:var(--radius-pill);background:#fff}}
@media(max-width:768px){{.nav{{display:none}}}}
.hero{{background:linear-gradient(135deg,#0066CC,#004C99);color:#fff;padding:110px 24px 56px}}
.hero h1{{font-size:clamp(1.5rem,2.6vw,2.1rem);font-weight:700;margin-bottom:10px}}
.hero .subtitle{{font-size:15px;opacity:.92}}
.section{{padding:48px 0}}
.section-title{{text-align:center;margin-bottom:24px}}
.section-title h2{{font-size:1.5rem;font-weight:700}}
.footer{{background:#1A1A2E;color:#fff;padding:40px 24px;text-align:center}}
.footer a{{color:#999}}
  </style>
</head>
<body>
  <header class="header"><div class="container">
    <a href="/en/" class="logo">Subao Global<span style="font-size:11px;color:var(--text-secondary);margin-left:8px">Ship to China</span></a>
    <nav class="nav">
      <a href="/en/">Home</a><a href="/en/usa-to-china/">USA to China</a>
      <a href="/en/tools/">Tools</a><a href="/en/blog/">Guides</a>
      <a href="{zh_url}" class="lang-switch" hreflang="zh-CN">🌐 English / 中文</a>
    </nav>
  </div></header>
  {body}
  <footer class="footer"><div class="container">© 2026 Subao Global Logistics | <a href="/en/">Home</a> · <a href="/sitemap.xml">Sitemap</a></div></footer>
</body>
</html>"""
        (ROOT / "en" / rel).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / "en" / rel).write_text(page, encoding="utf-8")
        return rel

count = 0
for city in CITIES:
    for item in ITEMS:
        gen_page("zh-cn", city, item)
        gen_page("en", city, item)
        count += 2
print(f"✅ 品类×城市组合页生成：{len(CITIES)} 城市 × {len(ITEMS)} 品类 × 2 语言 = {count} 页")
