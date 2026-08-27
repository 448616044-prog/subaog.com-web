import re
from pathlib import Path
ROOT = Path('.')
seen = set()
for d in ['zh-cn', 'en']:
    for p in (ROOT / d).rglob('*.html'):
        t = p.read_text(encoding='utf-8', errors='ignore')
        for m in re.finditer(r'.{25}([$]12|[$]150-200|[$]2/个|[$]1-3/个|[$]30 起).{25}', t):
            s = re.sub(r'<[^>]+>', ' ', m.group(0))
            s = re.sub(r'\s+', ' ', s).strip()
            if s not in seen:
                seen.add(s)
                print(f'[{p}]')
                print(f'  {s}\n')
