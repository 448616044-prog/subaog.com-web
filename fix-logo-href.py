"""修复 logo 不可点击问题:
1) 1825 页无 href 的图片 logo -> 加 href (zh-cn -> /zh-cn/, en -> /en/)
2) 9 页 seasia 页 <a href="/" class="logo"><img></a> -> href 改 /zh-cn/ + 补副标 span
"""
import re
from pathlib import Path
ROOT = Path('.')

# 1) 主体: 无 href 的图片 logo 加 href
no_href_zh = '<a style="display:flex;align-items:center;gap:12px;" class="logo">'
no_href_en = '<a style="display:flex;align-items:center;gap:12px;" class="logo">'
new_zh = '<a href="/zh-cn/" style="display:flex;align-items:center;gap:12px;" class="logo">'
new_en = '<a href="/en/" style="display:flex;align-items:center;gap:12px;" class="logo">'

c1_zh = c1_en = 0
for p in (ROOT / 'zh-cn').rglob('*.html'):
    t = p.read_text(encoding='utf-8', errors='ignore')
    if no_href_zh in t:
        t = t.replace(no_href_zh, new_zh)
        p.write_text(t, encoding='utf-8')
        c1_zh += 1
for p in (ROOT / 'en').rglob('*.html'):
    t = p.read_text(encoding='utf-8', errors='ignore')
    if no_href_en in t:
        t = t.replace(no_href_en, new_en)
        p.write_text(t, encoding='utf-8')
        c1_en += 1
print(f'[1] 无href补href: zh-cn {c1_zh} 页, en {c1_en} 页')

# 2) 9 个 seasia 页: <a href="/" class="logo"><img ...></a> (无副标)
#    -> href 改 /zh-cn/ + 补副标 span
old_sea = ('<a href="/" class="logo">'
           '<img src="/assets/images/logo.png" alt="速豹回国物流" '
           'style="height:55px;width:auto;display:block"></a>')
new_sea = ('<a href="/zh-cn/" style="display:flex;align-items:center;gap:12px;" class="logo">'
           '<img src="/assets/images/logo.png" alt="速豹回国物流" '
           'style="height:55px;width:auto;display:block">'
           '<span style="font-size:14px;color:var(--primary);font-weight:600;'
           'border-left:2px solid var(--primary-light);padding-left:14px;'
           'line-height:1.2;letter-spacing:0.5px">各国寄中国专线</span></a>')

c2 = 0
for p in (ROOT / 'zh-cn' / 'seasia-to-china').rglob('*.html'):
    t = p.read_text(encoding='utf-8', errors='ignore')
    if old_sea in t:
        t = t.replace(old_sea, new_sea)
        p.write_text(t, encoding='utf-8')
        c2 += 1
print(f'[2] seasia页 href=/ 改 /zh-cn/ + 补副标: {c2} 页')

# 验证
print('\n=== 验证 ===')
no_href = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        for m in re.finditer(r'<a [^>]*class="logo"[^>]*>', t):
            if 'href=' not in m.group(0):
                no_href += 1
print(f'剩余无 href 的 logo 锚点: {no_href}')
