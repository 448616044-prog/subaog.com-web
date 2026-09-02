#!/usr/bin/env python3
"""
修复 en 站 title 品牌名被省略号"…"截断的系统性 bug（334 处）。
品牌名统一补全为 "Subao Global"（与主流 581 处正常 title 一致）。
只处理 <title> 标签内的内容，不动正文。
幂等：已补全的不会重复处理。
"""
import re, glob, sys

DRY = "--run" not in sys.argv

def fix_title(core):
    fixed = core
    # 1. "| Subao…" → "| Subao Global"
    fixed = re.sub(r'\|\s*Subao…$', '| Subao Global', fixed)
    # 2. "|…" → "| Subao Global"
    fixed = re.sub(r'\|\s*…$', '| Subao Global', fixed)
    # 3. 无竖线的 "正文…" → "正文 | Subao Global"
    fixed = re.sub(r'…$', ' | Subao Global', fixed)
    return fixed

total_files = 0
total_repl = 0
for f in glob.glob('en/**/*.html', recursive=True):
    s = open(f, encoding='utf-8').read()
    m = re.search(r'(<title>)(.*?)(</title>)', s, re.S)
    if not m:
        continue
    old_title = m.group(2)
    if '…' not in old_title:
        continue
    new_title = fix_title(old_title)
    if new_title == old_title:
        print(f"  ⚠️ 未变化: {f}: {old_title.strip()}")
        continue
    total_files += 1
    total_repl += 1
    if not DRY:
        s = s[:m.start(2)] + new_title + s[m.end(2):]
        open(f, 'w', encoding='utf-8').write(s)
    if DRY and total_files <= 15:
        print(f"  [{'DRY' if DRY else '✅'}] {f}")
        print(f"       {old_title.strip()}  →  {new_title.strip()}")

print(f"\n{'DRY-RUN 预览' if DRY else '执行完成'}: {total_files} 个文件 title 补全品牌名")
if DRY:
    print("加 --run 实际执行")
