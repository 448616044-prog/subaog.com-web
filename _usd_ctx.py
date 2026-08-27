import re
from pathlib import Path
ROOT = Path('.')
# 提取所有含 $数字 的上下文（前后 45 字符，去标签）
seen = set()
rows = []
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        for m in re.finditer(r'[$][0-9]', t):
            s = max(0, m.start() - 45)
            e = min(len(t), m.end() + 45)
            seg = t[s:e]
            seg_clean = re.sub(r'<[^>]+>', ' ', seg)
            seg_clean = re.sub(r'\s+', ' ', seg_clean).strip()
            if seg_clean not in seen:
                seen.add(seg_clean)
                rows.append((str(p), seg_clean))
print(f'总唯一上下文: {len(rows)}\n')
for path, seg in rows:
    print(f'[{path}]\n  {seg}\n')
