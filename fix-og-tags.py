#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补齐 Open Graph 标签：只补缺失字段，从页面已有 title/description/canonical 提取。
og:type: blog 用 article，其余 website；og:locale: zh-cn 用 zh_CN，en 用 en_US。
用法：--dry-run 只统计
"""
import re, sys, glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = '--dry-run' in sys.argv

def main():
    files = sorted(glob.glob(ROOT + '/zh-cn/**/*.html', recursive=True)) + \
            sorted(glob.glob(ROOT + '/en/**/*.html', recursive=True))
    files_touched = 0
    tags_added = 0
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()

        title = re.search(r'<title>([^<]*)</title>', content)
        desc = re.search(r'<meta name="description" content="([^"]*)"', content)
        canon = re.search(r'<link rel="canonical" href="([^"]*)"', content)

        locale = 'zh_CN' if '/zh-cn/' in f else 'en_US'
        ogtype = 'article' if '/blog/' in f else 'website'

        missing = []
        if 'property="og:title"' not in content and title:
            missing.append(f'<meta property="og:title" content="{title.group(1)}">')
        if 'property="og:description"' not in content and desc:
            missing.append(f'<meta property="og:description" content="{desc.group(1)}">')
        if 'property="og:url"' not in content and canon:
            missing.append(f'<meta property="og:url" content="{canon.group(1)}">')
        if 'property="og:image"' not in content:
            missing.append('<meta property="og:image" content="https://subaog.com/assets/images/og-image.jpg">')
        if 'property="og:type"' not in content:
            missing.append(f'<meta property="og:type" content="{ogtype}">')
        if 'property="og:locale"' not in content:
            missing.append(f'<meta property="og:locale" content="{locale}">')

        if not missing:
            continue

        files_touched += 1
        tags_added += len(missing)

        if DRY:
            continue

        block = '\n  ' + '\n  '.join(missing)
        # 插入到 canonical 之后；若无 canonical，插到 </title> 之后
        if canon:
            anchor = canon.group(0)
            new_content = content.replace(anchor, anchor + block, 1)
        elif title:
            anchor = title.group(0)
            new_content = content.replace(anchor, anchor + block, 1)
        else:
            continue
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new_content)

    print(f'{"[DRY-RUN] " if DRY else ""}涉及文件: {files_touched}, 新增 OG 标签: {tags_added}')

if __name__ == '__main__':
    main()
