#!/usr/bin/env python3
"""全站内部断链审计"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(".")

# 构建有效 URL 集合
def build_valid_urls():
    valid = {"/", "/sitemap.xml", "/robots.txt", "/_redirects", "/favicon.ico"}
    # 根目录下其他静态资源
    for f in ROOT.iterdir():
        if f.is_file():
            valid.add("/" + f.name)
    for f in ROOT.rglob("*.html"):
        p = "/" + str(f)
        if f.name == "index.html":
            valid.add("/" + str(f.parent).rstrip("/") + "/")
            valid.add("/" + str(f.parent).rstrip("/"))  # 无尾斜杠也视为可 301
        else:
            valid.add(p[:-5])  # extensionless
            valid.add(p)       # .html
    # _redirects 源也视为有效（返回 3XX 而非 404）
    redirects = ROOT / "_redirects"
    redirect_sources = set()
    if redirects.exists():
        for line in redirects.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                src = parts[0]
                if src.startswith("/"):
                    redirect_sources.add(src)
                    # 去除尾斜杠的变体
                    if src.endswith("/"):
                        redirect_sources.add(src[:-1])
                    else:
                        redirect_sources.add(src + "/")
    return valid | redirect_sources, redirect_sources


def main():
    valid, redirects = build_valid_urls()
    link_re = re.compile(r'href="(/[^"#]*)"')
    broken = defaultdict(list)  # target -> [(source_file, link)]
    total = 0

    for f in ROOT.rglob("*.html"):
        t = f.read_text(encoding="utf-8", errors="ignore")
        body = t.split("</head>", 1)[-1]
        for m in link_re.finditer(body):
            href = m.group(1)
            total += 1
            # 忽略合法根路径与已验证 URL
            if href in valid:
                continue
            # 检查是否匹配 redirect 规则（通配）
            matched = False
            for r in redirects:
                if r.endswith("*") and href.startswith(r[:-1]):
                    matched = True
                    break
            if matched:
                continue
            broken[href].append(str(f))

    print(f"扫描内链: {total} 条 | 断链目标: {len(broken)} 个")
    if broken:
        for target, sources in sorted(broken.items(), key=lambda x: -len(x[1]))[:30]:
            print(f"  ❌ {target}")
            print(f"      来自: {', '.join(sources[:5])}{'...' if len(sources)>5 else ''} ({len(sources)} 页)")
    else:
        print("✅ 未发现内部断链")
    return len(broken)


if __name__ == "__main__":
    main()
