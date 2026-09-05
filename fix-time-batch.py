#!/usr/bin/env python3
"""全站时效统一 10-15 工作日（用 find 拿清单避开 .git，静默批量处理）。"""
import subprocess, re

def fix_en(t):
    # 时效拆解（特殊）
    t = t.replace('7-10 days air transit + 1-2 days customs clearance + 1-3 days last-mile delivery',
                  '10-15 working days door-to-door (incl. customs and last-mile delivery)')
    t = t.replace('7-10 days air transit + 1-2 days customs + 1-3 days domestic delivery',
                  '10-15 working days door-to-door (incl. customs and delivery)')
    # 整体时效
    t = re.sub(r'7[–-]10 days door-to-door', '10-15 working days door-to-door', t)
    t = re.sub(r'7[–-]10 days', '10-15 working days', t)
    t = re.sub(r'7[–-]10 day delivery', '10-15 working day delivery', t)
    t = re.sub(r'7[–-]12 days', '10-15 working days', t)
    t = re.sub(r'7[–-]12 day delivery', '10-15 working day delivery', t)
    t = re.sub(r'7[–-]12 Days', '10-15 Days', t)
    # info-card 裸数字
    t = re.sub(r'>7[–-]12<', '>10-15<', t)
    t = re.sub(r'>7-10<', '>10-15<', t)
    return t

def fix_zh(t):
    t = re.sub(r'空运 7-12 天', '空运 10-15 个工作日', t)
    t = re.sub(r'7-12 天', '10-15 个工作日', t)
    t = re.sub(r'7-10 天', '10-15 个工作日', t)
    t = re.sub(r'7–12 天', '10-15 个工作日', t)
    t = re.sub(r'>7-10<', '>10-15<', t)
    t = re.sub(r'>7–12<', '>10-15<', t)
    return t

files = subprocess.check_output(['find', 'en', 'zh-cn', '-name', '*.html']).decode('utf-8').split('\n')
count_f = 0
for f in files:
    if not f.strip():
        continue
    try:
        t = open(f, encoding='utf-8').read()
    except Exception:
        continue
    o = t
    t = fix_en(t) if f.startswith('en/') else fix_zh(t)
    if t != o:
        open(f, 'w', encoding='utf-8').write(t)
        count_f += 1
print('DONE 修改文件数:', count_f)
