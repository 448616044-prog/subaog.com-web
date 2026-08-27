#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复新价格表块的两处问题:
1. 服务包含行: 去掉 "含清关 + 100元申报手续费。"(已在表"资料"列单独说明)
2. 删掉整行"轨迹: m.qianxunimport.com"
只针对之前 fix-price-table.py 替换过的 7 个国家集群 zh-cn 页面
"""
import re
from pathlib import Path

ROOT = Path(".")
PREFIXES = [
    "usa-to-china", "canada-to-china", "australia-to-china",
    "europe-to-china", "japan-to-china", "korea-to-china", "seasia-to-china",
]

fixed = 0
for pfx in PREFIXES:
    for f in (ROOT / "zh-cn" / pfx).rglob("*.html"):
        t = f.read_text(encoding="utf-8", errors="ignore")
        orig = t
        # 1) 服务包含: 去 "，含清关 + 100元申报手续费。"
        t = t.replace("，含清关 + 100元申报手续费。", "")
        # 2) 删含 qianxunimport.com 的整行(轨迹行, 按行处理更稳)
        new_lines = [
            l for l in t.split("\n") if "qianxunimport.com" not in l
        ]
        t = "\n".join(new_lines)
        if t != orig:
            f.write_text(t, encoding="utf-8")
            fixed += 1
print(f"修复 {fixed} 页")
