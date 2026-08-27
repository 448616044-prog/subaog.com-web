#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
subaog.com — 全站技术 SEO 综合质检
覆盖维度: title/meta 长度、canonical/hreflang clean-URL、H1、schema 类型、
FAQPage 覆盖率、中文站 meta 去堆砌残留、lang、sitemap、断链(调用已有审计)
"""
import re
import json
from pathlib import Path
from collections import Counter

ROOT = Path(".")

def main():
    files = sorted(ROOT.rglob("*.html"))
    # 排除跳转页/404(无真实内容)
    skip_names = {"404.html", "index.html"}  # index.html 是根跳转页
    content_files = []
    for f in files:
        if f.name in skip_names and f.parent == ROOT:
            continue
        content_files.append(f)

    total = len(files)
    n = len(content_files)

    S = {
        "title_missing": [], "title_long": [],
        "meta_missing": [], "meta_long": [],
        "canon_missing": [], "canon_html": [],
        "hl_missing": [], "hl_html": [],
        "h1_missing": [], "h1_multi": [],
        "lang_missing": [],
        "zh_meta_junk": [],
    }
    schema = Counter()
    faq_yes = 0
    faq_missing = []

    for f in content_files:
        t = f.read_text(encoding="utf-8", errors="ignore")
        # title
        m = re.search(r"<title>(.*?)</title>", t, re.S)
        if not m or not m.group(1).strip():
            S["title_missing"].append(f)
        elif len(m.group(1).strip()) > 65:
            S["title_long"].append(f)
        # meta description
        md = re.search(r'<meta name="description" content="([^"]*)"', t)
        if not md or not md.group(1).strip():
            S["meta_missing"].append(f)
        elif len(md.group(1)) > 160:
            S["meta_long"].append(f)
        # canonical
        c = re.search(r'<link rel="canonical" href="([^"]*)"', t)
        if not c:
            S["canon_missing"].append(f)
        elif c.group(1).endswith(".html") or "/index.html" in c.group(1):
            S["canon_html"].append(f)
        # hreflang
        hl = re.findall(r'<link rel="alternate" hreflang="[^"]*" href="([^"]*)"', t)
        if not hl:
            S["hl_missing"].append(f)
        elif any(h.endswith(".html") or "/index.html" in h for h in hl):
            S["hl_html"].append(f)
        # H1
        h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", t, re.S)
        if not h1:
            S["h1_missing"].append(f)
        elif len(h1) > 1:
            S["h1_multi"].append(f)
        # schema 类型
        for st in re.findall(r'"@type":\s*"([A-Za-z]+)"', t):
            schema[st] += 1
        # FAQPage (有空格)
        if '"@type": "FAQPage"' in t:
            faq_yes += 1
        else:
            faq_missing.append(f)
        # lang
        if "<html lang=" not in t:
            S["lang_missing"].append(f)
        # 中文站 meta 堆砌残留
        if "zh-cn/" in str(f):
            mc = md.group(1) if md else ""
            if "12年国际物流经验" in mc or "双清包税门到门" in mc:
                S["zh_meta_junk"].append(f)

    print("=" * 60)
    print(f"subaog.com 全站技术 SEO 质检报告")
    print(f"总文件 {total} | 内容页 {n} (排除根 index 跳转页/404)")
    print("=" * 60)

    def show(name, lst, is_bad=True):
        mark = "❌" if (lst and is_bad) else "✅"
        print(f"  {mark} {name}: {len(lst)}")
        if lst:
            for x in lst[:5]:
                print(f"      - {x}")
            if len(lst) > 5:
                print(f"      ... 共 {len(lst)} 个")

    print("\n【1. 基础标签】")
    show("缺 title", S["title_missing"])
    show("title 超长(>65)", S["title_long"])
    show("缺 meta description", S["meta_missing"])
    show("meta 超长(>160)", S["meta_long"])
    show("缺 lang", S["lang_missing"])
    show("缺 H1", S["h1_missing"])
    show("多 H1", S["h1_multi"])

    print("\n【2. canonical/hreflang clean-URL】")
    show("缺 canonical", S["canon_missing"])
    show("canonical 仍 .html", S["canon_html"])
    show("缺 hreflang", S["hl_missing"])
    show("hreflang 仍 .html", S["hl_html"])

    print("\n【3. 结构化数据 schema 覆盖】")
    for k, v in schema.most_common(12):
        print(f"  · {k}: {v}")

    print("\n【4. FAQPage 覆盖率】")
    faq_rate = faq_yes / n * 100 if n else 0
    print(f"  · 有 FAQPage: {faq_yes} / {n} = {faq_rate:.1f}%")
    if faq_missing:
        print(f"  · 无 FAQPage 样例({len(faq_missing)}):")
        for x in faq_missing[:8]:
            print(f"      - {x}")

    print("\n【5. 中文站 meta 去堆砌残留】")
    show("zh-cn meta 仍含堆砌串", S["zh_meta_junk"])

    # sitemap
    print("\n【6. sitemap】")
    sm = ROOT / "sitemap.xml"
    if sm.exists():
        txt = sm.read_text(encoding="utf-8", errors="ignore")
        locs = re.findall(r"<loc>([^<]+)</loc>", txt)
        html_urls = [u for u in locs if u.endswith(".html") or "/index.html" in u]
        print(f"  · URL 数: {len(locs)}")
        print(f"  · 仍 .html: {len(html_urls)}")

    # 断链(独立审计)
    print("\n【7. 内部断链】")
    links = 0
    broken = 0
    valid = set()
    for f in content_files:
        valid.add(str(f))
        # 目录形式也合法(index.html 的目录)
        if f.name == "index.html":
            valid.add(str(f.parent))
    for f in content_files:
        t = f.read_text(encoding="utf-8", errors="ignore")
        for href in re.findall(r'href="([^"]+)"', t):
            if href.startswith(("http", "mailto:", "tel:", "#", "javascript")):
                continue
            links += 1
            # 站内相对/绝对路径
            path = href.split("#")[0].split("?")[0]
            if not path:
                continue
            # 绝对 /en/xxx
            if path.startswith("/"):
                rel = path.lstrip("/")
            else:
                rel = str((f.parent / path).resolve().relative_to(ROOT.resolve()))
            # 检查文件或目录
            cand = ROOT / rel
            if rel.endswith(".html"):
                ok = cand.exists()
            else:
                ok = cand.exists() or (ROOT / (rel + ".html")).exists() or (cand / "index.html").exists()
            if not ok:
                broken += 1
                if broken <= 8:
                    print(f"      - {f} -> {href}")
    print(f"  · 内链: {links} | 断链: {broken}")

    print("\n" + "=" * 60)
    # 健康分
    issues = sum(len(v) for v in S.values()) + len(faq_missing) + broken
    print(f"体检结论: 检测 {n} 内容页, 发现 {issues} 个问题点")

if __name__ == "__main__":
    main()
