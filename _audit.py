import re
from pathlib import Path
from collections import Counter
ROOT = Path('.')
# 1) logo 高度
hgts = Counter()
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        for m in re.findall(r'height:\d+px;width:auto;display:block', t):
            hgts[m] += 1
for k, v in hgts.most_common():
    print(f'  {v:5d}  {k}')
print()
# 2) logo-sub 变体
subs = Counter()
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        for m in re.findall(r'<span class="logo-sub"[^>]*>[^<]+</span>', t):
            subs[m] += 1
for k, v in subs.most_common(15):
    print(f'  {v:5d}  {k}')
print('总副标变体数:', len(subs))
# 3) 学生行李页面结构
print('\n=== student-luggage 关键布局 ===')
sp = ROOT / 'zh-cn' / 'student-luggage' / 'index.html'
t = sp.read_text(encoding='utf-8', errors='ignore')
# 找包含 "出发国家地区" 的块
i = t.find('出发国家地区')
print(f'  表格块位置: {i}')
# 找最近的 <table> ... </table>
m = re.search(r'<table[^>]*>.*?</table>', t[i-300:i+2000], re.S)
if m:
    print(m.group(0)[:1500])
