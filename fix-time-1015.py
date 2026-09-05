#!/usr/bin/env python3
"""全站空运时效统一 10-15 工作日：清理 7-12 / 7-10 违规时效残留。"""
import re, os

# 先精确处理「时效拆解」（避免把拆解子项误改）
def fix_detailed(t):
    # en/faq.html + en/index.html 的 7-10 days air transit 拆解 → 10-15 总
    t = t.replace('7-10 days air transit + 1-2 days customs clearance + 1-3 days last-mile delivery',
                  '10-15 working days door-to-door (incl. customs and last-mile delivery)')
    t = t.replace('7-10 days air transit + 1-2 days customs + 1-3 days domestic delivery',
                  '10-15 working days door-to-door (incl. customs and delivery)')
    t = t.replace('7-10 days air transit + 1-2 days customs clearance + 1-3 days last-mile delivery.',
                  '10-15 working days door-to-door (incl. customs and last-mile delivery).')
    return t

def fix_en(t):
    t = fix_detailed(t)
    # 整体时效 7-10 / 7-12 → 10-15 working days
    t = re.sub(r'7[–-]10 days door-to-door', '10-15 working days door-to-door', t)
    t = re.sub(r'7[–-]10 days', '10-15 working days', t)
    t = re.sub(r'7[–-]10 day delivery', '10-15 working day delivery', t)
    t = re.sub(r'7[–-]12 days', '10-15 working days', t)
    t = re.sub(r'7[–-]12 day delivery', '10-15 working day delivery', t)
    t = re.sub(r'7[–-]12 Days', '10-15 Days', t)
    t = re.sub(r'>7[–-]12<', '>10-15<', t)  # info-card big
    return t

def fix_zh(t):
    t = re.sub(r'空运 7-12 天', '空运 10-15 个工作日', t)
    t = re.sub(r'7-12 天', '10-15 个工作日', t)
    t = re.sub(r'7-10 天', '10-15 个工作日', t)
    t = re.sub(r'7–12 天', '10-15 个工作日', t)
    return t

total_files = 0
total_hits = 0
for base in ['en', 'zh-cn']:
    for root, dirs, files in os.walk(base):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            p = os.path.join(root, fn)
            try:
                t = open(p, encoding='utf-8').read()
            except Exception:
                continue
            orig = t
            if base == 'en':
                t = fix_en(t)
            else:
                t = fix_zh(t)
            if t != orig:
                open(p, 'w', encoding='utf-8').write(t)
                # 统计替换的时效数字
                import re as _re
                hits = len(_re.findall(r'10-15 working days|10-15 Days|10-15 个工作日', t)) - len(_re.findall(r'10-15 working days|10-15 Days|10-15 个工作日', orig))
                total_files += 1
                total_hits += max(hits, 1)
                print(f'  ✅ {p}')

print(f'\n完成：{total_files} 个文件，约 {total_hits} 处时效统一')
