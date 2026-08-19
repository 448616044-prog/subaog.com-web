# -*- coding: utf-8 -*-
"""
subaog.com 英文站批量生成引擎
生成：9 国线路 Pillar + 城市页（Stage 3）、工具页（Stage 4）、city 交叉页（Stage 6）。
复用 en-data.py 数据层，统一 clean URL + hreflang + canonical + lang-switch + Schema。
幂等：重复运行会覆盖重写，安全。
"""
import json
from pathlib import Path
import en_data as D

DOMAIN = "https://subaog.com"
EN = Path("en")
ZH = Path("zh-cn")
GA_ID = "G-DJGPMS9MOB"

# ---------------- URL helpers（与 inject-multilang.py 一致：clean URL） ----------------
def clean(rel: str) -> str:
    if rel == "index.html":
        return ""
    if rel.endswith("/index.html"):
        return rel[: -len("index.html")]
    return rel


def en_url(rel: str) -> str:
    return f"{DOMAIN}/en/{clean(rel)}"


def zh_url(rel: str) -> str:
    return f"{DOMAIN}/zh-cn/{clean(rel)}"


# ---------------- 共享 CSS ----------------
CSS = """
:root{--primary:#0066CC;--primary-dark:#004C99;--primary-light:#E6F0FA;--green:#25D366;--bg:#F5F7FA;--text:#1A1A2E;--text-secondary:#64748B;--border:#E2E8F0;--radius:10px;--radius-lg:16px;--radius-pill:24px;--nav-height:68px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;color:var(--text);line-height:1.6;font-size:16px;background:var(--bg);overflow-x:hidden}
a{text-decoration:none;color:inherit}
.container{max-width:1100px;margin:0 auto;padding:0 24px}
.header{position:fixed;top:0;left:0;right:0;height:var(--nav-height);background:rgba(255,255,255,.96);backdrop-filter:blur(12px);z-index:1000;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.header .container{display:flex;align-items:center;justify-content:space-between;height:100%}
.logo{font-size:20px;font-weight:700;color:var(--primary)}
.logo span{font-size:11px;color:var(--text-secondary);font-weight:400;border-left:2px solid var(--border);padding-left:8px;margin-left:8px}
.nav{display:flex;align-items:center;gap:2px}
.nav a{padding:7px 13px;font-size:13px;font-weight:500;color:var(--text-secondary);border-radius:var(--radius-pill);transition:all .2s;white-space:nowrap}
.nav a:hover,.nav a.active{color:var(--primary);background:var(--primary-light)}
.nav .btn-wa{background:var(--green);color:#fff;padding:7px 16px;font-weight:600}
.burger{display:none;background:none;border:none;font-size:24px;cursor:pointer;color:var(--text)}
.lang-switch{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;font-size:13px;font-weight:600;color:var(--primary);border:1.5px solid var(--primary-light);border-radius:var(--radius-pill);background:#fff}
.lang-switch:hover{background:var(--primary);color:#fff;border-color:var(--primary)}
.lang-switch .sep{color:var(--border);margin:0 2px;font-weight:400}
.lang-switch .lang-en{color:var(--primary)}
.lang-switch:hover .lang-en,.lang-switch:hover .sep{color:#fff}
@media(max-width:768px){.nav{display:none;position:absolute;top:var(--nav-height);left:0;right:0;background:#fff;flex-direction:column;padding:16px 24px;box-shadow:0 8px 32px rgba(0,0,0,.1);gap:4px;max-height:calc(100vh - var(--nav-height));overflow-y:auto}.nav.open{display:flex}.burger{display:block}.nav a{width:100%;padding:10px 16px}.lang-switch{width:100%;justify-content:flex-start;padding:10px 16px;border-radius:var(--radius);border-color:var(--border)}}
.hero{background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;padding:120px 24px 72px}
.hero .container{max-width:1100px}
.hero h1{font-size:clamp(1.6rem,3vw,2.3rem);font-weight:800;letter-spacing:-.5px;line-height:1.25;margin-bottom:16px}
.hero .subtitle{font-size:16px;opacity:.92;max-width:680px;line-height:1.7;margin-bottom:28px}
.hero-cta{display:flex;gap:14px;flex-wrap:wrap}
.btn-primary{background:#fff;color:var(--primary);padding:13px 26px;border-radius:var(--radius-pill);font-weight:700;font-size:15px}
.btn-outline{border:1.5px solid rgba(255,255,255,.6);color:#fff;padding:12px 24px;border-radius:var(--radius-pill);font-weight:600;font-size:15px}
.section{padding:56px 0}
.section-title{text-align:center;margin-bottom:36px}
.section-title h2{font-size:1.7rem;font-weight:700;margin-bottom:8px}
.section-title p{color:var(--text-secondary);font-size:15px}
.info-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:40px}
.info-card{background:#fff;border-radius:var(--radius-lg);padding:26px;text-align:center;border:1px solid var(--border)}
.info-card .big{font-size:1.8rem;font-weight:800;color:var(--primary);margin-bottom:4px}
.info-card .label{font-size:13px;color:var(--text-secondary)}
.price-table{width:100%;border-collapse:collapse;margin:20px 0;font-size:14px;background:#fff;border-radius:var(--radius);overflow:hidden}
.price-table th{background:var(--primary);color:#fff;padding:12px 16px;text-align:left;font-weight:600}
.price-table td{padding:11px 16px;border-bottom:1px solid var(--border)}
.price-table tr:nth-child(even) td{background:#f8fafc}
.note{font-size:13px;color:var(--text-secondary);text-align:center;margin-top:6px}
.process{display:flex;justify-content:center;gap:22px;flex-wrap:wrap}
.step{text-align:center;width:210px}
.step-num{width:46px;height:46px;border-radius:50%;background:var(--primary);color:#fff;display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:700;margin:0 auto 12px}
.step h4{font-size:15px;font-weight:600;margin-bottom:4px}
.step p{font-size:13px;color:var(--text-secondary)}
.features{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:20px}
.feature{background:#fff;border-radius:var(--radius-lg);padding:26px;border:1px solid var(--border)}
.feature .icon{font-size:30px;margin-bottom:12px}
.feature h3{font-size:16px;font-weight:600;margin-bottom:6px}
.feature p{font-size:14px;color:var(--text-secondary)}
.can-ship{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}
.can-ship li{list-style:none;background:#fff;border:1px solid var(--border);border-radius:var(--radius);padding:12px 16px;font-size:14px;display:flex;gap:8px;align-items:center}
.can-ship .yes{color:#00B900;font-weight:700}
.can-ship .no{color:#E53935;font-weight:700}
.faq-list{max-width:760px;margin:0 auto}
.faq-item{border-bottom:1px solid var(--border)}
.faq-q{width:100%;padding:16px 0;text-align:left;background:none;border:none;font-size:15px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-family:inherit;color:var(--text)}
.faq-q:hover{color:var(--primary)}
.faq-a{padding:0 0 16px;font-size:14px;color:var(--text-secondary);line-height:1.7;display:none}
.faq-a.show{display:block}
.faq-icon{transition:transform .3s;font-size:12px;color:var(--text-secondary)}
.cta-section{background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;padding:56px 24px;text-align:center;border-radius:var(--radius-lg);margin:0 24px 56px}
.cta-section h2{font-size:1.5rem;margin-bottom:10px}
.cta-section p{opacity:.9;margin-bottom:22px}
.footer{background:#1A1A2E;color:#fff;padding:48px 24px 24px}
.footer-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:30px;max-width:1100px;margin:0 auto}
@media(max-width:768px){.footer-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:480px){.footer-grid{grid-template-columns:1fr}}
.footer h4{font-size:13px;font-weight:600;margin-bottom:14px;color:#ccc}
.footer a,.footer p{display:block;color:#999;font-size:13px;margin-bottom:8px}
.footer a:hover{color:#fff}
.footer-bottom{text-align:center;padding-top:30px;margin-top:30px;border-top:1px solid rgba(255,255,255,.1);font-size:12px;color:#666}
"""


