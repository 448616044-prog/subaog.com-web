#!/usr/bin/env python3
"""subaog.com 城市交叉页程序化生成 — 美国TOP10城市 × 中国TOP10城市"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f'{BASE}/city', exist_ok=True)

# 美国出发城市 + 中国到达城市
us_cities = [
    ('new-york', '纽约'), ('los-angeles', '洛杉矶'), ('san-francisco', '旧金山'),
    ('chicago', '芝加哥'), ('houston', '休斯顿'), ('seattle', '西雅图'),
    ('boston', '波士顿'), ('washington-dc', '华盛顿'), ('miami', '迈阿密'), ('dallas', '达拉斯')
]
cn_cities = [
    ('beijing', '北京'), ('shanghai', '上海'), ('guangzhou', '广州'),
    ('shenzhen', '深圳'), ('chengdu', '成都'), ('hangzhou', '杭州'),
    ('nanjing', '南京'), ('wuhan', '武汉'), ('xiamen', '厦门'), ('tianjin', '天津')
]

css = '''<style>
:root{--primary:#0066CC;--primary-dark:#004C99;--primary-light:#E6F0FA;--accent:#E65100;--bg:#F5F7FA;--bg-white:#FFFFFF;--text:#1A1A2E;--text-secondary:#64748B;--border:#E2E8F0;--radius:10px;--nav-height:68px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:var(--text);line-height:1.8;font-size:16px;background:var(--bg)}
a{text-decoration:none;color:inherit}
.header{position:fixed;top:0;left:0;right:0;height:var(--nav-height);background:rgba(255,255,255,0.96);backdrop-filter:blur(12px);z-index:1000;box-shadow:0 1px 3px rgba(0,0,0,0.05)}
.header .container{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:100%}
.logo{font-size:20px;font-weight:700;color:var(--primary)}
.nav{display:flex;gap:4px}
.nav a{padding:7px 14px;font-size:13px;font-weight:500;color:var(--text-secondary);border-radius:24px}
.nav a:hover{color:var(--primary);background:var(--primary-light)}
.city-hero{background:linear-gradient(135deg,#0066CC,#004C99);color:#fff;padding:100px 24px 48px;text-align:center}
.city-hero h1{font-size:clamp(1.3rem,2.3vw,1.8rem);margin-bottom:8px}
.city-hero .subtitle{opacity:.9}
.content{max-width:860px;margin:32px auto;padding:0 24px}
.info-box{padding:14px 18px;border-radius:var(--radius);margin:14px 0;font-size:14px}
.info-box.primary{background:var(--primary-light);border-left:4px solid var(--primary)}
table{width:100%;border-collapse:collapse;font-size:14px;background:var(--bg-white);border-radius:var(--radius);overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.06);margin:14px 0}
th{background:var(--primary);color:#fff;padding:10px 14px;text-align:left;font-weight:600}
td{padding:10px 14px;border-bottom:1px solid var(--border)}
tr:nth-child(even){background:var(--bg)}
h2{font-size:1.3rem;color:var(--primary);margin:36px 0 14px;padding-bottom:8px;border-bottom:2px solid var(--primary-light)}
.cta-bar{text-align:center;padding:28px 24px;margin:32px 0;background:var(--primary-light);border-radius:var(--radius-lg)}
.btn-primary{display:inline-flex;align-items:center;gap:6px;background:var(--accent);color:#fff;padding:12px 28px;border-radius:24px;font-weight:600;font-size:15px}
.links-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin:14px 0}
.link-card{display:block;padding:14px 18px;background:var(--bg-white);border:1px solid var(--border);border-radius:var(--radius)}
.link-card h4{font-size:14px;font-weight:600;color:var(--primary)}
.link-card p{font-size:12px;color:var(--text-secondary);margin:2px 0 0}
.footer{background:#1A1A2E;color:#fff;padding:48px 24px 24px;margin-top:64px}
.footer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:32px;max-width:1200px;margin:0 auto}
.footer h4{font-size:13px;color:#ccc;margin-bottom:12px}
.footer a,.footer p{display:block;color:#999;font-size:12px;margin-bottom:6px}
.footer a:hover{color:#fff}
.footer-bottom{text-align:center;padding-top:24px;margin-top:24px;border-top:1px solid rgba(255,255,255,0.1);font-size:11px;color:#666}
@media(max-width:768px){.nav{display:none}}
</style>'''

count = 0
for us_slug, us_name in us_cities:
    for cn_slug, cn_name in cn_cities:
        slug = f'{us_slug}-to-{cn_slug}'
        h1 = f'{us_name}寄{cn_name} | 美国{us_name}到中国{cn_name}物流专线'
        title = f'{h1} | 速豹国际物流'
        desc = f'从美国{us_name}寄快递到中国{cn_name}。空运7-10天、海运25-35天门到门。{us_name}上门取件，{cn_name}派送到家。免费估价。'
        
        # Generate related city links
        related = ''
        for u2, _ in us_cities[:6]:
            if u2 != us_slug:
                related += f'<a href="/city/{u2}-to-{cn_slug}" class="link-card"><h4>{us_name.replace(us_slug,u2)}寄{cn_name}</h4><p>{cn_name}物流专线</p></a>'
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="applicable-device" content="pc,mobile">
  <title>{title}</title><meta name="description" content="{desc}">
  <link rel="canonical" href="https://subaog.com/city/{slug}">
  <meta property="og:title" content="{h1}"><meta property="og:description" content="{desc}">
  <meta property="og:type" content="website"><meta name="lastmod" content="2026-08-07">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://subaog.com/"}},{{"@type":"ListItem","position":2,"name":"城市专线","item":"https://subaog.com/city/"}},{{"@type":"ListItem","position":3,"name":"{us_name}→{cn_name}","item":"https://subaog.com/city/{slug}"}}]}}</script>
  {css}
</head>
<body>
  <header class="header"><div class="container"><a href="/" class="logo">速豹国际<span style="font-size:11px;color:var(--text-secondary);font-weight:400;margin-left:8px">美国寄中国</span></a><nav class="nav"><a href="/">首页</a><a href="/usa-to-china/">美国寄中国</a><a href="/pricing.html">运费报价</a><a href="/tools/">工具</a></nav></div></header>
  <section class="city-hero"><div class="container"><h1>美国{us_name}寄中国{cn_name}</h1><p class="subtitle">空运7-10天 · 海运25-35天 · 门到门专线</p></div></section>
  <div class="content">
    <div class="info-box primary">📍 速豹国际提供美国{us_name}到中国{cn_name}的物流专线服务：{us_name}上门取件 → 中国{cn_name}派送到家。留学生行李、代购包裹、搬家货运均可。</div>
    <h2>运输方式与价格</h2>
    <table><tr><th>运输方式</th><th>价格/lb</th><th>时效</th><th>适合物品</th></tr><tr><td>空运专线</td><td>$5-8</td><td>7-10天</td><td>中小包裹、行李、代购</td></tr><tr><td>海运专线</td><td>$2-4</td><td>25-35天</td><td>搬家、大件家具、批量货运</td></tr><tr><td>国际快递</td><td>$10-25</td><td>3-5天</td><td>急件、文件、高价值物品</td></tr></table>
    <h2>{us_name}取件范围</h2><p>{us_name}市区及周边地区均支持上门取件。也可自行送到我们在{us_name}的合作仓库。</p>
    <h2>{cn_name}配送范围</h2><p>{cn_name}全境派送到家，包括市区及周边区县。一线城市配送时效更快。</p>
    <div class="cta-bar"><h3>{us_name}寄{cn_name}，立即获取报价</h3><p style="color:var(--text-secondary);margin-bottom:12px">30分钟出方案，免费上门估价</p><a href="https://wa.me/1XXXXXXXXXX" class="btn-primary" target="_blank">💬 WhatsApp 免费咨询</a></div>
    <h2>其他城市寄{cn_name}</h2><div class="links-grid">{related}</div>
    <h2>更多攻略</h2><div class="links-grid"><a href="/usa-to-china/" class="link-card"><h4>美国寄中国全攻略</h4><p>空运/海运/快递对比</p></a><a href="/tools/shipping-calculator" class="link-card"><h4>运费计算器</h4><p>免费估算运费</p></a></div>
  </div>
  <footer class="footer"><div class="footer-grid"><div><h4>速豹国际物流</h4><p>美国寄中国专线</p></div><div><h4>核心服务</h4><a href="/usa-to-china/">美国寄中国</a><a href="/blog/student-luggage-shipping-guide">留学生行李</a></div><div><h4>工具</h4><a href="/tools/shipping-calculator">运费计算器</a><a href="/tools/can-i-ship">能不能寄</a></div><div><h4>联系</h4><p>WhatsApp: +1-XXX-XXX-XXXX</p></div></div><div class="footer-bottom"><p>&copy; 2026 速豹国际物流</p></div></footer>
</body></html>'''
        
        path = f'{BASE}/city/{slug}.html'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1

print(f'✅ 城市交叉页生成完成：{count} 页 ({len(us_cities)}美国城市 × {len(cn_cities)}中国城市)')
print(f'   输出目录：{BASE}/city/')
