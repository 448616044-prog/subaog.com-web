import re
from pathlib import Path
ROOT = Path('.')

EN = '\u2013'
EM = '\u2014'

# 正则删除规则 (顺序敏感)
# 1) 海运价 $3-5/kg or ¥45/kg (hyphen 或 en dash)
RE_SEA_PRICE = re.compile(r'\$3[-\u2013]5/kg\s+or\s+¥45/kg')

# 2) $800-1500/m³
RE_CONTAINER = re.compile(r'\$800-1500/m³')

# 3) 20尺$3000-6000 / 40尺$5000-9000
RE_FEET = re.compile(r'20尺\$3000-6000\s*/\s*40尺\$5000-9000')

# 4) $12/kg
RE_12KG = re.compile(r'\$12/kg')

# 5) 1-20 kg (en dash)
RE_1_20 = re.compile(r'1[-\u2013]20\s*kg\s*\$12/kg')

def clean_file(p):
    t = p.read_text(encoding='utf-8', errors='ignore')
    orig = t
    t = RE_SEA_PRICE.sub('', t)
    t = RE_CONTAINER.sub('', t)
    t = RE_FEET.sub('', t)
    t = RE_1_20.sub('20kg+', t)
    t = RE_12KG.sub('', t)
    # 清理空括号 ( ) 和 空的价格描述
    t = t.replace('cheaper ()', 'cheaper')
    t = t.replace('（已下架） $', '（已下架） ')
    t = t.replace('</td><td></td>', '</td><td>已下架</td>')
    t = t.replace('  ', ' ')
    if t != orig:
        p.write_text(t, encoding='utf-8')
        return True
    return False

targets = [
    'en/blog/moving-season-sea-freight.html',
    'zh-cn/blog/usa-to-china-sea-freight.html',
    'zh-cn/blog/usa-moving-to-china-guide.html',
    'zh-cn/usa-moving-to-china/index.html',
    'en/usa-moving-to-china/index.html',
    'en/blog/usa-to-china-shipping-cost.html',
    'zh-cn/blog/usa-to-china-shipping-cost.html',
]
for tp in targets:
    if clean_file(ROOT / tp):
        print(f'✅ {tp}')

# 最终残留检查
print('\n=== 残留 ===')
leftover = ['$2-4/kg', '$3-5/kg', f'$3{EN}5/kg', '$800-1500', '$8000-22500',
            '¥45/kg', '$30 起', '$150-200', '$12 起', '$12/kg', '$0.5-0.6/kg']
any_left = False
for tg in leftover:
    cnt = 0
    for d in ['zh-cn', 'en']:
        for p in (ROOT / d).rglob('*.html'):
            cnt += p.read_text(encoding='utf-8', errors='ignore').count(tg)
    if cnt:
        print(f'残留 {cnt}  {repr(tg)}')
        any_left = True
if not any_left:
    print('全部清零 ✅')
