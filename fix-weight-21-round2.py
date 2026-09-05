#!/usr/bin/env python3
"""修复重量替换的两个边缘情况"""
import re
import subprocess
import os

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# 1. 修复计算器：<input id="weight" ... min="20" value="20" placeholder="20" ...>
#    替换所有 (min|value|placeholder)="20" 为 21（只在含 id="weight" 的 input 上）
def fix_calc_input(content):
    # 找到所有 <input ... id="weight" ...> 标签，逐个处理
    def repl(m):
        tag = m.group(0)
        # 在这个 input 标签内，把所有 (min|value|placeholder)="20" 改成 21
        new_tag = re.sub(r'\b(min|value|placeholder)="20"\b', r'\1="21"', tag)
        return new_tag
    return re.sub(r'<input[^>]*id="weight"[^>]*>', repl, content)

# 2. 修复残留 20kg+（可能有空格包围，如 "20kg+ 起步"）
#    但因为之前规则有 \b 边界，"20kg+" 应该都已经匹配
#    残留可能是 "20kg+" 后面跟的不是字母数字但不是单词边界（如 + 后直接跟空格是边界）
#    实际看，可能是 " 20kg+" 前后有空格但用 grep 的模式
RESIDUAL_PATT = re.compile(r'\b20kg\+')

result = subprocess.run(
    ['find', 'en', 'zh-cn', '-name', '*.html'],
    cwd=BASE, capture_output=True, text=True, timeout=60
)
files = [f for f in result.stdout.strip().split('\n') if f]

# 阶段 1：修计算器
calc_fixed = 0
for rel in files:
    p = os.path.join(BASE, rel)
    with open(p, encoding='utf-8') as f:
        original = f.read()
    new_content = fix_calc_input(original)
    if new_content != original:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new_content)
        calc_fixed += 1
print(f"计算器 input 修复文件数: {calc_fixed}")

# 阶段 2：扫残留 20kg+
residual_files = []
for rel in files:
    p = os.path.join(BASE, rel)
    with open(p, encoding='utf-8') as f:
        t = f.read()
    matches = RESIDUAL_PATT.findall(t)
    if matches:
        residual_files.append((rel, len(matches)))

print(f"\n残留 20kg+ 文件数: {len(residual_files)}")
for rel, cnt in residual_files[:10]:
    print(f"  [{cnt} 次] {rel}")

# 阶段 3：查残留"起运 20kg / 最低 20kg"
print(f"\n=== 残留起运/最低 20kg ===")
for rel in files:
    p = os.path.join(BASE, rel)
    with open(p, encoding='utf-8') as f:
        t = f.read()
    if re.search(r'起运\s*20kg|最低\s*20kg|Minimum\s+20kg', t):
        print(f"  {rel}")
        # 显示上下文
        for m in re.finditer(r'.{0,30}(起运|最低|Minimum)\s*20kg.{0,20}', t):
            print(f"    {m.group(0)[:80]}")