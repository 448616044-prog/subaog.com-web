#!/usr/bin/env python3
"""sitemap 直接清理（区分语言）"""
import re

with open("sitemap.xml", encoding='utf-8') as f:
    content = f.read()

before = content.count("<loc>")
print(f"原始 URL 数: {before}")

total = 0
configs = [
    ("australia-to-china", "milk-powder"),
    ("australia-to-china", "wine"),
    ("australia-to-china", "supplements"),
    ("europe-to-china", "milk-powder"),
    ("europe-to-china", "wine"),
]
for region, item in configs:
    pat = re.compile(
        r'<url>\s*<loc>\s*https://subaog\.com/(en|zh-cn)/' +
        re.escape(region) + r'/[^/]+/' +
        re.escape(item) + r'/?\s*</loc>[^<]*<lastmod>[^<]*</lastmod>[^<]*<changefreq>[^<]*</changefreq>[^<]*<priority>[^<]*</priority>\s*</url>'
    )
    matches = pat.findall(content)
    content = pat.sub('', content)
    total += len(matches)
    print(f"  {region}/{item}: 移除 {len(matches)} 条")

after = content.count("<loc>")
print(f"最终 URL 数: {after}")
print(f"共移除: {total}")

with open("sitemap.xml", 'w', encoding='utf-8') as f:
    f.write(content)