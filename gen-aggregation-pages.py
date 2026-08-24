#!/usr/bin/env python3
"""生成 2 类流量聚合页（中英双语）：
1) can-i-ship 分类 hub: /zh-cn/can-i-ship-index/ + /en/can-i-ship-index/ — 25 品类分组互链
2) 线路总览 hub: /zh-cn/routes/ + /en/routes/ — 9 条线路互链
模板复用站点风格(can-i-ship 工具页样式)。
"""
from pathlib import Path

BASE = Path(".")
SITE = "https://subaog.com"
ITEMS = {
    "supplements":("保健品","Supplements"),"baby-formula":("奶粉","Baby Formula"),"coffee":("咖啡","Coffee"),
    "tea":("茶叶","Tea"),"snacks":("零食","Snacks"),"wine":("红酒","Wine"),"pet-food":("宠物食品","Pet Food"),
    "medicine":("中药材","Medicine"),"cosmetics":("化妆品","Cosmetics"),"perfume":("香水","Perfume"),
    "luxury-bags":("奢侈品包","Luxury Bags"),"electronics":("电子产品","Electronics"),
    "medical-devices":("医疗器械","Medical Devices"),"tools":("工具","Tools"),"auto-parts":("汽车零件","Auto Parts"),
    "furniture":("家具","Furniture"),"kitchenware":("厨具","Kitchenware"),"curtains":("窗帘","Curtains"),
    "toys":("玩具","Toys"),"figurines":("摆件手办","Figurines"),"books":("书籍","Books"),"shoes":("鞋子","Shoes"),
    "musical-instruments":("乐器","Musical Instruments"),"bicycles":("自行车","Bicycles"),"pet-supplies":("宠物用品","Pet Supplies"),
}
CANI_GROUPS = {
    "食品与保健":["supplements","baby-formula","coffee","tea","snacks","wine","pet-food","medicine"],
    "美妆与奢侈品":["cosmetics","perfume","luxury-bags"],
    "电子与器材":["electronics","medical-devices","tools","auto-parts"],
    "家居与生活":["furniture","kitchenware","curtains","toys","figurines","books","shoes"],
    "爱好与出行":["musical-instruments","bicycles","pet-supplies"],
}
ROUTES = {
    "usa-to-china":("美国寄中国","USA to China"),"japan-to-china":("日本寄中国","Japan to China"),
    "korea-to-china":("韩国寄中国","Korea to China"),"europe-to-china":("欧洲寄中国","Europe to China"),
    "canada-to-china":("加拿大寄中国","Canada to China"),"australia-to-china":("澳洲寄中国","Australia to China"),
    "seasia-to-china":("东南亚寄中国","Southeast Asia to China"),
    "student-luggage":("留学生行李","Student Luggage"),"usa-moving-to-china":("美国搬家回中国","US Moving to China"),
}

def css():
    return """<style>:root{--primary:#0066CC;--primary-dark:#004C99;--primary-light:#E6F0FA;--accent:#E65100;--green:#00B900;--bg:#F5F7FA;--bg-white:#FFF;--text:#1A1A2E;--text-secondary:#64748B;--border:#E2E8F0;--radius:10px;--radius-lg:16px;--radius-pill:24px;--nav-height:68px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:var(--text);line-height:1.7;font-size:16px;background:var(--bg);overflow-x:hidden}
a{text-decoration:none;color:inherit}
.container{max-width:1100px;margin:0 auto;padding:0 24px}
.header{position:fixed;top:0;left:0;right:0;height:var(--nav-height);background:rgba(255,255,255,.96);backdrop-filter:blur(12px);z-index:1000;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.header .container{display:flex;align-items:center;justify-content:space-between;height:100%}
.logo{font-size:20px;font-weight:700;color:var(--primary)}
.logo span{font-size:11px;color:var(--text-secondary);font-weight:400;border-left:2px solid var(--border);padding-left:8px;margin-left:8px}
.nav{display:flex;align-items:center;gap:2px}
.nav a{padding:7px 13px;font-size:13px;font-weight:500;color:var(--text-secondary);border-radius:var(--radius-pill);white-space:nowrap}
.nav a:hover,.nav a.active{color:var(--primary);background:var(--primary-light)}
.nav .btn-line{background:var(--green);color:#fff;padding:7px 16px;font-weight:600}
.route-hero{background:linear-gradient(135deg,#0066CC,#004C99);color:#fff;padding:110px 24px 64px}
.route-hero h1{font-size:clamp(1.5rem,2.6vw,2.2rem);font-weight:700;margin-bottom:14px;line-height:1.35}
.route-hero .subtitle{font-size:16px;opacity:.92;max-width:680px;line-height:1.7;margin-bottom:24px}
.section{padding:52px 0}
.section-title{text-align:center;margin-bottom:32px}
.section-title h2{font-size:1.6rem;font-weight:700;margin-bottom:6px}
.section-title p{color:var(--text-secondary);font-size:15px}
.group{background:#fff;border:1px solid var(--border);border-radius:var(--radius-lg);padding:28px;margin-bottom:20px}
.group h3{font-size:1.2rem;font-weight:700;color:var(--primary-dark);margin-bottom:16px}
.pill-row{line-height:2.6}
.pill{display:inline-block;margin:5px 6px;padding:7px 15px;background:var(--primary-light);border-radius:20px;font-size:14px;color:var(--primary);font-weight:600;transition:.2s}
.pill:hover{background:var(--primary);color:#fff}
.cta-section{background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;padding:52px 24px;text-align:center;border-radius:var(--radius-lg);margin:0 24px 52px}
.cta-section h2{font-size:1.4rem;margin-bottom:10px}
.cta-section p{opacity:.9;margin-bottom:20px}
.footer{background:#1A1A2E;color:#fff;padding:48px 24px 24px}
.footer-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:28px;max-width:1100px;margin:0 auto}
.footer h4{font-size:13px;font-weight:600;margin-bottom:12px;color:#ccc}
.footer a,.footer p{display:block;color:#999;font-size:13px;margin-bottom:8px}
.footer a:hover{color:#fff}
.footer-bottom{text-align:center;padding-top:28px;margin-top:28px;border-top:1px solid rgba(255,255,255,.1);font-size:12px;color:#666}</style>"""

