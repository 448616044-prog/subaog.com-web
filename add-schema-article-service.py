#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补齐结构化数据缺口：
1. 40 篇 can-i-ship 物品页缺 Article schema（中英各20）
2. 核心转化页注入 Service+Offer schema（物流服务商核心）

幂等：已有则跳过，可安全重跑。
"""
import re
import json
from pathlib import Path

ROOT = Path(".")

# ============ Part 1: 补齐 Article schema ============
def extract_meta(path):
    t = path.read_text(encoding="utf-8", errors="ignore")
    title = re.search(r"<title>([^<]+)</title>", t)
    desc = re.search(r'<meta name="description" content="([^"]*)"', t)
    headline = ""
    if title:
        # 去掉 " | Subao..." 品牌后缀
        headline = re.split(r"\s*\|\s*", title.group(1))[0].strip()
    description = desc.group(1).strip() if desc else headline
    return headline, description

def build_article_ld(headline, description, lang):
    pub_name = "Subao Global Logistics" if lang == "en" else "速豹回国物流"
    obj = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "inLanguage": lang,
        "publisher": {"@type": "Organization", "name": pub_name},
    }
    return "<script type=\"application/ld+json\">" + json.dumps(obj, ensure_ascii=False) + "</script>"

def part1():
    fixed = 0
    for d in ["zh-cn", "en"]:
        lang = "zh-CN" if d == "zh-cn" else "en"
        for p in sorted((ROOT / d / "blog").glob("*.html")):
            if p.name == "index.html":
                continue
            t = p.read_text(encoding="utf-8", errors="ignore")
            if '"@type": "Article"' in t or '"@type":"Article"' in t:
                continue  # 已有
            if "FAQPage" not in t:
                continue  # 非物品页（不强行加）
            headline, description = extract_meta(p)
            if not headline:
                continue
            ld = build_article_ld(headline, description, lang)
            # 注入到 </head> 前
            t = t.replace("</head>", ld + "\n</head>", 1)
            p.write_text(t, encoding="utf-8")
            fixed += 1
    print(f"[Part1] 补 Article schema: {fixed} 篇")

# ============ Part 2: 核心转化页 Service schema ============
SERVICE_CORE = [
    "zh-cn/index.html", "en/index.html",
    "zh-cn/pricing.html", "en/pricing.html",
    "zh-cn/usa-to-china/index.html", "en/usa-to-china/index.html",
    "zh-cn/canada-to-china/index.html", "en/canada-to-china/index.html",
    "zh-cn/europe-to-china/index.html", "en/europe-to-china/index.html",
    "zh-cn/japan-to-china/index.html", "en/japan-to-china/index.html",
    "zh-cn/korea-to-china/index.html", "en/korea-to-china/index.html",
    "zh-cn/seasia-to-china/index.html", "en/seasia-to-china/index.html",
    "zh-cn/australia-to-china/index.html", "en/australia-to-china/index.html",
    "zh-cn/can-i-ship-index/index.html", "en/can-i-ship-index/index.html",
    "zh-cn/routes/index.html", "en/routes/index.html",
]

def build_service_ld(lang):
    if lang == "en":
        obj = {
            "@context": "https://schema.org",
            "@type": "Service",
            "serviceType": "International air freight forwarding to China",
            "provider": {"@type": "Organization", "name": "Subao Global Logistics", "url": "https://subaog.com"},
            "areaServed": ["US", "CA", "MX", "AU", "NZ", "GB", "DE", "FR", "IT", "ES", "IE", "JP", "KR", "TH", "SG", "PH", "MY"],
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "Tax-inclusive air freight to China (door-to-door)",
                "itemListElement": [
                    {"@type": "Offer", "priceCurrency": "CNY", "price": "100", "description": "USA / Canada / Mexico / Australia / New Zealand: from CNY 100/kg (20-99kg), CNY 90/kg (100kg+)"},
                    {"@type": "Offer", "priceCurrency": "CNY", "price": "90", "description": "Europe (UK/DE/FR/IT/ES/IE): from CNY 90/kg (20-99kg), CNY 80/kg (100kg+)"},
                    {"@type": "Offer", "priceCurrency": "CNY", "price": "80", "description": "Japan / Korea / Thailand / Singapore / Philippines / Taiwan / Malaysia: from CNY 80/kg (20-99kg), CNY 70/kg (100kg+)"},
                ],
            },
        }
    else:
        obj = {
            "@context": "https://schema.org",
            "@type": "Service",
            "serviceType": "国际空运专线寄中国（双清包税门到门）",
            "provider": {"@type": "Organization", "name": "速豹回国物流", "url": "https://subaog.com"},
            "areaServed": ["US", "CA", "MX", "AU", "NZ", "GB", "DE", "FR", "IT", "ES", "IE", "JP", "KR", "TH", "SG", "PH", "MY"],
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "包税空运专线寄中国（双清门到门）",
                "itemListElement": [
                    {"@type": "Offer", "priceCurrency": "CNY", "price": "100", "description": "美国/加拿大/墨西哥/澳大利亚/新西兰：¥100/kg（20-99kg），¥90/kg（100kg+）"},
                    {"@type": "Offer", "priceCurrency": "CNY", "price": "90", "description": "欧洲（英/德/法/意/西/爱等）：¥90/kg（20-99kg），¥80/kg（100kg+）"},
                    {"@type": "Offer", "priceCurrency": "CNY", "price": "80", "description": "日本/韩国/泰国/新加坡/菲律宾/中国台湾/马来西亚：¥80/kg（20-99kg），¥70/kg（100kg+）"},
                ],
            },
        }
    return "<script type=\"application/ld+json\">" + json.dumps(obj, ensure_ascii=False) + "</script>"

def part2():
    fixed = 0
    for rel in SERVICE_CORE:
        p = ROOT / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        if '"@type": "Service"' in t or '"@type":"Service"' in t:
            continue  # 已有
        lang = "en" if rel.startswith("en/") else "zh-CN"
        ld = build_service_ld(lang)
        t = t.replace("</head>", ld + "\n</head>", 1)
        p.write_text(t, encoding="utf-8")
        fixed += 1
    print(f"[Part2] 注入 Service schema: {fixed} 页")

if __name__ == "__main__":
    part1()
    part2()
