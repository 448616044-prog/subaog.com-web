#!/usr/bin/env python3
"""最终修复计算器起始值"""
import re
import os

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"
TARGETS = [
    "en/tools/shipping-calculator.html",
    "zh-cn/tools/shipping-calculator.html",
    "zh-cn/index.html",
]

def fix_calc_input(content):
    def repl(m):
        tag = m.group(0)
        return re.sub(r'(?<![\d])(min|value|placeholder)="20"', r'\1="21"', tag)
    return re.sub(r'<input[^>]*id="weight"[^>]*>', repl, content)

for rel in TARGETS:
    p = os.path.join(BASE, rel)
    with open(p, encoding='utf-8') as f:
        original = f.read()
    new = fix_calc_input(original)
    if new != original:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new)
        print(f"[FIXED] {rel}")
    else:
        print(f"[OK] {rel}")

# 验证
print("\n=== 最终计算器状态 ===")
for rel in TARGETS:
    p = os.path.join(BASE, rel)
    with open(p, encoding='utf-8') as f:
        for line in f:
            if 'id="weight"' in line:
                print(f"{rel}: {line.strip()[:200]}")