def head(lang, slug, title, desc, canon_path):
    return f"""<!DOCTYPE html>
<html lang="{ 'zh-CN' if lang=='zh-cn' else 'en' }">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><meta name="applicable-device" content="pc,mobile">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="alternate" hreflang="zh-CN" href="{SITE}/zh-cn/{slug}/">
<link rel="alternate" hreflang="en" href="{SITE}/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="{SITE}/zh-cn/{slug}/">
<link rel="canonical" href="{SITE}/zh-cn/{slug}/">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/zh-cn/{slug}/"><meta property="og:type" content="website">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"{SITE}/zh-cn/"}},{{"@type":"ListItem","position":2,"name":"{ '能不能寄' if slug=='can-i-ship-index' else '回国线路' }","item":"{SITE}/zh-cn/{slug}/"}}]}}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DJGPMS9MOB"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-DJGPMS9MOB');</script>
{css()}
</head>"""

def header_nav(lang, active):
    return f'''<body>
<header class="header"><div class="container">
<a href="/zh-cn/" class="logo">速豹回国物流<span>美国→中国专线</span></a>
<nav class="nav">
<a href="/{lang}/">首页</a><a href="/{lang}/usa-to-china/" class="{'active' if active=='usa' else ''}">美国寄中国</a>
<a href="/{lang}/student-luggage/">留学生行李</a><a href="/{lang}/pricing.html">运费报价</a>
<a href="/{lang}/tools/">免费工具</a><a href="/{lang}/blog/">攻略</a><a href="/{lang}/contact.html">联系我们</a>
<a href="https://d.salesmartly.com/fuxikn" class="btn-line" target="_blank" rel="noopener">💬 免费咨询</a>
</nav></div></header>'''

def footer(lang):
    return f'''<footer class="footer"><div class="footer-grid">
<div><h4>回国线路</h4><a href="/{lang}/usa-to-china/">美国→中国</a><a href="/{lang}/japan-to-china/">日本→中国</a><a href="/{lang}/korea-to-china/">韩国→中国</a><a href="/{lang}/routes/">全部线路 →</a></div>
<div><h4>寄件指南</h4><a href="/{lang}/pricing.html">运费报价</a><a href="/{lang}/tools/">免费工具</a><a href="/{lang}/can-i-ship-index/">能不能寄</a><a href="/{lang}/blog/">攻略中心</a></div>
<div><h4>关于我们</h4><a href="/{lang}/about.html">公司介绍</a><a href="/{lang}/contact.html">联系我们</a></div>
<div><h4>联系方式</h4><p>客服：<a href="https://d.salesmartly.com/fuxikn" target="_blank" rel="noopener">在线咨询</a></p><p>邮箱：<a href="mailto:info@subaog.com">info@subaog.com</a></p></div>
</div><div class="footer-bottom">© 2026 速豹回国物流 | <a href="/sitemap.xml" style="color:#999">Sitemap</a></div></footer></body></html>'''

