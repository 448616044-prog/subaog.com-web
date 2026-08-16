#!/usr/bin/env python3
"""生成 subaog.com 东南亚 11 个页面"""
import os

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# ===== 公共 CSS =====
COMMON_CSS = """
    :root{--primary:#0066CC;--primary-dark:#004C99;--primary-light:#E6F0FA;--accent:#E65100;--green:#00B900;--bg:#F5F7FA;--bg-white:#FFFFFF;--text:#1A1A2E;--text-secondary:#64748B;--border:#E2E8F0;--radius:10px;--radius-lg:16px;--radius-pill:24px;--nav-height:68px}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:var(--text);line-height:1.8;font-size:16px;background:var(--bg);-webkit-font-smoothing:antialiased}
    a{text-decoration:none;color:inherit}
    .container{max-width:860px;margin:0 auto;padding:0 24px}
    .header{position:fixed;top:0;left:0;right:0;height:var(--nav-height);background:rgba(255,255,255,0.96);backdrop-filter:blur(12px);z-index:1000;box-shadow:0 1px 3px rgba(0,0,0,0.05)}
    .header .container{display:flex;align-items:center;justify-content:space-between;height:100%;max-width:1200px}
    .logo{font-size:20px;font-weight:700;color:var(--primary)}
    .nav{display:flex;gap:4px}
    .nav a{padding:7px 14px;font-size:13px;font-weight:500;color:var(--text-secondary);border-radius:24px;white-space:nowrap}
    .nav a:hover,.nav a.active{color:var(--primary);background:var(--primary-light)}
    .dropdown{position:relative}
    .dropdown-toggle{cursor:pointer;display:flex;align-items:center;gap:4px}
    .dropdown-toggle::after{content:'▾';font-size:10px}
    .dropdown-menu{display:none;position:absolute;top:100%;left:0;background:#fff;border-radius:var(--radius);box-shadow:0 8px 32px rgba(0,0,0,0.1);min-width:200px;padding:8px 0;z-index:1001;border:1px solid var(--border)}
    .dropdown:hover .dropdown-menu{display:block}
    .dropdown-menu a{display:block;padding:10px 20px;border-radius:0;font-size:13px}
    .dropdown-menu a:hover{background:var(--primary-light);color:var(--primary)}
    .dropdown-menu .coming-soon{color:#999;font-size:12px;padding:10px 20px}
    .dropdown-menu .sep{border-top:1px solid var(--border);margin:4px 0}
    .burger{display:none;background:none;border:none;font-size:24px;cursor:pointer;padding:4px 8px}
    @media(max-width:768px){
      .nav{display:none;position:absolute;top:var(--nav-height);left:0;right:0;background:#fff;flex-direction:column;padding:16px 24px;box-shadow:0 8px 32px rgba(0,0,0,0.1);gap:4px}
      .nav.open{display:flex}.burger{display:block}.nav a{width:100%;padding:10px 16px}
      .dropdown-menu{position:static;box-shadow:none;border:none;padding:0 0 0 16px;display:none}
      .dropdown.open .dropdown-menu{display:block}
    }
    .hero{background:linear-gradient(135deg,#0066CC,#004C99);color:#fff;padding:100px 24px 48px;text-align:center}
    .hero h1{font-size:clamp(1.4rem,2.5vw,2rem);margin-bottom:12px;line-height:1.3}
    .hero .subtitle{opacity:.9;max-width:600px;margin:0 auto;font-size:15px}
    .content-section{padding:48px 0}
    .content-section h2{font-size:1.4rem;margin:36px 0 16px;color:var(--text)}
    .content-section h3{font-size:1.15rem;margin:28px 0 12px;color:var(--primary);border-bottom:2px solid var(--primary-light);padding-bottom:6px}
    .content-section p{margin-bottom:14px;color:var(--text-secondary);line-height:1.9}
    .content-section ul,.content-section ol{margin:12px 0 20px 20px;color:var(--text-secondary)}
    .content-section li{margin-bottom:6px;line-height:1.8}
    .info-box{background:var(--primary-light);border-radius:var(--radius);padding:20px 24px;margin:24px 0}
    .info-box h4{color:var(--primary);margin-bottom:8px;font-size:15px}
    .info-box p,.info-box li{font-size:14px;margin-bottom:4px}
    .price-table{width:100%;border-collapse:collapse;margin:20px 0;background:var(--bg-white);border-radius:var(--radius);overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.06)}
    .price-table th{background:var(--primary);color:#fff;padding:12px 16px;text-align:left;font-size:14px}
    .price-table td{padding:10px 16px;border-bottom:1px solid var(--border);font-size:14px}
    .price-table tr:hover td{background:var(--primary-light)}
    .cta-box{background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;border-radius:var(--radius-lg);padding:32px;text-align:center;margin:32px 0}
    .cta-box h3{color:#fff;border:none;font-size:1.2rem;margin-top:0}
    .cta-box p{color:rgba(255,255,255,0.85);margin-bottom:20px}
    .btn-cta{display:inline-block;background:var(--accent);color:#fff;padding:14px 32px;border-radius:var(--radius-pill);font-weight:600;font-size:15px;transition:all .2s}
    .btn-cta:hover{background:#CC5200;transform:translateY(-1px)}
    .step-list{counter-reset:step;list-style:none;margin:20px 0;padding:0}
    .step-list li{counter-increment:step;display:flex;gap:16px;align-items:flex-start;margin-bottom:20px;padding:16px;background:var(--bg-white);border-radius:var(--radius);box-shadow:0 1px 3px rgba(0,0,0,0.04)}
    .step-list li::before{content:counter(step);background:var(--primary);color:#fff;min-width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;flex-shrink:0}
    .footer{background:#1A1A2E;color:#fff;padding:48px 24px 24px;margin-top:64px}
    .footer-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:32px;max-width:1200px;margin:0 auto}
    @media(max-width:768px){.footer-grid{grid-template-columns:repeat(2,1fr)}}
    @media(max-width:480px){.footer-grid{grid-template-columns:1fr}}
    .footer h4{font-size:14px;font-weight:600;margin-bottom:14px;color:#ccc}
    .footer a,.footer p{display:block;color:#999;font-size:13px;margin-bottom:8px;transition:color .2s}
    .footer a:hover{color:#fff}
    .footer .coming-soon{color:#555;font-size:12px}
    .footer-bottom{text-align:center;padding-top:32px;margin-top:32px;border-top:1px solid rgba(255,255,255,0.1);font-size:12px;color:#666}
    .footer-bottom a{color:#999;display:inline}
    .breadcrumb{font-size:13px;color:var(--text-secondary);margin-bottom:24px}
    .breadcrumb a{color:var(--primary)}
    .breadcrumb a:hover{text-decoration:underline}
    .related-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:24px 0}
    .related-link{background:var(--bg-white);border:1px solid var(--border);border-radius:var(--radius);padding:16px;transition:all .2s;display:block}
    .related-link:hover{border-color:var(--primary);box-shadow:0 4px 12px rgba(0,0,0,0.08)}
    .related-link strong{display:block;color:var(--text);margin-bottom:4px;font-size:14px}
    .related-link span{color:var(--text-secondary);font-size:12px}
"""

