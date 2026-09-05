"""扫描 canonical 无内链页面"""
import os, re
from collections import defaultdict

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

def get_canonical(html_path):
    with open(html_path, encoding="utf-8") as f:
        t = f.read()
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', t)
    if m:
        return m.group(1).strip()
    return None

def canon_to_path(canon_url, html_path):
    """把 canonical URL 转成相对路径或绝对路径"""
    # https://subaog.com/zh-cn/usa-to-china/atlanta/furniture/
    if canon_url.startswith("http"):
        # 截取 path
        from urllib.parse import urlparse
        u = urlparse(canon_url)
        path = u.path
    else:
        path = canon_url
    # 去掉前导 /
    path = path.lstrip("/")
    # 加上 BASE
    return os.path.join(BASE, path)


# 1) 收集所有页面 + canonical URL
pages = []  # [(file_path, canonical_path, ...)]
canonicals = defaultdict(list)  # canonical_path -> [referrer file]

# 范围：en/usa-to-china 和 zh-cn/usa-to-china（city×item 集中地）
for lang in ["en", "zh-cn"]:
    base_dir = f"{BASE}/{lang}/usa-to-china"
    if not os.path.isdir(base_dir):
        continue
    for city_dir in sorted(os.listdir(base_dir)):
        cp = f"{base_dir}/{city_dir}"
        if not os.path.isdir(cp):
            continue
        # hub page
        idx = f"{cp}/index.html"
        if os.path.isfile(idx):
            pages.append(idx)
        # city×item pages
        for item in sorted(os.listdir(cp)):
            ip = f"{cp}/{item}/index.html"
            if os.path.isfile(ip):
                pages.append(ip)

print(f"USA pages 总数: {len(pages)}")

# 2) 收集所有页面文件中的内链（href）
internal_links_per_page = defaultdict(set)
for f in pages:
    with open(f, encoding="utf-8") as fp:
        t = fp.read()
    # 抽取所有 href
    for m in re.finditer(r'href="([^"#?]+?)"', t):
        h = m.group(1)
        if h.startswith("http"):
            from urllib.parse import urlparse
            h = urlparse(h).path
        h = h.lstrip("/")
        # 跳过外部锚点、mailto 等
        if h.startswith(("mailto:", "tel:", "javascript:")):
            continue
        # 去掉 query 和 fragment
        h = h.split("?")[0].split("#")[0]
        if h.endswith("/"):
            h = h[:-1]
        if h.endswith(".html"):
            target = os.path.join(BASE, h)
        elif h.endswith("/"):
            target = os.path.join(BASE, h, "index.html")
        else:
            target = os.path.join(BASE, h + "/index.html")
        # 也加 index.html 形式
        internal_links_per_page[f].add(target)

# 3) 检查每个 page 的目标路径（HTML 路径或目录路径）是否被任何页面链接
orphans = []
for f in pages:
    # 把当前页转为几种 URL 形式
    rel = os.path.relpath(f, BASE)
    candidates = [rel]
    # 目录路径（不带 /index.html）
    if rel.endswith("/index.html"):
        candidates.append(rel[:-len("/index.html")])
        candidates.append(rel[:-len("/index.html")] + "/")
    # 检查是否有任何内部页面链接到它
    has_link = False
    for other, links in internal_links_per_page.items():
        if other == f:
            continue
        for link in links:
            if link == f or link == os.path.join(BASE, rel) or link == os.path.join(BASE, rel.rstrip("/")):
                has_link = True
                break
        if has_link:
            break
    if not has_link:
        orphans.append(rel)

print(f"\n孤立页面（无内链支持）数: {len(orphans)}")
print(f"\n=== 前 30 个孤立页面 ===")
for o in orphans[:30]:
    print(f"  {o}")