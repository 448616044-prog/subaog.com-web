#!/usr/bin/env python3
"""
subaog.com 欧洲 luxury-goods 改写：去「代购/全新」话术，改「二手/个人自用」导向
禁运红线：「原封未拆/带标签新品」属特殊状态禁运，需按实价申报
改写方向：「Used luxury / pre-owned / personal effects」

执行范围：欧洲 8 城市 × en/zh-cn = 16 页
"""
import os
import re

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# 改写规则
# 原则：把所有 "Luxury Goods" 等表述改成 "Used Luxury Goods" 或 "Pre-Owned Luxury Goods"
# 严禁触发「全新/代购/未拆封/带标签/购买」等话术
RULES = [
    # title / h1 / og:title
    (r'Ship Luxury Goods from ([^<|]+)', r'Ship Used Luxury Goods from \1'),
    (r'<title>Ship Used Luxury Goods from ([^<]+)</title>',
     r'<title>Ship Pre-Owned Luxury Goods from \1 (Personal Use, 2026)</title>'),
    (r'<h1>Ship Used Luxury Goods from ([^<]+)</h1>',
     r'<h1>Ship Pre-Owned Luxury Goods from \1 (Personal Use)</h1>'),

    # 触发「全新/带标签/购买」的话术：明确删除或改写
    # 由于原文没有直接写「全新/未拆封」，主要是 "declare value and insure"
    # 这个保留，因为是合规要求

    # FAQ 问题改写
    (r'"name":"Can I ship luxury goods from ([^"]+)"',
     r'"name":"Can I ship used/pre-owned luxury goods from \1"'),
    (r'Can I ship luxury goods from ([^?]+)\?',
     r'Can I ship used/pre-owned luxury goods from \1?'),

    # 答案加"used/pre-owned"前缀
    (r'"Yes — luxury bags, watches and accessories \(LV, Chanel\) ship by air; declare value and insure\."',
     r'"Yes — used/pre-owned personal-use luxury bags, watches and accessories (LV, Chanel) ship by air; declare value and insure. New-with-tag items require declared invoice and may be restricted."'),

    # 可见 FAQ 答案
    (r'>Yes — luxury bags, watches and accessories \(LV, Chanel\) ship by air; declare value and insure\.<',
     r'>Yes — used/pre-owned personal-use luxury bags, watches and accessories (LV, Chanel) ship by air; declare value and insure. New-with-tag items require declared invoice and may be restricted.<'),

    # verdict section
    (r'<h2[^>]*>Verdict: Allowed</h2>',
     r'<h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">Verdict: Allowed for used/personal-use items</h2>'),
    (r'Verdict: Allowed</h2>',
     r'Verdict: Allowed for used/personal-use items</h2>'),
    (r'<p style="color:var\(--text-secondary\);line-height:1\.9">Allowed\. Luxury bags, watches and accessories \(LV, Chanel, Hermès\) — declare value and insure high-value items\.</p>',
     r'<p style="color:var(--text-secondary);line-height:1.9">Used/pre-owned personal-use items allowed. Luxury bags, watches and accessories (LV, Chanel, Hermès) — declare value and insure high-value items. Note: brand-new with tags (unopened retail stock) is treated as restricted status — must declare true invoice value.</p>'),

    # packing tips
    (r'Keep receipts and certificates, cushion carefully, and insure high-value items\.',
     r'Keep receipts and certificates, cushion carefully, and insure high-value items. For used/pre-owned pieces, original purchase proof is helpful for customs.'),

    # CTA
    (r'Get a quote for Luxury Goods from ([^<]+)',
     r'Get a quote for used/pre-owned luxury items from \1'),

    # meta description 加 "pre-owned"
    (r'content="Ship Luxury Goods from ([^"]+)"',
     r'content="Ship pre-owned / used luxury goods from \1"'),

    # meta description: Allowed. Luxury bags → Allowed for used/personal items. Pre-owned luxury bags
    (r'content="Ship Used Luxury Goods from ([^,]+), Europe to China: Allowed\. Luxury bags',
     r'content="Ship pre-owned / used luxury goods from \1, Europe to China: allowed for personal-use items. Pre-owned luxury bags'),

    # og:title 同步
    (r'property="og:title" content="Ship Luxury Goods from ([^"]+)"',
     r'property="og:title" content="Ship pre-owned / used luxury goods from \1"'),
]

# 城市列表（en + zh-cn）
EU_CITIES = ["amsterdam", "berlin", "brussels", "london", "madrid", "milan", "paris", "rome"]


def fix_one(path):
    with open(path, encoding='utf-8') as f:
        original = f.read()

    new = original
    diffs = []
    for pattern, replacement in RULES:
        if re.search(pattern, new):
            cnt = len(re.findall(pattern, new))
            new = re.sub(pattern, replacement, new)
            diffs.append(f"  {pattern[:60]}: {cnt} 次")

    if new != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
    return new != original, diffs


def main():
    changed = 0
    for lang in ["en", "zh-cn"]:
        for city in EU_CITIES:
            p = f"{BASE}/{lang}/europe-to-china/{city}/luxury-goods/index.html"
            if not os.path.isfile(p):
                continue
            was, diffs = fix_one(p)
            if was:
                changed += 1
                print(f"[{lang}/europe-to-china/{city}/luxury-goods]")
                for d in diffs:
                    print(d)

    print(f"\n=== 完成 ===")
    print(f"改写文件数: {changed}")


if __name__ == '__main__':
    main()