#!/usr/bin/env python3
"""how-to-choose 对比页修复（zh-cn 严重破坏 + en 宣传海运）+ blog/index 卡片标题改空运。"""
def apply(f, repl):
    t = open(f, encoding='utf-8').read()
    for a, b in repl:
        c = t.count(a)
        if c == 0:
            print(f'  ❌ 未匹配 {f}: {a[:55]}')
        else:
            t = t.replace(a, b)
    open(f, 'w', encoding='utf-8').write(t)
    print(f'✅ {f}')

# ===== zh-cn how-to-choose（"海运→空运"机械替换导致的错乱）=====
apply('zh-cn/blog/how-to-choose-international-shipping-method.html', [
 ('空运vs空运vs邮政vs专线', '空运vs海运vs邮政vs专线'),
 ('国际快递选空运还是空运？', '国际快递选空运还是海运？'),
 ('空运快但贵、空运慢但便宜', '空运快但贵、海运慢但便宜（海运已下架）'),
 ('<tr><td>🚢 空运专线</td><td style="color:var(--green)">¥45-55/kg</td><td></td><td>50kg+超大件、不急</td><td>急用、食品</td></tr>',
  '<tr><td>🚢 海运</td><td style="color:var(--text-secondary)">已下架</td><td>—</td><td>—</td><td>—</td></tr>'),
 ('<p><strong>搬家回国（100kg+）</strong>→ 空运专线，¥45-55/kg，省钱为主不急</p>',
  '<p><strong>搬家回国（100kg+）</strong>→ 空运专线，¥90/kg（100kg+ 档），省钱为主不急</p>'),
 ('大件省钱选专线，小件方便选邮政，不急超省选空运，十万火急选FedEx/DHL。',
  '大件省钱选空运专线，小件方便选邮政，海运已下架，十万火急选FedEx/DHL。'),
 ('空运、空运、邮政、专线怎么选？', '空运、海运、邮政、专线怎么选？'),
 ('大件/搬家选空运（，最便宜）', '大件/搬家选空运专线（10-15 个工作日，双清包税）'),
 ('Q：什么情况选空运最划算？', 'Q：什么情况选空运专线最划算？'),
 ('搬家、家具、大批量行李（50kg以上）选空运，价格约空运的1/3。缺点是慢。不着急的选空运。',
  '搬家、家具、大批量行李（50kg以上）选空运专线，¥90-100/kg，10-15 个工作日，双清包税。海运已下架。'),
])

# ===== en how-to-choose（宣传海运 → 空运）=====
apply('en/blog/how-to-choose-international-shipping-method.html', [
 ('Air, sea, or express? The right choice depends on three things: weight, urgency, and item type.',
  'Air or express? The right choice depends on three things: weight, urgency, and item type. (Sea freight is discontinued.)'),
 ('Under 2kg → express or USPS. 2–50kg → consolidated air. 50kg+ → sea freight. Weight is the biggest cost driver.',
  'Under 2kg → express or USPS. 2–50kg → consolidated air. 50kg+ → consolidated air (sea freight discontinued). Weight is the biggest cost driver.'),
 ('Need it in days → express. Can wait 10–15 days → air. Can wait a month → sea. Slower almost always means cheaper.',
  'Need it in days → express. Can wait 10–15 days → air (our only line). Sea freight is discontinued.'),
 ('Fragile or time-sensitive → air. Bulky furniture → sea. High-value small items → express with insurance.',
  'Fragile or time-sensitive → air. Bulky furniture → air (10-15 working days). High-value small items → express with insurance.'),
])

# ===== blog/index 卡片标题改空运 =====
apply('en/blog/index.html', [
 ('USA to China Sea Freight', 'USA to China Air Freight'),
 ('Moving Back to China: Sea Freight Guide', 'Moving Back to China by Air'),
])
apply('zh-cn/blog/index.html', [
 ('美国海运回国全攻略：搬家/大件/商业货运怎么走海运', '美国寄中国空运全攻略：搬家/大件怎么走空运'),
 ('美国海运到中国完整指南：海运流程、拼柜vs整柜费用对比、时效多久、搬家回国走海运怎么操作。大件运输首选',
  '美国寄中国空运指南：空运价格、时效、搬家大件怎么寄（海运已下架）'),
])

print('\n完成')
