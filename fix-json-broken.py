#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复删海运导致的 JSON-LD 破坏 + 正文标点残破
13 个海运相关页: 重新生成 FAQPage(空运主题)
"""
import re
import json
from pathlib import Path

ROOT = Path(".")

BROKEN = [
    "zh-cn/tools/transit-time.html",
    "zh-cn/blog/moving-season-sea-freight.html",
    "zh-cn/blog/graduation-luggage-shipping.html",
    "zh-cn/blog/usa-to-china-sea-freight.html",
    "zh-cn/blog/usa-to-china-shipping-time.html",
    "zh-cn/blog/student-luggage-shipping-guide.html",
    "zh-cn/blog/how-to-choose-international-shipping-method.html",
    "zh-cn/usa-moving-to-china/index.html",
    "en/tools/transit-time.html",
    "en/blog/moving-season-sea-freight.html",
    "en/blog/graduation-luggage-shipping.html",
    "en/blog/usa-to-china-sea-freight.html",
    "en/blog/usa-to-china-shipping-time.html",
]

FAQS_ZH = [
    ("空运寄中国要多久？", "空运 10-15 个工作日，门到门（日韩 7-12 天）。"),
    ("空运寄中国多少钱？", "包税双清：美/加/墨/澳/新 ¥100/kg、欧洲 ¥90/kg、日韩东南亚 ¥80/kg（20-99kg），起重 20kg，含清关费 100 元申报手续费。"),
    ("空运能寄什么？", "行李、个人物品、衣物、书籍、小家电等（武器/毒品/动植物/食品/烟酒等禁运品除外）。"),
]
FAQS_EN = [
    ("How long does air freight to China take?", "Air freight takes 10–15 working days door-to-door (Japan/Korea 7–12 days)."),
    ("How much does air freight to China cost?", "Tax-inclusive door-to-door: USA/CA/MX/AU/NZ ¥100/kg, Europe ¥90/kg, Japan/Korea/SEA ¥80/kg (20–99 kg). Minimum 20 kg, plus ¥100 declaration fee."),
    ("What can I ship by air?", "Luggage, personal items, clothing, books, small appliances (weapons, plants, food, tobacco, alcohol etc. excluded)."),
]


def rebuild_faq(lang):
    faqs = FAQS_ZH if lang == "zh-cn" else FAQS_EN
    obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }
    return json.dumps(obj, ensure_ascii=False)


def main():
    fixed = 0
    for rel in BROKEN:
        p = ROOT / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        lang = "zh-cn" if rel.startswith("zh-cn/") else "en"
        # 删除所有 FAQPage JSON-LD 块(含破坏的)
        t = re.sub(
            r'<script type="application/ld\+json">\s*\{[^{}]*"@type"\s*:\s*"FAQPage".*?</script>',
            "",
            t,
            flags=re.S,
        )
        # 重新注入空运 FAQPage
        ld = '<script type="application/ld+json">' + rebuild_faq(lang) + "</script>"
        t = t.replace("</head>", ld + "\n</head>", 1)
        p.write_text(t, encoding="utf-8")
        fixed += 1
        print(f"✅ {rel}")
    print(f"\n修复 {fixed} 页")


if __name__ == "__main__":
    main()
