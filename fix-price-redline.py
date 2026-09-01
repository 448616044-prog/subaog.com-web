#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价格红线修复：清理全站旧价残留 + bug 价，统一到 2026-08-27 新包税价。
新价三档两区间：
  档1 美/加/墨/澳/新：20-99kg ¥100/kg，100kg+ ¥90/kg  → 区间 ¥90-100/kg
  档2 欧洲：20-99kg ¥90/kg，100kg+ ¥80/kg             → 区间 ¥80-90/kg
  档3 日/韩/泰/新/菲/台/马：20-99kg ¥80/kg，100kg+ ¥70/kg → 区间 ¥70-80/kg
"""
import os, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
dry = '--dry-run' in sys.argv

def replace_in_file(fpath, old, new, label):
    if not os.path.exists(fpath):
        print('  ❌ 缺失 %s' % fpath); return 0
    c = open(fpath, encoding='utf-8').read()
    n = c.count(old)
    if n == 0:
        print('  ⚠️ 未找到「%s」 %s' % (old, fpath)); return 0
    if not dry:
        c = c.replace(old, new)
        open(fpath, 'w', encoding='utf-8').write(c)
    print('  %s %s ×%d 「%s」→「%s」' % ('[dry]' if dry else '✅', fpath, n, old, new))
    return n

def replace_in_glob(pattern, old, new, label):
    total = 0
    files = sorted(glob.glob(pattern, recursive=True))
    for f in files:
        total += replace_in_file(f, old, new, label)
    print('  └─ %s：%d 个文件' % (label, len(files)))
    return total

print('=== 1. 城市页区间价（档1澳洲/加拿大 → ¥90-100/kg；档2欧洲 → ¥80-90/kg）===')
replace_in_glob(os.path.join(ROOT, 'zh-cn/australia-to-china/*/index.html'), '¥80-100/kg', '¥90-100/kg', '澳洲城市页(档1)')
replace_in_glob(os.path.join(ROOT, 'zh-cn/canada-to-china/*/index.html'), '¥80-100/kg', '¥90-100/kg', '加拿大城市页(档1)')
replace_in_glob(os.path.join(ROOT, 'zh-cn/europe-to-china/*/index.html'), '¥80-100/kg', '¥80-90/kg', '欧洲城市页(档2)')

print('\n=== 2. 留学生行李对比页（美国档1）===')
replace_in_file(os.path.join(ROOT, 'zh-cn/blog/student-luggage-express-comparison.html'), '¥80-100/kg 起', '¥100/kg 起', 'zh-cn')
replace_in_file(os.path.join(ROOT, 'en/blog/student-luggage-express-comparison.html'), 'from ¥80-100/kg', 'from ¥100/kg', 'en')

print('\n=== 3. en 站对比页 ¥70-80/kg → ¥90-100/kg（从美国寄，档1）===')
for f in ['en/city/san-diego-to-hangzhou.html',
          'en/blog/dhl-vs-usps-china.html',
          'en/blog/usps-vs-ups-china.html',
          'en/blog/fedex-vs-ups-china.html',
          'en/blog/dhl-vs-fedex-vs-ups-china.html']:
    replace_in_file(os.path.join(ROOT, f), '¥70-80/kg', '¥90-100/kg', f)

print('\n=== 4. 旧价铁证（75/kg 欧洲、70/kg 亚、每档降¥5）===')
replace_in_file(os.path.join(ROOT, 'zh-cn/blog/usa-to-china-shipping-cost.html'),
    '20kg+ ¥100/kg（美国档）、75/kg（欧洲档）、70/kg（亚档）；100kg+ 每档再降 ¥5',
    '20-99kg ¥100/kg（美国档）、¥90/kg（欧洲档）、¥80/kg（亚档）；100kg+ 每档降 ¥10',
    'usa-to-china-shipping-cost')

print('\n=== 5. bug 价 ¥80-11/kg → ¥90-100/kg ===')
replace_in_file(os.path.join(ROOT, 'zh-cn/blog/dhl-vs-fedex-vs-ups-china.html'), '¥80-11/kg', '¥90-100/kg', 'dhl-vs-fedex')

print('\n=== 6. bug 价 ¥100-25 → $15-25（USPS First-Class 第三方参考价）===')
replace_in_file(os.path.join(ROOT, 'zh-cn/report/usa-china-shipping-cost-report-2026.html'), '¥100-25', '$15-25', 'zh-cn report')
replace_in_file(os.path.join(ROOT, 'en/report/usa-china-shipping-cost-report-2026.html'), '¥100-25', '$15-25', 'en report')

print('\n=== 7. ¥100-80/kg 顺序反 bug → ¥90-100/kg（档1）===')
replace_in_file(os.path.join(ROOT, 'zh-cn/blog/graduation-luggage-shipping.html'), '¥100/kg 起 或 ¥100-80/kg（20kg+）', '¥100/kg 起（20kg+）', 'graduation-luggage')
replace_in_file(os.path.join(ROOT, 'zh-cn/blog/usa-to-china-shipping-time.html'), '¥100-80/kg（20kg+）', '¥90-100/kg（20kg+）', 'usa-to-china-shipping-time')
replace_in_file(os.path.join(ROOT, 'zh-cn/blog/how-to-choose-international-shipping-method.html'), '¥100-80/kg', '¥90-100/kg', 'how-to-choose')

print('\n完成。')
