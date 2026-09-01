#!/usr/bin/env python3
"""subaog.com en 站「USA→China 寄送」主题簇内链矩阵铺开。
11 个高曝光商业页(占全站57%曝光)内链覆盖仅1-6页, 6页无 Related routes 区块。
统一在 footer 底部 Related routes 区块注入标准主题簇链接集(10簇成员+2聚合页)。
幂等: 带 <!-- internal-link-cluster:usa-to-china --> 标记, 已处理则跳过。
用法: python3 fix-internal-link-matrix.py [--run]  (默认 dry-run)
"""
import re, sys, os
from datetime import date

DRY = "--run" not in sys.argv
BASE = "en/blog"
MARK = "<!-- internal-link-cluster:usa-to-china -->"

# 11 个簇成员: slug -> 锚文本
CLUSTER = [
    ("usps-to-china-complete-guide",   "USPS to China guide"),
    ("usa-to-china-shipping-cost",     "USA to China cost"),
    ("cheapest-way-ship-to-china",     "cheapest way to China"),
    ("usa-to-china-cheapest-way",      "cheapest USA to China"),
    ("how-to-ship-from-usa-to-china",  "how to ship from USA"),
    ("usps-vs-ups-china",              "USPS vs UPS"),
    ("dhl-vs-fedex-vs-ups-china",      "DHL vs FedEx vs UPS"),
    ("amazon-shopping-to-china",       "Amazon to China"),
    ("can-i-ship-supplements-to-china","supplements to China"),
    ("best-courier-for-china-shipping","best courier to China"),
    ("dhl-vs-usps-china",              "DHL vs USPS"),
]

PILL = ('<a href="/en/blog/{slug}" style="display:inline-block;margin:5px 6px;'
        'padding:7px 15px;background:#fff;border:1px solid var(--border);'
        'border-radius:20px;font-size:13px;color:var(--text);text-decoration:none;'
        'font-weight:500">{anchor} \u2192</a>')

AGG = ('<a href="/en/routes/" style="display:inline-block;margin:5px 6px;'
       'padding:7px 15px;background:#fff;border:1px solid var(--border);'
       'border-radius:20px;font-size:13px;color:var(--text);text-decoration:none;'
       'font-weight:500">All routes \u2192</a>'
       '<a href="/en/can-i-ship-index/" style="display:inline-block;margin:5px 6px;'
       'padding:7px 15px;background:#fff;border:1px solid var(--border);'
       'border-radius:20px;font-size:13px;color:var(--text);text-decoration:none;'
       'font-weight:500">Can I ship to China \u2192</a>')

def build_rr_section(skip_slug):
    pills = AGG
    for slug, anchor in CLUSTER:
        if slug == skip_slug:
            continue
        pills += PILL.format(slug=slug, anchor=anchor)
    return ('    <section class="section" style="background:#F5F7FA">\n'
            '    <div class="container">\n'
            f'      {MARK}\n'
            '      <div class="section-title"><h2>Related routes</h2></div>\n'
            f'      <div style="text-align:center;line-height:2.4">{pills}</div>\n'
            '    </div>\n'
            '  </section>\n')

# 旧 Related routes section 的删除正则(整段, 含 section 开标签到 </section>)
OLD_RR = re.compile(
    r'<section class="section" style="background:#F5F7FA">\s*'
    r'<div class="container">\s*'
    r'<div class="section-title"><h2>Related routes</h2></div>.*?</section>',
    re.S)

def process(f):
    s = open(f, encoding='utf-8').read()
    if MARK in s:
        return "skip(已处理)"
    # 删除旧 RR section(若有)
    s2, n_del = OLD_RR.subn('', s)
    # 在 </footer> 前插入新 RR section
    if '</footer>' not in s2:
        return "ERROR(无</footer>)"
    idx = s2.rfind('</footer>')
    new_rr = build_rr_section(os.path.basename(f)[:-5])
    s3 = s2[:idx] + new_rr + s2[idx:]
    if not DRY:
        open(f, 'w', encoding='utf-8').write(s3)
    return f"插入(删旧{n_del}段)"

if __name__ == '__main__':
    n_ins = 0
    for slug, _ in CLUSTER:
        f = os.path.join(BASE, slug + '.html')
        if not os.path.exists(f):
            print(f"  MISSING {slug}")
            continue
        r = process(f)
        if r.startswith('插入'):
            n_ins += 1
        print(f"  {slug}: {r}")
    print(f"\n{'[DRY-RUN]' if DRY else '[已执行]'} 共 {n_ins} 个页面插入/更新内链矩阵")