# ===== 公共 Header =====
HEADER = """  <header class="header">
    <div class="container">
      <a href="/" class="logo">速豹回国物流</a>
      <button class="burger" aria-label="菜单" onclick="document.querySelector('.nav').classList.toggle('open')">☰</button>
      <nav class="nav">
        <a href="/">首页</a>
        <div class="dropdown">
          <a href="#" class="dropdown-toggle" onclick="event.preventDefault();this.parentElement.classList.toggle('open')">回国线路</a>
          <div class="dropdown-menu">
            <a href="/usa-to-china/">🇺🇸 美国→中国</a>
            <a href="/seasia-to-china/">🌏 东南亚→中国</a>
            <a href="/seasia-to-china/singapore/">　新加坡→中国</a>
            <a href="/seasia-to-china/malaysia/">　马来西亚→中国</a>
            <span class="sep"></span>
            <span class="coming-soon">🇯🇵 日本→中国（即将上线）</span>
            <span class="coming-soon">🇪🇺 欧洲→中国（即将上线）</span>
          </div>
        </div>
        <a href="/student-luggage/">留学生行李</a>
        <a href="/pricing.html">运费报价</a>
        <a href="/tools/">免费工具</a>
        <a href="/blog/">攻略</a>
        <a href="/about.html">关于我们</a>
      </nav>
    </div>
  </header>"""

# ===== 公共 Footer =====
FOOTER = """  <footer class="footer">
    <div class="footer-grid">
      <div>
        <h4>回国线路</h4>
        <a href="/usa-to-china/">🇺🇸 美国→中国</a>
        <a href="/seasia-to-china/singapore/">🇸🇬 新加坡→中国</a>
        <a href="/seasia-to-china/malaysia/">🇲🇾 马来西亚→中国</a>
        <span class="coming-soon">🇯🇵 日本→中国（即将上线）</span>
        <span class="coming-soon">🇪🇺 欧洲→中国（即将上线）</span>
      </div>
      <div>
        <h4>寄件指南</h4>
        <a href="/seasia-to-china/packing-guide/">打包指南</a>
        <a href="/blog/usa-to-china-prohibited-items">禁运品清单</a>
        <a href="/blog/usa-to-china-customs-duty">清关流程</a>
        <a href="/faq.html">常见问题 FAQ</a>
        <a href="/tools/shipping-calculator">价格计算器</a>
      </div>
      <div>
        <h4>关于我们</h4>
        <a href="/about.html">公司介绍</a>
        <a href="/contact.html">联系我们</a>
        <p>服务条款</p>
        <p>隐私政策</p>
      </div>
      <div>
        <h4>联系方式</h4>
        <p>💬 WhatsApp: +1-XXX-XXX-XXXX</p>
        <p>💬 微信: subao_global</p>
        <p>📧 邮箱: info@subaog.com</p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 速豹回国物流 Subao Global Logistics. All rights reserved. | <a href="/sitemap.xml">Sitemap</a></p>
    </div>
  </footer>"""

def page(title, description, canonical, og_title, og_desc, schema_json, breadcrumb_json, body_html):
    """生成完整 HTML 页面"""
    schemas = ""
    if schema_json:
        for s in schema_json:
            schemas += f'  <script type="application/ld+json">\n{s}\n  </script>\n'
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="applicable-device" content="pc,mobile">
  <meta name="format-detection" content="telephone=no">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:image" content="https://subaog.com/assets/images/og-image.jpg">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="zh_CN">
  <meta name="lastmod" content="2026-08-09">
{schemas}
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXX"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-XXXXXXXX');</script>
  <style>{COMMON_CSS}</style>
</head>
<body>
{HEADER}
  <section class="hero">
    <div class="container">
      <h1>{breadcrumb_json[-1][0]}</h1>
      <p class="subtitle">{og_desc}</p>
    </div>
  </section>
  <section class="content-section">
    <div class="container">
{body_html}
    </div>
  </section>
{FOOTER}
  <script>
  document.querySelectorAll('.faq-question').forEach(function(btn){{
    btn.addEventListener('click',function(){{this.classList.toggle('open');this.nextElementSibling.classList.toggle('show')}});
  }});
  </script>
</body>
</html>"""

def breadcrumb(items):
    """生成 BreadcrumbList Schema + HTML"""
    b = [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(items)]
    schema = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": b}, ensure_ascii=False)
    html = '<div class="breadcrumb">' + ' › '.join([f'<a href="{u}">{n}</a>' if u else n for n, u in items]) + '</div>'
    return schema, html

def faq_schema(qas):
    """生成 FAQPage Schema"""
    entities = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False)

import json

# ================================================================
# Page 1: 东南亚总览 /seasia-to-china/
# ================================================================
bc_items = [("首页", "https://subaog.com/"), ("东南亚寄中国", "")]
bc_schema, bc_html = breadcrumb(bc_items)

body = f"""{bc_html}
<p>速豹回国物流覆盖<strong>新加坡、马来西亚、泰国、菲律宾</strong>等多个东南亚国家到中国的回国行李寄送服务。双清包税、门到门、10-15工作日送达，是东南亚华人/留学生/代购回国寄物的首选渠道。</p>

<h2>为什么选择速豹东南亚专线</h2>
<div class="info-box">
  <h4>📦 双清包税，一口价无隐藏费用</h4>
  <p>报价含基础关税，不会中途加收"清关费""查验费"。告别二次收费焦虑。</p>
</div>
<div class="info-box">
  <h4>🚪 门到门全链路</h4>
  <p>从你在新加坡/马来西亚的家门口取件，直接送到中国收件地址。中间无需自己跑腿。</p>
</div>
<div class="info-box">
  <h4>⏱ 10-15工作日稳定时效</h4>
  <p>空运干线+中国内地快递派送，全程可追踪。比海运快3倍，比国际快递便宜50%。</p>
</div>

<h2>东南亚→中国 价格一览</h2>
<table class="price-table">
  <tr><th>重量梯度</th><th>价格</th><th>时效</th><th>服务</th></tr>
  <tr><td>21kg+</td><td><strong>70 元/kg</strong></td><td>10-15 工作日</td><td>双清包税门到门</td></tr>
  <tr><td>100kg+</td><td><strong>65 元/kg</strong></td><td>10-15 工作日</td><td>双清包税门到门</td></tr>
</table>
<p style="font-size:13px;color:var(--text-secondary)">* 体积重公式：长×宽×高(cm) ÷ 5000，实重与体积重取大值计费。</p>

<h2>寄件流程</h2>
<ol class="step-list">
  <li><div><strong>联系客服</strong><br>告知出发国、物品类型和预估重量，获取精准报价</div></li>
  <li><div><strong>打包寄仓</strong><br>自行打包或安排上门取件，寄到东南亚中转仓</div></li>
  <li><div><strong>跨境运输</strong><br>空运干线发往中国口岸，清关后国内派送</div></li>
  <li><div><strong>签收到家</strong><br>顺丰/EMS/德邦派送上门，全程10-15工作日</div></li>
</ol>

<h2>覆盖国家</h2>
<div class="related-links">
  <a href="/seasia-to-china/singapore/" class="related-link"><strong>🇸🇬 新加坡→中国</strong><span>留学生行李/搬家/代购专场</span></a>
  <a href="/seasia-to-china/malaysia/" class="related-link"><strong>🇲🇾 马来西亚→中国</strong><span>留学生行李/搬家/代购专场</span></a>
