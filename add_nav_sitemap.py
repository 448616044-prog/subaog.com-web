"""城市 hub 页插入品类导航 + sitemap 追加 224 条 URL"""
import os, re
from data_regions import TIERS, CITIES, build_items

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"
SITE = "https://subaog.com"
LASTMOD = "2026-09-05"

def build_nav_en(region, city_slug, city, items):
    """英文品类导航区"""
    links = ""
    for slug, d in items.items():
        links += (
            f'<a href="/en/{region}/{city_slug}/{slug}/" style="background:#fff;border:1px solid var(--border);border-radius:10px;padding:12px 16px;font-size:14px;color:var(--text)">'
            f'<span style="color:#00B900;font-weight:700">✓</span> {d["en"]}</a>'
        )
    return (
        f'<section class="section" style="background:#fff;padding:40px 0">'
        f'<div class="container"><div class="section-title"><h2>What can I ship from {city["en"]} to China</h2></div>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px">{links}</div>'
        f'</div></section>\n'
    )

def build_nav_zh(region, city_slug, city, items):
    """中文品类导航区"""
    links = ""
    for slug, d in items.items():
        links += (
            f'<a href="/zh-cn/{region}/{city_slug}/{slug}/" style="background:#fff;border:1px solid var(--border);border-radius:10px;padding:12px 16px;font-size:14px;color:var(--text)">'
            f'<span style="color:#00B900;font-weight:700">✓</span> {d["zh"]}</a>'
        )
    return (
        f'<section class="section" style="background:#fff;padding:40px 0">'
        f'<div class="container"><div class="section-title"><h2>从{city["zh"]}可寄什么回国</h2></div>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px">{links}</div>'
        f'</div></section>\n'
    )

# 1) 城市页插入品类导航
nav_added = 0
for region, tier in TIERS.items():
    items = build_items(region)
    for city_slug, city in CITIES[region].items():
        # en
        en_path = f"{BASE}/en/{region}/{city_slug}/index.html"
        with open(en_path, encoding="utf-8") as f:
            t = f.read()
        nav_en = build_nav_en(region, city_slug, city, items)
        if "What can I ship from" not in t:
            t = t.replace("<footer class=\"footer\">", nav_en + "<footer class=\"footer\">", 1)
            with open(en_path, "w", encoding="utf-8") as f:
                f.write(t)
            nav_added += 1
        # zh
        zh_path = f"{BASE}/zh-cn/{region}/{city_slug}/index.html"
        with open(zh_path, encoding="utf-8") as f:
            t = f.read()
        nav_zh = build_nav_zh(region, city_slug, city, items)
        if "可寄什么回国" not in t:
            t = t.replace("<footer class=\"footer\">", nav_zh + "<footer class=\"footer\">", 1)
            with open(zh_path, "w", encoding="utf-8") as f:
                f.write(t)
            nav_added += 1

print(f"城市页插入品类导航: {nav_added} 页")

# 2) sitemap 追加
sitemap_path = f"{BASE}/sitemap.xml"
with open(sitemap_path, encoding="utf-8") as f:
    sm = f.read()

new_urls = []
for region, tier in TIERS.items():
    for city_slug in CITIES[region].keys():
        for item_slug in build_items(region).keys():
            for lang in ["en", "zh-cn"]:
                url = f"{SITE}/{lang}/{region}/{city_slug}/{item_slug}/"
                new_urls.append(
                    f"  <url><loc>{url}</loc><lastmod>{LASTMOD}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>"
                )

# 去重（避免重复追加）
existing = set(re.findall(r'<loc>(https://subaog.com/[^<]+)</loc>', sm))
new_unique = [u for u in new_urls if re.search(r'<loc>(https://subaog.com/[^<]+)</loc>', u).group(1) not in existing]

print(f"sitemap 新增 URL: {len(new_unique)}")

# 在 </urlset> 之前插入
if new_unique:
    insert = "\n".join(new_unique) + "\n"
    sm = sm.replace("</urlset>", insert + "</urlset>")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sm)
    print(f"sitemap 更新完成")

# 校验 sitemap 总 URL 数
with open(sitemap_path, encoding="utf-8") as f:
    final = f.read()
print(f"sitemap 总 URL 数: {len(re.findall(r'<loc>', final))}")