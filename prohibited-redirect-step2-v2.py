#!/usr/bin/env python3
"""
subaog.com 禁运品类阶段 2 v2：_redirects + sitemap + 城市 hub 内链清理（修复合并行）
"""
import os
import re

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

PROHIBITED_ITEMS = ["milk-powder", "wine", "supplements"]
REGIONS = ["australia-to-china", "europe-to-china"]
LANGS = ["en", "zh-cn"]


def step2_sitemap():
    """sitemap.xml 移除禁运品类 URL（修复版：单行 <url>...</url>）"""
    p = f"{BASE}/sitemap.xml"
    with open(p, encoding='utf-8') as f:
        content = f.read()

    original_count = content.count("<loc>")
    print(f"=== sitemap 清理 ===")
    print(f"原始 URL 数: {original_count}")

    removed_total = 0
    new_content = content
    for region in REGIONS:
        for item in PROHIBITED_ITEMS:
            if region == "europe-to-china" and item == "supplements":
                continue
            # 单行格式：<url><loc>https://subaog.com/<region>/.../<item>/</loc>...</url>
            pat = re.compile(
                r'<url>\s*<loc>\s*https://subaog\.com/' +
                re.escape(region) + r'/[^/]+/' +
                re.escape(item) + r'/?\s*</loc>[^<]*<lastmod>[^<]*</lastmod>[^<]*<changefreq>[^<]*</changefreq>[^<]*<priority>[^<]*</priority>\s*</url>'
            )
            matches = pat.findall(new_content)
            new_content = pat.sub('', new_content)
            removed_total += len(matches)
            print(f"  移除 {region}/{item}: {len(matches)} 条")

    final_count = new_content.count("<loc>")
    with open(p, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"最终 URL 数: {final_count}")
    print(f"共移除: {removed_total}")
    return removed_total


def step2_hub_nav():
    """城市 hub 内链清理（修复版：跨行匹配 <a>...</a>）"""
    print(f"\n=== 城市 hub 内链清理 ===")
    cleaned_files = 0
    cleaned_links = 0

    for region in REGIONS:
        for lang in LANGS:
            base = f"{BASE}/{lang}/{region}"
            if not os.path.isdir(base):
                continue
            for entry in os.listdir(base):
                idx = f"{base}/{entry}/index.html"
                if not os.path.isfile(idx):
                    continue
                with open(idx, encoding='utf-8') as f:
                    content = f.read()

                original = content
                for item in PROHIBITED_ITEMS:
                    if region == "europe-to-china" and item == "supplements":
                        continue
                    # 跨行匹配 <a href="...item/"...>...</a>
                    pat = re.compile(
                        r'<a[^>]*href="/' + re.escape(lang) + r'/' +
                        re.escape(region) + r'/' + re.escape(entry) + r'/' +
                        re.escape(item) + r'/?[^"]*"[^>]*>.*?</a>',
                        re.DOTALL
                    )
                    matches = pat.findall(content)
                    content = pat.sub('', content)
                    cleaned_links += len(matches)

                if content != original:
                    with open(idx, 'w', encoding='utf-8') as f:
                        f.write(content)
                    cleaned_files += 1

    print(f"清理城市 hub 文件数: {cleaned_files}")
    print(f"移除链接数: {cleaned_links}")
    return cleaned_files


def main():
    step2_sitemap()
    step2_hub_nav()


if __name__ == '__main__':
    main()