</div>

<h2>常见问题</h2>
<div class="faq-item" style="border-bottom:1px solid var(--border)">
  <button class="faq-question" style="width:100%;padding:18px 0;text-align:left;background:none;border:none;font-size:16px;font-weight:500;cursor:pointer;display:flex;justify-content:space-between">东南亚寄中国能寄什么物品？<span style="font-size:12px">▼</span></button>
  <div class="faq-answer" style="display:none;padding-bottom:18px;font-size:14px;color:var(--text-secondary)"><p>可以寄：旧衣物、书籍、日用品、保健品、化妆品（旧物）、厨房用品等个人旧物品。不能寄：新鲜食品、肉类、电池（部分）、液体（部分）、仿牌。具体品类请咨询客服确认。</p></div>
</div>
<div class="faq-item" style="border-bottom:1px solid var(--border)">
  <button class="faq-question" style="width:100%;padding:18px 0;text-align:left;background:none;border:none;font-size:16px;font-weight:500;cursor:pointer;display:flex;justify-content:space-between">从新加坡/马来西亚寄回国要多久？<span style="font-size:12px">▼</span></button>
  <div class="faq-answer" style="display:none;padding-bottom:18px;font-size:14px;color:var(--text-secondary)"><p>全程10-15工作日。其中东南亚本地取件+集货1-3天，空运干线5-7天，中国清关1-2天，国内快递派送1-3天。</p></div>
</div>

<div class="cta-box">
  <h3>准备从东南亚寄东西回国？</h3>
  <p>告诉我们出发国家和物品类型，30分钟出报价</p>
  <a href="https://wa.me/1XXXXXXXXXX" class="btn-cta" target="_blank">💬 WhatsApp 免费咨询</a>
</div>"""

faqs = [
    ("东南亚寄中国能寄什么物品？", "可以寄：旧衣物、书籍、日用品、保健品、化妆品（旧物）、厨房用品等个人旧物品。不能寄：新鲜食品、肉类、电池（部分）、液体（部分）、仿牌。"),
    ("东南亚寄中国多少钱？", "21kg以上70元/kg，100kg以上65元/kg。双清包税门到门。计费取实重和体积重（长×宽×高÷5000）的较大值。"),
    ("从新加坡寄回国要多久？", "全程10-15工作日。东南亚本地取件+集货1-3天，空运5-7天，清关1-2天，国内派送1-3天。"),
]

html = page(
    "东南亚寄中国：回国行李物流全攻略 | 速豹回国物流",
    "东南亚寄中国回国行李专线：新加坡、马来西亚寄中国，双清包税门到门。21kg+ 70元/kg，100kg+ 65元/kg，10-15工作日送达。留学生/搬家/代购均可。",
    "https://subaog.com/seasia-to-china/",
    "东南亚寄中国：回国行李物流全攻略 | 速豹回国物流",
    "东南亚寄中国回国行李专线：新加坡、马来西亚寄中国，双清包税门到门。21kg+ 70元/kg，100kg+ 65元/kg，10-15工作日。",
    [json.dumps({"@context":"https://schema.org","@type":"Organization","name":"速豹回国物流","url":"https://subaog.com"}), bc_schema, faq_schema(faqs)],
    bc_items,
    body
)

os.makedirs(f"{BASE}/seasia-to-china", exist_ok=True)
with open(f"{BASE}/seasia-to-china/index.html", "w") as f:
    f.write(html)
print("✅ /seasia-to-china/ 总览页")

# ================================================================
# Page 2: 新加坡 Pillar /seasia-to-china/singapore/
# ================================================================
bc_items2 = [("首页", "https://subaog.com/"), ("东南亚寄中国", "https://subaog.com/seasia-to-china/"), ("新加坡→中国", "")]
bc_s2, bc_h2 = breadcrumb(bc_items2)

body2 = f"""{bc_h2}
<p>新加坡寄中国回国行李专线：双清包税门到门，10-15工作日。覆盖全岛取件（SingPost / 自送仓 / 上门取货）。留学生毕业回国、移民搬家、代购发货一站式搞定。</p>

<h2>新加坡→中国 线���概览</h2>
<table class="price-table">
  <tr><th>项目</th><th>详情</th></tr>
  <tr><td>运输方式</td><td>空运专线</td></tr>
  <tr><td>时效</td><td><strong>10-15 工作日</strong>门到门</td></tr>
  <tr><td>21kg+ 价格</td><td><strong>70 元/kg</strong></td></tr>
  <tr><td>100kg+ 价格</td><td><strong>65 元/kg</strong></td></tr>
  <tr><td>计费方式</td><td>实重 vs 体积重（长×宽×高÷5000）取大值</td></tr>
  <tr><td>清关方式</td><td>双清包税（含基础关税）</td></tr>
  <tr><td>赔付</td><td>丢件按保价赔付，未保价按行业标准</td></tr>
</table>

<h2>寄件流程</h2>
<ol class="step-list">
  <li><div><strong>新加坡本地取件</strong><br>支持 SingPost 寄送、自行送到仓库、或预约上门取件</div></li>
  <li><div><strong>仓储打包</strong><br>免费提供纸箱、拆外包装减重、加固易碎品</div></li>
  <li><div><strong>跨境运输+清关</strong><br>空运干线→中国口岸清关（广州/深圳/上海）</div></li>
  <li><div><strong>国内派送到门</strong><br>顺丰/EMS/德邦派送到你指定的中国地址</div></li>
</ol>

<h2>能寄什么？</h2>
<div class="info-box">
  <h4>✅ 可以寄</h4>
  <p>衣物、书籍、日用品、保健品、化妆品（旧物）、厨房用品、小型家电（不含电池）、纪念品</p>
</div>
<div class="info-box">
  <h4>❌ 不能寄</h4>
  <p>新鲜食品、肉类、电池（锂电池）、液体（部分）、仿牌/盗版、武器、易燃易爆品</p>
</div>

<h2>适合你的场景</h2>
<div class="related-links">
  <a href="/seasia-to-china/singapore/student/" class="related-link"><strong>🎓 留学生毕业回国行李</strong><span>NUS/NTU/SMU 毕业季寄送指南</span></a>
  <a href="/seasia-to-china/singapore/moving/" class="related-link"><strong>📦 搬家/移民回国行李</strong><span>大件搬家全攻略，100kg+更优惠</span></a>
  <a href="/seasia-to-china/singapore/shopping/" class="related-link"><strong>🛒 代购/购物寄回国</strong><span>新加坡保健品/化妆品/零食寄中国</span></a>
</div>

<div class="cta-box">
  <h3>从新加坡寄东西回国？</h3>
  <p>30分钟出报价，全岛取件覆盖</p>
  <a href="https://wa.me/1XXXXXXXXXX" class="btn-cta" target="_blank">💬 WhatsApp 免费咨询</a>
