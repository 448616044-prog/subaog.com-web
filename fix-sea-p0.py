import re
from pathlib import Path

ROOT = Path('.')

# 海运/搬家/对比主题页（保留海运概念，用户决策）
def is_theme(p):
    s = str(p).lower()
    return any(k in s for k in [
        'sea-freight', 'shipping-time', 'transit-time', 'moving-season', 'graduation',
        'usa-moving-to-china', 'how-to-choose-international-shipping', 'moving-to-china-guide',
    ])

REPLACES = [
    # 英文普通页海运残留 → 空运
    ('by sea', 'by air'),
    # 中文普通页走海运 → 走空运
    ('走海运', '走空运'),
    # sea freight 特殊形态
    ('Airsea freight', 'Air freight'),
    ('Air or sea freight', 'Air freight'),
    ('; sea freight .', ''),
    ('→ sea freight', '→ air freight'),
    (', sea freight', ', air freight'),
]

fixed = 0
skipped = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        if is_theme(p):
            skipped += 1
            continue
        t = p.read_text(encoding='utf-8', errors='ignore')
        orig = t
        for old, new in REPLACES:
            t = t.replace(old, new)
        if t != orig:
            p.write_text(t, encoding='utf-8')
            fixed += 1

print(f'海运清理: {fixed} 文件（跳过 {skipped} 个主题页）')

# 残留检查（排除主题页）
print()
print('=== 残留检查 ===')
for tg in ['by sea', '走海运', 'sea freight']:
    cnt = 0
    files = set()
    for d in ['zh-cn', 'en']:
        for p in (ROOT / d).rglob('*.html'):
            if is_theme(p):
                continue
            t = p.read_text(encoding='utf-8', errors='ignore')
            c = t.count(tg)
            if c:
                cnt += c
                files.add(str(p))
    print(f'  {tg}: {cnt} 处 / {len(files)} 文件')
    for f in list(files)[:5]:
        print(f'      {f}')
