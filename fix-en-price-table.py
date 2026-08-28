import re
from pathlib import Path

ROOT = Path('.')

# 8 个 en 国家集群页的正确档位价（红线）
TIERS = {
    'en/usa-to-china/index.html': ('¥100/kg', '¥90/kg'),
    'en/canada-to-china/index.html': ('¥100/kg', '¥90/kg'),
    'en/australia-to-china/index.html': ('¥100/kg', '¥90/kg'),
    'en/usa-moving-to-china/index.html': ('¥100/kg', '¥90/kg'),
    'en/europe-to-china/index.html': ('¥90/kg', '¥80/kg'),
    'en/japan-to-china/index.html': ('¥80/kg', '¥70/kg'),
    'en/korea-to-china/index.html': ('¥80/kg', '¥70/kg'),
    'en/seasia-to-china/index.html': ('¥80/kg', '¥70/kg'),
}

def build_table(price1, price2):
    return (
        '<table class="price-table">\n'
        '  <thead><tr><th>Weight</th><th>Air freight (all-inclusive)</th></tr></thead>\n'
        '  <tbody>\n'
        f'    <tr><td style="font-weight:600">20–99 kg</td><td>{price1}</td></tr>\n'
        f'    <tr><td style="font-weight:600">100 kg+</td><td>{price2}</td></tr>\n'
        '  </tbody>\n'
        '</table>'
    )

fixed = 0
for path, (p1, p2) in TIERS.items():
    p = ROOT / path
    if not p.exists():
        print(f'  MISSING {path}')
        continue
    t = p.read_text(encoding='utf-8', errors='ignore')
    new_table = build_table(p1, p2)
    t2, n = re.subn(r'<table class="price-table">.*?</table>', new_table, t, flags=re.S)
    if n:
        p.write_text(t2, encoding='utf-8')
        fixed += 1
        print(f'  ✅ {path}: {p1}/{p2}')
    else:
        print(f'  ⚠️ {path}: 未匹配到 price-table')

print(f'\n重建 {fixed}/8 个价格表')
