#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final pass: unify remaining transit-time violations to 10-15 working days.
Only touches files that actually contain a violation (idempotent)."""
import subprocess, sys

base = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# 1) all zh-cn usa-to-china city×item pages
files = subprocess.check_output(
    ["find", "zh-cn/usa-to-china", "-name", "index.html"], cwd=base
).decode("utf-8").splitlines()

# 2) the two remaining en blog files with "7-10 business days air"
files += [
    "en/blog/us-package-forwarding.html",
    "en/blog/amazon-us-ship-to-china.html",
]

# Replacement rules (exact, safe)
zh_pairs = [
    (">7-10<", ">10-15<"),
    (">7\u201310<", ">10-15<"),  # en-dash 7–10
    (">7-12<", ">10-15<"),
    (">7\u201312<", ">10-15<"),
]
en_pairs = [
    ("7-10 business days air", "10-15 working days air"),
]

changed = 0
for rel in files:
    p = base + "/" + rel
    try:
        with open(p, "r", encoding="utf-8") as f:
            t = f.read()
    except Exception as e:
        print("SKIP", rel, e, file=sys.stderr)
        continue
    orig = t
    if rel.startswith("en/"):
        for a, b in en_pairs:
            t = t.replace(a, b)
    else:
        for a, b in zh_pairs:
            t = t.replace(a, b)
    if t != orig:
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
        changed += 1

print("DONE 修改文件数:", changed, "共扫描:", len(files))
