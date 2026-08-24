#!/usr/bin/env python3
"""中词 4 页推首页优化：
- 给 4 个排 11-30 的页补长尾 FAQ（可见+FAQPage Schema）
- 给孤儿页 san-diego-to-hangzhou 补入链（从 /en/usa-to-china/san-diego/ hub）
长尾问按页定制。
"""
import re
from pathlib import Path

BASE = Path(".")

FAQ = {
"en/blog/dhl-vs-fedex-vs-ups-china.html": [
    ("Is DHL cheaper than FedEx to ship to China?",
     "For documents and parcels under 5kg DHL and FedEx are comparable; for 21kg+ heavy cargo the Chinese DDP line (¥70-80/kg all-in) beats both by 40-60%."),
    ("How long does DHL take to deliver to China?",
     "DHL express to major Chinese cities is typically 3-5 business days; remote areas 5-7 days."),
    ("DHL vs UPS for shipping to China — which is better?",
     "DHL has a denser China network and faster customs clearance; UPS is stronger on the US domestic leg. Compare by weight on our calculator."),
],
"en/city/san-diego-to-hangzhou.html": [
    ("How much does it cost to ship from San Diego to Hangzhou?",
     "21kg+ via the DDP line is ¥70-80/kg all-in; express carriers charge 2-3x more for the same weight."),
    ("How long does San Diego to Hangzhou shipping take?",
     "DDP air is 10-15 days door-to-door; sea freight 25-35 days."),
    ("What is the best way to ship San Diego to China?",
     "For luggage and boxes use the Chinese DDP line with free San Diego pickup; for urgent documents use DHL."),
],
"zh-cn/city/miami-to-shanghai.html": [
    ("迈阿密寄上海多少钱？",
     "21kg 以上双清包税专线 ¥70-80/kg 一口价；国际快递贵 2-3 倍。"),
    ("迈阿密到上海要多久？",
     "空运专线 10-15 天门到门；海运 25-35 天。"),
    ("迈阿密寄上海走什么渠道？",
     "行李/包裹走华人双清专线（迈阿密免费上门取件）；急件走 DHL。"),
],
"zh-cn/seasia-to-china/singapore/index.html": [
    ("新加坡寄中国多少钱？",
     "21kg+ 双清包税专线 ¥70-80/kg；文件走 DHL 3-5 天。"),
    ("新加坡寄中国有哪些渠道？",
     "空运专线（10-15 天）、海运（25-35 天）、国际快递急件三种。"),
    ("新加坡寄中国时效？",
     "空运专线门到门 10-15 个工作日，比直接走 FedEx/UPS 省 40-60%。"),
],
}

FAQ_CSS = """.faq2-item{border-bottom:1px solid var(--border)}
.faq2-q{width:100%;padding:16px 0;text-align:left;background:none;border:none;font-size:15px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;font-family:inherit;color:var(--text)}
.faq2-a{padding:0 0 16px;font-size:14px;color:var(--text-secondary);line-height:1.7;display:none}
.faq2-a.show{display:block}"""

def inject_faq(path, qas):
    p = BASE / path
    t = p.read_text(encoding="utf-8")
    if "长尾问题" in t or "More long-tail" in t:
        print("  skip (already done):", path); return
    # visible block
    items = "".join(
        f'<div class="faq2-item"><button class="faq2-q">{q}<span>▼</span></button><div class="faq2-a">{a}</div></div>'
        for q, a in qas)
    sec = f'''  <section class="section" style="background:#fff"><div class="container">
    <div class="section-title"><h2>{'更多长尾问题' if path.startswith('zh') else 'More long-tail questions'}</h2></div>
    <div class="faq-list" style="max-width:760px;margin:0 auto">{items}</div></div></section>'''
    # ensure FAQ css present
    if ".faq2-item" not in t:
        t = t.replace("</style>", FAQ_CSS + "\n</style>", 1)
    # JSON-LD FAQPage (separate block, safe)
    schema = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (repr(q), repr(a)) for q, a in qas) + ']}'
    jsonld = f'<script type="application/ld+json">{schema}</script>'
    # insert visible section + jsonld before </footer> (兼容行内闭合)
    fi = t.rfind("</footer>")
    if fi < 0:
        print("  FAIL no footer:", path); return
    t = t[:fi] + sec + "\n  " + jsonld + "\n" + t[fi:]
    # faq toggle script
    toggle = '<script>document.querySelectorAll(\'.faq2-q\').forEach(function(q){q.addEventListener(\'click\',function(){var a=q.nextElementSibling;a.classList.toggle(\'show\');q.querySelector(\'span\').textContent=a.classList.contains(\'show\')?\'▲\':\'▼\';});});</script>'
    if "faq2-q" not in t.split("</body>")[0][-2000:]:
        t = t.replace("</body>", toggle + "\n</body>", 1)
    p.write_text(t, encoding="utf-8")
    print("  ✅ FAQ 注入:", path)

def inject_incoming_link():
    # san-diego-to-hangzhou 孤儿 -> 从 /en/usa-to-china/san-diego/ hub 补入链
    hub = BASE / "en/usa-to-china/san-diego/index.html"
    target = "/en/city/san-diego-to-hangzhou.html"
    if not hub.exists():
        print("  hub 缺失"); return
    t = hub.read_text(encoding="utf-8")
    if target in t:
        print("  skip incoming (已链)"); return
    link = f'<a href="{target}" style="display:inline-block;margin:5px 6px;padding:7px 15px;background:#fff;border:1px solid var(--border);border-radius:20px;font-size:13px;color:var(--text);text-decoration:none;font-weight:500">San Diego → Hangzhou 直达 →</a>'
    # 插入到城市 hub 的可寄品类区块后（找 "可寄品类" 区块末尾，简化为插入 footer 前）
    fi = t.rfind("</footer>")
    if fi < 0:
        print("  FAIL no footer in hub"); return
    t = t[:fi] + f'\n  <section class="section" style="background:#F5F7FA"><div class="container"><div class="section-title"><h2>San Diego 城市直达线路</h2></div><div style="text-align:center;line-height:2.4">{link}</div></div></section>\n' + t[fi:]
    hub.write_text(t, encoding="utf-8")
    print("  ✅ san-diego hub 补入链 -> san-diego-to-hangzhou")

for path, qas in FAQ.items():
    inject_faq(path, qas)
inject_incoming_link()
print("\n中词优化完成")
