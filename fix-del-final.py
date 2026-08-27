import re
from pathlib import Path
ROOT = Path('.')

def fix(path, old, new):
    p = ROOT / path
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8', errors='ignore')
    if old in t:
        t = t.replace(old, new)
        p.write_text(t, encoding='utf-8')
        print(f'✅ {path}')

EN_DASH = '\u2013'
EM_DASH = '\u2014'

# en/moving-season 海运价 (en dash)
fix('en/blog/moving-season-sea-freight.html',
    f'sea but ~40% cheaper (${EN_DASH}3{EN_DASH}5/kg or ¥45/kg)',
    'sea freight (discontinued)')

# zh-cn 海运拼柜 $800-1500
for f in ['zh-cn/blog/usa-moving-to-china-guide.html',
          'zh-cn/usa-moving-to-china/index.html']:
    fix(f, '海运拼柜 $800-1500/m³', '海运拼柜（已下架）')

# zh-cn sea-freight 费用
fix('zh-cn/blog/usa-to-china-sea-freight.html',
    '费用 $800-1500/m³ 20尺$3000-6000 / 40尺$5000-9000',
    '费用 以客服估价为准（海运已下架）')

# en/usa-moving-to-china 1-20kg
fix('en/usa-moving-to-china/index.html',
    f'1{EN_DASH}20 kg $12/kg {EM_DASH} Air',
    f'20kg+ {EM_DASH} Air')

# 最终残留检查
print()
leftover = ['$2-4/kg', '$3-5/kg', f'$3{EN_DASH}5/kg', '$800-1500', '$8000-22500',
            '¥45/kg', '$30 起', '$150-200', '$12 起', '$12/kg', '$0.5-0.6/kg']
for tg in leftover:
    cnt = 0
    for d in ['zh-cn', 'en']:
        for p in (ROOT / d).rglob('*.html'):
            cnt += p.read_text(encoding='utf-8', errors='ignore').count(tg)
    if cnt:
        print(f'残留 {cnt}  {repr(tg)}')
print('=== 完成 ===')
