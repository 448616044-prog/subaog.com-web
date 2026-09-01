#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清洗 subaog.com 站内 .html 内链 -> clean URL
规则：href="(https://subaog.com)?/(zh-cn|en)/PATH.html" -> 去掉 .html
只处理站内路径，绝不碰外链 / canonical / hreflang / og:url
用法：python3 cleanup-internal-links.py --dry-run   # 只统计不改
      python3 cleanup-internal-links.py             # 实际替换
"""
import re, sys, glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))

# 匹配 href="..." 中站内 .html 结尾的链接（仅 subaog.com 站内 /zh-cn/ 或 /en/）
PATTERN = re.compile(r'href="((?:https://subaog\.com)?/(?:zh-cn|en)/[^"]*?)\.html"')

DRY = '--dry-run' in sys.argv

def main():
    files = sorted(glob.glob(ROOT + '/zh-cn/**/*.html', recursive=True)) + \
            sorted(glob.glob(ROOT + '/en/**/*.html', recursive=True))
    total_files = 0
    total_repl = 0
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        new_content, n = PATTERN.subn(r'href="\1"', content)
        if n > 0:
            total_files += 1
            total_repl += n
            if not DRY:
                with open(f, 'w', encoding='utf-8') as fh:
                    fh.write(new_content)
    print(f'{"[DRY-RUN] " if DRY else ""}涉及文件: {total_files} 个, 替换 href 处数: {total_repl}')
    if DRY:
        # 打印几个替换样本
        print('--- 样本预览 ---')
        cnt = 0
        for f in files:
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()
            for m in PATTERN.finditer(content):
                print(f'  {os.path.basename(f)}: {m.group(0)}  ->  href="{m.group(1)}"')
                cnt += 1
                if cnt >= 8:
                    return
                break

if __name__ == '__main__':
    main()
