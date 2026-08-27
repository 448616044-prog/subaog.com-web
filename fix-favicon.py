"""注入 favicon (使用现有 logo.png) 到全站 HTML 页面."""
import re
from pathlib import Path
ROOT = Path('.')

# 注入/替换 <head> 中的 favicon link
FAVICON_LINK = '<link rel="icon" type="image/png" href="/assets/images/logo.png">\n  '

# 匹配三种情况:
# 1) 已有 favicon 的 - rel=icon 或 rel="shortcut icon" - 替换
# 2) 没有 favicon - 在 <meta charset=...> 之后插入
# 3) 已有 apple-touch-icon - 也补一条 icon

RE_ICON = re.compile(r'<link rel="(icon|shortcut icon)"[^>]*>\n?\s*', re.I)
RE_AFTER_CHARSET = re.compile(r'(<meta charset="[^"]+"[^>]*>)')

c_added = c_replaced = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        orig = t
        # 检查是否已有 rel="icon"
        has_icon = bool(re.search(r'<link rel="(icon|shortcut icon)"', t, re.I))
        if has_icon:
            # 替换为标准 PNG
            t = RE_ICON.sub(FAVICON_LINK, t, count=1)
            if t != orig:
                c_replaced += 1
        else:
            # 没有 favicon, 在 charset meta 之后插入
            if RE_AFTER_CHARSET.search(t):
                t = RE_AFTER_CHARSET.sub(r'\1\n  ' + FAVICON_LINK.rstrip(), t, count=1)
                c_added += 1
        if t != orig:
            p.write_text(t, encoding='utf-8')

print(f'[favicon] 新增 {c_added} 页, 替换 {c_replaced} 页')

# 验证
print('\n=== 验证 ===')
no_fav = 0
total_fav = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        if '<link rel="icon"' in t or '<link rel="shortcut icon"' in t:
            total_fav += 1
        else:
            no_fav += 1
print(f'有 favicon: {total_fav} 页')
print(f'无 favicon: {no_fav} 页')