</div>"""

faqs2 = [
    ("新加坡寄中国多少钱？", "21kg以上70元/kg，100kg以上65元/kg。双清包税门到门。例如：3箱共60kg = 60×70 = 4,200元。"),
    ("新加坡寄中国多久能到？", "全程10-15工作日。本地取件1-2天，空运5-7天，清关1-2天，派送1-3天。"),
    ("新加坡本地怎么取件？", "三选一：1)自己送到仓库 2)SingPost寄到仓库 3)预约上门取件（需额外收费）。"),
]

html2 = page(
    "新加坡寄中国回国行李：价格/时效/流程（2026）| 速豹回国物流",
    "新加坡回国行李物流，双清包税门到门。21kg+ 70元/kg，100kg+ 65元/kg，10-15工作日。NUS/NTU留学生毕业寄、搬家移民、代购发货。全岛取件，全程追踪。",
    "https://subaog.com/seasia-to-china/singapore/",
    "新加坡寄中国回国行李：价格/时效/流程（2026）| 速豹回国物流",
    "新加坡回国行李物流，双清包税门到门。21kg+ 70元/kg，100kg+ 65元/kg，10-15工作日。",
    [json.dumps({"@context":"https://schema.org","@type":"Organization","name":"速豹回国物流","url":"https://subaog.com"}), bc_s2, faq_schema(faqs2)],
    bc_items2,
    body2
)

os.makedirs(f"{BASE}/seasia-to-china/singapore", exist_ok=True)
with open(f"{BASE}/seasia-to-china/singapore/index.html", "w") as f:
    f.write(html2)
print("✅ /seasia-to-china/singapore/ Pillar")

# ================================================================
# Page 5: 新加坡打包指南 /seasia-to-china/packing-guide/
# ================================================================
bc_items_pg = [("首页", "https://subaog.com/"), ("东南亚寄中国", "https://subaog.com/seasia-to-china/"), ("打包指南", "")]
bc_pg, bc_hpg = breadcrumb(bc_items_pg)

body_pg = f"""{bc_hpg}
<p>回国行李打包是跨境物流中最容易被忽视的关键环节。打包不当不仅增加体积重，还可能导致破损、被退运。本文从纸箱选型、填充技巧、到避坑检查，手把手教你搞定回国行李打包。</p>

<h2>1. 纸箱怎么选</h2>
<div class="info-box">
  <h4>📐 推荐尺寸</h4>
  <ul>
    <li><strong>常规箱</strong>：50×40×30cm（最常用，不易超体积重）</li>
    <li><strong>大件箱</strong>：60×50×40cm（适合衣物、被褥等轻抛货）</li>
    <li><strong>书籍箱</strong>：40×30×30cm（书太重，小箱控制单箱重量）</li>
  </ul>
</div>
<div class="info-box">
  <h4>⚠️ 避坑提醒</h4>
  <ul>
    <li>单箱<strong>不超过25kg</strong>，超重可能被加收附加费</li>
    <li>单边<strong>不超过120cm</strong>，围长（长+2宽+2高）不超过266cm</li>
    <li>Home Depot / IKEA / Shopee 都能买到合适的搬家纸箱</li>
  </ul>
</div>

<h2>2. 易碎品怎么包</h2>
<ol class="step-list">
  <li><div><strong>气泡膜包裹</strong><br>易碎品先用气泡膜包2-3层，边角重点加厚</div></li>
  <li><div><strong>珍珠棉/泡沫填充</strong><br>箱子底部、四周、顶部铺珍珠棉或泡沫块</div></li>
  <li><div><strong>无缝隙原则</strong><br>摇晃箱子听不到物品碰撞声才合格</div></li>
  <li><div><strong>标记易碎</strong><br>箱体外用红色胶带标记"FRAGILE"</div></li>
</ol>

<h2>3. 衣物打包技巧</h2>
<div class="info-box">
  <h4>👕 真空压缩袋是神器</h4>
  <p>羽绒服、棉被、毛衣等蓬松衣物用真空压缩袋，体积能减少50-70%。提醒：压缩后箱子会变重，注意单箱不超过25kg。</p>
</div>

<h2>4. 禁运品检查清单</h2>
<p>装箱前逐项检查，以下<strong>绝对不能放</strong>：</p>
<ul>
  <li>❌ 锂电池、充电宝（必须随身携带）</li>
  <li>❌ 打火机、喷雾罐（易燃易爆）</li>
  <li>❌ 新鲜食物、肉类、水果</li>
  <li>❌ 现金、贵重首饰（建议随身带）</li>
  <li>❌ 药品（需处方证明）</li>
  <li>❌ 酒精类液体</li>
</ul>

<h2>5. 体积重计算演示</h2>
<div class="info-box">
  <h4>📏 公式：长(cm) × 宽(cm) × 高(cm) ÷ 5000 = 体积重(kg)</h4>
  <p>示例：箱子 50×40×30cm → 60,000 ÷ 5000 = <strong>12kg 体积重</strong></p>
  <p>如果实际重量 10kg，则按 12kg 收费（取大值）</p>
  <p style="margin-top:8px">💡 <strong>省钱技巧</strong>：衣物用真空压缩袋减少体积，可以有效降低体积重。</p>
</div>

<h2>6. 常见打包错误</h2>
<ul>
  <li><strong>错误1：箱子太满</strong>——箱子鼓包变形，运输中容易破裂</li>
  <li><strong>错误2：只用胶带封一次</strong>——用"工"字封箱法，横竖各3道</li>
  <li><strong>错误3：不写标签</strong>——每箱贴姓名+地址+电话标签</li>
  <li><strong>错误4：贵重物品混在普通箱</strong>——建议单独保价</li>
</ul>

<div class="cta-box">
  <h3>不确定怎么打包？</h3>
  <p>拍照发给客服，我们免费帮你评估打包方案</p>
  <a href="https://wa.me/1XXXXXXXXXX" class="btn-cta" target="_blank">💬 WhatsApp 免费咨询</a>
</div>"""

html_pg = page(
    "回国行李打包指南：不破损、不超重、不被退 | 速豹回国物流",
    "回国行李打包完整指南：纸箱选型、易碎品包装、真空压缩袋技巧、禁运品检查清单、体积重计算演示。从打包到寄出一站式搞定。",
    "https://subaog.com/seasia-to-china/packing-guide/",
    "回国行李打包指南：不破损、不超重、不被退 | 速豹回国物流",
    "回国行李打包完整指南：纸箱选型、易碎品包装、禁运品检查清单、体积重计算。从打包到寄出一站式搞定。",
    [json.dumps({"@context":"https://schema.org","@type":"Organization","name":"速豹回国物流","url":"https://subaog.com"}), bc_pg],
    bc_items_pg,
    body_pg
)

os.makedirs(f"{BASE}/seasia-to-china/packing-guide", exist_ok=True)
with open(f"{BASE}/seasia-to-china/packing-guide/index.html", "w") as f:
    f.write(html_pg)
print("✅ /seasia-to-china/packing-guide/ 打包指南")

# ================================================================
# Page: 东南亚价格页 /seasia-to-china/pricing/
# ================================================================
bc_items_pr = [("首页", "https://subaog.com/"), ("东南亚寄中国", "https://subaog.com/seasia-to-china/"), ("价格对比", "")]
bc_pr, bc_hpr = breadcrumb(bc_items_pr)

body_pr = f"""{bc_hpr}
<p>东南亚→中国回国行李专线价格全透明。新加坡、马来西亚统一价，双清包税，无隐藏费用。</p>

