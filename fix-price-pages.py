#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一 pricing.html 主表 + shipping-calculator 计算规则 价格为最新 3 档包税价
新价: 档1 ¥100/90, 档2 ¥90/80, 档3 ¥80/70 (起重20kg)
用占位符法避免连环替换
"""
from pathlib import Path

ROOT = Path(".")


def swap_prices(t: str) -> str:
    """占位符法: 旧价 -> 新价 (人民币元/kg 或 ¥/kg 两种格式)"""
    pairs = [
        ("80元/kg", "100元/kg"),
        ("75元/kg", "90元/kg"),
        ("70元/kg", "80元/kg"),
        ("65元/kg", "70元/kg"),
        ("¥80/kg", "¥100/kg"),
        ("¥75/kg", "¥90/kg"),
        ("¥70/kg", "¥80/kg"),
        ("¥65/kg", "¥70/kg"),
    ]
    # 占位
    for i, (old, new) in enumerate(pairs):
        t = t.replace(old, f"__PRICE{i}__")
    # 还原
    for i, (old, new) in enumerate(pairs):
        t = t.replace(f"__PRICE{i}__", new)
    return t


def main():
    targets = [
        "zh-cn/pricing.html",
        "zh-cn/tools/shipping-calculator.html",
    ]
    for rel in targets:
        p = ROOT / rel
        t = p.read_text(encoding="utf-8", errors="ignore")
        new = swap_prices(t)
        if new != t:
            p.write_text(new, encoding="utf-8")
            print(f"✅ {rel}")
        else:
            print(f"• 无变化 {rel}")


if __name__ == "__main__":
    main()