# ---------------- 页头/页脚 ----------------
def nav_html(active: str, lang_zh: str) -> str:
    routes = [
        ("usa-to-china/", "USA"),
        ("japan-to-china/", "Japan"),
        ("korea-to-china/", "Korea"),
        ("europe-to-china/", "Europe"),
        ("canada-to-china/", "Canada"),
        ("australia-to-china/", "Australia"),
        ("seasia-to-china/", "SE Asia"),
    ]
    items = [f'<a href="/en/usa-to-china/"{" class=\"active\"" if active=="usa" else ""}>USA→China</a>']
    items.append(f'<a href="/en/student-luggage/"{" class=\"active\"" if active=="student" else ""}>Student Luggage</a>')
    items.append(f'<a href="/en/pricing.html"{" class=\"active\"" if active=="pricing" else ""}>Pricing</a>')
    items.append(f'<a href="/en/blog/"{" class=\"active\"" if active=="blog" else ""}>Blog</a>')
    items.append(f'<a href="/en/about.html"{" class=\"active\"" if active=="about" else ""}>About</a>')
    items.append(f'<a href="/en/contact.html"{" class=\"active\"" if active=="contact" else ""}>Contact</a>')
    nav = "\n        ".join(items)
    return f"""  <header class="header">
    <div class="container">
      <a href="/en/" class="logo">Subao Global<span>Shipping to China</span></a>
      <button class="burger" aria-label="Menu" onclick="document.querySelector('.nav').classList.toggle('open')">☰</button>
      <nav class="nav">
        {nav}
        <a href="{lang_zh}" class="lang-switch" hreflang="zh-CN"><span>中文</span><span class="sep">/</span><span class="lang-en">English</span></a>
        <a href="https://d.salesmartly.com/fuxikn" class="btn-wa" target="_blank" rel="noopener">💬 Live Chat</a>
      </nav>
    </div>
  </header>"""