<h2>价格表</h2>
<table class="price-table">
  <tr><th>国家/区域</th><th>21kg+</th><th>100kg+</th><th>时效</th><th>服务</th></tr>
  <tr><td>🇸🇬 新加坡→中国</td><td><strong>70 元/kg</strong></td><td><strong>65 元/kg</strong></td><td>10-15 工作日</td><td>双清包税门到门</td></tr>
  <tr><td>🇲🇾 马来西亚→中国</td><td><strong>70 元/kg</strong></td><td><strong>65 元/kg</strong></td><td>10-15 工作日</td><td>双清包税门到门</td></tr>
</table>

<h2>费用说明</h2>
<div class="info-box">
  <h4>📦 包含在报价中的</h4>
  <ul><li>空运干线运费</li><li>出口报关</li><li>中国进口清关</li><li>基础关税</li><li>国内快递派送</li></ul>
</div>
<div class="info-box">
  <h4>💰 可能产生的额外费用</h4>
  <ul><li>上门取件费（按距离计）</li><li>清单申报费 +100元</li><li>超规箱附加费（>25kg 或单边>120cm）</li><li>运输保险（货值1%）</li></ul>
</div>

<h2>计费规则</h2>
<p>国际快递采用<strong>实重与体积重比较取大值</strong>的计费方式：</p>
<p style="font-size:18px;text-align:center;padding:16px;background:var(--primary-light);border-radius:var(--radius)"><strong>体积重(kg) = 长(cm) × 宽(cm) × 高(cm) ÷ 5000</strong></p>
<p>示例：一个 50×40×30cm 的箱子 = 12kg 体积重。如果实重 10kg，则按 12kg 收费。</p>

<h2>费用估算示例</h2>
<table class="price-table">
  <tr><th>场景</th><th>物品</th><th>估算重量</th><th>预估费用</th></tr>
  <tr><td>留学生毕业回国</td><td>3箱衣物+书籍</td><td>约60kg</td><td>60×70 = <strong>4,200元</strong></td></tr>
  <tr><td>搬家回国</td><td>10箱家具+日用品</td><td>约200kg</td><td>200×65 = <strong>13,000元</strong></td></tr>
  <tr><td>代购发货</td><td>2箱保健品</td><td>约30kg</td><td>30×70 = <strong>2,100元</strong></td></tr>
</table>

<div class="cta-box">
  <h3>获取你的专属报价</h3>
  <p>告诉我们出发国、物品和重量，30分钟出精准报价</p>
  <a href="https://wa.me/1XXXXXXXXXX" class="btn-cta" target="_blank">💬 WhatsApp 免费报价</a>
</div>"""

html_pr = page(
    "东南亚寄中国价格 | 新加坡马来西亚回国行李费用 | 速豹回国物流",
    "东南亚寄中国回国行李价格全透明：新加坡、马来西亚 21kg+ 70元/kg，100kg+ 65元/kg。双清包税门到门，10-15工作日。费用估算、计费规则、省钱技巧。",
    "https://subaog.com/seasia-to-china/pricing/",
    "东南亚寄中国价格 | 新加坡马来西亚回国行李费用 | 速豹回国物流",
    "东南亚寄中国回国行李价格：21kg+ 70元/kg，100kg+ 65元/kg。双清包税门到门。",
    [json.dumps({"@context":"https://schema.org","@type":"Organization","name":"速豹回国物流","url":"https://subaog.com"}), bc_pr],
    bc_items_pr,
    body_pr
)

os.makedirs(f"{BASE}/seasia-to-china/pricing", exist_ok=True)
with open(f"{BASE}/seasia-to-china/pricing/index.html", "w") as f:
    f.write(html_pr)
print("✅ /seasia-to-china/pricing/ 价格页")

print("\n🎉 核心 4 页完成，生成 8 个场景页...")

# ================================================================
# 快速生成场景页（共享模板）
# ================================================================
SCENE_PAGES = [
    # 新加坡场景页
    ("seasia-to-china/singapore/student/", "新加坡留学生毕业回国行李怎么寄？（NUS/NTU 实测）",
     "新加坡留学生毕业回国行李邮寄指南：NUS/NTU/SMU毕业季攻略。费用估算、取件流程、常见行李清单、学生专属建议。",
     "新加坡留学生毕业回国行李怎么寄？", "新加坡留学生毕业回国行李邮寄指南：NUS/NTU/SMU毕业季攻略。费用估算、取件流程、行李清单。",
     [
         ("首页", "https://subaog.com/"), ("东南亚寄中国", "https://subaog.com/seasia-to-china/"),
         ("新加坡→中国", "https://subaog.com/seasia-to-china/singapore/"), ("留学生行李", "")
     ],
     """<p>每年5-7月是新加坡毕业季，NUS、NTU、SMU 的留学生面临同一个问题：<strong>几年攒下的行李怎么运回国？</strong>本文基于真实寄送经验，带你一步步搞定新加坡毕业回国行李。</p>

<h2>毕业季时间表</h2>
<div class="info-box">
  <h4>📅 关键时间节点</h4>
  <ul>
    <li><strong>5月初</strong>：开始整理行李，分类"寄/扔/随身带"</li>
    <li><strong>5月中旬</strong>：联系物流公司，确认报价和取件时间</li>
    <li><strong>5月下旬-6月</strong>：高峰期，建议<strong>提前2周</strong>预约取件</li>
    <li><strong>6-7月</strong>：行李在途中，10-15天后到家</li>
  </ul>
</div>

<h2>常见行李清单</h2>
<ul>
  <li>👕 衣物鞋包（占大头，最重）</li>
  <li>📚 书籍/教材/笔记</li>
  <li>💻 电子产品（笔记本电脑、iPad、相机——<strong>电池需随身携带</strong>）</li>
  <li>🛏️ 床品/被褥（用真空压缩袋）</li>
  <li>🎁 纪念品/伴手礼</li>
  <li>🍳 小型厨房用品（电饭煲、锅具）</li>
</ul>

<h2>费用估算</h2>
<table class="price-table">
  <tr><th>行李量</th><th>估算重量</th><th>预估费用</th></tr>
  <tr><td>1-2箱（精简派）</td><td>约20-30kg</td><td>30×70 = <strong>2,100元</strong></td></tr>
  <tr><td>3-4箱（标准派）</td><td>约50-80kg</td><td>60×70 = <strong>4,200元</strong></td></tr>
  <tr><td>5箱+（囤货派）</td><td>约100kg+</td><td>100×65 = <strong>6,500元</strong></td></tr>
</table>

<h2>NUS/NTU 取件点</h2>
<div class="info-box">
  <h4>📍 取件方式</h4>
  <ul>
    <li><strong>自己送到仓库</strong>：新加坡中部/东部设有集货仓</li>
    <li><strong>预约上门取件</strong>：可到 NUS Utown / NTU Hall 取件（需提前预约）</li>
    <li><strong>SingPost 寄送</strong>：从校内邮局寄到仓库</li>
  </ul>
</div>

