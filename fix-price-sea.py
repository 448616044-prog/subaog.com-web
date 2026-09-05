#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprehensive price + sea-freight + transit-time corruption cleanup.

Red lines enforced:
- Air only (sea = discontinued), CNY only for own prices, min 20kg,
- 3-tier pricing: US ¥100/90, EU ¥90/80, Asia ¥80/70, 10-15 working days.
"""
import subprocess

base = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"
files = subprocess.check_output(["find", "en", "zh-cn", "-name", "*.html"], cwd=base).decode().splitlines()

# Global exact-string replacements (safe/idempotent; only corrupt files match)
GLOBAL = [
    # --- en: corrupted "¥80–11/kg ... –5/kg" (US tier) -> clean ¥100/¥90 ---
    ("Air freight from ¥80–11/kg for shipments over 20kg, and –5/kg (luggage line, effective 2026-6-30).",
     "Air freight from ¥100/kg (20–99kg), and ¥90/kg (100kg+) — luggage line, tax-inclusive."),
    # --- en: corrupted USPS third-party reference ¥100–30 -> $10–30 ---
    ("Small parcels (under 2kg) cost ¥100–30 via USPS-style channels.",
     "For reference, small parcels via USPS cost about $10–30."),
    ("USPS First Class is cheapest at ¥100–30.", "USPS First Class is cheapest at about $10–30."),
    ("USPS is cheapest for tiny parcels (under 2kg) at ¥100–30.",
     "USPS is cheapest for tiny parcels (under 2kg) at about $10–30."),
    # --- en: blank sea phrase in transit FAQ -> remove blank ---
    ("10–15 working days door-to-door. . During peak seasons",
     "10–15 working days door-to-door. During peak seasons"),
    # --- en dhl-vs-fedex comparison table corrupted price ---
    ("Cost 3–5x | ¥80–11/kg", "Cost 3–5x | ¥100/kg"),
    # --- zh: blank "不急用的选。" (was "不急用的选海运。") -> sea discontinued ---
    ("不急用的选。急用的选空运：", "海运已下架，统一走空运专线。空运："),
]

# File-specific replacements
SPECIFIC = {
    "en/usa-moving-to-china/index.html": [
        ("Air freight–5/kg (20kg+).", "Air freight from ¥100/kg (20kg+), ¥90/kg (100kg+)."),
        ("Air freight takes door-to-door. Air freight (for smaller moves) takes 10–15 days.",
         "Air freight takes 10–15 working days door-to-door (incl. customs + delivery)."),
    ],
    "en/blog/usa-to-china-cheapest-way.html": [
        (". Slower () but unbeatable for moving or bulk shipping.",
         "Air freight line (10–15 working days) — unbeatable for moving or bulk shipping."),
    ],
    "zh-cn/usa-to-china/index.html": [
        ("美国寄中国：1-20kg ¥100/kg、21-99kg ¥80/kg、100kg+ ¥90/kg（空运双清包税门到门）",
         "美国寄中国：20-99kg ¥100/kg、100kg+ ¥90/kg（空运双清包税门到门）"),
        # 美国 tier: fix wrong ¥80 -> ¥100 (already have "空运：" prefix from global)
        ("空运：¥80/kg起。华人集运专线比美国邮政", "空运：¥100/kg起。华人集运专线比美国邮政"),
        # trunk air transit should be 3-5 days, not 10-15
        ("空运干线10-15 个工作日+清关1-2天", "空运干线3-5 天+清关1-2天"),
    ],
}

changed_files = 0
total_hits = 0
for rel in files:
    p = base + "/" + rel
    try:
        with open(p, "r", encoding="utf-8") as f:
            t = f.read()
    except Exception:
        continue
    orig = t
    for a, b in GLOBAL:
        t = t.replace(a, b)
    if rel in SPECIFIC:
        for a, b in SPECIFIC[rel]:
            c = t.count(a)
            if c == 0:
                print(f"WARN 未命中 {rel}: {a[:40]}...")
            else:
                total_hits += c
            t = t.replace(a, b)
    if t != orig:
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
        changed_files += 1

print("DONE 修改文件数:", changed_files, "specific命中:", total_hits)
