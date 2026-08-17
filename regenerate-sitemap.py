#!/usr/bin/env python3
"""
regenerate-sitemap.py
=====================
基于 /zh-cn/ 目录实际存在的 .html 文件，重新生成 sitemap.xml。
支持 hreflang 注解（如果 /en/ 对应文件存在则标记，否则只列 zh-CN）。
"""
import re
from pathlib import Path

ROOT = Path("/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com")
ZH = ROOT / "zh-cn"
EN = ROOT / "en"
SITEMAP = ROOT / "sitemap.xml"
DOMAIN = "https://subaog.com"

# 首页（根选择器）单独存在
ROOT_URL = f"{DOMAIN}/"
ZH_HOME = f"{DOMAIN}/zh-cn/"
EN_HOME = f"{DOMAIN}/en/"


def priority_for(rel: str) -> str:
    """根据路径决定优先级。"""
    if rel == "index.html":
        return "1.0"
    if rel in ("about.html", "faq.html", "contact.html", "pricing.html"):
        return "0.7"
    if rel.startswith("usa-to-china/") or rel == "usa-to-china/index.html":
        return "0.9"
    if rel.endswith("/index.html") and rel.count("/") == 1:
        # 二级目录首页（pillar 页）
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


def build_urlset() -> str:
    lines = []
    today = "2026-08-17"

    # ---- 根选择器页（语言选择）----
    lines.append(f'  <url><loc>{ROOT_URL}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>')

    # ---- 扫 /zh-cn/ 所有 html ----
    zh_files = sorted(ZH.rglob("*.html"))
    for f in zh_files:
        rel = f.relative_to(ZH).as_posix()
        if rel == "404.html":
            continue  # 排除 404 页面
        # 转 URL：index.html → /zh-cn/foo/；其他 → /zh-cn/foo.html
        if rel == "index.html":
            url = ZH_HOME
        elif rel.endswith("/index.html"):
            url = f"{DOMAIN}/zh-cn/{rel[:-len('index.html')]}"
        else:
            url = f"{DOMAIN}/zh-cn/{rel}"

        # 检查 /en/ 对应是否存在
        en_rel = rel
        en_path = EN / en_rel
        if en_path.exists():
            en_url = f"{DOMAIN}/en/{rel[:-len('index.html')]}" if rel.endswith("/index.html") else f"{DOMAIN}/en/{rel}"
            if rel == "index.html":
                en_url = EN_HOME
            elif rel.endswith("/index.html"):
                en_url = f"{DOMAIN}/en/{rel[:-len('index.html')]}"
            # 暂不为 zh-CN URL 写 hreflang 注解（保持 sitemap 简洁，等 /en/ 全量后再补）
            lines.append(
                f'  <url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>{changefreq_for(rel)}</changefreq><priority>{priority_for(rel)}</priority></url>'
            )
        else:
            lines.append(
                f'  <url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>{changefreq_for(rel)}</changefreq><priority>{priority_for(rel)}</priority></url>'
            )

    # ---- /en/ 已有页面 ----
    if EN.exists():
        en_files = sorted(EN.rglob("*.html"))
        for f in en_files:
            rel = f.relative_to(EN).as_posix()
            if rel == "404.html":
                continue  # 排除 404 页面
            if rel == "index.html":
                url = EN_HOME
            elif rel.endswith("/index.html"):
                url = f"{DOMAIN}/en/{rel[:-len('index.html')]}"
            else:
                url = f"{DOMAIN}/en/{rel}"
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