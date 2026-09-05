#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix remaining transit-time / sea-freight residual corruption in 2 files."""
base = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

edits = [
    # 1) en/tools/transit-time.html — meta descriptions still say 7-15
    ("en/tools/transit-time.html", [
        ("Air freight 7-15 working days", "Air freight 10-15 working days"),
    ]),
    # 2) zh-cn/blog/usa-to-china-shipping-time.html — duplicate sea question + corrupted "空运省 40%"
    ("zh-cn/blog/usa-to-china-shipping-time.html", [
        ('{"@type": "Question", "name": "美国寄中国空运要多久？", "acceptedAnswer": {"@type": "Answer", "text": "。美西 25 天左右，美东 30-35 天。"}}',
         '{"@type": "Question", "name": "美国寄中国海运要多久？", "acceptedAnswer": {"@type": "Answer", "text": "海运已下架，现统一空运专线 10-15 个工作日。"}}'),
        ('<div class="faq-item"><button class="faq-q">美国寄中国空运要多久？<span>▼</span></button><div class="faq-a">。美西 25 天左右，美东 30-35 天。</div></div>',
         '<div class="faq-item"><button class="faq-q">美国寄中国海运要多久？<span>▼</span></button><div class="faq-a">海运已下架，现统一空运专线 10-15 个工作日。</div></div>'),
        ('"text": "急（<2 周）→ 空运；不急/大件 → 空运省 40%。"',
         '"text": "急（<2 周）→ 空运；不急/大件 → 空运专线（10-15 个工作日，双清包税）。"'),
        ('<div class="faq-a">急（<2 周）→ 空运；不急/大件 → 空运省 40%。</div>',
         '<div class="faq-a">急（<2 周）→ 空运；不急/大件 → 空运专线（10-15 个工作日，双清包税）。</div>'),
    ]),
]

for rel, pairs in edits:
    p = base + "/" + rel
    with open(p, "r", encoding="utf-8") as f:
        t = f.read()
    for a, b in pairs:
        n = t.count(a)
        if n == 0:
            print(f"WARN 未命中: {rel} :: {a[:50]}...")
        t = t.replace(a, b)
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)
    print(f"OK {rel} ({len(pairs)} 组替换)")