<h2>毕业回国还需要注意</h2>
<ul>
  <li>🏠 提前1个月通知房东退房，安排清洁</li>
  <li>✈️ 确认机票日期，行李海运建议在起飞前3-4周寄出</li>
  <li>💳 关闭新加坡银行卡、取消电话合约</li>
  <li>📋 学生签证注销前确保所有手续办完</li>
</ul>

<p style="margin-top:24px">👉 搬家场景请查看：<a href="/seasia-to-china/singapore/moving/" style="color:var(--primary);font-weight:600">新加坡搬家/移民回国行李全攻略 →</a></p>
<p>👉 不确定能寄什么？<a href="/seasia-to-china/singapore/shopping/" style="color:var(--primary);font-weight:600">看看代购和购物寄送指南 →</a></p>

<div class="cta-box">
  <h3>NUS/NTU 毕业行李寄回国？</h3>
  <p>告诉我们校区和预估箱数，30分钟出方案</p>
  <a href="https://wa.me/1XXXXXXXXXX" class="btn-cta" target="_blank">💬 WhatsApp 免费咨询</a>
</div>"""
    ),

    # 新加坡搬家场景
    ("seasia-to-china/singapore/moving/", "新加坡搬家/移民回国行李全攻略 | 速豹回国物流",
     "新加坡搬家回国行李专线：大件家具/电器/厨房用品寄中国。100kg+ 65元/kg，海运更便宜。移民回国免税额度、清关流程、大货攻略。",
     "新加坡搬家/移民回国行李全攻略", "新加坡搬家回国行李专线：大件物品寄中国指南，100kg+更优惠。移民回国攻略。",
     [
         ("首页", "https://subaog.com/"), ("东南亚寄中国", "https://subaog.com/seasia-to-china/"),
         ("新加坡→中国", "https://subaog.com/seasia-to-china/singapore/"), ("搬家回国", "")
     ],
     """<p>从新加坡搬家回中国，行李量往往是留学生的3-5倍。大件家具、厨房电器、多年积累的衣物书籍——怎么运最划算？本文给你完整方案。</p>

<h2>搬家 vs 留学生行李的区别</h2>
<table class="price-table">
  <tr><th>对比维度</th><th>留学生行李</th><th>搬家回国</th></tr>
  <tr><td>典型重量</td><td>20-80kg</td><td>100-500kg</td></tr>
  <tr><td>物品种类</td><td>衣物+书籍为主</td><td>家具+电器+全屋物品</td></tr>
  <tr><td>建议方式</td><td>空运专线</td><td>空运+海运混搭</td></tr>
  <tr><td>清关</td><td>个人物品</td><td>可能需要清单申报</td></tr>
</table>

<h2>100kg+ 大货价格</h2>
<div class="info-box">
  <h4>💰 大货优惠价</h4>
  <p>100kg 以上 <strong>65元/kg</strong>，比 21kg+ 的 70元/kg 便宜 5元/kg。以 200kg 为例，节省 = 200×5 = <strong>1,000元</strong>。</p>
</div>

<h2>大件物品怎么寄</h2>
<ul>
  <li><strong>家具</strong>：可拆卸的拆开打包（省体积），不能拆的按实际尺寸计体积重</li>
  <li><strong>电器</strong>：原包装最好，无原包装用气泡膜+泡沫+硬纸箱</li>
  <li><strong>厨房用品</strong>：锅碗瓢盆分别包裹，空隙填满防撞</li>
  <li><strong>装饰品/摆件</strong>：气泡膜+纸箱，标记易碎</li>
</ul>

<h2>移民回国免税额度</h2>
<div class="info-box">
  <h4>🛃 中国海关规定</h4>
  <p>中国籍旅客回国，个人自用旧物品总值在<strong>5,000元人民币以内</strong>免税。超过部分按品类税率缴税。如果是移民（持外国长期居留），可按"分离运输行李"申报，免税额度更高。具体以海关最新政策为准。</p>
</div>

<h2>海运备选方案</h2>
<p>如果体积很大且不赶时间（可以等25-35天），海运更便宜。但搬家行李一般建议空运为主——时效稳定，清关快。除非你的家具有 5-10 个大件，否则空运性价比更高。</p>

<p style="margin-top:24px">👉 留学生场景：<a href="/seasia-to-china/singapore/student/" style="color:var(--primary);font-weight:600">新加坡留学生毕业回国行李怎么寄 →</a></p>

<div class="cta-box">
  <h3>准备从新加坡搬家回国？</h3>
  <p>告诉我们物品种类和预估重量，获取搬家专属方案</p>
  <a href="https://wa.me/1XXXXXXXXXX" class="btn-cta" target="_blank">💬 WhatsApp 免费报价</a>
</div>"""
    ),

    # 新加坡代购场景
    ("seasia-to-china/singapore/shopping/", "新加坡代购/购物寄回国：能寄什么？| 速豹回国物流",
     "新加坡代购寄回国指南：保健品/化妆品/零食/纪念品能不能寄？怎么寄最省钱？双清包税门到门，10-15工作日。",
     "新加坡代购/购物寄回国：能寄什么？", "新加坡代购寄回国指南：保健品/化妆品/零食/纪念品能不能寄？双清包税门到门。",
     [
         ("首页", "https://subaog.com/"), ("东南亚寄中国", "https://subaog.com/seasia-to-china/"),
         ("新加坡→中国", "https://subaog.com/seasia-to-china/singapore/"), ("代购发货", "")
     ],
     """<p>新加坡代购和购物寄回国最常见的问题：<strong>什么东西能寄？什么东西会卡关？</strong>本文基于真实清关经验，给你一份完整的可寄/不可寄清单。</p>

<h2>新加坡代购热门品类</h2>
<table class="price-table">
  <tr><th>品类</th><th>能否寄</th><th>注意事项</th></tr>
  <tr><td>💊 保健品</td><td>✅ 可以</td><td>每种不超过6瓶，总价建议控制在1000元以内</td></tr>
  <tr><td>💄 化妆品</td><td>✅ 可以（旧物）</td><td>全新未拆封可能需要缴税，旧物免税</td></tr>
  <tr><td>🍪 零食/饼干</td><td>✅ 可以</td><td>预包装食品可寄，新鲜/自制不可</td></tr>
  <tr><td>☕ 白咖啡/即溶</td><td>✅ 可以</td><td>商业包装，不超过个人自用范围</td></tr>
  <tr><td>🧴 护肤品</td><td>✅ 可以</td><td>液体≤100ml/瓶，超过需单独咨询</td></tr>
  <tr><td>👜 包包</td><td>✅ 可以</td><td>旧包免税，新包可能需补税</td></tr>
  <tr><td>📱 电子产品</td><td>⚠️ 有条件</td><td>不含电池的可以，含锂电池需取出随身带</td></tr>
  <tr><td>🍖 肉干/肉骨茶料包</td><td>❌ 不可以</td><td>肉类制品一律禁运</td></tr>
  <tr><td>💊 处方药</td><td>❌ 不可以</td><td>需处方证明，一般不建议寄</td></tr>
</table>

<h2>代购寄件省钱技巧</h2>
<ul>
  <li><strong>凑单到21kg</strong>：21kg 起享受 70元/kg，散件小包价格更高</li>
  <li><strong>拆外包装减体积</strong>：去掉不必要的纸盒，减少体积重</li>
  <li><strong>合箱寄送</strong>：多件合在一起寄比分开寄更省</li>
