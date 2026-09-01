#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 en/city 美国城市页价格红线违规：档1 ¥100/kg 被错写成档2 ¥90/kg"""
import os, io, glob, sys

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com/en/city"
DRY = "--run" not in sys.argv

RULES = [
    # (old, new) —— 全部美国城市页，档1 起价应为 ¥100/kg
    ("from ¥90/kg", "from ¥100/kg"),                                    # subtitle + meta + og (1080)
    ('class="big">¥90<', 'class="big">¥100<'),                          # info-card (360)
    ("¥90/kg for shipments over 20kg", "¥100/kg for shipments over 20kg"),  # FAQ (720)
    ("¥90-100/kg all-in", "¥100/kg all-in"),                            # FAQ 区间价 (2)
    ("Small parcels cost ¥100\u201330", "Small parcels cost $10\u201330"),  # 乱码 ¥100–30 → $10–30 (360)
]

files = sorted(glob.glob(os.path.join(BASE, "*.html")))
total_files = 0
total_repl = 0
unmatched = {}
for f in files:
    rel = os.path.relpath(f, os.path.dirname(BASE) + "/..")
    c = io.open(f, encoding="utf-8").read()
    n = 0
    for old, new in RULES:
        k = c.count(old)
        if k:
            c = c.replace(old, new)
            n += k
        else:
            unmatched.setdefault(old, 0)
            unmatched[old] += 0
    if n:
        total_files += 1
        total_repl += n
        if not DRY:
            io.open(f, "w", encoding="utf-8").write(c)
        if DRY:
            print("  [dry] " + rel + " x" + str(n))
        else:
            print("  [OK] " + rel + " x" + str(n))

print("\n" + ("DRY-RUN" if DRY else "DONE") + ": " + str(total_files) +
      " files, " + str(total_repl) + " replacements")

# 报告每个规则命中的文件数（DRY 时）
if DRY:
    for old, new in RULES:
        cnt = sum(1 for f in files if old in io.open(f, encoding="utf-8").read())
        print("  规则 [" + old + "] → [" + new + "] 命中 " + str(cnt) + " 文件")
