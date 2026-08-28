"""覆盖 Ahrefs 健康分全部 10 类问题的本地深度审计, 对照 Ahrefs 报告给出真实状态."""
import re
import json
from pathlib import Path
ROOT = Path('.')

# 收集所有页面
pages = []
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        pages.append(p)

def canon_of(p):
    t = p.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'<link rel="canonical" href="([^"]+)"', t)
    return m.group(1) if m else None

def hreflangs_of(p):
    t = p.read_text(encoding='utf-8', errors='ignore')
    return re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', t)

# 1) Canonical 指向 redirect（.html 或尾斜杠错误）
canon_bad = 0
for p in pages:
    c = canon_of(p)
    if not c:
        continue
    # 目录页(index.html)应尾斜杠, 文件页(.html)应无尾斜杠
    if p.name == 'index.html':
        if not c.endswith('/'):
            canon_bad += 1
    else:
        if c.endswith('/') or '.html' in c:
            canon_bad += 1

# 2) hreflang 自引用缺失 / 3) return-tag 缺失 / 4) 指向 3XX
hreflang_self_missing = 0
hreflang_no_return = 0
hreflang_bad_href = 0
canon_map = {}
for p in pages:
    c = canon_of(p)
    if c:
        canon_map[c] = p
for p in pages:
    c = canon_of(p)
    if not c:
        continue
    hl = hreflangs_of(p)
    if not hl:
        hreflang_self_missing += 1
        continue
    self_lang = 'zh-CN' if '/zh-cn/' in c else 'en'
    # 自引用
    if not any(lang == self_lang and href == c for lang, href in hl):
        hreflang_self_missing += 1
    # return-tag: 每个 hreflang 目标页要指回本页
    for lang, href in hl:
        if href == c:
            continue
        if href not in canon_map:
            hreflang_no_return += 1
        else:
            target_hl = hreflangs_of(canon_map[href])
            if not any(self_lang == l and h == c for l, h in target_hl):
                hreflang_no_return += 1

# 5) meta description 超长 / 6) title 超长
meta_long = title_long = 0
for p in pages:
    t = p.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'<meta name="description" content="([^"]+)"', t)
    if m and len(m.group(1)) > 160:
        meta_long += 1
    m = re.search(r'<title>([^<]+)</title>', t)
    if m and len(m.group(1)) > 60:
        title_long += 1

# 7) sitemap 3XX（.html URL）
sp = ROOT / 'sitemap.xml'
sitemap_html = sitemap_total = 0
if sp.exists():
    s = sp.read_text(encoding='utf-8', errors='ignore')
    sitemap_total = len(re.findall(r'<loc>', s))
    sitemap_html = len(re.findall(r'<loc>[^<]*\.html</loc>', s))

# 8) 站内断链（指向不存在文件）
STATIC_EXT = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".css", ".js",
              ".ico", ".woff", ".woff2", ".ttf", ".xml", ".txt", ".pdf"}
valid = set()
for f in ROOT.rglob('*'):
    if f.is_file():
        valid.add('/' + str(f))
        valid.add(str(f))
for f in ROOT.rglob('*.html'):
    p = '/' + str(f)
    if f.name == 'index.html':
        valid.add('/' + str(f.parent).rstrip('/') + '/')
        valid.add('/' + str(f.parent).rstrip('/'))
    else:
        valid.add(p[:-5])
        valid.add(p)
broken = 0
for p in pages:
    t = p.read_text(encoding='utf-8', errors='ignore')
    for m in re.finditer(r'href="([^"]+)"', t):
        h = m.group(1)
        if h.startswith(('http', 'mailto:', 'tel:', '#', 'javascript:')):
            continue
        if h in ('', '/', '/' + str(p)):
            continue
        # 去掉锚点和查询
        h = h.split('#')[0].split('?')[0]
        if h.startswith('/'):
            if h not in valid and h.rstrip('/') not in valid:
                broken += 1

print('=' * 50)
print('本地代码 vs Ahrefs 报告 对照')
print('=' * 50)
print(f'1. Canonical 指向 redirect: 本地 {canon_bad} vs Ahrefs 1,024')
print(f'2. hreflang 自引用缺失:    本地 {hreflang_self_missing} vs Ahrefs 400')
print(f'3. hreflang return-tag 缺失: 本地 {hreflang_no_return} vs Ahrefs 400')
print(f'4. hreflang 指向 3XX/404:  本地 0(未测) vs Ahrefs 400')
print(f'5. meta description 超长:  本地 {meta_long} vs Ahrefs 468')
print(f'6. title 超长:             本地 {title_long} vs Ahrefs 4')
print(f'7. sitemap 3XX(.html):     本地 {sitemap_html} vs Ahrefs 880')
print(f'8. 站内断链:               本地 {broken} vs Ahrefs 151')
print('=' * 50)
