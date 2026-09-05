#!/usr/bin/env python3
"""海运主题页 → 空运诚实承接页改造（4 文件，中英各 2）。
保留 sea freight/海运 词承接搜索，正文明确「海运已下架→只提供空运」，
修复空白数字、错乱文案、美元价残留。"""
import re

def apply(f, repl, regex=()):
    t = open(f, encoding='utf-8').read()
    orig = t
    total = 0
    for a, b in repl:
        c = t.count(a)
        if c == 0:
            print(f'  ❌ 未匹配: {f} :: {a[:60]}')
        else:
            t = t.replace(a, b)
            total += c
    for pat, sub in regex:
        t2, n = re.subn(pat, sub, t)
        if n == 0:
            print(f'  ❌ 正则未匹配: {f} :: {pat[:60]}')
        else:
            t = t2
            total += n
    open(f, 'w', encoding='utf-8').write(t)
    print(f'✅ {f} 替换 {total} 处 ({len(orig)}->{len(t)} bytes)')

# ============ 1. en/blog/usa-to-china-sea-freight.html ============
fix_en_usa_sea = [
    ('<title>USA to China Sea Freight: Costs & Timeline (2026) | Subao Global</title>',
     '<title>Sea Freight to China? We Now Ship by Air (10-15 Days) | Subao Global</title>'),
    ('<meta property="og:title" content="USA to China Sea Freight: Costs & Timeline (2026) | Subao Global">',
     '<meta property="og:title" content="Sea Freight to China? We Now Ship by Air (10-15 Days) | Subao Global">'),
    ('"headline": "USA to China Sea Freight"',
     '"headline": "USA to China Air Freight"'),
    ('<h1>USA to China Sea Freight</h1>',
     '<h1>USA to China Air Freight (Sea Freight Discontinued)</h1>'),
    ('<p class="subtitle">Sea freight is the cheapest way to move large volumes from the USA to China — if you can wait .</p>',
     '<p class="subtitle">Sea freight to China has been discontinued — we now ship by air only, 10-15 working days door-to-door.</p>'),
    ('What does sea freight cost?</h2>', 'What does air freight cost?</h2>'),
    ('Sea freight starts at about  for shipments over 20kg. For full moves and furniture, per-kg rates drop further with volume.',
     'Air freight is tax-inclusive: ¥100/kg (US/CA/MX/AU/NZ tier), ¥90/kg (Europe tier), ¥80/kg (Asia tier) for 20-99kg; 100kg+ drops to ¥90/¥80/¥70. Minimum 20kg.'),
    ('How long does sea freight take?</h2>', 'How long does air freight take?</h2>'),
    ('line-height:1.8"> door-to-door, including US pickup, ocean transit, China customs, and final delivery. Air freight is 10–15 days for comparison.',
     'line-height:1.8"> 10-15 working days door-to-door, including US pickup, air transit, China customs, and final delivery.'),
    ('When to choose sea freight</h2>', 'Why we ship by air (sea discontinued)</h2>'),
    ('Choose sea freight for furniture, household goods, bulk books, and anything heavy where you don\'t need speed. Air freight wins when time matters.',
     'We discontinued sea freight and now ship everything by air: furniture, household goods, and bulk items all go air consolidated from 20kg — 10-15 working days, tax-inclusive.'),
    ('> door-to-door. Air freight is 10–15 days.', '> 10-15 working days door-to-door.'),
    ('Is air freight cheaper than air?', 'Is air freight more expensive than sea?'),
    ('Yes — roughly 40% cheaper per kg for large shipments.',
     'Yes, air costs more per kg than sea — but sea freight is discontinued, so air (10-15 working days) is now the only option.'),
    ('"name": "Blog/Usa To China Sea Freig"', '"name": "Blog/Air Freight To China"'),
]
fix_en_usa_sea_regex = [
    (r'<meta name="description" content="[^"]*">',
     '<meta name="description" content="Sea freight to China has been discontinued — we now ship by air only: 10-15 working days, tax-inclusive from ¥90/kg, from 20kg minimum.">'),
    (r'<meta property="og:description" content="[^"]*">',
     '<meta property="og:description" content="Sea freight to China has been discontinued — we now ship by air only: 10-15 working days, tax-inclusive.">'),
    (r'"description": "Air freight from the USA to China[^"]*"',
     '"description": "Sea freight to China is discontinued — we now ship by air only (10-15 working days, tax-inclusive)."'),
]

