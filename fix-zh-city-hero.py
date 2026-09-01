#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 zh-cn/city 360 页 hero 结构 bug：section/subtitle 未闭合 + content div 缺失"""
import os, io, glob, sys

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com/zh-cn/city"
DRY = "--run" not in sys.argv

# 精确模式（360 页一致）
OLD = "空运10-15 个工作日 ·。留学生行李、代购包裹、搬家货运均可。</div>"
NEW = "空运10-15 个工作日 · 留学生行李、代购包裹、搬家货运均可</p></div></section><div class=\"content\">"

files = sorted(glob.glob(os.path.join(BASE, "*.html")))
n_files = 0
n_repl = 0
miss = 0
for f in files:
    c = io.open(f, encoding="utf-8").read()
    k = c.count(OLD)
    if k == 0:
        miss += 1
        print("  [WARN] 未匹配: " + os.path.basename(f))
        continue
    c = c.replace(OLD, NEW)
    n_files += 1
    n_repl += k
    if not DRY:
        io.open(f, "w", encoding="utf-8").write(c)

print("\n" + ("DRY-RUN" if DRY else "DONE") + ": " + str(n_files) +
      " files, " + str(n_repl) + " replacements" + (", 未匹配 " + str(miss) if miss else ""))
