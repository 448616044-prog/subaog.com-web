#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
18 个海运主题页: 只统一价格(美元->人民币, 空运旧价->新价), 保留海运概念, 删海运价格数字
"""
import re
from pathlib import Path

ROOT = Path(".")

PAGES = [
    "zh-cn/blog/graduation-luggage-shipping.html",
    "zh-cn/blog/how-to-choose-international-shipping-method.html",
    "zh-cn/blog/moving-season-sea-freight.html",
    "zh-cn/blog/student-luggage-shipping-guide.html",
    "zh-cn/blog/usa-moving-to-china-guide.html",
    "zh-cn/blog/usa-to-china-sea-freight.html",
    "zh-cn/blog/usa-to-china-shipping-time.html",
    "zh-cn/tools/transit-time.html",
    "zh-cn/usa-moving-to-china/index.html",
    "en/blog/graduation-luggage-shipping.html",
    "en/blog/how-to-choose-international-shipping-method.html",
    "en/blog/moving-season-sea-freight.html",
    "en/blog/student-luggage-shipping-guide.html",
    "en/blog/usa-moving-to-china-guide.html",
    "en/blog/usa-to-china-sea-freight.html",
    "en/blog/usa-to-china-shipping-time.html",
    "en/tools/transit-time.html",
    "en/usa-moving-to-china/index.html",
]

# 空运旧价 -> 新价 (zh-cn)
ZH_AIR = [("¥80", "¥100"), ("¥75", "¥90"), ("¥70", "¥80"), ("¥65", "¥70")]

# 美元 -> 人民币 (en)
USD = [
    ("$10.50", "¥90"), ("$10.5", "¥90"),
    ("$10.40", "¥90"), ("$10.4", "¥90"),
    ("$9.70", "¥80"), ("$9.7", "¥80"),
    ("$9.50", "¥80"), ("$9.5", "¥80"),
    ("$11.00", "¥100"), ("$11", "¥100"),
    ("$9.00", "¥70"), ("$9", "¥70"),
    ("$15.00", "¥100"), ("$15", "¥100"),
]

# 海运价格数字删除 (保留"海运/sea freight"概念)
ZH_SEA_PRICE = [
    (r"海运约\s*[¥$][0-9./\-]+", "海运"),
    (r"海运专线约\s*[¥$][0-9./\-]+（[^）]*）", "海运专线"),
    (r"海运\s*[¥$][0-9./\-]+/kg", "海运"),
    (r"海运[¥$][0-9./\-]+", "海运"),
]
EN_SEA_PRICE = [
    (r"[Ss]ea freight from about \$[0-9./\-]+(?:/kg)?", "Sea freight"),
    (r"[Ss]ea freight from \$[0-9./\-]+(?:/kg)?", "Sea freight"),
    (r"[Ss]ea freight \$[0-9./\-]+(?:/kg)?", "Sea freight"),
    (r"[Ss]ea freight from \$[0-9.]+–\$[0-9.]+/kg[^)]*\)", "Sea freight"),
]


def swap(t, pairs):
    for i, (o, n) in enumerate(pairs):
        t = t.replace(o, f"__T{i}__")
    for i, (o, n) in enumerate(pairs):
        t = t.replace(f"__T{i}__", n)
    return t


def main():
    fixed = 0
    for rel in PAGES:
        p = ROOT / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        orig = t
        if rel.startswith("zh-cn/"):
            t = swap(t, ZH_AIR)
            for pat, rep in ZH_SEA_PRICE:
                t = re.sub(pat, rep, t)
        else:
            t = swap(t, USD)
            for pat, rep in EN_SEA_PRICE:
                t = re.sub(pat, rep, t)
        if t != orig:
            p.write_text(t, encoding="utf-8")
            fixed += 1
            print(f"✅ {rel}")
    print(f"\n修复 {fixed} 页")


if __name__ == "__main__":
    main()
