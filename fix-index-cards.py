#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复主页国家卡片价格: 按国家档位精准替换(80/75/70/65 元/kg + 美元 -> 新 ¥100/90/80/70)
zh-cn: 80元/kg -> ¥100/kg(档1) / 90/kg(档2) / 80/kg(档3)
en: $4.50/kg etc -> ¥100/kg(档1) / ¥90/kg(档2) / ¥80/kg(档3)
"""
import re
from pathlib import Path

ROOT = Path(".")

# 档位 -> (20-99kg价, 100kg+价)
PRICES = {1: ("100", "90"), 2: ("90", "80"), 3: ("80", "70")}

# 国家 -> 档位
ZH_TIER = {
    "美国": 1, "加拿大": 1, "澳大利亚": 1, "澳洲": 1,
    "欧洲": 2,
    "新加坡": 3, "马来西亚": 3, "日本": 3, "韩国": 3,
}
EN_TIER = {
    "USA": 1, "Canada": 1, "Australia": 1,
    "Europe": 2,
    "Japan": 3, "Korea": 3, "SE Asia": 3,
}


def fix_zh_cards(t: str) -> str:
    def repl(m):
        country = m.group(1)
        tier = ZH_TIER.get(country, 1)
        p1, p2 = PRICES[tier]
        return f'<h3>{country}→中国</h3>\n          <div class="route-price">20-99kg <strong>¥{p1}/kg</strong> | 100kg+ <strong>¥{p2}/kg</strong></div>'
    return re.sub(
        r'<h3>([^→]+)→中国</h3>\s*<div class="route-price">21kg\+\s*<strong>[^<]+</strong>\s*\|\s*100kg\+\s*<strong>[^<]+</strong></div>',
        repl, t,
    )


def fix_en_cards(t: str) -> str:
    def repl(m):
        country = m.group(1)
        tier = EN_TIER.get(country, 1)
        p1, p2 = PRICES[tier]
        return f'<h3>{country} → China</h3>\n          <div class="price">from ¥{p1}/kg · 20kg+ (100kg+ ¥{p2}/kg)</div>\n          <div class="meta">\\2</div>'
    return re.sub(
        r'<h3>([^→]+?) → China</h3>\s*<div class="price">from \$[0-9.]+/kg · 21kg\+</div>\s*<div class="meta">([^<]+)</div>',
        repl, t,
    )


def main():
    for rel, fixer in [("zh-cn/index.html", fix_zh_cards), ("en/index.html", fix_en_cards)]:
        p = ROOT / rel
        t = p.read_text(encoding="utf-8", errors="ignore")
        new = fixer(t)
        if new != t:
            p.write_text(new, encoding="utf-8")
            print(f"✅ {rel}")
        else:
            print(f"• 无变化 {rel}")


if __name__ == "__main__":
    main()