</ul>

<p style="margin-top:24px">👉 留学生场景：<a href="/seasia-to-china/singapore/student/" style="color:var(--primary);font-weight:600">新加坡留学生毕业回国行李怎么寄 →</a></p>

<div class="cta-box">
  <h3>准备从新加坡代购寄回国？</h3>
  <p>告诉我们想寄的物品，帮您确认是否可寄</p>
  <a href="https://wa.me/1XXXXXXXXXX" class="btn-cta" target="_blank">💬 WhatsApp 免费咨询</a>
</div>"""
    ),

    # ========== 马来西亚场景页 ==========
    # 马来西亚 Pillar
    ("seasia-to-china/malaysia/", "马来西亚寄中国回国行李：价格/时效/流程（2026）| 速豹回国物流",
     "马来西亚回国行李物流，双清包税门到门。21kg+ 70元/kg，100kg+ 65元/kg，10-15工作日。UM/UPM/UKM留学生毕业寄、搬家移民、代购发货。PosLaju/GDEX/J&T取件，全程追踪。",
     "马来西亚寄中国回国行李：价格/时效/流程（2026）| 速豹回国物流",
     "马来西亚回国行李物流，双清包税门到门。21kg+ 70元/kg，100kg+ 65元/kg，10-15工作日。",
     [
         ("首页", "https://subaog.com/"), ("东南亚寄中国", "https://subaog.com/seasia-to-china/"),
         ("马来西亚→中国", "")
     ],
     """<p>马来西亚寄中国回国行李专线：双清包税门到门，10-15工作日。覆盖全马取件（PosLaju / GDEX / J&T上门）。KL、槟城、新山华人社区首选渠道。</p>

<h2>马来西亚→中国 线路概览</h2>
<table class="price-table">
  <tr><th>项目</th><th>详情</th></tr>
  <tr><td>运输方式</td><td>空运专线</td></tr>
  <tr><td>时效</td><td><strong>10-15 工作日</strong>门到门</td></tr>
  <tr><td>21kg+ 价格</td><td><strong>70 元/kg</strong></td></tr>
  <tr><td>100kg+ 价格</td><td><strong>65 元/kg</strong></td></tr>
  <tr><td>清关口岸</td><td>广州/深圳（不同于新加坡清关路径）</td></tr>
  <tr><td>取件方式</td><td>PosLaju / GDEX / J&T 上门取件 + 自送仓</td></tr>
</table>

<h2>寄件流程</h2>
<ol class="step-list">
  <li><div><strong>马来西亚本地取件</strong><br>PosLaju / GDEX / J&T 上门取件，或自行送到 KL 仓库</div></li>
  <li><div><strong>仓储打包</strong><br>免费纸箱、拆外包装减重、易碎品加固</div></li>
  <li><div><strong>跨境运输+清关</strong><br>空运→广州/深圳清关</div></li>
  <li><div><strong>国内派送到门</strong><br>顺丰/EMS/德邦派送</div></li>
</ol>

<h2>能寄什么？</h2>
<div class="info-box">
  <h4>✅ 可以寄</h4>
  <p>旧衣物、书籍、日用品、保健品、化妆品（旧物）、白咖啡、榴莲干（预包装）、纪念品</p>
</div>
<div class="info-box">
  <h4>❌ 不能寄</h4>
  <p>新鲜榴莲、肉类制品、电池（锂电池）、液体（部分）、仿牌、武器</p>
</div>

<h2>马来西亚华人社区覆盖</h2>
<ul>
  <li>🏙️ <strong>KL 吉隆坡</strong>：主仓库所在地，最快当天入库</li>
  <li>🌉 <strong>槟城 Penang</strong>：北马华人集中区，GDEX覆盖</li>
  <li>🌴 <strong>新山 JB</strong>：南马华人枢纽，J&T上门</li>
  <li>🎓 <strong>雪兰莪/霹雳/马六甲</strong>：PosLaju全覆盖</li>
</ul>

<h2>适合你的场景</h2>
<div class="related-links">
  <a href="/seasia-to-china/malaysia/student/" class="related-link"><strong>🎓 留学生毕业回国行李</strong><span>UM/UPM/UKM 毕业季寄送指南</span></a>
  <a href="/seasia-to-china/malaysia/moving/" class="related-link"><strong>📦 搬家/移民回国行李</strong><span>大马搬家回国全攻略</span></a>
  <a href="/seasia-to-china/malaysia/shopping/" class="related-link"><strong>🛒 代购/购物寄回国</strong><span>白咖啡/榴莲干/保健品寄中国</span></a>
</div>

<div class="cta-box">
  <h3>从马来西亚寄东西回国？</h3>
  <p>30分钟出报价，全马取件覆盖</p>
  <a href="https://wa.me/1XXXXXXXXXX" class="btn-cta" target="_blank">💬 WhatsApp 免费咨询</a>
</div>"""
    ),
]

# 批量生成页面的函数
for slug, title, desc, og_title, og_desc, bc, body_content in SCENE_PAGES:
    bc_schema, bc_html = breadcrumb(bc)
    faqs_local = [
        ("寄中国多少钱？", "21kg以上70元/kg，100kg以上65元/kg。双清包税门到门。"),
        ("多久能到？", "全程10-15工作日。本地取件1-3天，空运5-7天，清关1-2天，国内派送1-3天。"),
    ]

    html_page = page(
        f"{title} | 速豹回国物流",
        desc,
        f"https://subaog.com/{slug}",
        f"{og_title} | 速豹回国物流",
        desc,
        [json.dumps({"@context":"https://schema.org","@type":"Organization","name":"速豹回国物流","url":"https://subaog.com"}), bc_schema, faq_schema(faqs_local)],
        bc,
        body_content
    )

    full_path = os.path.join(BASE, slug, "index.html")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(html_page)
    print(f"✅ /{slug}")

# ================================================================
# 马来西亚 student/moving/shopping 快速生成
# ================================================================
MY_PAGES = [
    ("seasia-to-china/malaysia/student/", "马来西亚留学生毕业回国行李怎么寄？（UM/UPM 实测）",
     "马来西亚留学生毕业回国行李邮寄指南：UM/UPM/UKM毕业季攻略。费用估算、取件流程、行李清单、学生专属建议。",
     [
         ("首页", "https://subaog.com/"), ("东南亚寄中国", "https://subaog.com/seasia-to-china/"),
         ("马来西亚→中国", "https://subaog.com/seasia-to-china/malaysia/"), ("留学生行李", "")
     ],
     """<p>每年 UM、UPM、UKM 的毕业生都面临行李回国问题。马来西亚和新加坡情况类似但不完全相同——本地快递（PosLaju/GDEX/J&T）和清关口岸都有差异。</p>
