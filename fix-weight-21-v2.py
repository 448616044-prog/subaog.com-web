#!/usr/bin/env python3
"""
subaog.com 重量红线替换 v2 — 修复中英文边界问题
"""
import os
import re
import subprocess

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# 关键修复：用 (?<![\d]) 替代 `\b`，兼容中文字符与英文数字之间的边界
# (?<![\d])20kg = 前面不是数字
# (?![\d])20kg = 后面不是数字
# 但 20kg+ 后面是 + 不是数字，所以无需 lookahead

REPLACEMENTS = [
    # 1. 价格区间下限
    (r'(?<![\d])20-99kg(?![\d])', '21-99kg'),

    # 2. 区间下限 + 标志
    (r'(?<![\d])20kg\+', '21kg+'),

    # 3. 比较运算符 + 20kg（前后都不是数字）
    (r'(?<![\d])>=?20kg(?![\d])', '≥21kg'),
    (r'(?<![\d])<=?20kg(?![\d])', '<21kg'),

    # 4. Minimum 20kg
    (r'(?<![\d])Minimum\s+20kg(?![\d])', 'Minimum 21kg'),
    (r'(?<![\d])minimum\s+20kg(?![\d])', 'minimum 21kg'),

    # 5. 中文起运重量短语
    (r'起运\s*20kg', '起运 21kg'),
    (r'最低起运\s*20kg', '最低起运 21kg'),
    (r'最低\s*20kg', '最低 21kg'),

    # 6. 独立 20kg（前后都不是数字）
    (r'(?<![\d])20kg(?![\d])', '21kg'),
]

def fix_calc_input(content):
    """修复计算器 input 内所有 (min|value|placeholder)="20" → 21"""
    def repl(m):
        tag = m.group(0)
        return re.sub(r'\b(min|value|placeholder)="20"\b', r'\1="21"', tag)
    return re.sub(r'<input[^>]*id="weight"[^>]*>', repl, content)


def main():
    result = subprocess.run(
        ['find', 'en', 'zh-cn', '-name', '*.html'],
        cwd=BASE, capture_output=True, text=True, timeout=60
    )
    files = [f for f in result.stdout.strip().split('\n') if f]

    changed_total = 0
    calc_fixed_total = 0

    for rel in files:
        p = os.path.join(BASE, rel)
        try:
            with open(p, encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        original = content
        diffs = []

        # 计算器
        new_content = fix_calc_input(content)
        if new_content != content:
            calc_diff = len(re.findall(r'id="weight"[^>]*>', content))
            diffs.append(f"  计算器 input 修复 ×{calc_diff}")
            content = new_content
            calc_fixed_total += 1

        # 通用替换
        for pattern, replacement in REPLACEMENTS:
            matches = re.findall(pattern, content)
            if matches:
                diffs.append(f"  {pattern[:30]}... ×{len(matches)}")
                content = re.sub(pattern, replacement, content)

        if content != original:
            changed_total += 1
            with open(p, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[{rel}]")
            for d in diffs:
                print(d)

    print(f"\n=== 完成 ===")
    print(f"改动文件数: {changed_total}")


if __name__ == '__main__':
    main()