import re
from pathlib import Path
ROOT = Path('.')
# 精确 dump 所有待删项的完整句子（去标签）
targets = ['$2-4/kg', '$3-5/kg', '$3–5/kg', '$800-1500', '$8000-22500', '¥45/kg',
           '$30 起', '$150-200', '$12 起', '$12/kg', '$0.5-0.6/kg']
seen = set()
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        for tg in targets:
            for m in re.finditer(re.escape(tg), t):
                s = max(0, m.start() - 50)
                e = min(len(t), m.end() + 50)
                seg = re.sub(r'<[^>]+>', ' ', t[s:e])
                seg = re.sub(r'\s+', ' ', seg).strip()
                key = (str(p), seg)
                if key not in seen:
                    seen.add(key)
                    print(f'[{p}]')
                    print(f'  ...{seg}...\n')
