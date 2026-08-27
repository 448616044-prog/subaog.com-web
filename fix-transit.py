#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站空运时效统一为 10-15 个工作日 + 删海运时效(25-35)
保留快递竞品时效(3-5天/1-3天 是 FedEx/DHL 对比)
"""
from pathlib import Path

ROOT = Path(".")

ZH_TRANSIT = [
    ("7-10 个工作日", "10-15 个工作日"),
    ("7-10 工作日", "10-15 个工作日"),
    ("7-10个工作日", "10-15 个工作日"),
    ("7-10 天", "10-15 个工作日"),
    ("7-10天", "10-15 个工作日"),
    ("7-12 个工作日", "10-15 个工作日"),
    ("7-12天", "10-15 个工作日"),
    ("10-15 工作日", "10-15 个工作日"),
    ("10-15工作日", "10-15 个工作日"),
    ("10-15 天", "10-15 个工作日"),
    ("10-15天", "10-15 个工作日"),
    ("10-15 个工作日", "10-15 个工作日"),  # 兜底统一
    # 删海运时效
    ("25-35 个工作日", ""),
    ("25-35 工作日", ""),
    ("25-35 天", ""),
    ("25-35天", ""),
    ("25-35天门到门", ""),
]

EN_TRANSIT = [
    ("7-10 working days", "10-15 working days"),
    ("7–10 working days", "10–15 working days"),
    ("7-12 working days", "10-15 working days"),
    ("7–12 working days", "10–15 working days"),
    # 删海运时效
    ("25–35 days", ""),
    ("25-35 days", ""),
]


def main():
    fixed = 0
    for d, pairs in [("zh-cn", ZH_TRANSIT), ("en", EN_TRANSIT)]:
        for f in sorted((ROOT / d).rglob("*.html")):
            t = f.read_text(encoding="utf-8", errors="ignore")
            orig = t
            for old, new in pairs:
                t = t.replace(old, new)
            if t != orig:
                f.write_text(t, encoding="utf-8")
                fixed += 1
    print(f"修复 {fixed} 页")


if __name__ == "__main__":
    main()