# ============ 2. zh-cn/blog/usa-to-china-sea-freight.html ============
fix_zh_usa_sea = [
    ('<title>美国海运回国全攻略2026：流程、费用、时效一次讲透 | 速豹国际</title>',
     '<title>美国寄中国空运攻略2026：费用、时效一次讲透（海运已停）| 速豹国际</title>'),
    ('<meta name="description" content="美国海运到中国完整指南：海运流程、拼柜vs整柜费用对比、时效多久、搬家回国走海运怎么操作。大件运输首选">',
     '<meta name="description" content="美国寄中国现已只提供空运（10-15个工作日）：空运价格、时效、搬家大件怎么寄。海运已下架，改走空运更快更省心">'),
    ('<meta property="og:title" content="美国海运回国全攻略2026：流程、费用、时效一次讲透 | 速豹国际">',
     '<meta property="og:title" content="美国寄中国空运攻略2026：费用、时效一次讲透（海运已停）| 速豹国际">'),
    ('<meta property="og:description" content="美国海运到中国完整指南：海运流程、拼柜vs整柜费用对比、时效多久、搬家回国走海运怎么操作。大件运输首选。...">',
     '<meta property="og:description" content="美国寄中国现已只提供空运（10-15个工作日）：空运价格、时效、搬家大件怎么寄。海运已下架，改走空运更快更省心。...">'),
    ('"name":"美国海运回国全攻略：搬家/大件/商业货运怎么走海运"',
     '"name":"美国寄中国空运全攻略：搬家/大件怎么走空运"'),
    ('<h1>美国海运回国全攻略：搬家/大件/商业货运怎么走海运</h1>',
     '<h1>美国寄中国空运全攻略：海运已下架，改走空运</h1>'),
    ('<p class="subtitle">拼柜 vs 整柜、费用计算、时效说明——全部讲清楚</p>',
     '<p class="subtitle">空运费用、时效、搬家大件怎么寄——一次讲透</p>'),
    ('<p>东西太多空运太贵？搬家回国或者商业货运，海运是最经济的选择。但海运流程相对复杂，这篇帮你搞清楚。</p>',
     '<p>海运已下架，我们现在只提供空运（10-15 个工作日门到门）。这篇讲清楚空运的费用、时效和搬家大件怎么寄。</p>'),
    ('<h2>一、拼柜(LCL) vs 整柜(FCL)</h2><div class="table-wrap"><table><tr><th></th><th>拼柜 LCL</th><th>整柜 FCL</th></tr><tr><td>适合</td><td>1-15m³</td><td>15m³以上</td></tr><tr><td>费用</td><td>已下架</td><td></td></tr><tr><td>时效</td><td>稍慢(等拼柜)</td><td>较快</td></tr></table></div>',
     '<h2>一、空运价格（三档）</h2><div class="table-wrap"><table><tr><th>区域</th><th>20-99kg</th><th>100kg+</th></tr><tr><td>美/加/墨/澳/新</td><td>¥100/kg</td><td>¥90/kg</td></tr><tr><td>欧洲</td><td>¥90/kg</td><td>¥80/kg</td></tr><tr><td>日/韩/泰/新/菲/台/马</td><td>¥80/kg</td><td>¥70/kg</td></tr></table></div>'),
    ('<h2>二、海运流程</h2><ol><li>联系客服评估货物量</li><li>预约上门取件或自行送货到仓库</li><li>专业包装（打木架/缠绕膜）</li><li>装柜上船</li><li>海上运输15-20天</li><li>到港清关3-5天</li><li>国内派送到家</li></ol>',
     '<h2>二、空运流程</h2><ol><li>联系客服评估货物量</li><li>预约上门取件或自行送货到仓库</li><li>专业包装（打木架/缠绕膜）</li><li>装机起飞</li><li>空运运输（10-15 个工作日）</li><li>清关（双清包税）</li><li>国内派送到家</li></ol>'),
    ('<h2>三、海运比空运省多少？</h2><p>以100lb（约45kg）为例：空运$450-750，海运。省50-70%。货物越重越划算。</p>',
     '<h2>三、空运价格怎么算？</h2><p>以 45kg 为例：美/加/墨/澳/新 ¥100/kg = ¥4,500（20-99kg 档），双清包税门到门。按实重或体积重（长×宽×高÷5000）取大者计费，最低 20kg 起运。</p>'),
    ('<h3>需要海运服务？</h3>', '<h3>需要空运服务？</h3>'),
    ('<p>空运/海运/快递全方位对比</p>', '<p>空运专线全方位对比</p>'),
]
fix_zh_usa_sea_regex = [
    (r'"headline":"美国空运回国全攻略[^"]*"',
     '"headline":"美国寄中国空运全攻略：搬家/大件怎么走空运"'),
    (r'"description":"美国空运到中国完整指南[^"]*"',
     '"description":"美国寄中国现已只提供空运（10-15个工作日）：空运价格、时效、搬家大件怎么寄。海运已下架，改走空运。"'),
]

