#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站起步规则: 20kg 起重 -> 21kg 起步, 不足 21kg 不予收寄(红线变更)
"""
from pathlib import Path

ROOT = Path(".")

ZH = [
    ("起重 20kg，不足 20kg 按 20kg 算", "最低起运 21kg（实重或体积重≥21kg 方可出运，不足 21kg 不予收寄）"),
    ("起重 20kg：不足 20kg 按 20kg 算（即最低收费 20kg）", "最低起运 21kg（实重或体积重≥21kg 方可收寄；不足 21kg 不予出运）"),
    ("最低收费 20kg", "最低起运 21kg"),
    ("20kg（最低收费）", "21kg（最低起运）"),
]
EN = [
    ("Minimum charge: 20 kg", "Minimum 21 kg (actual or volumetric weight ≥21 kg required; below not accepted)"),
    ("shipments under 20 kg are billed as 20 kg", "shipments under 21 kg are not accepted"),
    ("20kg minimum, plus 100 RMB", "21kg minimum, plus 100 RMB"),
    ("20kg starting, plus", "21kg starting, plus"),
]


def main():
    fixed = 0
    for d, pairs in [("zh-cn", ZH), ("en", EN)]:
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
