import re
from pathlib import Path

ROOT = Path('.')

# 错误价格修复规则（顺序敏感）
REPLACES = [
    # 连环替换 bug：¥80-80/kg → 档1美国 ¥100/kg
    ('¥80-80/kg', '¥100/kg'),
    # 档1美国 100kg+ 旧价 → ¥90/kg
    ('¥70-75/kg', '¥90/kg'),
    # en 站 en-dash 区间价 → 档1美国正确值
    ('¥70–80/kg', '¥100/kg'),
    ('¥65–75/kg', '¥90/kg'),
    # 残破数字 ¥1000-200 → ¥1000-2000（后面非数字）
]

fixed = 0
files = set()

for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        orig = t
        for old, new in REPLACES:
            t = t.replace(old, new)
        # 残破数字（正则，负向前瞻确保不匹配 ¥1000-2000 前缀）
        t = re.sub(r'¥1000-200(?!\d)', '¥1000-2000', t)
        # 去重复：¥100/kg 起 或 ¥100/kg → ¥100/kg 起
        t = t.replace('¥100/kg 起 或 ¥100/kg', '¥100/kg 起')
        # USPS 竞品价恢复美元（¥100-30 是 $10-30 被误替换）
        t = t.replace('¥100-30', '$10-30')
        if t != orig:
            p.write_text(t, encoding='utf-8')
            fixed += 1
            files.add(str(p))

print(f'错误价格修复: {fixed} 文件')

# 残留检查
print()
print('=== 残留检查 ===')
for tg in ['¥80-80/kg', '¥70-75/kg', '¥70–80/kg', '¥65–75/kg', '¥1000-200 ', '¥100-30', '¥65']:
    cnt = 0
    for d in ['zh-cn', 'en']:
        for p in (ROOT / d).rglob('*.html'):
            cnt += p.read_text(encoding='utf-8', errors='ignore').count(tg)
    print(f'  {tg}: {cnt} 处 {"✅" if cnt == 0 else "❌"}')
