#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复单引号 JSON-LD(非法 JSON) -> ast 解析重建为合法双引号 JSON"""
import re
import json
import ast
from pathlib import Path

ROOT = Path(".")


def main():
    fixed = 0
    for p in sorted(ROOT.rglob("*.html")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        changed = False
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            blk = m.group(1).strip()
            if not blk:
                continue
            try:
                json.loads(blk)
                continue  # 合法跳过
            except Exception:
                pass
            try:
                obj = ast.literal_eval(blk)
                fixed_blk = json.dumps(obj, ensure_ascii=False)
            except Exception as e:
                print(f"  ❌ 无法修复 {p}: {str(e)[:60]}")
                continue
            t = t.replace(blk, fixed_blk, 1)
            changed = True
        if changed:
            p.write_text(t, encoding="utf-8")
            fixed += 1
            print(f"  ✅ 修复 {p.relative_to(ROOT)}")
    print(f"\n修复 {fixed} 页")


if __name__ == "__main__":
    main()