<h2>毕业季时间表</h2><div class="info-box"><h4>📅 马来西亚毕业季</h4><ul><li><strong>7-8月</strong>：公立大学（UM/UPM/UKM）主毕业季</li><li><strong>5-6月 / 11-12月</strong>：私立大学（Taylor's/Sunway/INTI）</li><li>建议<strong>提前2周</strong>联系物流预约取件</li></ul></div>
<h2>常见行李清单</h2><ul><li>👕 衣物鞋包</li><li>📚 书籍/教材</li><li>💻 电子产品（电池随身带）</li><li>🛏️ 床品/被褥（真空袋压缩）</li><li>🎁 纪念品（锡器、Batik等）</li></ul>
<h2>费用估算</h2><table class="price-table"><tr><th>行李量</th><th>估算重量</th><th>预估费用</th></tr><tr><td>2-3箱</td><td>约40-60kg</td><td>60×70=<strong>4,200元</strong></td></tr><tr><td>4-5箱</td><td>约80-100kg</td><td>100×65=<strong>6,500元</strong></td></tr></table>
<h2>马来西亚大学取件</h2><div class="info-box"><h4>📍 UM/UPM/UKM 附近</h4><ul><li><strong>KL 仓库</strong>：可自送或预约上门</li><li><strong>PosLaju</strong>：全国邮局覆盖，从学校寄到仓库</li><li><strong>GDEX/J&T</strong>：西马主要城市上门取件</li></ul></div>
<p style="margin-top:24px">👉 搬家场景：<a href="/seasia-to-china/malaysia/moving/" style="color:var(--primary);font-weight:600">马来西亚搬家/移民回国行李全攻略 →</a></p>
<div class="cta-box"><h3>UM/UPM 毕业行李寄回国？</h3><p>告诉我们校区和预估箱数，30分钟出方案</p><a href="https://wa.me/1XXXXXXXXXX" class="btn-cta" target="_blank">💬 WhatsApp 免费咨询</a></div>"""
    ),
    ("seasia-to-china/malaysia/moving/", "马来西亚搬家/移民回国行李全攻略 | 速豹回国物流",
     "马来西亚搬家回国行李专线：大件家具/电器寄中国。100kg+ 65元/kg，海运可备选。KL/槟城/新山取件，双清包税门到门。",
     [
         ("首页", "https://subaog.com/"), ("东南亚寄中国", "https://subaog.com/seasia-to-china/"),
         ("马来西亚→中国", "https://subaog.com/seasia-to-china/malaysia/"), ("搬家回国", "")
     ],
     """<p>从马来西亚搬家回中国，比留学生行李量大得多。本文专为移民/长期居住回国的华人准备。</p>
<h2>搬家 vs 留学生行李</h2><table class="price-table"><tr><th>维度</th><th>留学生</th><th>搬家</th></tr><tr><td>重量</td><td>20-80kg</td><td>100-500kg</td></tr><tr><td>品类</td><td>衣物+书籍</td><td>家具+电器+全屋</td></tr></table>
<h2>100kg+ 大货优势</h2><div class="info-box"><p>100kg 以上 <strong>65元/kg</strong>，比 21kg+ 的 70元/kg 便宜 5元/kg。200kg 的搬家单直接省 <strong>1,000元</strong>。</p></div>
<h2>大件寄送注意</h2><ul><li>家具尽量拆卸，减少体积重</li><li>电器用原包装或加厚防护</li><li>锡器/瓷器等易碎品单独标记</li><li>超过10箱建议分批发货</li></ul>
<h2>清关要点</h2><p>马来西亚→中国清关走广州/深圳口岸。个人旧物品总值 5,000元内免税。大货搬家可能需要清单申报（+100元申报费）。</p>
<p style="margin-top:24px">👉 留学生场景：<a href="/seasia-to-china/malaysia/student/" style="color:var(--primary);font-weight:600">马来西亚留学生毕业回国行李怎么寄 →</a></p>
<div class="cta-box"><h3>从马来西亚搬家回国？</h3><p>告诉我们物品种类和预估重量，获取专属方案</p><a href="https://wa.me/1XXXXXXXXXX" class="btn-cta" target="_blank">💬 WhatsApp 免费报价</a></div>"""
    ),
    ("seasia-to-china/malaysia/shopping/", "马来西亚代购/购物寄回国：能寄什么？| 速豹回国物流",
     "马来西亚代购寄回国指南：白咖啡/旧街场/榴莲干/肉骨茶料能不能寄？保健品/化妆品/纪念品怎么寄最省钱？双清包税门到门。",
     [
         ("首页", "https://subaog.com/"), ("东南亚寄中国", "https://subaog.com/seasia-to-china/"),
         ("马来西亚→中国", "https://subaog.com/seasia-to-china/malaysia/"), ("代购发货", "")
     ],
     """<p>马来西亚代购和购物寄回国，热门品类包括白咖啡、榴莲零食、肉骨茶料包、锡器等。但不同品类有不同的寄送规则。</p>
<h2>马来西亚代购热门品类</h2><table class="price-table"><tr><th>品类</th><th>能否寄</th><th>注意事项</th></tr><tr><td>☕ 白咖啡/即溶饮料</td><td>✅ 可以</td><td>商业包装，不超过自用范围</td></tr><tr><td>🍈 榴莲干/榴莲零食</td><td>✅ 可以</td><td>预包装零食可寄，新鲜榴莲❌</td></tr><tr><td>🍖 肉骨茶料包</td><td>⚠️ 看成分</td><td>纯药材香料可以，含肉块的❌</td></tr><tr><td>💊 保健品</td><td>✅ 可以</td><td>每种不超过6瓶</td></tr><tr><td>💄 化妆品</td><td>✅ 可以（旧物）</td><td>全新可能需缴税</td></tr><tr><td>🏺 锡器</td><td>✅ 可以</td><td>易碎品，需加固包装</td></tr></table>
<h2>代购省钱技巧</h2><ul><li>凑到21kg享受70元/kg优惠价</li><li>拆外包装减体积（特别是礼盒装）</li><li>同一收货地址合并寄送省运费</li></ul>
<p style="margin-top:24px">👉 留学生场景：<a href="/seasia-to-china/malaysia/student/" style="color:var(--primary);font-weight:600">马来西亚留学生毕业回国行李怎么寄 →</a></p>
<div class="cta-box"><h3>准备从马来西亚代购寄回国？</h3><p>告诉我们想寄的物品，帮您确认是否可寄</p><a href="https://wa.me/1XXXXXXXXXX" class="btn-cta" target="_blank">💬 WhatsApp 免费咨询</a></div>"""
    ),
]

for slug, title, desc, bc, body_content in MY_PAGES:
    bc_schema, bc_html = breadcrumb(bc)
    faqs_local = [
        ("马来西亚寄中国多少钱？", "21kg以上70元/kg，100kg以上65元/kg。双清包税门到门。"),
        ("多久能到？", "全程10-15工作日。本地取件1-3天，空运5-7天，清关1-2天，派送1-3天。"),
    ]
    html_page = page(
        f"{title} | 速豹回国物流",
        desc,
        f"https://subaog.com/{slug}",
        f"{title} | 速豹回国物流",
        desc,
        [json.dumps({"@context":"https://schema.org","@type":"Organization","name":"速豹回国物流","url":"https://subaog.com"}), bc_schema, faq_schema(faqs_local)],
        bc,
        body_content
    )
    full_path = os.path.join(BASE, slug, "index.html")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(html_page)
    print(f"✅ /{slug}")

print("\n🎉 全部 11 个东南亚页面生成完毕！")
