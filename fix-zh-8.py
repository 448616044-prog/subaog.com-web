#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Targeted fix for remaining 8 zh-cn files (price + sea-blank corruption)."""
base = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

files = [
    "zh-cn/usa-to-china/index.html",
    "zh-cn/canada-to-china/index.html",
    "zh-cn/australia-to-china/index.html",
    "zh-cn/europe-to-china/index.html",
    "zh-cn/japan-to-china/index.html",
    "zh-cn/korea-to-china/index.html",
    "zh-cn/seasia-to-china/singapore/index.html",
    "zh-cn/seasia-to-china/malaysia/index.html",
]

# applied to all 8
GLOBAL = [
    ("不急用的选。急用的选空运：", "海运已下架，统一走空运专线。空运："),
]

# applied only to usa-to-china (档1 US tier)
SPECIFIC = {
    "zh-cn/usa-to-china/index.html": [
        ("美国寄中国：1-20kg ¥100/kg、21-99kg ¥80/kg、100kg+ ¥90/kg（空运双清包税门到门）",
         "美国寄中国：20-99kg ¥100/kg、100kg+ ¥90/kg（空运双清包税门到门）"),
        ("空运：¥80/kg起。华人集运专线比美国邮政", "空运：¥100/kg起。华人集运专线比美国邮政"),
        ("空运干线10-15 个工作日+清关1-2天", "空运干线3-5 天+清关1-2天"),
    ],
}

for rel in files:
    p = base + "/" + rel
    with open(p, "r", encoding="utf-8") as f:
        t = f.read()
    orig = t
    for a, b in GLOBAL:
        t = t.replace(a, b)
    for a, b in SPECIFIC.get(rel, []):
        if t.count(a) == 0:
            print(f"WARN 未命中 {rel}: {a[:40]}")
        t = t.replace(a, b)
    if t != orig:
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
        print("OK", rel)
    else:
        print("NOCHANGE", rel)