# ============ 3. en/blog/moving-season-sea-freight.html ============
fix_en_moving = [
    ('<title>Moving Back to China: Sea Freight Guide (2026) | Subao Global</title>',
     '<title>Moving Back to China by Air (Sea Freight Discontinued) | Subao Global</title>'),
    ('<meta property="og:title" content="Moving Back to China: Sea Freight Guide (2026) | Subao Global">',
     '<meta property="og:title" content="Moving Back to China by Air (Sea Freight Discontinued) | Subao Global">'),
    ('"headline": "Moving Back to China: Sea Freight Guide"',
     '"headline": "Moving Back to China by Air"'),
    ('"name": "Blog/Moving Season Sea Freig"', '"name": "Blog/Moving Season Air Freight"'),
    ('<h1>Moving Back to China: Sea Freight Guide</h1>',
     '<h1>Moving Back to China by Air (Sea Freight Discontinued)</h1>'),
    ('<p class="subtitle">Moving back to China by sea: sea vs air cost comparison, furniture/appliance packing, volumetric weight, customs rules, and money-saving tips.</p>',
     '<p class="subtitle">Sea freight has been discontinued — move back to China by air: 10-15 working days, furniture/appliance packing, volumetric weight, and customs rules.</p>'),
    ('<h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">Sea vs air for moving</h2><p style="color:var(--text-secondary);line-height:1.9">Air 7–15 days but pricier (¥80–11/kg); sea but ~40% cheaper. Furniture and appliances go by sea; urgent small luggage by air.</p>',
     '<h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">Air vs sea for moving</h2><p style="color:var(--text-secondary);line-height:1.9">Air takes 10-15 working days and is tax-inclusive (¥100/kg US tier, ¥90/kg Europe, ¥80/kg Asia). Sea freight is discontinued — everything now ships by air, including furniture and appliances.</p>'),
    ('4) Sea transit → 5) Tax-inclusive clearance',
     '4) Air transit (10-15 working days) → 5) Tax-inclusive clearance'),
    ('<p style="font-size:13px;color:var(--text-secondary);margin-top:4px">Sea freight moving line: furniture, appliances, tax-inclusive</p>',
     '<p style="font-size:13px;color:var(--text-secondary);margin-top:4px">Air freight moving line: furniture, appliances, tax-inclusive, 10-15 working days</p>'),
]
fix_en_moving_regex = [
    (r'<meta name="description" content="[^"]*">',
     '<meta name="description" content="Moving back to China by air: sea freight has been discontinued, 10-15 working days door-to-door, furniture/appliance packing, volumetric weight, customs rules | 12+.">'),
    (r'<meta property="og:description" content="[^"]*">',
     '<meta property="og:description" content="Moving back to China by air: sea freight discontinued, 10-15 working days, furniture/appliance packing, volumetric weight, customs rules.">'),
    (r'"description": "Moving back to China by sea[^"]*"',
     '"description": "Moving back to China by air: sea freight discontinued, 10-15 working days, furniture/appliance packing, volumetric weight, customs rules."'),
]

