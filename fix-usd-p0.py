import re
from pathlib import Path

ROOT = Path('.')

def is_sea_theme(p):
    s = str(p).lower()
    return any(k in s for k in ['sea-freight', 'shipping-time', 'transit-time', 'moving-season', 'graduation'])

# 替换规则（按顺序，先长后短，避免子串误伤）
# 注意：$5-8/lb、$5-8/磅 必须先于裸 $5-8 处理
REPLACE = [
    # en dash 变体
    ('$5–8/lb', '¥100/kg'),
    ('$5–8/磅', '¥100/kg'),
    # 带单位后缀
    ('$5-8/lb', '¥100/kg'),
    ('$5-8/磅', '¥100/kg'),
    ('$4-6/lb', '¥80/kg'),
    ('$4-6/磅', '¥80/kg'),
    # 小包裹
    ('$10 起', '¥100/kg 起'),
    # 冗余 $6/kg（前面已有 ¥100/kg）
    ('¥100/kg $6/kg', '¥100/kg'),
    # 裸 $5-8（表格，最后处理）
    ('$5-8', '¥100/kg'),
    # 裸 $4-6
    ('$4-6', '¥80/kg'),
]

total_fixed = 0
files_fixed = 0

for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        if is_sea_theme(p):
            continue
        t = p.read_text(encoding='utf-8', errors='ignore')
        orig = t
        for old, new in REPLACE:
            t = t.replace(old, new)
        if t != orig:
            p.write_text(t, encoding='utf-8')
            files_fixed += 1
            # 统计该文件替换了几处
            for old, new in REPLACE:
                total_fixed += orig.count(old)

print(f'美元价清理: {files_fixed} 文件, 约 {total_fixed} 处替换')

# 残留检查（只查自家价，排除竞品上下文）
print()
print('=== 残留检查（自家美元价）===')
for tg in ['$5-8', '$4-6/lb', '$6/kg', '$10 起', '$5–8']:
    cnt = 0
    files = set()
    for d in ['zh-cn', 'en']:
        for p in (ROOT / d).rglob('*.html'):
            if is_sea_theme(p):
                continue
            t = p.read_text(encoding='utf-8', errors='ignore')
            c = t.count(tg)
            if c:
                cnt += c
                files.add(str(p))
    if cnt:
        print(f'  {tg}: {cnt} 处 / {len(files)} 文件')
    else:
        print(f'  {tg}: 0 ✅')
