import re
from pathlib import Path

ROOT = Path('.')

# 公式描述 ÷6000 → ÷5000（红线），保留对比避坑内容
REPLACES = [
    ('长×宽×高(cm) ÷ 6000', '长×宽×高(cm) ÷ 5000'),
    ('长×宽×高(cm)÷6000', '长×宽×高(cm)÷5000'),
    ('长×宽×高÷6000', '长×宽×高÷5000'),
    ('L×W×H (cm) ÷ 6000', 'L×W×H (cm) ÷ 5000'),
    ('L×W×H(cm)÷6000', 'L×W×H(cm)÷5000'),
    ('L×W×H÷6000', 'L×W×H÷5000'),
    ('width × height (cm) ÷ 6000', 'width × height (cm) ÷ 5000'),
    ('÷ 6000（部分渠道 ÷5000）', '÷ 5000'),
    ('÷ 6000 (some carriers use ÷5000)', '÷ 5000'),
    ('60,000÷6,000', '60,000÷5,000'),
    # 快递附加费美元价 → 删
    ('Express surcharge: +$1.20/kg.', 'Express surcharge applies.'),
]

fixed = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        orig = t
        for old, new in REPLACES:
            t = t.replace(old, new)
        if t != orig:
            p.write_text(t, encoding='utf-8')
            fixed += 1

print(f'÷6000→÷5000 + 附加费清理: {fixed} 文件')

# 残留检查
print()
print('=== 残留检查 ===')
for tg in ['÷6000', '÷ 6000', '+$1.20/kg', '÷6,000']:
    cnt = 0
    files = set()
    for d in ['zh-cn', 'en']:
        for p in (ROOT / d).rglob('*.html'):
            t = p.read_text(encoding='utf-8', errors='ignore')
            c = t.count(tg)
            if c:
                cnt += c
                files.add(str(p))
    print(f'  {tg}: {cnt} 处 / {len(files)} 文件')
    for f in list(files)[:5]:
        print(f'      {f}')
