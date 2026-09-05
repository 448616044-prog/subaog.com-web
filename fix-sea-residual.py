#!/usr/bin/env python3
"""海运残留清理：搬家/行李/时效页（7 个 A 类页面）。
海运宣传→空运，修复空白数字、美元价残留、错乱文案。"""
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

# ===== 1. zh-cn/blog/student-luggage-shipping-guide.html（美元价红线 + 海运）=====
apply('zh-cn/blog/student-luggage-shipping-guide.html', [
 ('空运？海运？超重行李？三个方案对比，帮你省下一张机票钱',
  '空运？合箱？超重行李？三个方案帮你省钱'),
 ('<h2>方案一：海运专线（最省钱）</h2><p>适合不着急的东西：衣物、书籍、日用品、小家电。$2-4/lb，门到门。100lb的行李约$200-400。</p>',
  '<h2>方案一：空运专线（20kg 起）</h2><p>适合衣物、书籍、日用品、小家电等行李。¥100/kg（美加墨澳新档，20-99kg），10-15 个工作日门到门，双清包税。100kg 行李约 ¥9,000（100kg+ 档 ¥90/kg）。</p>'),
 ('<h2>方案二：空运专线（速度快）</h2><p>适合需要尽快收到的东西：毕业证、贵重物品、换季衣物。$5-6/lb，10-15 个工作日门到门。50lb约$250-300。</p>',
  '<h2>方案二：合箱集运（多箱更省）</h2><p>多个包裹合并成一批，按合并后总重量或体积重（长×宽×高÷5000）取大者计费，10-15 个工作日门到门。适合毕业季一次性寄回多箱。</p>'),
 ('<h2>方案三：混搭（最聪明）</h2><p>急用的走空运、不急的走空运。两箱空运+四箱海运，总费用约$500-800，比全部空运省一半。</p>',
  '<h2>方案三：打包省钱（最聪明）</h2><p>真空压缩衣物被子、拆装大件降低体积重，能显著省运费。急用的贵重物品单独走空运，不急的大批量走空运专线，双清包税。</p>'),
 ('用Home Depot的Heavy Duty纸箱（$2/个）', '用 Home Depot 的 Heavy Duty 纸箱'),
 ('<p>空运/海运/快递全方位对比</p>', '<p>空运专线全方位对比</p>'),
])

# ===== 2. en/usa-moving-to-china/index.html =====
apply('en/usa-moving-to-china/index.html', [
 ('Sea freight from with tax-inclusive customs and free pickup.',
  'Air freight with tax-inclusive customs and free pickup.'),
 ('Airsea freight, tax-inclusive, no hidden fees',
  'Air freight, tax-inclusive, no hidden fees'),
 ('Air or sea freight with full tracking on every leg.',
  'Air freight with full tracking on every leg.'),
 ('<div class="feature"><div class="icon">🚢</div><h3>Sea freight</h3><p>Cost-effective for large volume moves.</p></div>',
  '<div class="feature"><div class="icon">✈️</div><h3>Air freight</h3><p>10-15 working days for large volume moves.</p></div>'),
])

# ===== 3. zh-cn/usa-moving-to-china/index.html =====
apply('zh-cn/usa-moving-to-china/index.html', [
 ('<title>美国搬家回中国完整指南 2026 | 家具海运搬家全攻略 | 速豹国际</title>',
  '<title>美国搬家回中国完整指南 2026 | 家具家电空运搬家全攻略 | 速豹国际</title>'),
 ('从美国搬家回中国终极指南：海运拼柜vs国际搬家公司费用对比',
  '从美国搬家回中国终极指南：空运vs国际搬家公司费用对比'),
 ('<p class="subtitle">海运搬家全流程、费用明细、打包清单</p>',
  '<p class="subtitle">空运搬家全流程、费用明细、打包清单</p>'),
 ('<tr><td>海运拼柜</td><td>已下架</td><td>4-5周</td><td>家具+家电+行李</td></tr>',
  '<tr><td>空运专线（大件）</td><td>¥100/kg起</td><td>10-15个工作日</td><td>家具+家电+行李</td></tr>'),
 ('<li>海运发出（15-20天海上运输）</li>', '<li>空运发出（10-15 个工作日）</li>'),
 ('搬家回国走空运还是海运？', '搬家回国怎么寄？'),
])

