#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
subaog.com — 补 blog/工具/聚合页 FAQPage (中英)
主题词映射 + 模板生成 3 个 FAQ, 注入 JSON-LD + 可见区块, 幂等
"""
import re
import json
from pathlib import Path

ROOT = Path(".")

# slug -> (中文主题词, 英文主题词)
TOPICS = {
    "can-i-ship-baby-formula-to-china": ("奶粉", "baby formula"),
    "can-i-ship-cosmetics-to-china": ("化妆品", "cosmetics"),
    "can-i-ship-electronics-to-china": ("电子产品", "electronics"),
    "can-i-ship-luxury-bags-to-china": ("奢侈品包", "luxury bags"),
    "can-i-ship-supplements-to-china": ("保健品", "supplements"),
    "how-to-choose-international-shipping-method": ("国际物流渠道", "international shipping method"),
    "how-to-pack-for-international-shipping": ("国际包裹打包", "international packaging"),
    "international-customs-duty-guide": ("国际关税", "international customs duty"),
    "international-shipping-insurance-guide": ("国际物流保险", "shipping insurance"),
    "japan-to-china-shipping-guide": ("日本寄中国", "shipping from Japan to China"),
    "prohibited-items-complete-guide": ("禁运品", "prohibited items"),
    "shipping-cost-save-money-tips": ("物流省钱", "saving on shipping"),
    "shipping-from-asia-to-china-comparison": ("亚洲寄中国", "shipping from Asia to China"),
    "student-luggage-express-comparison": ("留学生行李快递", "student luggage express"),
    "student-luggage-shipping-guide": ("留学生行李", "student luggage"),
    "usa-moving-to-china-guide": ("搬家回国", "moving to China"),
    "usa-to-china-cheapest-way": ("最便宜寄中国", "cheapest way to ship to China"),
    "usa-to-china-customs-duty": ("美国寄中国关税", "USA to China customs duty"),
    "usa-to-china-packaging-guide": ("美国寄中国打包", "USA to China packaging"),
    "usa-to-china-prohibited-items": ("美国寄中国禁运品", "USA to China prohibited items"),
    "usa-to-china-sea-freight": ("美国寄中国海运", "USA to China sea freight"),
    "usps-vs-fedex-vs-chinese-courier": ("USPS/FedEx 对比", "USPS vs FedEx vs Chinese courier"),
    "index": ("跨境物流", "cross-border shipping"),
}


def faqs_for(slug, lang):
    zh, en = TOPICS.get(slug, ("跨境物流", "cross-border shipping"))
    if lang == "zh-cn":
        if slug.startswith("can-i-ship-"):
            return [
                (f"{zh}能寄回中国吗？", f"可以，属可寄品类，我们协助正规报关清关。"),
                (f"寄{zh}回中国要交税吗？", "超个人自用合理数量需缴关税/增值税（约 13%），以海关核定为准。"),
                (f"寄{zh}回中国多久到？", "空运 10-15 个工作日，海运 25-35 天，门到门。"),
            ]
        return [
            (f"{zh}怎么选最划算？", "小件/急件走空运，大件/搬家走海运，本页有详细对比。"),
            (f"{zh}大概多少钱？", "空运约 $9.5/kg（21kg 起），海运约 $5.5/kg，可免费估价。"),
            (f"{zh}多久能到？", "空运 10-15 个工作日，海运 25-35 天。"),
        ]
    else:
        if slug.startswith("can-i-ship-"):
            return [
                (f"Can I ship {en} to China?", "Yes, it's an allowed category and we handle customs declaration."),
                (f"Is there duty on {en} to China?", "Amounts above the personal-use allowance incur duty/VAT (about 13%), as assessed by customs."),
                (f"How long does {en} take to China?", "Air freight 10–15 working days; sea freight 25–35 days, door-to-door."),
            ]
        return [
            (f"What's the cheapest way for {en}?", "Small/urgent items by air, bulky/moving by sea — this page compares options."),
            (f"How much does {en} cost?", "Air freight from about $9.5/kg (21kg+); sea freight from about $5.5/kg. Free quote."),
            (f"How long does {en} take?", "Air freight 10–15 working days; sea freight 25–35 days."),
        ]


def build_jsonld(faqs):
    main = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": main}, ensure_ascii=False)


def build_visible(faqs, lang):
    title = "常见问题" if lang == "zh-cn" else "FAQ"
    items = []
    for q, a in faqs:
        items.append(
            '<div style="border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px;margin-bottom:10px">'
            f'<h3 style="font-size:15px;font-weight:600;margin:0 0 6px">{q}</h3>'
            f'<p style="margin:0;color:#64748B;line-height:1.7">{a}</p></div>'
        )
    return ('<section style="max-width:1100px;margin:40px auto;padding:0 24px">'
            f'<h2 style="font-size:22px;font-weight:700;margin-bottom:16px">{title}</h2>'
            + "".join(items) + "</section>")


def process(rel):
    f = ROOT / rel
    if not f.exists():
        return "missing"
    t = f.read_text(encoding="utf-8", errors="ignore")
    if "FAQPage" in t:
        return "skip"
    lang = "zh-cn" if rel.startswith("zh-cn/") else "en"
    slug = rel.split("/")[-1].replace(".html", "")
    if slug == "index":
        slug = "index"
    faqs = faqs_for(slug, lang)
    ld = '<script type="application/ld+json">' + build_jsonld(faqs) + "</script>"
    t = t.replace("</head>", ld + "\n</head>", 1)
    vis = build_visible(faqs, lang)
    if "</footer>" in t:
        t = t.replace("</footer>", vis + "\n</footer>", 1)
    f.write_text(t, encoding="utf-8")
    return "done"


def main():
    targets = []
    # blog 页 (排除已有/城市页)
    for p in sorted(ROOT.glob("en/blog/*.html")) + sorted(ROOT.glob("zh-cn/blog/*.html")):
        targets.append(str(p))
    # tools 页
    for p in sorted(ROOT.glob("en/tools/*.html")) + sorted(ROOT.glob("zh-cn/tools/*.html")):
        targets.append(str(p))
    # 聚合页
    for p in ["en/can-i-ship-index/index.html", "zh-cn/can-i-ship-index/index.html",
              "en/routes/index.html", "zh-cn/routes/index.html",
              "en/faq.html", "zh-cn/faq.html", "en/pricing.html", "zh-cn/pricing.html",
              "en/contact.html", "zh-cn/contact.html",
              "en/report/usa-china-shipping-cost-report-2026.html", "zh-cn/report/usa-china-shipping-cost-report-2026.html",
              "zh-cn/student-luggage/index.html", "zh-cn/seasia-to-china/packing-guide/index.html",
              "zh-cn/seasia-to-china/pricing/index.html"]:
        targets.append(p)

    done = skip = missing = 0
    for rel in targets:
        r = process(rel)
        if r == "done":
            done += 1
            print(f"  ✅ {rel}")
        elif r == "skip":
            skip += 1
        else:
            missing += 1
            print(f"  ⏭️ 不存在: {rel}")
    print(f"\n修复 {done} | 跳过(已有) {skip} | 不存在 {missing}")


if __name__ == "__main__":
    main()
