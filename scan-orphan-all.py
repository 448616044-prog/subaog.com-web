"""全站扫描孤立页面（canonical 无内链）"""
import os, re
from collections import defaultdict

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

def collect_pages():
    """收集所有 HTML 页面的相对路径"""
    pages = []
    # 用 find 而非 os.walk 避免超时
    files = []
    for sub in ["en", "zh-cn", "tools", "blog", "city", "report",
                "japan-to-china", "korea-to-china", "seasia-to-china",
                "canada-to-china", "australia-to-china", "europe-to-china",
                "taiwan-to-china", "mexico-to-china", "newzealand-to-china",
                "usa-to-china", "usa-moving-to-china", "uk-to-china",
                "student-luggage", "about", "index.html", "404.html"]:
        p = f"{BASE}/{sub}"
        if os.path.isfile(p):
            files.append(sub)
        elif os.path.isdir(p):
            import subprocess
            r = subprocess.run(["find", p, "-name", "*.html"],
                              capture_output=True, text=True, timeout=30)
            files.extend(r.stdout.strip().split("\n"))
    pages = [os.path.relpath(f, BASE) for f in files if f]
    return pages

pages = collect_pages()
print(f"全站页面总数: {len(pages)}")

# 2) 收集所有页面文件中的内链
internal_links_per_page = defaultdict(set)
for f in pages:
    full = os.path.join(BASE, f)
    if not os.path.isfile(full):
        continue
    with open(full, encoding="utf-8") as fp:
        t = fp.read()
    for m in re.finditer(r'href="([^"#?]+?)"', t):
        h = m.group(1)
        if h.startswith("http"):
            from urllib.parse import urlparse
            h = urlparse(h).path
        h = h.lstrip("/")
        if h.startswith(("mailto:", "tel:", "javascript:")):
            continue
        h = h.split("?")[0].split("#")[0]
        if h.endswith("/"):
            target = os.path.join(BASE, h, "index.html")
            internal_links_per_page[f].add(target)
            internal_links_per_page[f].add(os.path.join(BASE, h.rstrip("/")))
        elif h.endswith(".html"):
            internal_links_per_page[f].add(os.path.join(BASE, h))
            # clean URL 形式（去 .html）
            internal_links_per_page[f].add(os.path.join(BASE, h[:-5]))
        else:
            # clean URL（无 .html 也无 /）—— 可能是 /en/tools/can-i-ship
            target_idx = os.path.join(BASE, h, "index.html")
            target_html = os.path.join(BASE, h + ".html")
            internal_links_per_page[f].add(target_idx)
            internal_links_per_page[f].add(target_html)

# 3) 检查孤立页面
orphans = []
for f in pages:
    candidates = [f]
    if f.endswith("/index.html"):
        candidates.append(f[:-len("/index.html")])
        candidates.append(f[:-len("/index.html")] + "/")

    has_link = False
    for other, links in internal_links_per_page.items():
        if other == f:
            continue
        for link in links:
            link_rel = os.path.relpath(link, BASE) if not link.endswith("/") else link
            if link in [os.path.join(BASE, c) for c in candidates]:
                has_link = True
                break
            if link_rel in candidates:
                has_link = True
                break
        if has_link:
            break
    if not has_link:
        orphans.append(f)

print(f"\n孤立页面（无内链支持）数: {len(orphans)}")
print(f"\n=== 全部孤立页面（按目录分布）===")
from collections import Counter
buckets = Counter()
for o in orphans:
    dir_ = o.split("/")[0] if "/" in o else "(root)"
    buckets[dir_] += 1
for k, v in sorted(buckets.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print(f"\n=== 前 50 个孤立页面 ===")
for o in orphans[:50]:
    print(f"  {o}")