def footer_html() -> str:
    return """  <footer class="footer">
    <div class="footer-grid">
      <div>
        <h4>Routes</h4>
        <a href="/en/usa-to-china/">USA → China</a>
        <a href="/en/japan-to-china/">Japan → China</a>
        <a href="/en/korea-to-china/">Korea → China</a>
        <a href="/en/europe-to-china/">Europe → China</a>
        <a href="/en/canada-to-china/">Canada → China</a>
        <a href="/en/australia-to-china/">Australia → China</a>
        <a href="/en/seasia-to-china/">Singapore/Malaysia → China</a>
      </div>
      <div>
        <h4>Guides</h4>
        <a href="/en/pricing.html">Pricing</a>
        <a href="/en/blog/prohibited-items-complete-guide.html">Prohibited items</a>
        <a href="/en/blog/international-customs-duty-guide.html">Customs & duty</a>
        <a href="/en/blog/how-to-pack-for-international-shipping.html">Packing guide</a>
        <a href="/en/faq.html">FAQ</a>
      </div>
      <div>
        <h4>Company</h4>
        <a href="/en/about.html">About us</a>
        <a href="/en/contact.html">Contact</a>
        <a href="/en/blog/">Blog</a>
      </div>
      <div>
        <h4>Contact</h4>
        <p>Live Chat: <a href="https://d.salesmartly.com/fuxikn" target="_blank" rel="noopener">Chat now</a></p>
        <p>Email: <a href="mailto:info@subaog.com">info@subaog.com</a></p>
        <p>Hours: Mon–Fri 09:00–21:00 GMT+8</p>
      </div>
    </div>
    <div class="footer-bottom">© 2026 Subao Global Logistics. All rights reserved.</div>
  </footer>"""


