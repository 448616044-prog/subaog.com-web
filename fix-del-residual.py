"""删除剩余美元价(海运价 + 附加费 + 全包 + 小包裹), 用户指令"海运价删、其余删".

策略: 精确字符串替换, 删除价格数字, 保留通顺句子.
- 海运价: 删数字, 标注"已下架/仅空运"
- 附加费$30/全包$150-200/小包裹$12/1-20kg$12/kg: 删数字
"""
import re
from pathlib import Path
ROOT = Path('.')

# 每个 (old, new), 按文件精确替换
RULES = [
    # === 海运价 ===
    # zh-cn/index.html
    ('，50kg以上约$2-4/kg，门到门', '，门到门'),
    # zh-cn moving-season-sea-freight (FAQ + 正文)
    ('约 $3-5/kg 或 ¥45/kg（20kg+），含双清包税。对比空运省 40%。', '海运服务已下架，本渠道仅提供空运专线。'),
    ('空运 7-15 天到但贵（¥100/kg）；海运 但省 40%（$3-5/kg 或 ¥45/kg）。', '空运 10-15 个工作日到但贵（¥100/kg）；海运服务已下架。'),
    # en moving-season-sea-freight
    ('≈$3–5/kg or ¥45/kg (20kg+), tax-inclusive. About 40% cheaper than ai',
     'Sea freight discontinued — we only offer air freight. About 40% cheaper than ai'),
    ('sea but ~40% cheaper ($3–5/kg or ¥45/kg)', 'sea freight (discontinued)'),
    # usa-moving-to-china-guide
    ('约$800-1500/立方米。一个2-3人家庭的所有物品约10-15m³，总运费$8000-22500人民币。',
     '以客服估价为准。'),
    ('海运拼柜 $800-1500/m³ 4-5周', '海运拼柜（已下架）4-5周'),
    # usa-to-china-sea-freight
    ('费用 $800-1500/m³ 20尺$3000-6000 / 40尺$5000-9000', '费用 以客服估价为准（海运已下架）'),
    # usa-moving-to-china/index (zh-cn)
    ('海运拼柜 $800-1500/m³ 4-5周', '海运拼柜（已下架）4-5周'),
    # en usa-to-china-shipping-cost
    ('100kg+ drops $0.5-0.6/kg per tier. Sea: ~¥45/kg.', '100kg+ drops per tier. Sea freight discontinued.'),
    # en usa-moving-to-china/index: 1-20kg $12/kg
    ('1–20 kg $12/kg — Air', '20kg+ — Air'),

    # === 附加费 $30 ===
    ('偏远地区附加：$30 起（视地区）', '偏远地区附加：以客服确认为准'),
    ('偏远取件 $30 起', '偏远取件以客服确认为准'),

    # === 华人专线全包 $150-200 ===
    ('华人专线约 $150-200 全包', '华人专线双清包税门到门全包'),
    ('30kg 行李约 $150-200 全包', '30kg 行李双清包税门到门全包'),

    # === 日本小包裹 $12 起 ===
    ('，小包裹约 $12 起，可免费估价', '，可免费估价'),

    # === en japan index: all parcels start around $12 ===
    ('all parcels start around $12. Request a free quote fo', 'Request a free quote fo'),
]

total = 0
files = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        orig = t
        for old, new in RULES:
            if old in t:
                t = t.replace(old, new)
        if t != orig:
            p.write_text(t, encoding='utf-8')
            files += 1

print(f'删除处理 {files} 文件')

# 残留检查
print('\n=== 残留检查 ===')
leftover = ['$2-4/kg', '$3-5/kg', '$3–5/kg', '$800-1500', '$8000-22500', '¥45/kg',
            '$30 起', '$150-200', '$12 起', '$12/kg', '$0.5-0.6/kg']
for tg in leftover:
    cnt = 0
    for d in ['zh-cn', 'en']:
        for p in (ROOT / d).rglob('*.html'):
            cnt += p.read_text(encoding='utf-8', errors='ignore').count(tg)
    if cnt:
        print(f'  残留 {cnt:3d}  {tg}')
