#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 subaog.com 站内死链：
提取所有 href 指向的站内 clean URL，检查对应 .html 文件是否存在。
输出死链清单（目标文件缺失）。
"""
import re, sys, glob, os, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))

# 提取所有 href 里的站内路径（/zh-cn/... 或 /en/...，含完整 URL 和绝对路径）
HREF = re.compile(r'href="((?:https://subaog\.com)?/(?:zh-cn|en)/[^"#?]*)"')

def url_to_path(url_path):
    """clean URL -> 对应文件系统路径"""
    # 去掉 https://subaog.com 前缀
    p = url_path
    if p.startswith('https://subaog.com'):
        p = p[len('https://subaog.com'):]
    # 去掉尾部斜杠
    if p.endswith('/'):
        p = p[:-1]
    if p == '':
        return None
    # clean URL -> .html 文件
    # 目录页：/zh-cn/australia-to-china/ -> /zh-cn/australia-to-china/index.html
    # 但这里已经去了尾斜杠，需要判断是目录还是文件
    # 先尝试直接 .html
    file_candidate = ROOT + p + '.html'
    if os.path.isfile(file_candidate):
        return file_candidate
    # 尝试目录 index.html
    dir_candidate = ROOT + p + '/index.html'
    if os.path.isfile(dir_candidate):
        return dir_candidate
    return None

def main():
    files = sorted(glob.glob(ROOT + '/zh-cn/**/*.html', recursive=True)) + \
            sorted(glob.glob(ROOT + '/en/**/*.html', recursive=True))
    all_links = set()
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        for m in HREF.finditer(content):
            all_links.add(m.group(1))

    # 检查每个唯一链接
    broken = []
    for link in sorted(all_links):
        target = url_to_path(link)
        if target is None:
            broken.append(link)

    print(f'唯一站内链接总数: {len(all_links)}')
    print(f'死链数（目标文件缺失）: {len(broken)}')
    if broken:
        print('--- 死链清单 ---')
        for b in broken:
            print(f'  {b}')

    # 额外：统计链接对应的目标文件是否在 sitemap 中（clean URL 合法性）
    return

if __name__ == '__main__':
    main()