# ============ 4. zh-cn/blog/moving-season-sea-freight.html ============
fix_zh_moving = [
    ('<title>搬家回国海运攻略 2026｜家具家电怎么运最省</title>',
     '<title>搬家回国空运攻略 2026｜家具家电怎么运回国（海运已停）</title>'),
    ('<meta name="description" content="搬家回国海运全流程：海运 vs 空运费用对比、家具家电打包、体积重怎么算、海关限制、省钱技巧，华人搬家回国必看">',
     '<meta name="description" content="搬家回国空运全流程（海运已下架）：空运费用 10-15 个工作日、家具家电打包、体积重怎么算、海关限制、省钱技巧">'),
    ('<meta property="og:title" content="搬家回国海运全攻略">',
     '<meta property="og:title" content="搬家回国空运全攻略（海运已停）">'),
    ('<meta property="og:description" content="搬家回国海运全流程：海运 vs 空运费用对比、家具家电打包、体积重怎么算、海关限制、省钱技巧，华人搬家回国必看">',
     '<meta property="og:description" content="搬家回国空运全流程（海运已下架）：空运费用 10-15 个工作日、家具家电打包、体积重怎么算、海关限制、省钱技巧">'),
    ('"name": "搬家回国海运全攻略"', '"name": "搬家回国空运全攻略"'),
    ('<h1>搬家回国海运全攻略</h1>', '<h1>搬家回国空运全攻略（海运已下架）</h1>'),
    ('<p class="subtitle">搬家回国海运全流程：海运 vs 空运费用对比、家具家电打包、体积重怎么算、海关限制、省钱技巧，华人搬家回国必看 | 速豹回国物流</p>',
     '<p class="subtitle">海运已下架，搬家回国改走空运：10-15 个工作日门到门，家具家电打包、体积重怎么算、海关限制、省钱技巧一次讲透</p>'),
    ('<h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">海运 vs 空运搬家</h2><p style="color:var(--text-secondary);line-height:1.9">空运 10-15 个工作日到但贵（¥100/kg）；海运服务已下架。家具家电大件必选海运；着急的小件行李才空运。</p>',
     '<h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">空运 vs 海运搬家</h2><p style="color:var(--text-secondary);line-height:1.9">空运 10-15 个工作日门到门，双清包税（¥100/kg 美加墨澳新、¥90/kg 欧洲、¥80/kg 亚洲）。海运已下架，家具家电大件现在也全部走空运。</p>'),
    ('④ 海运  → ⑤ 清关（双清包税）', '④ 空运（10-15 个工作日） → ⑤ 清关（双清包税）'),
    ('<p style="font-size:13px;color:var(--text-secondary);margin-top:4px">搬家海运回国专线：家具家电、双清包税</p>',
     '<p style="font-size:13px;color:var(--text-secondary);margin-top:4px">搬家空运回国专线：家具家电、双清包税、10-15 个工作日</p>'),
]
fix_zh_moving_regex = [
    (r'"headline": "搬家回国海运全攻略[^"]*"',
     '"headline": "搬家回国空运全攻略"'),
]

apply('en/blog/usa-to-china-sea-freight.html', fix_en_usa_sea, fix_en_usa_sea_regex)
apply('zh-cn/blog/usa-to-china-sea-freight.html', fix_zh_usa_sea, fix_zh_usa_sea_regex)
apply('en/blog/moving-season-sea-freight.html', fix_en_moving, fix_en_moving_regex)
apply('zh-cn/blog/moving-season-sea-freight.html', fix_zh_moving, fix_zh_moving_regex)
print('\n全部完成')
