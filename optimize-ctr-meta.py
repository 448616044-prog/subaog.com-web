#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
subaog.com — B 组 CTR 急救 meta 微调 (保守, 不碰 title 保护排名)
对齐 GSC 8-26: B 组词排名 ≤11 但 0 点击 -> 在 meta description 加「免费估价」强意图钩子
规则:
- 仅改 <meta name="description"> 与 <meta property="og:description"> 的 content
- 幂等: 已含 free quote / 免费估价 则跳过
- 在品牌尾「 | Subao...」前插入钩子, 避免重复品牌
"""
import re
from pathlib import Path

ROOT = Path(".")
# B 组最高价值页 (en + zh-cn), GSC pos<=11 且 0 点击
TARGETS = [
    "en/blog/cheapest-way-ship-to-china.html",
    "zh-cn/blog/cheapest-way-ship-to-china.html",
    "en/blog/amazon-shopping-to-china.html",
    "zh-cn/blog/amazon-shopping-to-china.html",
    "en/blog/usps-to-china-complete-guide.html",
    "zh-cn/blog/usps-to-china-complete-guide.html",
    "en/japan-to-china/index.html",
    "zh-cn/japan-to-china/index.html",
    "en/blog/usps-vs-ups-china.html",
    "zh-cn/blog/usps-vs-ups-china.html",
    "en/blog/ebay-ship-to-china.html",
    "zh-cn/blog/ebay-ship-to-china.html",
    "en/blog/dhl-vs-fedex-vs-ups-china.html",
    "zh-cn/blog/dhl-vs-fedex-vs-ups-china.html",
    "en/city/san-diego-to-hangzhou.html",
    "zh-cn/city/san-diego-to-hangzhou.html",
]


def add_hook(c: str, lang: str) -> str:
    if lang == "en":
        if re.search(r"free quote", c, re.I):
            return c
        hook = " — Get a free instant quote"
    else:
        if "免费估价" in c:
            return c
        hook = "，免费估价"
    # 统一句末加钩子 (品牌可能在句中, 不往前插)
    return c.rstrip().rstrip(".。") + hook + "."


def main():
    fixed = 0
    for rel in TARGETS:
        f = ROOT / rel
        if not f.exists():
            print(f"  ⏭️  跳过(不存在): {rel}")
            continue
        lang = "en" if rel.startswith("en/") else "zh-cn"
        t = f.read_text(encoding="utf-8", errors="ignore")
        new_t = t
        for tag in ['name="description"', 'property="og:description"']:
            pat = re.compile(
                r'(<meta[^>]*?{tag}[^>]*?content=")([^"]*)(")'.format(tag=tag), re.S
            )

            def repl(m, _lang=lang):
                before, content, after = m.group(1), m.group(2), m.group(3)
                cleaned = add_hook(content, _lang)
                if cleaned != content:
                    return before + cleaned + after
                return m.group(0)

            new_t = pat.sub(repl, new_t)
        if new_t != t:
            f.write_text(new_t, encoding="utf-8")
            fixed += 1
            m = re.search(r'name="description" content="([^"]*)"', new_t)
            print(f"  ✅ {rel} -> {m.group(1)[:85] if m else ''}")
        else:
            print(f"  • 已含钩子, 跳过: {rel}")
    print(f"\n修复 {fixed} 页")


if __name__ == "__main__":
    main()
