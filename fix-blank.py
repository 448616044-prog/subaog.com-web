#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final cleanup: remove blank double-period + broken URL corruption from sea-freight removal."""
import subprocess

base = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"
files = subprocess.check_output(
    ["find", "en/city", "en/blog", "en/japan-to-china", "en/seasia-to-china", "en/report",
     "-name", "*.html"], cwd=base
).decode().splitlines()

# Specific fixes that must run BEFORE the global "door-to-door. ." replace
SPECIFIC = {
    "en/seasia-to-china/singapore/moving/index.html": [
        ("door-to-door. .com/en/seasia-to-china/singapore/moving/",
         "door-to-door in 10-15 working days, tax-inclusive."),
    ],
    "en/seasia-to-china/malaysia/moving/index.html": [
        ("door-to-door. .com/en/seasia-to-china/malaysia/moving/",
         "door-to-door in 10-15 working days, tax-inclusive."),
    ],
    "en/report/usa-china-shipping-cost-report-2026.html": [
        ("to , 20x cheaper.", "to our consolidated air freight line, 20x cheaper."),
    ],
}

GLOBAL = [
    ("door-to-door. .", "door-to-door."),
]

changed = 0
for rel in files:
    p = base + "/" + rel
    try:
        with open(p, "r", encoding="utf-8") as f:
            t = f.read()
    except Exception:
        continue
    orig = t
    for a, b in SPECIFIC.get(rel, []):
        t = t.replace(a, b)
    for a, b in GLOBAL:
        t = t.replace(a, b)
    if t != orig:
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
        changed += 1

print("DONE 修改文件数:", changed, "共扫描:", len(files))
