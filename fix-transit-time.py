#!/usr/bin/env python3
"""transit-time 时效工具页修复：统一 10-15 工作日（去 7-12 违规）+ 去海运第二值 + FAQ 去重复错乱。"""
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

# ===== en/tools/transit-time.html =====
# 1) option 统一 air:10-15（去 sea）
apply('en/tools/transit-time.html', [
 ('<option value="air:7-12,sea:18-25">Japan → China</option>', '<option value="air:10-15">Japan → China</option>'),
 ('<option value="air:7-12,sea:15-22">Korea → China</option>', '<option value="air:10-15">Korea → China</option>'),
 ('<option value="air:7-12,sea:12-18">SE Asia → China</option>', '<option value="air:10-15">SE Asia → China</option>'),
 ('<option value="air:10-15,sea">USA → China</option>', '<option value="air:10-15">USA → China</option>'),
 ('<option value="air:10-15,sea:30-40">Canada → China</option>', '<option value="air:10-15">Canada → China</option>'),
 ('<option value="air:10-15,sea">Australia → China</option>', '<option value="air:10-15">Australia → China</option>'),
 ('<option value="air:10-15,sea:30-40">Europe → China</option>', '<option value="air:10-15">Europe → China</option>'),
 # 2) JS 去 sea
 ("var air = v[0].split(':')[1], sea = v[1].split(':')[1];",
  "var air = v[0].split(':')[1];"),
 ("'<div style=\"font-size:1.5rem;font-weight:800;color:var(--primary)\">Air: ' + air + ' days</div><div style=\"font-size:13px;color:var(--text-secondary)\">Sea freight: ' + sea + ' days door-to-door</div>'",
  "'<div style=\"font-size:1.5rem;font-weight:800;color:var(--primary)\">Air freight: ' + air + ' days</div><div style=\"font-size:13px;color:var(--text-secondary)\">Door-to-door, tax-inclusive</div>'"),
 # 3) 第一个答案 7-15→10-15
 ('Air freight to China takes 7–15 working days door-to-door, depending on origin. Japan/Korea are fastest (7–12 days), USA/Europe 10–15 days.',
  'Air freight to China takes 10-15 working days door-to-door, depending on origin, tax-inclusive.'),
 # 4) 第二个答案（海运时效误写）→ 海运下架说明
 ('Air freight takes 12–40 days depending on origin. Southeast Asia 12–18 days, USA/Australia , Europe 30–40 days.',
  'Sea freight is discontinued — we only offer air freight (10-15 working days door-to-door).'),
])
# 5) 第二个问题改 Is sea freight available?（答案替换后再改问题）
t = open('en/tools/transit-time.html', encoding='utf-8').read()
c = t.count('"name": "How long does air freight to China take?", "acceptedAnswer": {"@type": "Answer", "text": "Sea freight is discontinued')
t = t.replace('"name": "How long does air freight to China take?", "acceptedAnswer": {"@type": "Answer", "text": "Sea freight is discontinued',
              '"name": "Is sea freight available?", "acceptedAnswer": {"@type": "Answer", "text": "Sea freight is discontinued')
c2 = t.count('<button class="faq-q">How long does air freight to China take?<span class="faq-icon">▼</span></button><div class="faq-a">Sea freight is discontinued')
t = t.replace('<button class="faq-q">How long does air freight to China take?<span class="faq-icon">▼</span></button><div class="faq-a">Sea freight is discontinued',
              '<button class="faq-q">Is sea freight available?<span class="faq-icon">▼</span></button><div class="faq-a">Sea freight is discontinued')
open('en/tools/transit-time.html', 'w', encoding='utf-8').write(t)
print(f'  ✅ en 第二问题改 2 处 (jsonld={c}, html={c2})')

# ===== zh-cn/tools/transit-time.html =====
apply('zh-cn/tools/transit-time.html', [
 ('<option value="日本,7-12,18-25">日本 → 中国</option>', '<option value="日本,10-15">日本 → 中国</option>'),
 ('<option value="韩国,7-12,15-22">韩国 → 中国</option>', '<option value="韩国,10-15">韩国 → 中国</option>'),
 ('<option value="东南亚,7-12,12-18">东南亚 → 中国</option>', '<option value="东南亚,10-15">东南亚 → 中国</option>'),
 ('<option value="加拿大,10-15,30-40">加拿大 → 中国</option>', '<option value="加拿大,10-15">加拿大 → 中国</option>'),
 ('<option value="欧洲,10-15,30-40">欧洲 → 中国</option>', '<option value="欧洲,10-15">欧洲 → 中国</option>'),
 ("'<div style=\"font-size:1.5rem;font-weight:800;color:var(--primary)\">' + v[0] + ' → 中国</div><div style=\"font-size:14px;color:var(--text-secondary)\">空运：' + v[1] + ' 天 · 海运：' + v[2] + ' 天（门到门）</div>'",
  "'<div style=\"font-size:1.5rem;font-weight:800;color:var(--primary)\">' + v[0] + ' → 中国</div><div style=\"font-size:14px;color:var(--text-secondary)\">空运：' + v[1] + ' 天（门到门，双清包税）</div>'"),
 ('查询各国寄中国的门到门时效，空运vs海运对比。', '查询各国寄中国的门到门时效（10-15 个工作日，双清包税）。'),
 ('空运vs海运时效对比，免费时效查询工具', '空运时效，免费时效查询工具'),
 ('空运到中国7-15工作日门到门，视出发国而定。日本/韩国最快（10-15 个工作日），美国/欧洲10-15 个工作日。',
  '空运到中国 10-15 个工作日门到门，视出发国而定，双清包税。'),
 ('空运12-40天视出发国而定。东南亚12-18天，美国/澳洲，欧洲30-40天。',
  '海运已下架，只提供空运（10-15 个工作日门到门）。'),
])
# 第二个问题改「海运还能寄吗？」
t = open('zh-cn/tools/transit-time.html', encoding='utf-8').read()
c = t.count('"name": "空运寄中国要多久？", "acceptedAnswer": {"@type": "Answer", "text": "海运已下架')
t = t.replace('"name": "空运寄中国要多久？", "acceptedAnswer": {"@type": "Answer", "text": "海运已下架',
              '"name": "海运还能寄吗？", "acceptedAnswer": {"@type": "Answer", "text": "海运已下架')
c2 = t.count('<button class="faq-q">空运寄中国要多久？<span>▼</span></button><div class="faq-a">海运已下架')
t = t.replace('<button class="faq-q">空运寄中国要多久？<span>▼</span></button><div class="faq-a">海运已下架',
              '<button class="faq-q">海运还能寄吗？<span>▼</span></button><div class="faq-a">海运已下架')
open('zh-cn/tools/transit-time.html', 'w', encoding='utf-8').write(t)
print(f'  ✅ zh-cn 第二问题改 2 处 (jsonld={c}, html={c2})')

print('\n完成')
