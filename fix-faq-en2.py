import re
from pathlib import Path

t = Path('en/faq.html').read_text(encoding='utf-8', errors='ignore')

# 可见区块 Q1 答案（美元+海运）
t = t.replace(
    '$4.50/kg (20kg+) air, $2.40/kg sea. From Japan/Korea/Europe: $3.80/kg air, $2.10/kg sea. From Australia/Canada: $4.20/kg air. From SE Asia: $3.50/kg air.',
    '¥100/kg (20-99kg), ¥90/kg (100kg+). From Japan/Korea/Europe: ¥90/kg, ¥80/kg. From Australia/Canada: ¥100/kg, ¥90/kg. From SE Asia: ¥80/kg, ¥70/kg.'
)

# 可见区块 Q2 21-100kg → 20-99kg
t = t.replace('our 21-100kg air tier — fast and cost-effective', 'our 20-99kg air tier — fast and cost-effective')

# 可见区块 Q3 体积重 ÷6000 → ÷5000 + 修破句
t = t.replace('÷ 6000. . The chargeable', '÷ 5000. The chargeable')
t = t.replace('weighs 12.5kg volumetric (air) — even if it only weighs 5kg actual, you\'ll be billed for 12.5kg',
              'weighs 25kg volumetric (air) — even if it only weighs 5kg actual, you\'ll be billed for 25kg')

Path('en/faq.html').write_text(t, encoding='utf-8')
print('✅ 可见区块残留补充替换完成')

# 最终残留检查
t2 = Path('en/faq.html').read_text(encoding='utf-8', errors='ignore')
print()
print('=== 最终残留检查 ===')
for tg in ['$4.50/kg', '$2.40/kg sea', '$3.80/kg', '$2.10/kg', '$4.20/kg', '$3.50/kg', '21-100kg', '÷ 6000', '12.5kg', '$10-30', 'For shipments over 50kg', '¥80/kg 起']:
    c = t2.count(tg)
    print(f'  {tg}: {c} 处 {"✅" if c == 0 else "❌"}')
