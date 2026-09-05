#!/usr/bin/env python3
"""
subaog.com 重量红线替换 v3 — 修复计算器起始值
关键修复：用 (?<![\d]) 替代 \\b，避免 "20" 后引号导致 \\b 失效
"""
import re

def fix_calc_input(content):
    """修复计算器 input 内所有 (min|value|placeholder)="20" → 21"""
    def repl(m):
        tag = m.group(0)
        # (?<![\d]) 前面不是数字（避免 120kg 等误伤）
        # 不需要后置 \b，因为 "20" 后面是 " 不是数字
        return re.sub(r'(?<![\d])(min|value|placeholder)="20"', r'\1="21"', tag)
    return re.sub(r'<input[^>]*id="weight"[^>]*>', repl, content)


# 测试
sample = '<input type="number" id="weight" value="20" min="20" placeholder="20" autocomplete="off">'
print("修复前:", sample)
print("修复后:", fix_calc_input(sample))