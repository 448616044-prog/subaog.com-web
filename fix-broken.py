import re
from pathlib import Path

ROOT = Path('.')

def is_sea_theme(p):
    s = str(p).lower()
    return any(k in s for k in ['sea-freight', 'shipping-time', 'transit-time', 'moving-season', 'graduation'])

# 破句修复规则（删海运残留）
REPLACES = [
    # 通用FAQ破句：大件/搬家走，→ 大件/搬家也走空运
    ('大件/搬家走，本页有详细对比', '大件/搬家也走空运，本页有详细对比'),
    # 通用FAQ破句 + 旧价：空运约¥80/kg（20kg起），kg，可免费估价 → ¥80-100/kg
    ('空运约 ¥80/kg（20kg 起），kg，可免费估价', '空运约 ¥80-100/kg（20kg 起），可免费估价'),
    # en consolidated 破句
    ('consolidated .', 'consolidated air freight'),
    # 需拆装，走。 → 需拆装，走空运。
    ('需拆装，走。', '需拆装，走空运。'),
    # 需拆装，走， → 需拆装，走空运，
    ('需拆装，走，', '需拆装，走空运，'),
]

fixed = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        if is_sea_theme(p):
            continue
        t = p.read_text(encoding='utf-8', errors='ignore')
        orig = t
        for old, new in REPLACES:
            t = t.replace(old, new)
        if t != orig:
            p.write_text(t, encoding='utf-8')
            fixed += 1

print(f'破句修复: {fixed} 文件')

# 残留检查
print()
print('=== 残留检查 ===')
for tg in ['大件/搬家走，', '，kg，可免费估价', 'consolidated .', '需拆装，走。', '需拆装，走，']:
    cnt = 0
    for d in ['zh-cn', 'en']:
        for p in (ROOT / d).rglob('*.html'):
            if is_sea_theme(p):
                continue
            cnt += p.read_text(encoding='utf-8', errors='ignore').count(tg)
    print(f'  {tg}: {cnt} 处 {"✅" if cnt == 0 else "❌"}')
