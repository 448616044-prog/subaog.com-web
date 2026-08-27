import re
from pathlib import Path
from collections import Counter
ROOT = Path('.')
# 1) logo 高度统计
hgts = Counter()
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        for m in re.findall(r'height:\d+px;width:auto;display:block', t):
            hgts[m] += 1
print('=== logo 高度分布 ===')
for k, v in hgts.most_common():
    print(f'  {v:5d}  {k}')

# 2) logo 后副标（<span> in <a class="logo">）
subs = Counter()
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        # logo 锚点里的 span
        m = re.search(r'<a [^>]*class="logo"[^>]*>.*?<span[^>]*>([^<]+)</span>', t, re.S)
        if m:
            subs[m.group(1).strip()] += 1
        else:
            # 没有副标
            subs['(no sub)'] += 1
print('\n=== logo 后副标文本分布 ===')
for k, v in subs.most_common(10):
    print(f'  {v:5d}  {repr(k)}')

# 3) student-luggage 状况
print('\n=== student-luggage 样式块行数 ===')
sp = ROOT / 'zh-cn' / 'student-luggage' / 'index.html'
t = sp.read_text(encoding='utf-8', errors='ignore')
ms = re.search(r'<style[^>]*>(.*?)</style>', t, re.S)
if ms:
    print(f'  <style> {len(ms.group(1))} chars')
print(f'  hero block: {"<section class=\"hero\">" in t}')
print(f'  table in hero: {bool(re.search(r"<section class=\"hero\">.*?<table>", t, re.S))}')
