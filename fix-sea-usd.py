#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站价格统一(第二轮): ①删海运只留空运 ②美元价转人民币(en+zh-cn残留)
"""
import re
from pathlib import Path

ROOT = Path(".")

# ---- 删海运 (zh-cn) ----
ZH_SEA = [
    (r"海运专线约 \$[0-9./\-]+（[^）]*）", ""),
    (r"海运约 \$[0-9./\-]+", ""),
    (r"，海运[^。；，]*", ""),
    (r"、海运[^。；，]*", ""),
    (r"空运\s*/\s*海运专线", "空运专线"),
    (r"空运\s*/\s*海运", "空运"),
    (r"/\s*海运[^。；，]*", ""),
    (r"海运[^。；，]*", ""),
]

# ---- 删 sea freight (en) ----
EN_SEA = [
    (r"[Ss]ea freight from about \$[0-9./\-]+(?:/kg)?", ""),
    (r"[Ss]ea freight from \$[0-9./\-]+(?:/kg)?", ""),
    (r"，?[Ss]ea freight[^.,;]*", ""),
    (r",?\s*[Ss]ea freight[^.,;]*", ""),
    (r"[Aa]ir\s*/\s*[Ss]ea freight", "Air freight"),
    (r"/\s*[Ss]ea freight[^.,;]*", ""),
    (r"[Ss]ea freight[^.,;]*", ""),
]

# ---- 美元 -> 人民币 (占位符, 先长后短) ----
USD_PAIRS = [
    ("$10.50", "¥90"), ("$10.5", "¥90"),
    ("$10.40", "¥90"), ("$10.4", "¥90"),
    ("$9.70", "¥80"), ("$9.7", "¥80"),
    ("$9.50", "¥80"), ("$9.5", "¥80"),
    ("$11.00", "¥100"), ("$11", "¥100"),
    ("$9.00", "¥70"), ("$9", "¥70"),
    ("$15.00", "¥100"), ("$15", "¥100"),
]


def swap_usd(t: str) -> str:
    for i, (o, n) in enumerate(USD_PAIRS):
        t = t.replace(o, f"__USD{i}__")
    for i, (o, n) in enumerate(USD_PAIRS):
        t = t.replace(f"__USD{i}__", n)
    return t


def clean_zh(t: str) -> str:
    for pat, rep in ZH_SEA:
        t = re.sub(pat, rep, t)
    # 清理多余标点/空格
    t = re.sub(r"，{2,}", "，", t)
    t = re.sub(r"，\s*。", "。", t)
    t = re.sub(r"，\s*，", "，", t)
    t = re.sub(r"，\s*$", "", t)
    return t


def clean_en(t: str) -> str:
    for pat, rep in EN_SEA:
        t = re.sub(pat, rep, t)
    t = re.sub(r",\s*,", ",", t)
    t = re.sub(r",\s*\.", ".", t)
    return t


def main():
    fixed = 0
    # zh-cn: 删海运 + 美元残留转人民币
    for f in sorted((ROOT / "zh-cn").rglob("*.html")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        orig = t
        t = clean_zh(t)
        t = swap_usd(t)
        if t != orig:
            f.write_text(t, encoding="utf-8")
            fixed += 1
    # en: 删 sea freight + 美元转人民币
    for f in sorted((ROOT / "en").rglob("*.html")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        orig = t
        t = clean_en(t)
        t = swap_usd(t)
        if t != orig:
            f.write_text(t, encoding="utf-8")
            fixed += 1
    print(f"修复 {fixed} 页")


if __name__ == "__main__":
    main()
