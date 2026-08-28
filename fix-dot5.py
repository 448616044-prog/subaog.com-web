import re
from pathlib import Path

ROOT = Path('.')

# 1) 重建 en/seasia-to-china/pricing 价格表（东南亚档3 ¥80/¥70）
p = ROOT / 'en/seasia-to-china/pricing/index.html'
t = p.read_text(encoding='utf-8', errors='ignore')
new_table = (
    '<table class="price-table">\n'
    '  <thead><tr><th>Weight</th><th>Air freight (all-inclusive)</th></tr></thead>\n'
    '  <tbody>\n'
    '    <tr><td style="font-weight:600">20–99 kg</td><td>¥80/kg</td></tr>\n'
    '    <tr><td style="font-weight:600">100 kg+</td><td>¥70/kg</td></tr>\n'
    '  </tbody>\n'
    '</table>'
)
t, n = re.subn(r'<table class="price-table">.*?</table>', new_table, t, flags=re.S)
# 删海运美元价
t = t.replace('freight from ¥100/kg, sea from $4.5/kg', 'freight from ¥80/kg')
p.write_text(t, encoding='utf-8')
print(f'✅ en/seasia pricing 价格表重建 + 海运美元价清理 ({"重建" if n else "未匹配表"})')

# 2) zh-cn/usa-moving-to-china .5/kg 残破修复
p2 = ROOT / 'zh-cn/usa-moving-to-china/index.html'
t2 = p2.read_text(encoding='utf-8', errors='ignore')
t2 = t2.replace('走海运（，.5/kg起）', '走空运（¥100/kg起）')
t2 = t2.replace('走空运（，.5/kg起）', '走空运（¥100/kg起）')
t2 = t2.replace('走空运（10-15 个工作日，.5/kg起', '走空运（10-15 个工作日，¥100/kg起')
p2.write_text(t2, encoding='utf-8')
print('✅ zh-cn/usa-moving-to-china .5/kg 残破修复')

# 3) en/blog/index .5/kg 残破删
p3 = ROOT / 'en/blog/index.html'
t3 = p3.read_text(encoding='utf-8', errors='ignore')
t3 = t3.replace('.5/kg timeline', 'timeline')
p3.write_text(t3, encoding='utf-8')
print('✅ en/blog/index .5/kg 残破删除')

# 残留检查
print()
print('=== .5/kg 残留检查 ===')
cnt = 0
for d in ['zh-cn', 'en']:
    for f in (ROOT / d).rglob('*.html'):
        cnt += f.read_text(encoding='utf-8', errors='ignore').count('.5/kg')
print(f'  .5/kg: {cnt} 处 {"✅" if cnt == 0 else "❌"}')
