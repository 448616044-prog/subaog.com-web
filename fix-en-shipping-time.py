#!/usr/bin/env python3
"""en 时效页（7-10 违规 + 海运）+ blog/index 家具卡片 + student-luggage meta 收尾。"""
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

# ===== en/blog/usa-to-china-shipping-time.html（7-10 违规 + 海运宣传）=====
apply('en/blog/usa-to-china-shipping-time.html', [
 ('air 7-10 days, express 2-6 days', 'air 10-15 working days, express 2-6 days'),
 ('Air line: 10–15 working days door-to-door, best value. Sea: , cheapest for large/moving.',
  'Air line: 10–15 working days door-to-door, best value. Sea freight: discontinued — air is the only option for large/moving.'),
 ('transit (air 3–5 / sea 15–25 days)', 'transit (air 3–5 days)'),
 ('Air 7–10 days is typical, not a floor.', 'Air 10-15 working days is typical, not a floor.'),
 ('Choose the air line (7–10 days) not sea;', 'Choose the air line (10-15 working days);'),
 ('When to go by sea</h2><p style="color:var(--text-secondary);line-height:1.9">Not urgent (moving/large/volume)? Sea saves 40%; ship a month early and store free for 30 days at the warehouse.</p>',
  'Sea freight discontinued</h2><p style="color:var(--text-secondary);line-height:1.9">We no longer ship by sea — everything goes by air (10-15 working days). Ship a month early and store free for 30 days at the warehouse.</p>'),
 ('How long does sea take?', 'How long does air take?'),
 ('. West coast ~25, east coast 30–35.', '10-15 working days door-to-door (incl. customs + delivery).'),
 ('Urgent (<2 weeks) → air; not urgent/large → sea (save 40%).',
  'Urgent (<2 weeks) → air; sea freight is discontinued — air is the only option.'),
])

# ===== en/blog/index.html 家具卡片标题（与页面 title 对齐）=====
apply('en/blog/index.html', [
 ('Can I Ship Furniture to China? Sea Freight Guide (2026)', 'Can I Ship Furniture to China? Rules & Duty (2026)'),
])

# ===== zh-cn/student-luggage-shipping-guide meta =====
apply('zh-cn/blog/student-luggage-shipping-guide.html', [
 ('选空运还是海运', '选空运还是集运'),
])

print('\n完成')
