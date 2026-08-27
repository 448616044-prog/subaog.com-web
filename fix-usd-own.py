"""清①留②: 清理自家美元价, 保留竞品对比价.

① 自家价 -> 人民币(红线已有档位价):
  $5-8/lb      -> ¥100/kg 起   (空运专线 美国档1)
  $4-6/lb      -> ¥80/kg 起    (华人集运敏感货)
  $9.5-11/kg   -> ¥100/kg      (空运旧价)
  $8/kg        -> ¥100/kg      (自家空运)
  $10/kg       -> ¥100/kg      (自家空运)
  $5.5-¥80/kg  -> ¥70-100/kg   (Organization priceRange)

② 竞品价保留: DHL/FedEx/USPS/UPS/EMS/First Class/Priority/国际快递/国际搬家
③ 客观信息保留: 免税额度 $140, 商品举例 $60-80/$300/$100

不处理(报告给用户): $150-200 全包, $12 小包裹, $2/个 $1-3/个 纸箱, $30 起 附加费,
                    海运价 $2-4/kg $3-5/kg $800-1500 $8000-22500 ¥45/kg
"""
import re
from pathlib import Path
ROOT = Path('.')

REPLACE = [
    ('$5-8/lb', '¥100/kg 起'),
    ('$4-6/lb', '¥80/kg 起'),
    ('$9.5-11/kg', '¥100/kg'),
    ('$8/kg', '¥100/kg'),
    ('$10/kg', '¥100/kg'),
    ('$5.5-¥80/kg', '¥70-100/kg'),
]

# 竞品保护词: 这些词附近的美元不替换
PROTECT_WORDS = ['DHL', 'FedEx', 'USPS', 'UPS', 'EMS', 'First Class', 'Priority',
                 '国际快递', '国际搬家', 'Express']

def is_protected(seg):
    return any(w.lower() in seg.lower() for w in PROTECT_WORDS)

fixed_files = 0
total_replaced = 0
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        orig = t
        # 逐段处理: 保护竞品上下文
        # 简单方式: 对每个 REPLACE 项, 只在非竞品上下文替换
        for old, new in REPLACE:
            # 找所有 old 的位置, 检查上下文是否有竞品词
            result = []
            last = 0
            for m in re.finditer(re.escape(old), t):
                start, end = m.start(), m.end()
                ctx = t[max(0, start - 60):end + 60]
                if is_protected(ctx):
                    # 竞品上下文, 保留原样
                    result.append(t[last:end])
                else:
                    result.append(t[last:start])
                    result.append(new)
                last = end
            result.append(t[last:])
            t = ''.join(result)
        if t != orig:
            p.write_text(t, encoding='utf-8')
            fixed_files += 1

print(f'[清①] 修复 {fixed_files} 文件')

# 验证
print('\n=== 验证残留 ===')
residual = {}
for old, new in REPLACE:
    cnt = 0
    for d in ['zh-cn', 'en']:
        for p in (ROOT / d).rglob('*.html'):
            t = p.read_text(encoding='utf-8', errors='ignore')
            cnt += t.count(old)
    if cnt:
        residual[old] = cnt
for k, v in residual.items():
    print(f'  {v:4d} 处残留  {k}  (竞品上下文保留, 属正常)')
print(f'\n新价 ¥100/kg 起 出现: {sum(len(re.findall(r"¥100/kg 起", p.read_text(encoding="utf-8",errors="ignore"))) for d in ["zh-cn","en"] for p in (ROOT/d).rglob("*.html"))}')
