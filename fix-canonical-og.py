#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全站修复 canonical 缺闭合 > 与 og:type 多 > 的模板 bug"""
import os, re, io, glob, sys

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"
DRY = "--run" not in sys.argv

files = glob.glob(os.path.join(BASE, "**", "*.html"), recursive=True)
pat_canon = re.compile(r'^(\s*<link rel="canonical" href="[^"]+")$')  # 行尾缺 >
pat_og = re.compile(r'(<meta property="og:type" content="(?:article|website)")>>')  # og:type 多 >

fixed_files = 0
fixed_canon = 0
fixed_og = 0
for f in files:
    try:
        content = io.open(f, encoding="utf-8").read()
    except Exception:
        continue
    lines = content.split("\n")
    new = []
    n = 0
    for ln in lines:
        if pat_canon.match(ln):
            ln = ln + ">"
            fixed_canon += 1
            n += 1
        m2 = pat_og.search(ln)
        if m2:
            ln = ln.replace(m2.group(1) + ">>", m2.group(1) + ">")
            fixed_og += 1
            n += 1
        new.append(ln)
    if n:
        fixed_files += 1
        rel = os.path.relpath(f, BASE)
        if DRY:
            print("  [dry] " + rel + " x" + str(n))
        else:
            io.open(f, "w", encoding="utf-8").write("\n".join(new))
            print("  [OK] " + rel + " x" + str(n))

print("\n" + ("DRY-RUN" if DRY else "DONE") + ": " + str(fixed_files) +
      " files, canonical补> " + str(fixed_canon) + ", og:type去> " + str(fixed_og))
