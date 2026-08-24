#!/usr/bin/env python3
"""
regenerate-sitemap.py
=====================
基于 /zh-cn/ 与 /en/ 目录实际存在的 .html 文件，重新生成 sitemap.xml。
URL 形态与 Cloudflare Pages 最终 200 URL 对齐：
  - 目录 index.html → /zh-cn/foo/ （尾斜杠）
  - 普通 .html 文件 → /zh-cn/foo （无扩展名）
"""
import re
from pathlib import Path
from datetime import datetime

ROOT = Path("/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com")
ZH = ROOT / "zh-cn"
EN = ROOT / "en"
SITEMAP = ROOT / "sitemap.xml"
DOMAIN = "https://subaog.com"

ROOT_URL = f"{DOMAIN}/"
ZH_HOME = f"{DOMAIN}/zh-cn/"
EN_HOME = f"{DOMAIN}/en/"


def priority_for(rel: str) -> str:
    if rel == "index.html":
        return "1.0"
    if rel in ("about.html", "faq.html", "contact.html", "pricing.html"):
        return "0.7"
    if rel.startswith("usa-to-china/") or rel == "usa-to-china/index.html":
        return "0.9"
    if rel.endswith("/index.html") and rel.count("/") == 1:
        return "0.8"
    if rel.startswith("blog/") and rel != "blog/index.html":
        return "0.7"
    if rel.startswith("city/"):
        return "0.6"
    if rel.startswith("tools/"):
        return "0.7"
    if rel == "404.html":
        return "0.1"
    return "0.6"


def changefreq_for(rel: str) -> str:
    if rel == "index.html":
        return "weekly"
    if rel.startswith("city/"):
        return "monthly"
    return "weekly"


def file_to_url(rel: str, lang: str) -> str:
    """把相对路径转成规范 URL"""
    base = f"{DOMAIN}/{lang}"
    if rel == "index.html":
        return f"{base}/"
    if rel.endswith("/index.html"):
        path = rel[:-len("index.html")]
        return f"{base}/{path}"
    path = rel[:-len(".html")]
    return f"{base}/{path}"


def build_urlset() -> str:
    lines = []
    today = datetime.now().strftime("%Y-%m-%d")

    # 根选择器页
    lines.append(f'  <url><loc>{ROOT_URL}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>')

    # /zh-cn/
    zh_files = sorted(ZH.rglob("*.html"))
    for f in zh_files:
        rel = f.relative_to(ZH).as_posix()
        if rel == "404.html":
            continue
        url = file_to_url(rel, "zh-cn")
        lines.append(
            f'  <url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>{changefreq_for(rel)}</changefreq><priority>{priority_for(rel)}</priority></url>'
        )

    # /en/
    if EN.exists():
        en_files = sorted(EN.rglob("*.html"))
        for f in en_files:
            rel = f.relative_to(EN).as_posix()
            if rel == "404.html":
                continue
            url = file_to_url(rel, "en")
            lines.append(
                f'  <url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>{changefreq_for(rel)}</changefreq><priority>{priority_for(rel)}</priority></url>'
            )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(lines)
        + "\n</urlset>\n"
    )


def main():
    sitemap = build_urlset()
    SITEMAP.write_text(sitemap, encoding="utf-8")
    n = sitemap.count("<loc>")
    print(f"✅ sitemap.xml 已重新生成，共 {n} 条 URL")


if __name__ == "__main__":
    main()