def gen_can_i_ship(lang):
    slug="can-i-ship-index"
    title="能不能寄到中国？25 类物品寄送指南汇总 | 速豹回国物流" if lang=="zh-cn" else "Can I Ship to China? 25 Categories Guide Hub | Subao"
    desc="汇总保健品、化妆品、电子产品、家具等 25 类物品寄中国的清关要求与替代方案，点击查看详细攻略。" if lang=="zh-cn" else "Hub of 25 category guides: supplements, cosmetics, electronics, furniture shipping to China."
    body=""
    for gname, items in CANI_GROUPS.items():
        gn = gname if lang=="zh-cn" else gname  # group names zh only; for en use item english
        pills="".join(
            f'<a class="pill" href="/{lang}/blog/can-i-ship-{it}-to-china.html">{ITEMS[it][0] if lang=="zh-cn" else ITEMS[it][1]} →</a>'
            for it in items)
        gtitle = gname if lang=="zh-cn" else {
            "食品与保健":"Food & Health","美妆与奢侈品":"Beauty & Luxury","电子与器材":"Electronics & Gear",
            "家居与生活":"Home & Living","爱好与出行":"Hobby & Travel"}[gname]
        body+=f'<div class="group"><h3>{gtitle}</h3><div class="pill-row">{pills}</div></div>'
    html = head(lang,slug,title,desc,slug) + header_nav(lang,"") + f'''
<section class="route-hero"><div class="container">
<h1>{'能不能寄到中国？25 类物品全攻略' if lang=='zh-cn' else 'Can I Ship to China? 25 Categories'}</h1>
<p class="subtitle">{'从保健品、化妆品到家具、电子产品，按品类查看清关要求、禁运清单与替代方案。' if lang=='zh-cn' else 'From supplements to furniture — clearance rules, prohibited items and alternatives by category.'}</p>
</div></section>
<section class="section"><div class="container">
<div class="section-title"><h2>{'按品类查能不能寄' if lang=='zh-cn' else 'Browse by Category'}</h2><p>{'点击品类查看详细寄送攻略' if lang=='zh-cn' else 'Click a category for the full guide'}</p></div>
{body}
</div></section>
<div class="cta-section"><div class="container"><h2>{'不确定您的物品能不能寄？' if lang=='zh-cn' else 'Not sure if your item ships?'}</h2><p>{'免费咨询，30 分钟给方案' if lang=='zh-cn' else 'Free consultation, plan in 30 min'}</p><a href="/{lang}/contact.html" class="btn-line" style="background:#fff;color:var(--primary);padding:13px 26px;border-radius:24px;font-weight:700">📦 免费咨询</a></div></div>
''' + footer(lang)
    (BASE/lang/slug).mkdir(parents=True, exist_ok=True)
    (BASE/lang/slug/"index.html").write_text(html, encoding="utf-8")
    print(f"  ✅ {lang}/{slug}/")

def gen_routes(lang):
    slug="routes"
    title="回国物流线路总览 | 美国/日本/韩国/欧洲→中国 | 速豹回国物流" if lang=="zh-cn" else "All Shipping Routes to China | Subao Global"
    desc="覆盖美国、日本、韩国、欧洲、加拿大、澳洲、东南亚寄中国，及留学生行李、美国搬家回国专线。" if lang=="zh-cn" else "USA, Japan, Korea, Europe, Canada, Australia, SEA to China, plus student luggage & US moving."
    pills="".join(
        f'<a class="pill" href="/{lang}/{r}/">{ROUTES[r][0] if lang=="zh-cn" else ROUTES[r][1]} →</a>'
        for r in ROUTES)
    html = head(lang,slug,title,desc,slug) + header_nav(lang,"") + f'''
<section class="route-hero"><div class="container">
<h1>{'回国物流线路总览' if lang=='zh-cn' else 'All Shipping Routes to China'}</h1>
<p class="subtitle">{'选您的出发地线路，查看专属运费、时效与清关方案。' if lang=='zh-cn' else 'Pick your origin route for rates, transit & clearance.'}</p>
</div></section>
<section class="section"><div class="container">
<div class="section-title"><h2>{'全部回国线路' if lang=='zh-cn' else 'All Routes'}</h2><p>{'双清包税门到门 · 全美免费取件' if lang=='zh-cn' else 'DDP door-to-door · free pickup'}</p></div>
<div class="group"><h3>{'按出发地选择' if lang=='zh-cn' else 'By Origin'}</h3><div class="pill-row">{pills}</div></div>
</div></section>
<div class="cta-section"><div class="container"><h2>{'需要定制线路方案？' if lang=='zh-cn' else 'Need a custom route?'}</h2><p>{'告诉我们出发地与物品，免费报价' if lang=='zh-cn' else 'Tell us origin & items for a free quote'}</p><a href="/{lang}/contact.html" class="btn-line" style="background:#fff;color:var(--primary);padding:13px 26px;border-radius:24px;font-weight:700">📦 免费咨询</a></div></div>
''' + footer(lang)
    (BASE/lang/slug).mkdir(parents=True, exist_ok=True)
    (BASE/lang/slug/"index.html").write_text(html, encoding="utf-8")
    print(f"  ✅ {lang}/{slug}/")

for lang in ("zh-cn","en"):
    gen_can_i_ship(lang)
    gen_routes(lang)
print("\n聚合页生成完成（4 文件）")
