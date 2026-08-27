#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
subaog.com — 补中文站城市页 FAQPage(镜像英文站)
34 个 zh-cn 国家集群城市页缺 FAQPage(英文站已有), 注入 JSON-LD + 可见 FAQ 区块
幂等: 已含 FAQPage 跳过
"""
import re
import json
from pathlib import Path

ROOT = Path(".")

COUNTRIES = {
    "australia-to-china": {
        "cities": {"adelaide": "阿德莱德", "brisbane": "布里斯班", "gold-coast": "黄金海岸",
                   "melbourne": "墨尔本", "perth": "珀斯", "sydney": "悉尼"},
        "faqs": [
            ("{city}寄中国要多久？", "空运 10-15 个工作日，海运 25-35 天，全程门到门。"),
            ("澳洲保健品能寄中国吗？", "可以。保健品和维生素是核心品类，我们负责清关文件与成分限制确认。"),
            ("{city}寄中国多少钱？", "空运约 $9.5/kg（21kg 起），海运约 $5.5/kg，可免费估价。"),
        ],
    },
    "canada-to-china": {
        "cities": {"calgary": "卡尔加里", "edmonton": "埃德蒙顿", "montreal": "蒙特利尔",
                   "ottawa": "渥太华", "toronto": "多伦多", "vancouver": "温哥华"},
        "faqs": [
            ("{city}寄中国要多久？", "空运 10-15 个工作日，海运 25-35 天，全程门到门。"),
            ("{city}寄中国多少钱？", "空运约 $9.5/kg（21kg 起），海运约 $5.5/kg，可免费估价。"),
            ("加拿大能寄家居用品到中国吗？", "可以。家具、家电和家居用品均支持，按体积重计费。"),
        ],
    },
    "europe-to-china": {
        "cities": {"amsterdam": "阿姆斯特丹", "berlin": "柏林", "brussels": "布鲁塞尔",
                   "london": "伦敦", "madrid": "马德里", "milan": "米兰",
                   "paris": "巴黎", "rome": "罗马"},
        "faqs": [
            ("{city}寄中国要多久？", "空运 10-15 个工作日，海运 25-35 天，全程门到门。"),
            ("欧洲能寄奢侈品到中国吗？", "可以。奢侈品是核心品类，全程保价并合规清关。"),
            ("{city}寄中国多少钱？", "空运约 $9.5/kg（21kg 起），海运约 $5.5/kg，可免费估价。"),
        ],
    },
    "japan-to-china": {
        "cities": {"fukuoka": "福冈", "kobe": "神户", "kyoto": "京都", "nagoya": "名古屋",
                   "osaka": "大阪", "sapporo": "札幌", "tokyo": "东京", "yokohama": "横滨"},
        "faqs": [
            ("{city}寄中国要多久？", "空运 7-12 个工作日，门到门。"),
            ("日本化妆品能寄中国吗？", "可以。化妆品是核心品类，需符合成分备案要求。"),
            ("{city}寄中国多少钱？", "空运约 $9/kg（21kg 起），小包裹约 $12 起，可免费估价。"),
        ],
    },
    "korea-to-china": {
        "cities": {"busan": "釜山", "daegu": "大邱", "daejeon": "大田",
                   "gwangju": "光州", "incheon": "仁川", "seoul": "首尔"},
        "faqs": [
            ("{city}寄中国要多久？", "空运 7-12 个工作日，门到门。"),
            ("韩国化妆品能寄中国吗？", "可以。化妆品是核心品类，需符合成分备案要求。"),
            ("{city}寄中国多少钱？", "空运约 $8/kg（21kg 起），小包裹约 $10 起，可免费估价。"),
        ],
    },
}


def build_jsonld(faqs):
    main = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": main}, ensure_ascii=False)


def build_visible(faqs):
    items = []
    for q, a in faqs:
        items.append(
            '<div style="border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px;margin-bottom:10px">'
            f'<h3 style="font-size:15px;font-weight:600;margin:0 0 6px">{q}</h3>'
            f'<p style="margin:0;color:#64748B;line-height:1.7">{a}</p></div>'
        )
    return ('<section style="max-width:1100px;margin:40px auto;padding:0 24px">'
            '<h2 style="font-size:22px;font-weight:700;margin-bottom:16px">常见问题</h2>'
            + "".join(items) + "</section>")


def main():
    fixed = skipped = 0
    for country, cfg in COUNTRIES.items():
        for slug, cn in cfg["cities"].items():
            f = ROOT / "zh-cn" / country / slug / "index.html"
            if not f.exists():
                print(f"  ⏭️ 不存在: {f}")
                continue
            t = f.read_text(encoding="utf-8", errors="ignore")
            if "FAQPage" in t:
                skipped += 1
                continue
            faqs = [(q.format(city=cn), a) for q, a in cfg["faqs"]]
            ld = '<script type="application/ld+json">' + build_jsonld(faqs) + "</script>"
            t = t.replace("</head>", ld + "\n</head>", 1)
            vis = build_visible(faqs)
            if "</footer>" in t:
                t = t.replace("</footer>", vis + "\n</footer>", 1)
            f.write_text(t, encoding="utf-8")
            fixed += 1
            print(f"  ✅ {f.relative_to(ROOT)}")
    print(f"\n修复 {fixed} | 跳过(已有) {skipped}")


if __name__ == "__main__":
    main()
