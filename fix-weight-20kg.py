"""红线变更: 起运重量 21kg -> 20kg (用户 2026-08-27 17:31 确认, 选 B 全站改)

覆盖:
1. 全站文案 21kg/21 kg/21公斤 -> 20kg/20 kg/20公斤
2. calculator: min=21 value=21 -> 20; JS w<21 -> w<20; 文案"21kg"->"20kg"
3. FAQ/正文/JSON-LD 里的 21kg 全部同步

注意: 只替换带 kg/公斤 的 21, 不碰纯数字 21 (避免误伤日期/其他)。
"""
import re
from pathlib import Path
ROOT = Path('.')

# 全站替换规则 (顺序)
REPL = [
    ('21kg', '20kg'),
    ('21 kg', '20 kg'),
    ('21公斤', '20公斤'),
    ('21 公斤', '20 公斤'),
]

total = 0
files = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        orig = t
        for old, new in REPL:
            t = t.replace(old, new)
        if t != orig:
            p.write_text(t, encoding='utf-8')
            files += 1
            total += 1

print(f'[文案替换] {files} 文件, 21kg->20kg')

# calculator 特殊处理 (min/value/JS 数字)
def fix_calculator(path):
    t = Path(path).read_text(encoding='utf-8', errors='ignore')
    orig = t
    # zh-cn: min="21" value="21" 及 JS w<21
    t = t.replace('min="21"', 'min="20"')
    t = t.replace('value="21"', 'value="20"')
    t = t.replace('w<21', 'w<20')
    t = t.replace('min=21', 'min=20')
    # en: value="21" min="21"
    t = t.replace('value="21"', 'value="20"')
    t = t.replace('min="21"', 'min="20"')
    t = t.replace('w < 21', 'w < 20')
    t = t.replace('21kg minimum', '20kg minimum')
    t = t.replace('Minimum 21 kg', 'Minimum 20 kg')
    if t != orig:
        Path(path).write_text(t, encoding='utf-8')
        print(f'  ✅ calculator: {path}')
        return True
    return False

fix_calculator('zh-cn/tools/shipping-calculator.html')
fix_calculator('en/tools/shipping-calculator.html')

# 验证
print('\n=== 验证 ===')
cnt = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        cnt += t.count('21kg') + t.count('21 kg') + t.count('21公斤')
print(f'残留 21kg/21 kg/21公斤: {cnt}')
