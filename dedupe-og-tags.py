#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""去重 OG 标签：每个 og 字段保留第一次出现，删除后续重复行"""
import re, glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(ROOT + '/zh-cn/**/*.html', recursive=True)) + \
        sorted(glob.glob(ROOT + '/en/**/*.html', recursive=True))

OG_RE = re.compile(r'^\s*<meta property="og:([a-z:]+)" content="[^"]*">\s*$', re.M)

fixed_files = 0
removed = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    seen = {}
    lines = content.split('\n')
    out = []
    changed = False
    for line in lines:
        m = OG_RE.match(line)
        if m:
            key = m.group(1)
            if key in seen:
                removed += 1
                changed = True
                continue  # 删除重复行
            seen[key] = True
        out.append(line)
    if changed:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(out))
        fixed_files += 1

print(f'去重文件数: {fixed_files}, 删除重复 OG 标签: {removed}')
