#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充清洗：处理 JSON-LD / 任意上下文中 subaog.com 站内 .html URL（非 href）
规则：匹配 (https://subaog.com)?/(zh-cn|en)/PATH.html 的 .html 后缀并去掉
用法：--dry-run 只统计
"""
import re, sys, glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))

# 通用：任意引号上下文里的 subaog.com 站内 .html URL
# 匹配 /zh-cn/... 或 /en/... 或 https://subaog.com/... 且以 .html 结尾
PATTERN = re.compile(r'((?:https://subaog\.com)?/(?:zh-cn|en)/[^"\']*?)\.html')

DRY = '--dry-run' in sys.argv

def main():
    files = sorted(glob.glob(ROOT + '/zh-cn/**/*.html', recursive=True)) + \
            sorted(glob.glob(ROOT + '/en/**/*.html', recursive=True))
    total_files = 0
    total_repl = 0
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        new_content, n = PATTERN.subn(r'\1', content)
        if n > 0:
            total_files += 1
            total_repl += n
            if not DRY:
                with open(f, 'w', encoding='utf-8') as fh:
                    fh.write(new_content)
    print(f'{"[DRY-RUN] " if DRY else ""}涉及文件: {total_files}, 替换处数: {total_repl}')

if __name__ == '__main__':
    main()
