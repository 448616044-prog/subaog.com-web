# -*- coding: utf-8 -*-
"""
品类长尾页生成器：新增 10 个 can-i-ship 品类（中英文对称）
复用 gen-blog-en.py 的 render_page（英文）+ 内联中文模板。
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path("/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com")
DOMAIN = "https://subaog.com"
GA_ID = "G-DJGPMS9MOB"

# 复用英文模板
spec = importlib.util.spec_from_file_location("gec", "gen-en-content.py")
gec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gec)
render_page = gec.render_page
faq_html = gec.faq_html
faq_schema = gec.faq_schema
cta_html = gec.cta_html

# 10 个品类数据
ITEMS = [
    {"slug": "wine", "zh": "红酒", "en": "Wine", "rate": "50%", "verdict_zh": "限量可寄", "verdict_en": "Limited",
     "note_zh": "每人限 2 瓶，需如实申报，走海运更稳", "note_en": "Limit 2 bottles per person, declare accurately, sea freight recommended"},
    {"slug": "books", "zh": "书籍", "en": "Books", "rate": "15%", "verdict_zh": "可寄", "verdict_en": "Allowed",
     "note_zh": "教材/专业书/普通读物均可，注意政治敏感类禁运", "note_en": "Textbooks and general reading OK; politically sensitive material prohibited"},
    {"slug": "shoes", "zh": "鞋子", "en": "Shoes", "rate": "30%", "verdict_zh": "可寄", "verdict_en": "Allowed",
     "note_zh": "注意品牌鞋需提供购买凭证防知产纠纷", "note_en": "Branded shoes need purchase receipts to avoid IP disputes"},
    {"slug": "coffee", "zh": "咖啡", "en": "Coffee", "rate": "15%", "verdict_zh": "可寄", "verdict_en": "Allowed",
     "note_zh": "密封原包装，注意保质期", "note_en": "Sealed original packaging, mind shelf life"},
    {"slug": "pet-food", "zh": "宠物粮", "en": "Pet Food", "rate": "15%", "verdict_zh": "需确认", "verdict_en": "Check first",
     "note_zh": "含肉类成分可能受限，先发配料表确认", "note_en": "Meat-based formulas may be restricted; send ingredient list first"},
    {"slug": "medical-devices", "zh": "医疗器械", "en": "Medical Devices", "rate": "15%", "verdict_zh": "需证明", "verdict_en": "Doc required",
     "note_zh": "个人用小件可寄，需提供自用说明", "note_en": "Personal-use small devices OK with self-use declaration"},
    {"slug": "musical-instruments", "zh": "乐器", "en": "Musical Instruments", "rate": "15%", "verdict_zh": "可寄", "verdict_en": "Allowed",
     "note_zh": "大件乐器注意体积重，建议海运", "note_en": "Large instruments: mind volumetric weight, sea freight recommended"},
    {"slug": "bicycles", "zh": "自行车", "en": "Bicycles", "rate": "15%", "verdict_zh": "可寄", "verdict_en": "Allowed",
     "note_zh": "需拆装，走海运大件渠道最省", "note_en": "Disassemble first; sea freight most economical for large items"},
    {"slug": "tea", "zh": "茶叶", "en": "Tea", "rate": "15%", "verdict_zh": "可寄", "verdict_en": "Allowed",
     "note_zh": "密封原包装，散装茶需申报", "note_en": "Sealed original packaging; loose tea needs declaration"},
    {"slug": "snacks", "zh": "零食", "en": "Snacks", "rate": "15%", "verdict_zh": "可寄（不含肉类）", "verdict_en": "Allowed (no meat)",
     "note_zh": "糖果/饼干/巧克力可寄，肉类制品禁运", "note_en": "Candy/cookies/chocolate OK; meat products prohibited"},
]


# 通用 FAQ（每个品类页追加，台湾站打法：FAQ 是排 2-5 名的核心）
COMMON_FAQ_EN = [
    ("How long does shipping to China take?",
     "Air freight takes 10–15 working days door-to-door. Sea freight takes 25–35 days."),
    ("Will I pay customs duty?",
     "Personal items under RMB 1,000 (about $140) are duty-free. Our tax-inclusive service covers standard duty."),
    ("What's the cheapest way to ship to China?",
     "Chinese consolidated shipping is 40–60% cheaper than USPS/FedEx for parcels over 5kg."),
    ("What documents do I need?",
     "A simple item description and recipient info. We handle the customs paperwork for you."),
    ("What if my package is lost or damaged?",
     "Optional insurance is available. Report any issue within 48 hours of delivery."),
    ("Can you ship to any city in China?",
     "Yes — we deliver door-to-door to all major cities in mainland China."),
    ("Do you offer free pickup?",
     "Yes — free doorstep pickup across the USA."),
]

COMMON_FAQ_ZH = [
    ("寄中国要多久？", "空运10-15工作日门到门，海运25-35天。"),
    ("会被税吗？免税额多少？", "个人物品人民币1000元以下免税。我们的双清包税服务已含基础关税。"),
    ("哪个渠道最便宜？", "华人集运比FedEx/UPS便宜40-60%，5kg以上尤其划算。"),
    ("需要什么文件清关？", "简单物品清单+收件人信息即可，清关手续我们代办。"),
    ("丢了/破损怎么办？", "可选运输保险。签收后48小时内反馈问题。"),
    ("能寄到中国任何城市吗？", "可以，中国大陆主要城市门到门派送。"),
    ("有免费上门取件吗？", "有，全美免费上门取件。"),
]


def gen_en(item):
    slug = item["slug"]
    en = item["en"]
    zh = item["zh"]
    rel = f"blog/can-i-ship-{slug}-to-china.html"
    title = f"Can I Ship {en} to China? Rules & Duty (2026) | Subao Global"
    desc = f"Shipping {en.lower()} to China — {item['verdict_en']}, duty rate {item['rate']}, and packing tips. {item['note_en']}."
    faq = [
        (f"Can I ship {en.lower()} to China?",
         f"{item['verdict_en']}. {item['note_en']}. Duty rate is {item['rate']} on value above the RMB 1,000 personal allowance."),
        (f"How much duty will I pay on {en.lower()}?",
         f"{en} is taxed at {item['rate']} on value above RMB 1,000 (about $140). Personal-use quantities are often duty-free. Our tax-inclusive service covers standard duty."),
        (f"How should I pack {en.lower()} for shipping?",
         f"Keep {en.lower()} in original packaging, use cushioning, and declare the item accurately to avoid customs delays."),
    ] + COMMON_FAQ_EN
    body = f"""  <section class="hero" style="padding-bottom:48px"><div class="container">
      <h1>Can I Ship {en} to China?</h1>
      <p class="subtitle">{item['note_en']}. Duty rate {item['rate']}.</p>
    </div></section>
  <section class="section"><div class="container" style="max-width:800px">
    <div style="background:#fff;border:1px solid var(--border);border-radius:16px;padding:36px">
      <div style="margin-bottom:24px"><span style="font-size:13px;color:var(--text-secondary)">Verdict:</span> <strong style="font-size:18px;color:{'#00B900' if 'Allowed' in item['verdict_en'] else '#E65100'}">{item['verdict_en']}</strong></div>
      <p style="color:var(--text-secondary);line-height:1.8">{item['note_en']}</p>
      <div style="margin-top:24px"><span style="font-size:13px;color:var(--text-secondary)">Duty rate:</span> <strong>{item['rate']}</strong></div>
      <div style="margin-top:8px"><span style="font-size:13px;color:var(--text-secondary)">Transit:</span> <strong>10–15 working days</strong></div>
    </div>
    <div class="section-title" style="margin-top:40px"><h2>Related questions</h2></div>
    {faq_html(faq)}
  </div></section>
  {cta_html()}"""
    Path(ROOT / "en" / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(ROOT / "en" / rel).write_text(render_page(rel, title, desc, body, faq_schema(faq)), encoding="utf-8")


def gen_zh(item):
    slug = item["slug"]
    en = item["en"]
    zh = item["zh"]
    rel = f"blog/can-i-ship-{slug}-to-china.html"
    zh_url = f"{DOMAIN}/zh-cn/blog/can-i-ship-{slug}-to-china.html"
    en_url = f"{DOMAIN}/en/blog/can-i-ship-{slug}-to-china.html"
    title = f"美国{zh}能寄中国吗？税率、限制、避坑全攻略 | 速豹回国物流"
    desc = f"美国{zh}寄中国：{item['verdict_zh']}，税率{item['rate']}。{item['note_zh']}。全攻略一次讲透。"
    faq = [
        (f"美国{zh}能寄中国吗？", f"{item['verdict_zh']}。{item['note_zh']}。超出人民币1000元免税额部分按{item['rate']}税率计税。"),
        (f"寄{zh}回国要交多少税？", f"{zh}税率为{item['rate']}，超出人民币1000元免税额部分按此税率计。个人自用数量通常免税。我们的双清包税服务已含基础关税。"),
        (f"{zh}怎么打包寄回国？", f"保留原包装，做好缓冲防压，如实申报品名避免海关延误。"),
    ] + COMMON_FAQ_ZH
    faq_schema_zh = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    }, ensure_ascii=False)
    verdict_color = "#00B900" if "可寄" in item["verdict_zh"] else "#E65100"
    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="applicable-device" content="pc,mobile">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="alternate" hreflang="zh-CN" href="{zh_url}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="x-default" href="{zh_url}">
  <link rel="canonical" href="{zh_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{zh_url}">
  <meta property="og:locale" content="zh_CN">
  <meta name="lastmod" content="2026-08-17">
  <script type="application/ld+json">{faq_schema_zh}</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
  <style>
:root{{--primary:#0066CC;--primary-dark:#004C99;--primary-light:#E6F0FA;--green:#00B900;--bg:#F5F7FA;--text:#1A1A2E;--text-secondary:#64748B;--border:#E2E8F0;--radius-lg:16px;--radius-pill:24px;--nav-height:68px}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:var(--text);line-height:1.7;font-size:16px;background:var(--bg);overflow-x:hidden}}
a{{text-decoration:none;color:inherit}}
.container{{max-width:1100px;margin:0 auto;padding:0 24px}}
.header{{position:fixed;top:0;left:0;right:0;height:var(--nav-height);background:rgba(255,255,255,.96);backdrop-filter:blur(12px);z-index:1000;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
.header .container{{display:flex;align-items:center;justify-content:space-between;height:100%}}
.logo{{font-size:20px;font-weight:700;color:var(--primary)}}
.nav{{display:flex;align-items:center;gap:2px}}
.nav a{{padding:7px 13px;font-size:13px;font-weight:500;color:var(--text-secondary);border-radius:var(--radius-pill);white-space:nowrap}}
.nav a:hover{{color:var(--primary);background:var(--primary-light)}}
.nav .btn-line{{background:var(--green);color:#fff;padding:7px 16px;font-weight:600}}
.lang-switch{{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;font-size:13px;font-weight:600;color:var(--primary);border:1.5px solid var(--primary-light);border-radius:var(--radius-pill);background:#fff}}
@media(max-width:768px){{.nav{{display:none}}}}
.hero{{background:linear-gradient(135deg,#0066CC,#004C99);color:#fff;padding:100px 24px 48px}}
.hero h1{{font-size:clamp(1.5rem,2.6vw,2.1rem);font-weight:700;margin-bottom:10px;line-height:1.35}}
.hero .subtitle{{font-size:15px;opacity:.92;max-width:680px}}
.section{{padding:48px 0}}
.card{{background:#fff;border:1px solid var(--border);border-radius:16px;padding:32px;margin-bottom:24px}}
.verdict{{font-size:20px;font-weight:800;margin:12px 0}}
.meta{{font-size:14px;color:var(--text-secondary);margin:6px 0}}
.faq-item{{border-bottom:1px solid var(--border)}}
.faq-q{{width:100%;padding:16px 0;text-align:left;background:none;border:none;font-size:15px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;font-family:inherit;color:var(--text)}}
.faq-a{{padding:0 0 16px;font-size:14px;color:var(--text-secondary);line-height:1.7;display:none}}
.faq-a.show{{display:block}}
.cta-section{{background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;padding:48px 24px;text-align:center;border-radius:16px;margin:0 24px 48px}}
.btn-primary{{background:#fff;color:var(--primary);padding:13px 26px;border-radius:24px;font-weight:700;font-size:15px;display:inline-block}}
.footer{{background:#1A1A2E;color:#fff;padding:40px 24px;text-align:center}}
.footer a{{color:#999}}
  </style>
</head>
<body>
  <header class="header"><div class="container">
    <a href="/zh-cn/" class="logo">速豹回国物流<span style="font-size:11px;color:var(--text-secondary);margin-left:8px">美国寄中国</span></a>
    <nav class="nav">
      <a href="/zh-cn/">首页</a><a href="/zh-cn/usa-to-china/">美国寄中国</a>
      <a href="/zh-cn/student-luggage/">留学生行李</a><a href="/zh-cn/pricing.html">运费报价</a>
      <a href="/zh-cn/blog/" class="active">攻略</a>
      <a href="{en_url}" class="lang-switch" hreflang="en">🌐 中文 / English</a>
      <a href="https://d.salesmartly.com/fuxikn" class="btn-line" target="_blank" rel="noopener">💬 免费咨询</a>
    </nav>
  </div></header>

  <section class="hero"><div class="container">
    <h1>美国{zh}能寄中国吗？</h1>
    <p class="subtitle">{item['note_zh']}。税率{item['rate']}，10-15工作日门到门。</p>
  </div></section>

  <section class="section"><div class="container" style="max-width:800px">
    <div class="card">
      <div class="meta">寄件结论</div>
      <div class="verdict" style="color:{verdict_color}">{item['verdict_zh']}</div>
      <p style="color:var(--text-secondary)">{item['note_zh']}</p>
      <div class="meta" style="margin-top:16px">税率：<strong>{item['rate']}</strong></div>
      <div class="meta">时效：<strong>10-15工作日</strong></div>
    </div>
    <h2 style="font-size:1.4rem;font-weight:700;margin:24px 0 12px">常见问题</h2>
    {''.join(f'<div class="faq-item"><button class="faq-q">{q}<span>▼</span></button><div class="faq-a">{a}</div></div>' for q, a in faq)}
  </div></section>

  <section class="cta-section"><div class="container"><h2 style="font-size:1.3rem;margin-bottom:8px">不确定{zh}能不能寄？先问客服</h2><p style="opacity:.9;margin-bottom:18px">30分钟内回复，免费确认。</p><a href="/zh-cn/contact.html" class="btn-primary">免费咨询</a></div></section>

  <footer class="footer"><div class="container">© 2026 速豹回国物流 | <a href="/zh-cn/">首页</a> · <a href="/sitemap.xml">Sitemap</a></div></footer>
  <script>document.querySelectorAll('.faq-q').forEach(function(q){{q.addEventListener('click',function(){{var a=q.nextElementSibling;a.classList.toggle('show');q.querySelector('span').textContent=a.classList.contains('show')?'▲':'▼';}});}});</script>
</body>
</html>"""
    Path(ROOT / "zh-cn" / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(ROOT / "zh-cn" / rel).write_text(page, encoding="utf-8")


def main():
    for item in ITEMS:
        gen_en(item)
        gen_zh(item)
    print(f"✅ 生成 {len(ITEMS)} 个品类 × 中英文 = {len(ITEMS)*2} 页")


if __name__ == "__main__":
    main()
