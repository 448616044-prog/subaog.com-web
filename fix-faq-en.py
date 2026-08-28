import re
from pathlib import Path

ROOT = Path('.')

p = ROOT / 'en/faq.html'
t = p.read_text(encoding='utf-8', errors='ignore')

# Q1 美元+海运 → 人民币3档+只空运
t = t.replace(
    'Pricing varies by origin region and weight. From the USA: $4.50/kg (20kg+) air, $2.40/kg sea. From Japan/Korea/Europe: $3.80/kg air, $2.10/kg sea. From Australia/Canada: $4.20/kg air. From SE Asia: $3.50/kg air. All prices include tax-inclusive customs clearance and door-to-door delivery. Get an exact quote via 在线客服.',
    'Pricing varies by origin region and weight, all tax-inclusive door-to-door. USA/Canada/Mexico/Australia/New Zealand: ¥100/kg (20-99kg), ¥90/kg (100kg+). Europe (UK/Germany/France/Italy/Spain/Ireland): ¥90/kg, ¥80/kg. Japan/Korea/Thailand/Singapore/Philippines/Taiwan/Malaysia: ¥80/kg, ¥70/kg. Plus ¥100 customs declaration fee per shipment. Minimum chargeable weight 20kg. Get an exact quote via 在线客服.'
)

# Q2 破句+美元 → 人民币
t = t.replace(
    'For shipments over 50kg. For small parcels under 2lb, USPS First-Class International starts around $10-30. For mid-size shipments (5-50kg), our consolidated air freight typically runs ¥80/kg 起. The sweet spot for most personal shipments is our 21-100kg air tier.',
    'For shipments over 20kg, our consolidated air freight is the cheapest tax-inclusive option: ¥100/kg from the USA (20kg+), ¥90/kg from Europe, ¥80/kg from Japan/Korea/SE Asia. For small parcels under 2lb, USPS First-Class International starts around $10-30 (slower, not tax-included). The sweet spot for most personal shipments is our 20-99kg air tier.'
)

# Q3 破句+时效不统一 → 10-15 工作日
t = t.replace(
    'Door-to-door: 10-15 working days for most routes. Breakdown: 7-10 days air transit + 1-2 days customs clearance + 1-3 days last-mile delivery. . SE Asia routes are faster at 5-8 working days. Christmas, Chinese New Year, and Golden Week can add 3-5 days — book ahead during these periods.',
    'Door-to-door: 10-15 working days for all routes. Breakdown: 7-10 days air transit + 1-2 days customs clearance + 1-3 days last-mile delivery. Christmas, Chinese New Year, and Golden Week can add 3-5 days — book ahead during these periods.'
)

# Q9 体积重 ÷6000 → ÷5000（红线）+ 修破句
t = t.replace(
    'Air freight volumetric weight = (length × width × height in cm) ÷ 6000. . The chargeable weight is whichever is greater: actual or volumetric. A box measuring 50×50×50cm weighs 12.5kg volumetric (air) — even if it only weighs 5kg actual, you\'ll be billed for 12.5kg.',
    'Air freight volumetric weight = (length × width × height in cm) ÷ 5000. The chargeable weight is whichever is greater: actual or volumetric. A box measuring 50×50×50cm weighs 25kg volumetric (air) — even if it only weighs 5kg actual, you\'ll be billed for 25kg.'
)

p.write_text(t, encoding='utf-8')
print('✅ en/faq.html 重写完成')

# 残留检查
t2 = p.read_text(encoding='utf-8', errors='ignore')
print()
print('=== en/faq.html 残留检查 ===')
for tg in ['$4.50/kg', '$2.40/kg sea', '$3.80/kg', '$2.10/kg', '$4.20/kg', '$3.50/kg', '21-100kg', '÷ 6000', 'sea', 'by sea']:
    c = t2.count(tg)
    print(f'  {tg}: {c} 处 {"✅" if c == 0 else "❌"}')
