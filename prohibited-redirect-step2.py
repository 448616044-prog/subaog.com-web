#!/usr/bin/env python3
"""
subaog.com 禁运品类阶段 2：_redirects + sitemap + 城市 hub 内链清理
"""
import os
import re
import subprocess

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

PROHIBITED_ITEMS = ["milk-powder", "wine", "supplements"]
REGIONS = ["australia-to-china", "europe-to-china"]
LANGS = ["en", "zh-cn"]


def step2_redirects():
    """更新 _redirects：通配符 301 到对应城市 hub"""
    p = f"{BASE}/_redirects"
    with open(p, encoding='utf-8') as f:
        content = f.read()

    # 新增规则（6 条通配符）
    new_rules = []
    for region in REGIONS:
        for item in PROHIBITED_ITEMS:
            for lang in LANGS:
                # 澳洲 europe 只对实际删除的品类加规则
                if region == "europe-to-china" and item == "supplements":
                    continue  # 欧洲没 supplements 目录
                new_rules.append(f"/{lang}/{region}/*/{item}/  /{lang}/{region}/$1/  301")

    # 追加到 _redirects（末尾加分隔注释）
    separator = "\n\n# === 2026-09-05 禁运品类 301 重定向 ===\n"
    if separator.strip() not in content:
        content = content.rstrip() + separator + "\n".join(new_rules) + "\n"

    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"=== 阶段 2a：_redirects 已更新 ===")
    print(f"新增规则数: {len(new_rules)}")
    for r in new_rules:
        print(f"  {r}")


def step2_sitemap():
    """sitemap.xml 移除禁运品类 URL"""
    p = f"{BASE}/sitemap.xml"
    with open(p, encoding='utf-8') as f:
        content = f.read()

    # 构建要移除的 URL pattern
    patterns = []
    for region in REGIONS:
        for item in PROHIBITED_ITEMS:
            if region == "europe-to-china" and item == "supplements":
                continue
            patterns.append(f"/{region}/")
            patterns.append(item)

    original_count = content.count("<loc>")
    print(f"\n=== 阶段 2b：sitemap 清理 ===")
    print(f"原始 URL 数: {original_count}")

    # 移除含禁运品类的 URL
    removed = 0
    new_content = content
    for region in REGIONS:
        for item in PROHIBITED_ITEMS:
            if region == "europe-to-china" and item == "supplements":
                continue
            # 匹配 <url>...<loc>.../<region>/.../<item>/...</loc>...</url>
            # 简化：移除包含 /<region>/ 和 /<item>/ 的 <url> 块
            pattern = re.compile(
                r'<url>\s*<loc>https://subaog\.com/' +
                re.escape(region) +
                r'/[^<]*/' +
                re.escape(item) +
                r'/?\s*</loc>.*?</url>',
                re.DOTALL
            )
            matches = pattern.findall(new_content)
            new_content = pattern.sub('', new_content)
            removed += len(matches)
            print(f"  移除 {region}/{item}: {len(matches)} 条")

    final_count = new_content.count("<loc>")
    with open(p, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"最终 URL 数: {final_count}")
    print(f"共移除: {removed}")


def step4_hub_nav():
    """清理城市 hub 页的品类导航：移除禁运品类链接"""
    print(f"\n=== 阶段 2c：城市 hub 内链清理 ===")

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
                # 移除 href="/<lang>/<region>/<entry>/<prohibited-item>/" 的链接
                for item in PROHIBITED_ITEMS:
                    if region == "europe-to-china" and item == "supplements":
                        continue
                    # 匹配多种格式
                    pat = re.compile(
                        r'<a[^>]*href="/' + re.escape(lang) + r'/' +
                        re.escape(region) + r'/' + re.escape(entry) + r'/' +
                        re.escape(item) + r'/?"[^>]*>[^<]*</a>',
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


def main():
    step2_redirects()
    step2_sitemap()
    step4_hub_nav()


if __name__ == '__main__':
    main()