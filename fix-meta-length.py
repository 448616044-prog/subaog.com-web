#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复昨晚 CTR 钩子引入的 meta 超长回归(双重钩子) -> 去重 + 短钩子 + 截断 <=158"""
import re
from pathlib import Path

ROOT = Path(".")
TARGETS = [
    "en/blog/amazon-shopping-to-china.html",
    "en/blog/cheapest-way-ship-to-china.html",
    "en/blog/dhl-vs-fedex-vs-ups-china.html",
    "en/blog/ebay-ship-to-china.html",
    "en/blog/usps-to-china-complete-guide.html",
    "en/blog/usps-vs-ups-china.html",
    "en/japan-to-china/index.html",
    "en/city/san-diego-to-hangzhou.html",
]


def fix(c: str) -> str:
    # 去掉所有钩子(含站点自带 Get a free quote 与昨晚加的 instant quote)
    c = re.sub(r"\s*[—–-]?\s*Get a free (instant )?quote", "", c)
    c = re.sub(r"\s{2,}", " ", c).strip().rstrip(". ")
    # 截断到 145 留短钩子空间
    if len(c) > 145:
        cut = c[:145]
        idx = max(cut.rfind(". "), cut.rfind(", "), cut.rfind(" "))
        if idx > 80:
            cut = cut[:idx]
        c = cut.rstrip("., ")
    return c + " — Free quote"


def main():
    for rel in TARGETS:
        f = ROOT / rel
        t = f.read_text(encoding="utf-8", errors="ignore")
        for tag in ['name="description"', 'property="og:description"']:
            pat = re.compile(
                r'(<meta[^>]*?{tag}[^>]*?content=")([^"]*)(")'.format(tag=tag), re.S
            )
            t = pat.sub(lambda m: m.group(1) + fix(m.group(2)) + m.group(3), t)
        f.write_text(t, encoding="utf-8")
        m = re.search(r'name="description" content="([^"]*)"', t)
        c = m.group(1) if m else ""
        print(f"✅ {rel} ({len(c)} 字符) -> {c}")


if __name__ == "__main__":
    main()