# ---------------- 页面骨架 ----------------
def render_page(rel_path: str, title: str, desc: str, body: str, schema_extra: str = "", active: str = ""):
    """rel_path 相对于 en/，如 'usa-to-china/index.html'"""
    eu = en_url(rel_path)
    zu = zh_url(rel_path)
    og = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Subao Global Logistics",
        "url": "https://subaog.com",
        "logo": "https://subaog.com/assets/images/logo.png",
    }
    bc = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://subaog.com/en/"}],
    }
    parts = [rel_path.rstrip("index.html").strip("/")]
    if parts and parts[0]:
        bc["itemListElement"].append({
            "@type": "ListItem", "position": 2, "name": parts[0].replace("-", " ").title(),
            "item": eu,
        })
    schema_blocks = [json.dumps(og), json.dumps(bc)]
    if schema_extra:
        # schema_extra 可能含多个 JSON（如 FAQPage + Person），拆成独立 script
        dec = json.JSONDecoder()
        idx = 0
        s = schema_extra
        while idx < len(s):
            while idx < len(s) and s[idx] in ' \n\r\t':
                idx += 1
            if idx >= len(s):
                break
            if s[idx] == '{':
                try:
                    o, idx = dec.raw_decode(s, idx)
                    schema_blocks.append(json.dumps(o, ensure_ascii=False))
                except Exception:
                    break
            else:
                break
    schema_html = "\n  ".join(f'<script type="application/ld+json">{b}</script>' for b in schema_blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="applicable-device" content="pc,mobile">
  <meta name="format-detection" content="telephone=no">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="alternate" hreflang="zh-CN" href="{zu}">
  <link rel="alternate" hreflang="en" href="{eu}">
  <link rel="alternate" hreflang="x-default" href="{zu}">
  <link rel="canonical" href="{eu}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{eu}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="lastmod" content="2026-08-17">
  {schema_html}
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
  <style>{CSS}</style>
</head>
<body>
{nav_html(active, zu)}
{body}
{footer_html()}
<script>
  document.querySelectorAll('.faq-q').forEach(function(q){{
    q.addEventListener('click', function(){{
      var a = q.nextElementSibling;
      a.classList.toggle('show');
      q.querySelector('.faq-icon').textContent = a.classList.contains('show') ? '▲' : '▼';
    }});
  }});
</script>
</body>
</html>"""


# ---------------- 组件 ----------------
def process_html() -> str:
    steps = D.COMMON_PROCESS
    inner = ""
    for i, (t, d) in enumerate(steps, 1):
        inner += f'<div class="step"><div class="step-num">{i}</div><h4>{t}</h4><p>{d}</p></div>'
    return f'<div class="process">{inner}</div>'


def can_ship_html() -> str:
    items = ""
    for name, ok in D.COMMON_CAN_SHIP:
        mark = '<span class="yes">✓</span>' if ok else '<span class="no">✗</span>'
        items += f'<li>{mark}{name}</li>'
    return f'<ul class="can-ship">{items}</ul>'


def faq_html(faq_list) -> str:
    items = ""
    for q, a in faq_list:
        items += (f'<div class="faq-item"><button class="faq-q">{q}<span class="faq-icon">▼</span></button>'
                  f'<div class="faq-a">{a}</div></div>')
    return f'<div class="faq-list">{items}</div>'


def faq_schema(faq_list) -> str:
    entities = []
    for q, a in faq_list:
        entities.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities})


def routes_html(exclude: str) -> str:
    """其他线路卡片"""
    cards = ""
    for slug, c in D.COUNTRIES.items():
        if slug == exclude:
            continue
        cards += (f'<div class="feature"><div class="icon">{c["flag"]}</div>'
                  f'<h3>{c["name_en"]}</h3><p>{c["price_air"]} · {c["transit"]}</p>'
                  f'<a href="/en/{slug}/" style="color:var(--primary);font-weight:600;font-size:14px">Learn more →</a></div>')
    return f'<section class="section"><div class="container"><div class="section-title"><h2>Other routes to China</h2></div><div class="features">{cards}</div></div></section>'


def cta_html() -> str:
    return ('<section class="cta-section"><div class="container"><h2>Get a free shipping quote</h2>'
            '<p>Tell us what you are shipping and where — we reply within 30 minutes during business hours.</p>'
            '<a href="/en/contact.html" class="btn-primary">Request a quote</a></div></section>')


# ---------------- 生成器：国家 Pillar ----------------
def gen_country_pillar(slug: str):
    c = D.COUNTRIES[slug]
    rel = f"{slug}/index.html"
    title = f"{c['name_en']} — Door-to-Door, Tax-Inclusive | Subao Global Logistics"
    desc = (f"Ship from {c['short']} to China with Subao Global. Door-to-door in {c['transit']}, "
            f"tax-inclusive customs, {c['price_air']}. Free pickup and full tracking. Get a free quote.")

    # 价格表（重量段 × 空运/海运）
    price_rows = ""
    tiers = [
        ("1–20 kg", "$12/kg", "—", "Air 10–15 days"),
        ("21–99 kg", "$10.5/kg", "$6.5/kg", "Air 10–15 / Sea 25–35 days"),
        ("100 kg+", "$10/kg", "$6/kg", "Air 10–15 / Sea 25–35 days"),
    ]
    for w, a, s, t in tiers:
        price_rows += f'<tr><td style="font-weight:600">{w}</td><td>{a}</td><td>{s}</td><td>{t}</td></tr>'

    # FAQ 合并通用
    faq = c["faq"] + D.COMMON_FAQ[:2]

    body = f"""  <section class="hero">
    <div class="container">
      <h1>{c['h1']}</h1>
      <p class="subtitle">{c['subtitle']}</p>
      <div class="hero-cta">
        <a href="/en/contact.html" class="btn-primary">📦 Get a {c['short']} → China quote</a>
        <a href="#pricing" class="btn-outline">View pricing ↓</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="info-grid">
        <div class="info-card"><div class="big">{c['price_air'].replace('from ','')}</div><div class="label">Air freight /kg (21kg+)</div></div>
        <div class="info-card"><div class="big">{c['transit'].split()[0]}</div><div class="label">Days door-to-door</div></div>
        <div class="info-card"><div class="big">Tax-incl.</div><div class="label">One all-in price</div></div>
        <div class="info-card"><div class="big">Door</div><div class="label">Free pickup + delivery</div></div>
      </div>

      <div class="section-title" id="pricing"><h2>{c['short']} → China shipping rates</h2><p>Air & sea freight, tax-inclusive, no hidden fees</p></div>
      <table class="price-table">
        <thead><tr><th>Weight</th><th>Air freight</th><th>Sea freight</th><th>Transit time</th></tr></thead>
        <tbody>{price_rows}</tbody>
      </table>
      <p class="note">* All-inclusive door-to-door price covering pickup + freight + China customs + final delivery. Actual price varies slightly by item type and volume.</p>

      <div class="section-title" style="margin-top:48px"><h2>How it works</h2></div>
      {process_html()}
    </div>
  </section>

  <section class="section" style="background:#fff">
    <div class="container">
      <div class="section-title"><h2>Why choose Subao Global</h2></div>
      <div class="features">
        {''.join(f'<div class="feature"><div class="icon">{f["icon"]}</div><h3>{f["title"]}</h3><p>{f["desc"]}</p></div>' for f in c["features"])}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-title"><h2>What can I ship?</h2></div>
      {can_ship_html()}
    </div>
  </section>

  <section class="section" style="background:#fff">
    <div class="container">
      <div class="section-title"><h2>Frequently asked questions</h2></div>
      {faq_html(faq)}
    </div>
  </section>

  {routes_html(slug)}
  {cta_html()}"""

    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body, faq_schema(faq), active=""), encoding="utf-8")


# ---------------- 生成器：城市页 ----------------
def gen_city_page(slug: str, city: dict):
    c = D.COUNTRIES[slug]
    city_slug = city["en"].lower().replace(" ", "-").replace(",", "")
    rel = f"{slug}/{city_slug}/index.html"
    title = f"Ship from {city['en']} to China — Door-to-Door | Subao Global"
    desc = (f"Ship from {city['en']}, {c['short']} to China with Subao Global. Door-to-door in {c['transit']}, "
            f"tax-inclusive, {c['price_air']}. Free pickup in {city['en']}. Get a free quote.")
    faq = c["faq"][:3]

    body = f"""  <section class="hero">
    <div class="container">
      <h1>Ship from {city['en']} to China</h1>
      <p class="subtitle">Door-to-door shipping from {city['en']} to any city in China in {c['transit']}. Tax-inclusive customs clearance, free pickup, and full tracking — {c['price_air']}.</p>
      <div class="hero-cta">
        <a href="/en/contact.html" class="btn-primary">📦 Get a quote</a>
        <a href="/en/{slug}/" class="btn-outline">All {c['short']} routes →</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="info-grid">
        <div class="info-card"><div class="big">{c['price_air'].replace('from ','')}</div><div class="label">Air freight /kg</div></div>
        <div class="info-card"><div class="big">{c['transit'].split()[0]}</div><div class="label">Days door-to-door</div></div>
        <div class="info-card"><div class="big">Free</div><div class="label">Pickup in {city['en']}</div></div>
        <div class="info-card"><div class="big">Tax-incl.</div><div class="label">One all-in price</div></div>
      </div>

      <div class="section-title"><h2>How it works</h2></div>
      {process_html()}

      <div class="section-title" style="margin-top:48px"><h2>Why ship with Subao Global from {city['en']}</h2></div>
      <div class="features">
        {''.join(f'<div class="feature"><div class="icon">{f["icon"]}</div><h3>{f["title"]}</h3><p>{f["desc"]}</p></div>' for f in c["features"])}
      </div>
    </div>
  </section>

  <section class="section" style="background:#fff">
    <div class="container">
      <div class="section-title"><h2>Frequently asked questions</h2></div>
      {faq_html(faq)}
    </div>
  </section>

  {routes_html(slug)}
  {cta_html()}"""

    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body, faq_schema(faq)), encoding="utf-8")


# ---------------- 生成器：city 交叉页（美国城市 → 中国城市） ----------------
def gen_us_city_pair(us: str, cn: str):
    us_slug = us.lower().replace(" ", "-").replace(",", "")
    cn_slug = cn.lower().replace(" ", "-").replace(",", "")
    rel = f"city/{us_slug}-to-{cn_slug}.html"
    title = f"Ship from {us} to {cn} — Door-to-Door | Subao Global"
    desc = (f"Ship from {us} to {cn}, China with Subao Global. Door-to-door in 10–15 working days, "
            f"tax-inclusive, from $10.5/kg. Free pickup in {us}. Get a free quote.")
    faq = [
        (f"How long does shipping from {us} to {cn} take?",
         f"Air freight from {us} to {cn} takes 10–15 working days door-to-door. Sea freight takes 25–35 days."),
        (f"How much does shipping from {us} to {cn} cost?",
         f"Air freight starts at about $10.5/kg for shipments over 21kg. Small parcels cost $15–30. Request a free quote for an exact price."),
        (f"Do you offer pickup in {us}?",
         f"Yes — free doorstep pickup is available throughout {us}. We collect your items at a time that suits you."),
        (f"Can I ship personal items from {us} to {cn}?",
         "Yes. Clothing, books, supplements, cosmetics, electronics and household goods are all supported. Prohibited items include weapons, drugs and fresh food."),
    ]

    body = f"""  <section class="hero">
    <div class="container">
      <h1>Ship from {us} to {cn}</h1>
      <p class="subtitle">Door-to-door shipping from {us} to {cn}, China in 10–15 working days. Tax-inclusive customs clearance, free pickup, and full tracking — from $10.5/kg.</p>
      <div class="hero-cta">
        <a href="/en/contact.html" class="btn-primary">📦 Get a {us} → {cn} quote</a>
        <a href="/en/usa-to-china/" class="btn-outline">All USA routes →</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="info-grid">
        <div class="info-card"><div class="big">$10.5</div><div class="label">Air freight /kg (21kg+)</div></div>
        <div class="info-card"><div class="big">10–15</div><div class="label">Days door-to-door</div></div>
        <div class="info-card"><div class="big">Free</div><div class="label">Pickup in {us}</div></div>
        <div class="info-card"><div class="big">Tax-incl.</div><div class="label">One all-in price</div></div>
      </div>

      <div class="section-title"><h2>How it works</h2></div>
      {process_html()}
    </div>
  </section>

  <section class="section" style="background:#fff">
    <div class="container">
      <div class="section-title"><h2>Why ship with Subao Global</h2></div>
      <div class="features">
        <div class="feature"><div class="icon">🛡️</div><h3>Tax-inclusive</h3><p>One price covers pickup, freight, China customs and delivery.</p></div>
        <div class="feature"><div class="icon">🚚</div><h3>Free pickup</h3><p>Free doorstep pickup across {us}.</p></div>
        <div class="feature"><div class="icon">📍</div><h3>Full tracking</h3><p>Track every leg from {us} to {cn}.</p></div>
        <div class="feature"><div class="icon">💰</div><h3>40–60% cheaper</h3><p>Save vs. USPS/UPS/FedEx published rates.</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-title"><h2>Frequently asked questions</h2></div>
      {faq_html(faq)}
    </div>
  </section>

  {cta_html()}"""

    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body, faq_schema(faq)), encoding="utf-8")


# ---------------- 主入口 ----------------
def main():
    total = 0
    # Stage 3: 国家 Pillar + 城市页
    for slug, c in D.COUNTRIES.items():
        gen_country_pillar(slug)
        total += 1
        for city in c["cities"]:
            gen_city_page(slug, city)
            total += 1

    # Stage 6: city 交叉页
    for us in D.US_CITIES:
        for cn in D.CN_CITIES:
            gen_us_city_pair(us, cn)
            total += 1

    print(f"✅ 已生成 {total} 个英文页面")


if __name__ == "__main__":
    main()
