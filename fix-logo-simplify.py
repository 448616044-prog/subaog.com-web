"""调整 logo 显示为台湾站风格: 移除副标 span 和竖线, 只留图片 logo.
之前结构: <a ...><img><span...>各国寄中国专线</span></a>
之后结构: <a ...><img></a>  (跟台湾站 subao.tw 一致)
"""
import re
from pathlib import Path
ROOT = Path('.')

# 精确匹配当前的 logo 锚点（含副标和左竖线）
LOGO_RE_ZH = re.compile(
    r'<a href="/zh-cn/" style="display:flex;align-items:center;gap:12px;" class="logo">'
    r'<img src="/assets/images/logo\.png" alt="速豹回国物流" style="height:55px;width:auto;display:block;">'
    r'<span style="font-size:14px;color:var\(--primary\);font-weight:600;'
    r'border-left:2px solid var\(--primary-light\);padding-left:14px;'
    r'line-height:1\.2;letter-spacing:0\.5px">各国寄中国专线</span>'
    r'</a>'
)
LOGO_RE_EN = re.compile(
    r'<a href="/en/" style="display:flex;align-items:center;gap:12px;" class="logo">'
    r'<img src="/assets/images/logo\.png" alt="Subao Global" style="height:55px;width:auto;display:block;">'
    r'<span style="font-size:14px;color:var\(--primary\);font-weight:600;'
    r'border-left:2px solid var\(--primary-light\);padding-left:14px;'
    r'line-height:1\.2;letter-spacing:0\.5px">Shipping to China</span>'
    r'</a>'
)

NEW_LOGO_ZH = ('<a href="/zh-cn/" class="logo">'
               '<img src="/assets/images/logo.png" alt="速豹回国物流" '
               'style="height:50px;width:auto;display:block;" '
               'fetchpriority="high" decoding="async"></a>')
NEW_LOGO_EN = ('<a href="/en/" class="logo">'
               '<img src="/assets/images/logo.png" alt="Subao Global" '
               'style="height:50px;width:auto;display:block;" '
               'fetchpriority="high" decoding="async"></a>')

c_zh = c_en = 0
for p in (ROOT / 'zh-cn').rglob('*.html'):
    t = p.read_text(encoding='utf-8', errors='ignore')
    new_t = LOGO_RE_ZH.sub(NEW_LOGO_ZH, t)
    if new_t != t:
        p.write_text(new_t, encoding='utf-8')
        c_zh += 1
for p in (ROOT / 'en').rglob('*.html'):
    t = p.read_text(encoding='utf-8', errors='ignore')
    new_t = LOGO_RE_EN.sub(NEW_LOGO_EN, t)
    if new_t != t:
        p.write_text(new_t, encoding='utf-8')
        c_en += 1
print(f'zh-cn 改 {c_zh} 页, en 改 {c_en} 页')

# 验证
print('\n=== 验证 ===')
residual = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        # 残留 logo 副标
        if 'class="logo"' in t:
            for m in re.finditer(r'<a [^>]*class="logo"[^>]*>.{0,500}?</a>', t, re.S):
                if '各国寄中国专线' in m.group(0) or 'Shipping to China' in m.group(0):
                    residual += 1
                    break
print(f'logo 残留副标页面数: {residual}')
