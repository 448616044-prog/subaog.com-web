#!/usr/bin/env python3
"""中词攻坚：给 routes 聚合页(中英)注入 A 组 15 中词页反链，强化权重传导(11-30 -> 首页)。
幂等：先删旧 data-midword-boost 块再重插。只链真实存在的页(防断链)。
对齐用户战略：①中词攻坚 ③聚合页高效动作。
"""
from pathlib import Path
import re

ROOT = Path(".")

# A 组 15 中词(来自 gsc-demand-report.py) -> 对应 clean URL(中英)
MID = {
    "en": [
        ("/en/blog/dhl-vs-fedex-vs-ups-china", "DHL to China 对比"),
        ("/en/city/san-diego-to-hangzhou", "San Diego to Hangzhou"),
        ("/en/blog/ebay-ship-to-china", "eBay to China 转运"),
        ("/en/blog/usps-to-china-complete-guide", "USPS to China 指南"),
        ("/en/blog/usa-to-china-cheapest-way", "Cheapest way to China"),
        ("/en/blog/usa-to-china-shipping-cost", "China shipping cost"),
        ("/en/blog/amazon-us-ship-to-china", "Amazon ship to China"),
        ("/en/city/houston-to-xian", "Shipping to Xian"),
        ("/en/city/detroit-to-dalian", "Shipping to Dalian"),
        ("/en/city/atlanta-to-changsha", "Atlanta fragile shipping"),
    ],
    "zh-cn": [
        ("/zh-cn/blog/dhl-vs-fedex-vs-ups-china", "DHL 寄中国对比"),
        ("/zh-cn/city/san-diego-to-hangzhou", "圣地亚哥到杭州"),
        ("/zh-cn/blog/ebay-ship-to-china", "eBay 寄中国转运"),
        ("/zh-cn/blog/usps-to-china-complete-guide", "USPS 寄中国指南"),
        ("/zh-cn/blog/usa-to-china-cheapest-way", "最便宜寄中国"),
        ("/zh-cn/blog/usa-to-china-shipping-cost", "寄中国运费"),
        ("/zh-cn/blog/amazon-us-ship-to-china", "亚马逊寄中国"),
        ("/zh-cn/city/houston-to-xian", "寄中国西安"),
        ("/zh-cn/city/detroit-to-dalian", "寄中国大连"),
        ("/zh-cn/city/atlanta-to-changsha", "亚特兰大易碎品"),
    ],
}


def exists(url):
    p = ROOT / url.lstrip("/")
    return p.with_suffix(".html").exists() or (p / "index.html").exists()


def part(lang):
    routes = ROOT / lang / "routes" / "index.html"
    if not routes.exists():
        print("SKIP", routes, "不存在")
        return
    t = routes.read_text(encoding="utf-8")
    t = re.sub(r"\n*<section data-midword-boost>.*?</section>", "", t, flags=re.S)
    items, n = "", 0
    for url, label in MID[lang]:
        if exists(url):
            items += f'<a href="{url}" style="display:inline-block;margin:5px 6px;padding:7px 15px;background:#fff;border:1px solid var(--border);border-radius:20px;font-size:13px;color:var(--text);text-decoration:none;font-weight:500">{label}</a>\n'
            n += 1
        else:
            print(f"  跳过缺失 {url}")
    block = f'<section data-midword-boost>\n<h3 style="margin:18px 0 10px;font-size:16px">中词攻坚 Mid-word boost</h3>\n{items}</section>'
    t = t.replace("</footer>", block + "\n</footer>")
    routes.write_text(t, encoding="utf-8")
    print(f"✅ {lang}/routes 注入 {n} 中词反链")


part("en")
part("zh-cn")
