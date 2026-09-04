#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 en 站 meta description 结尾的省略号截断 bug（886 处）。
模板生成时把品牌 CTA 后缀截断成 "…"，导致 SERP 显示字面省略号，伤 CTR。

规则（幂等，精确匹配 meta description 的 content 值结尾 "…"）：
  - 省略号前是字母/数字（词被截断） -> 补句点 "."
  - 省略号前是逗号/分号/冒号/破折号等 -> 直接删省略号
  - 省略号前已是句点/感叹号/问号 -> 直接删省略号

用法：
  python3 fix-desc-ellipsis.py          # dry-run 预览
  python3 fix-desc-ellipsis.py --run    # 实际执行
"""
import re, glob, sys

DRY = "--run" not in sys.argv

META_DESC = re.compile(r'<meta name="description" content="([^"]*)"')

def fix_desc(desc):
    """返回 (新desc, 是否改动)"""
    if not desc.endswith("…"):
        return desc, False
    pre = desc[:-1].rstrip()  # 去掉省略号 + 尾部空格
    if not pre:
        return desc, False
    last = pre[-1]
    if last in ",;:—–-":
        new = pre  # 标点结尾，直接删省略号
    elif last in ".!?":
        new = pre  # 已有句点，直接删省略号
    else:
        new = pre + "."  # 词被截断，补句点
    return new, True

fixed_files = 0
fixed_total = 0
samples = []

for f in glob.glob("en/**/*.html", recursive=True):
    s = open(f, encoding="utf-8").read()
    m = META_DESC.search(s)
    if not m:
        continue
    desc = m.group(1)
    new_desc, changed = fix_desc(desc)
    if not changed:
        continue
    # 精确替换：只替换 content 值里的那个省略号
    new_full = m.group(0).replace(f'content="{desc}"', f'content="{new_desc}"')
    if len(samples) < 8:
        samples.append((f, desc[-45:], new_desc[-45:]))
    if not DRY:
        s = s.replace(m.group(0), new_full)
        open(f, "w", encoding="utf-8").write(s)
    fixed_files += 1
    fixed_total += 1

print(f"{'[DRY-RUN]' if DRY else '[已执行]'} 修复 {fixed_files} 个文件 / {fixed_total} 处省略号")
print("\n=== 样例（前 8）===")
for f, old, new in samples:
    print(f"  {f.split('/')[-1]}")
    print(f"    旧: ...{old}")
    print(f"    新: ...{new}")

if DRY:
    print("\n确认无误后执行: python3 fix-desc-ellipsis.py --run")
