#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站 zh-cn 价格统一 (最新 3 档包税价)
旧价 -> 新价 (占位符法避免连环): ¥80->¥100, ¥75->¥90, ¥70->¥80, ¥65->¥70
保护 price-block(已新价) + 海运 ¥45 不动
"""
import re
from pathlib import Path

ROOT = Path(".")
PAIRS = [("¥80", "¥100"), ("¥75", "¥90"), ("¥70", "¥80"), ("¥65", "¥70")]


def swap_global(t: str) -> str:
    for i, (o, n) in enumerate(PAIRS):
        t = t.replace(o, f"__PR{i}__")
    for i, (o, n) in enumerate(PAIRS):
        t = t.replace(f"__PR{i}__", n)
    return t


def main():
    fixed = 0
    for f in sorted((ROOT / "zh-cn").rglob("*.html")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        # 提取 price-block 保护
        blocks = re.findall(r'<div class="price-block".*?</div>\n</div>', t, re.S)
        for i, b in enumerate(blocks):
            t = t.replace(b, f"__BLOCK{i}__")
        new = swap_global(t)
        for i, b in enumerate(blocks):
            new = new.replace(f"__BLOCK{i}__", b)
        if new != t:
            f.write_text(new, encoding="utf-8")
            fixed += 1
    print(f"修复 {fixed} 页")


if __name__ == "__main__":
    main()
