"""在 hero 区 h1 上方加品牌定位 eyebrow 标签 (eyebrow 模式).

zh-cn: "各国寄中国专线"
en:    "Shipping to China"

样式: 小字/半透明/字间距, 不干扰 h1 和 subtitle, 幂等(检测 hero-eyebrow 标记).
"""
import re
from pathlib import Path
ROOT = Path('.')

EYEBROW_ZH = ('<p class="hero-eyebrow" style="font-size:13px;letter-spacing:3px;'
              'opacity:.85;margin:0 0 10px;font-weight:500">各国寄中国专线</p>')
EYEBROW_EN = ('<p class="hero-eyebrow" style="font-size:13px;letter-spacing:3px;'
              'opacity:.85;margin:0 0 10px;font-weight:500;text-transform:uppercase">Shipping to China</p>')

MARK = 'hero-eyebrow'

def add_eyebrow(text, eyebrow_html):
    # 找 <section class="hero"...> ... <h1
    m = re.search(r'<section class="hero"[^>]*>', text)
    if not m:
        return text, False
    start = m.end()
    # 从 hero 开始找第一个 <h1
    h1 = re.search(r'<h1[ >]', text[start:])
    if not h1:
        return text, False
    insert_pos = start + h1.start()
    text = text[:insert_pos] + eyebrow_html + text[insert_pos:]
    return text, True

c_zh = c_en = 0
for d, eb in [('zh-cn', EYEBROW_ZH), ('en', EYEBROW_EN)]:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        if MARK in t:
            continue  # 已加过
        new_t, added = add_eyebrow(t, eb)
        if added:
            p.write_text(new_t, encoding='utf-8')
            if d == 'zh-cn':
                c_zh += 1
            else:
                c_en += 1

print(f'zh-cn 加 eyebrow: {c_zh} 页')
print(f'en 加 eyebrow: {c_en} 页')

# 验证
print('\n=== 验证 ===')
for f in ['zh-cn/index.html', 'en/index.html', 'en/contact.html']:
    p = ROOT / f
    if p.exists():
        t = p.read_text(encoding='utf-8', errors='ignore')
        print(f'{f}: {"含eyebrow ✅" if MARK in t else "无eyebrow"}')