# ===== 4. en/blog/usa-moving-to-china-guide.html =====
apply('en/blog/usa-moving-to-china-guide.html', [
 ('how sea freight works for a full move', 'how air freight works for a full move'),
 ('Sea freight is the cost-effective choice for moves (). Air freight (10–15 days) suits smaller, time-sensitive moves.',
  'Sea freight is discontinued — air freight (10-15 working days) is now the only option for moves, tax-inclusive from ¥100/kg.'),
 ('>What does a move cost?</h2><p style="color:var(--text-secondary);line-height:1.8"></p>',
  '>What does a move cost?</h2><p style="color:var(--text-secondary);line-height:1.8">Air freight from ¥100/kg (20-99kg), ¥90/kg (100kg+), tax-inclusive door-to-door.</p>'),
 ('Air freightkg. Large moves get volume discounts.',
  'Air freight from ¥100/kg (20kg+). Large moves get volume discounts.'),
])

# ===== 5. zh-cn/blog/usa-moving-to-china-guide.html =====
apply('zh-cn/blog/usa-moving-to-china-guide.html', [
 ('美国搬家回中国终极指南：海运搬家流程、费用预算、打包技巧、海关手续。',
  '美国搬家回中国终极指南：空运搬家流程、费用预算、打包技巧、海关手续。'),
 ('<p class="subtitle">海运搬家全流程、费用明细、打包清单、避坑指南</p>',
  '<p class="subtitle">空运搬家全流程、费用明细、打包清单、避坑指南</p>'),
 ('<tr><td>海运拼柜</td><td>已下架</td><td>4-5周</td><td>个人/家庭搬家</td></tr>',
  '<tr><td>空运专线（大件）</td><td>¥100/kg起</td><td>10-15个工作日</td><td>个人/家庭搬家</td></tr>'),
 ('<strong>海运发出：</strong>拼柜上船→15-20天海上运输',
  '<strong>空运发出：</strong>装机起飞→10-15 个工作日'),
 ('<p>空运/海运/快递全方位对比</p>', '<p>空运专线全方位对比</p>'),
])

# ===== 6. zh-cn/blog/usa-to-china-shipping-time.html =====
apply('zh-cn/blog/usa-to-china-shipping-time.html', [
 ('干线运输（空运 3-5 天/海运 15-25 天）', '干线运输（空运 3-5 天）'),
 ('选空运专线（10-15 个工作日）而非海运', '选空运专线（10-15 个工作日）'),
 ('>什么时候该海运</h2><p style="color:var(--text-secondary);line-height:1.9">不赶时间（搬家/大件/批量）海运省 40%；提前 1 个月寄，行李先到仓免费存 30 天再发货。</p>',
  '>海运已下架，只提供空运</h2><p style="color:var(--text-secondary);line-height:1.9">本渠道已停海运，全部改走空运（10-15 个工作日）。搬家/大件/批量都走空运专线，双清包税；提前 1 个月寄，行李先到仓免费存 30 天再发货。</p>'),
])

# ===== 7. zh-cn/student-luggage/index.html =====
apply('zh-cn/student-luggage/index.html', [
 ('<div class="card"><h3>空运 + 海运混搭</h3><p>急用的走空运，剩下的走空运（搬家公司搬运），适合行李较多且有 1-2 个月缓冲的同学。</p></div>',
  '<div class="card"><h3>合箱集运 + 空运专线</h3><p>多个包裹合并成一批走空运（10-15 个工作日，双清包税），适合行李较多且有 1-2 个月缓冲的同学。</p></div>'),
])

print('\n全部完成')
