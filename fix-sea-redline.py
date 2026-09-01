#!/usr/bin/env python3
"""subaog.com en 站海运红线词残留清理。
红线: 只空运(海运已下架)。清理承诺海运服务的描述, 保留科普对比页(待用户决策)。
用法: python3 fix-sea-redline.py [--run]  (默认 dry-run)
"""
import re, sys, glob

DRY = "--run" not in sys.argv

# 精确替换映射 (承诺服务型海运词 → 空运/删除)
RULES = [
    ("Allowed (sea)", "Allowed"),                                    # 家具"可海运寄"→可寄
    ("by ; mind", "by air; mind"),                                    # 家具残缺"by ; mind"→"by air; mind"
    ("Disassemble first; sea\u2026", "Disassemble first."),           # 自行车desc截断"sea…"→"."
    ("sea , express", "express"),                                     # 时效页"sea , express"→"express"
    ("Door-to-door in Sea , tax-inclusive", "Door-to-door in 10-15 working days, tax-inclusive"),  # 搬家页乱码
    (", sea freight 12-40 days", ""),                                 # transit-time删海运时效
    ("air/sea/express rates", "air & express rates"),                 # 成本页删海运
]

# 跳过: 海运主题博客页(待用户决策) + 科普对比页(方法选择)
SKIP_IF = ["sea-freight", "how-to-choose-international-shipping-method"]

def main():
    total_files = 0
    total_repl = 0
    for f in sorted(glob.glob('en/**/*.html', recursive=True)):
        if any(k in f for k in SKIP_IF):
            continue
        s = open(f, encoding='utf-8').read()
        s2 = s
        file_repl = 0
        for old, new in RULES:
            n = s2.count(old)
            if n:
                s2 = s2.replace(old, new)
                file_repl += n
        if file_repl:
            total_files += 1
            total_repl += file_repl
            if not DRY:
                open(f, 'w', encoding='utf-8').write(s2)
            print(f"  {f}: {file_repl} 处")
    print(f"\n{'[DRY-RUN]' if DRY else '[已执行]'} 共 {total_files} 文件 / {total_repl} 处替换")

if __name__ == '__main__':
    main()
