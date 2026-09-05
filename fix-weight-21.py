#!/usr/bin/env python3
"""
subaog.com 全站重量红线替换脚本
业务红线更新（用户 2026-09-05 截图）：20kg+ → 21kg+
价格红线（用户决策：暂不替换）— 完全不动。
"""
import os
import re
import subprocess

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

REPLACEMENTS = [
    (r'\b20-99kg\b', '21-99kg'),
    (r'\b20kg\+', '21kg+'),
    (r'(?<=[\s（(])>=?20kg(?=[\s，。,.;:）)\-])', '≥21kg'),
    (r'(?<=[\s（(])<=?20kg(?=[\s，。,.;:）)\-])', '<21kg'),
    (r'\bMinimum\s+20kg\b', 'Minimum 21kg'),
    (r'\bminimum\s+20kg\b', 'minimum 21kg'),
    (r'起运\s*20kg', '起运 21kg'),
    (r'最低起运\s*20kg', '最低起运 21kg'),
    (r'最低\s*20kg', '最低 21kg'),
    (r'\b20kg\b', '21kg'),
]

CALC_PATTERN = re.compile(
    r'(<input\s+[^>]*id="weight"[^>]*?)\b(min|value|placeholder)="20"',
    re.IGNORECASE
)

def process_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, [f"读取失败: {e}"]

    original = content
    diffs = []

    def calc_repl(m):
        diffs.append(f"  计算器 {m.group(2)}: 20 → 21")
        return f'{m.group(1)}{m.group(2)}="21"'

    content = CALC_PATTERN.sub(calc_repl, content)

    for pattern, replacement in REPLACEMENTS:
        matches = re.findall(pattern, content)
        if matches:
            count = len(matches)
            diffs.append(f"  {pattern}: {count} 次")
            content = re.sub(pattern, replacement, content)

    if content != original:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, diffs
        except Exception as e:
            return False, [f"写入失败: {e}"]

    return False, []


def main():
    result = subprocess.run(
        ['find', 'en', 'zh-cn', '-name', '*.html'],
        cwd=BASE, capture_output=True, text=True, timeout=60
    )
    files = [f for f in result.stdout.strip().split('\n') if f]
    print(f"待处理 HTML 文件: {len(files)}")

    changed = 0
    for rel_path in files:
        abs_path = os.path.join(BASE, rel_path)
        was_changed, diffs = process_file(abs_path)
        if was_changed:
            changed += 1
            print(f"[{rel_path}]")
            for d in diffs:
                print(d)

    print(f"\n=== 完成 ===")
    print(f"改动文件数: {changed}")


if __name__ == '__main__':
    main()