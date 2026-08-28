"""补齐 86 个 zh-cn 城市×品类细分页缺失的 canonical + hreflang 三件套.

这些页面是建站批量生成时漏掉的半成品(缺 canonical/hreflang), 导致:
- Ahrefs 报 hreflang to redirect/broken (400)
- Missing reciprocal hreflang (400)
"""
import re
from pathlib import Path
ROOT = Path('.')

def build_meta(rel_path: str, lang: str):
    """根据文件相对路径构造 canonical + hreflang 三件套"""
    # rel_path 如 'usa-to-china/washington-dc/bicycles/index.html'
    parts = rel_path.split('/')
    if parts[-1] == 'index.html':
        dir_url = '/'.join(parts[:-1])  # usa-to-china/washington-dc/bicycles
        url = f'https://subaog.com/{lang}/{dir_url}/'
    else:
        url = f'https://subaog.com/{lang}/' + '/'.join(parts)
    return url

fixed = 0
for p in (ROOT / 'zh-cn').rglob('*.html'):
    t = p.read_text(encoding='utf-8', errors='ignore')
    if 'rel="canonical"' in t:
        continue  # 已有 canonical
    rel = str(p).replace('zh-cn/', '', 1)
    zh_url = build_meta(rel, 'zh-cn')
    en_rel = rel
    en_url = build_meta(rel, 'en')
    tags = (
        f'  <link rel="canonical" href="{zh_url}">\n'
        f'  <link rel="alternate" hreflang="zh-CN" href="{zh_url}">\n'
        f'  <link rel="alternate" hreflang="en" href="{en_url}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="{zh_url}">\n'
    )
    # 在 <title> 前插入
    if '<title>' in t:
        t = t.replace('<title>', tags + '  <title>', 1)
        p.write_text(t, encoding='utf-8')
        fixed += 1
    elif '<meta charset' in t:
        # 无 title 的兜底
        m = re.search(r'<meta charset[^>]*>', t)
        if m:
            t = t[:m.end()] + '\n' + tags + t[m.end():]
            p.write_text(t, encoding='utf-8')
            fixed += 1

print(f'补齐 {fixed} 页 canonical + hreflang')

# 验证
no_canon = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        if 'rel="canonical"' not in t:
            no_canon += 1
print(f'剩余缺 canonical: {no_canon}')
