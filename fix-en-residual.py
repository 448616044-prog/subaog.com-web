"""修复英文站"删海运"历史遗留的正文破句 + student-luggage 价格表破损。

背景: 之前 fix-sea-usd.py 删海运时, 把 "Air or sea" / "Air & sea" / "X days. Sea takes Y days"
等句子里的 sea 部分删掉, 留下破句。当时只回退了 18 个海运主题页, 大量非海运页(城市页/国家页)
的正文破句未修复。

修复规则(仅非海运主题页):
  1. "Air or ." / "Air & ." / "Air & ," -> "Air"
  2. "days. ." -> "days."
  3. "; sea ." -> ""
  4. ", sea ." -> ""
  5. "Sea freightkg" -> "" (删掉整段 "Sea freight $X/kg" 残句)
"""
import re
from pathlib import Path
ROOT = Path('.')

def is_sea_theme(p):
    s = str(p).lower()
    return any(k in s for k in ['sea-freight', 'shipping-time', 'transit-time',
                                'moving-season', 'graduation'])

# 通用破句修复规则 (顺序敏感)
RULES = [
    (r'Air or\s*\.', 'Air'),
    (r'Air &\s*,?', 'Air'),
    (r'Air &\s*\.', 'Air'),
    (r'Air&\s*,?', 'Air'),
    (r'days?\.\s*\.', 'days.'),
    (r';\s*[Ss]ea\s*\.', ''),
    (r',\s*[Ss]ea\s*\.', ''),
    (r'[Ss]ea\s+freight\s*kg[^<]*', ''),  # "Sea freightkg" 残句
    (r'[Ss]ea\s+freight\s*[¥$]?[0-9.]*/kg', ''),  # "Sea freight $5.5/kg" 残句
]

fixed_files = 0
total_subs = 0
for d in ['en']:
    for p in (ROOT / d).rglob('*.html'):
        if is_sea_theme(p):
            continue
        t = p.read_text(encoding='utf-8', errors='ignore')
        orig = t
        for pat, rep in RULES:
            t = re.sub(pat, rep, t)
        if t != orig:
            p.write_text(t, encoding='utf-8')
            fixed_files += 1
            total_subs += 1

print(f'[全站破句] 修复 {fixed_files} 文件')

# === student-luggage en 页精修 ===
print('\n=== student-luggage en 页精修 ===')
sp = ROOT / 'en' / 'student-luggage' / 'index.html'
t = sp.read_text(encoding='utf-8', errors='ignore')

# 1) 价格表重写 (破损 -> 3档人民币)
new_table = (
    '<table class="price-table">\n'
    '        <thead><tr><th>Origin</th><th>20-99kg</th><th>100kg+</th></tr></thead>\n'
    '        <tbody>\n'
    '          <tr><td>USA / Canada / Mexico / Australia / New Zealand</td><td><strong>¥100/kg</strong></td><td><strong>¥90/kg</strong></td></tr>\n'
    '          <tr><td>UK / Germany / France / Italy / Spain / Ireland + Europe</td><td><strong>¥90/kg</strong></td><td><strong>¥80/kg</strong></td></tr>\n'
    '          <tr><td>Japan / Korea / Thailand / Singapore / Philippines / Taiwan / Malaysia</td><td><strong>¥80/kg</strong></td><td><strong>¥70/kg</strong></td></tr>\n'
    '        </tbody>\n'
    '      </table>'
)
t = re.sub(r'<table class="price-table">.*?</table>', new_table, t, count=1, flags=re.S)

# 2) info-card 价格: 单档 -> 3档
old_card = ('<div class="info-card"><div class="big">¥80/kg (21kg+), ¥70/kg (100kg+) — '
            'luggage line, tax-inclusive (2026-6-30)</div><div class="label">Air freight /kg (21kg+)</div></div>')
new_card = ('<div class="info-card"><div class="big">¥100–70/kg</div>'
            '<div class="label">By origin · 21kg+ · tax-inclusive</div></div>')
t = t.replace(old_card, new_card)

# 3) section-title 副标 "Air & ," -> "Air freight,"
t = t.replace('Air & , tax-inclusive, no hidden fees',
              'Air freight, tax-inclusive, no hidden fees')

# 4) step "Air or ." -> "Air freight"
t = t.replace('<p>Air or .</p>', '<p>Air freight (10–15 working days)</p>')

# 5) FAQ 破句
t = t.replace('Air freight from about ¥70/kg (21kg+). kg. Student discounts apply during graduation season — ask for a quote.',
              'Air freight from ¥100/kg (21kg+), ¥90/kg (100kg+). Student discounts apply during graduation season — ask for a quote.')
t = t.replace('Air freight takes 10–15 working days. .',
              'Air freight takes 10–15 working days.')

# 6) 其他 info-grid 里的旧价 "¥80/kg (21kg+), ¥70/kg (100kg+) — luggage line"
t = t.replace('¥80/kg (21kg+), ¥70/kg (100kg+) — luggage line, tax-inclusive (2026-6-30)',
              '¥100–70/kg by origin, tax-inclusive')

sp.write_text(t, encoding='utf-8')
print('  ✅ student-luggage 价格表+info-card+FAQ 修复')

# 验证
print('\n=== 复验 ===')
t2 = sp.read_text(encoding='utf-8', errors='ignore')
print('  价格表 \$ 残留:', t2.count('$10/kg') + t2.count('$6/kg'))
print('  破句 Air or .:', t2.count('Air or .'))
print('  破句 days. .:', t2.count('days. .'))
print('  Sea 残留:', t2.count('Sea '))
print('  新价 ¥100:', t2.count('¥100'))
