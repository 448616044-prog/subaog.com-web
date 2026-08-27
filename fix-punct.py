#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理删海运后的残破标点(全站 zh-cn + en)"""
from pathlib import Path

ROOT = Path(".")

PUNCT = [
    ("；。", "。"),
    ("； ；", "；"),
    ("；，", "，"),
    ("，。", "。"),
    ("，；", "，"),
    ("; .", "."),
    ("; ,", ","),
    ("; ;", ";"),
    (", .", "."),
    ("  。", "。"),
    (" 。", "。"),
]


def main():
    fixed = 0
    for d in ["zh-cn", "en"]:
        for f in sorted((ROOT / d).rglob("*.html")):
            t = f.read_text(encoding="utf-8", errors="ignore")
            orig = t
            for old, new in PUNCT:
                t = t.replace(old, new)
            if t != orig:
                f.write_text(t, encoding="utf-8")
                fixed += 1
    print(f"修复 {fixed} 页")


if __name__ == "__main__":
    main()
