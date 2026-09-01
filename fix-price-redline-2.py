#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补充价格红线修复：美国场景 ¥80/kg起→¥100/kg起、日本¥70/kg起价、5kg+→20kg+、文案残缺/HTML bug"""
import sys, os, io

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"
DRY = "--dry-run" in sys.argv

# 每个条目: (相对路径, [(old, new), ...])
REPLACEMENTS = [
    # ---- A. 日本城市页 FAQ：空运约 ¥70/kg（20kg 起）→ ¥80/kg（20kg 起）（档3起价错误）----
    *[(f"zh-cn/japan-to-china/{c}/index.html",
       [("空运约 ¥70/kg（20kg 起），可免费估价。", "空运约 ¥80/kg（20kg 起），可免费估价。")])
      for c in ["tokyo","fukuoka","kobe","osaka","sapporo","kyoto","yokohama","nagoya"]],

    # ---- B. 首页 FAQ 残缺文案 + 美国场景 ¥80/kg起（档1应为 ¥100/kg起）----
    ("zh-cn/index.html", [
        ("中件（2-20lb）走空运专线约¥80/kg 起；大件（50lb+）走。不急用的建议走，急用走空运。",
         "中件（2-20lb）走空运专线约¥100/kg 起；大件（20kg+ 行李）走集运专线最划算。不急用建议走集运，急用走国际快递空运。"),
    ]),
    ("en/index.html", [
        ("For shipments over 50kg, consolidated air freight For small parcels under 2lb, USPS First-Class International starts around $10-30. For mid-size shipments (5-50kg), our consolidated air freight typically runs ¥80/kg 起.",
         "Consolidated air freight is the best value for shipments over 20kg. For small parcels under 2lb, USPS First-Class International starts around $10-30. For mid-size shipments (20kg+), our consolidated air freight typically runs ¥100/kg."),
    ]),

    # ---- C. 美国场景报告页/博客 ¥80/kg起 → ¥100/kg起 ----
    ("zh-cn/report/usa-china-shipping-cost-report-2026.html", [
        ("华人集运/专线单价 ¥80/kg 起", "华人集运/专线单价 ¥100/kg 起"),
    ]),
    ("en/report/usa-china-shipping-cost-report-2026.html", [
        ("consolidated lines charge ¥80/kg 起", "consolidated lines charge ¥100/kg 起"),
    ]),
    ("zh-cn/blog/can-i-ship-cosmetics-to-china.html", [
        ("华人快递敏感货专线：¥80/kg 起", "华人快递敏感货专线：¥100/kg 起"),
    ]),
    ("zh-cn/blog/can-i-ship-supplements-to-china.html", [
        ("¥80/kg 起，10-15 个工作日到门", "¥100/kg 起，10-15 个工作日到门"),
    ]),
    ("zh-cn/blog/usps-vs-fedex-vs-chinese-courier.html", [
        ("¥80/kg 起（5kg+）", "¥100/kg 起（20kg+）"),
        ("价格¥80/kg 起，10-15 个工作日到门", "价格¥100/kg 起，10-15 个工作日到门"),
    ]),
    ("en/blog/usps-vs-fedex-vs-chinese-courier.html", [
        ("from $5 (5kg+)", "from ¥100/kg (20kg+)"),
    ]),
    ("zh-cn/tools/shipping-calculator.html", [
        ("空运专线：¥100/kg 起，10-15 个工作日<br>，<br>国际快递(FedEx/UPS/DHL)：$10-25/lb，3-5天<br>华人快递集运：¥80/kg 起，10-15 个工作日",
         "空运专线：¥100/kg 起，10-15 个工作日<br>国际快递(FedEx/UPS/DHL)：$10-25/lb，3-5天<br>华人快递集运：¥100/kg 起，10-15 个工作日"),
        ("<p>① 凑重寄：10lb以上的包裹单价更低 ② 不急走。</p>",
         "<p>① 凑重寄：20kg 以上单价更低，凑够 20kg 再寄最划算；② 不急用走集运，急用走国际快递空运。</p>"),
    ]),

    # ---- D. 5kg+ → 20kg+（速豹自营语境，违反20kg起运红线）----
    ("en/blog/usps-to-china-complete-guide.html", [
        ("Chinese lines ¥100/kg from 5kg+ tax-inclusive", "Chinese lines ¥100/kg from 20kg+ tax-inclusive"),
    ]),
    ("zh-cn/blog/usps-to-china-complete-guide.html", [
        ("华人渠道 5kg+ ¥100/kg 双清包税", "华人渠道 20kg+ ¥100/kg 双清包税"),
    ]),
    ("en/blog/usa-to-china-shipping-cost.html", [
        ("Chinese line: ¥100/kg from 5kg+", "Chinese line: ¥100/kg from 20kg+"),
    ]),
    ("zh-cn/blog/usa-to-china-shipping-cost.html", [
        ("华人专线：¥100/kg 起（5kg+ 就划算）", "华人专线：¥100/kg 起（20kg+ 就划算）"),
    ]),
    ("zh-cn/blog/daigou-shipping-from-usa.html", [
        ("② 华人集运：¥100/kg，5kg+ 划算，适合日常代购。③ 敏感货专线：保健品/化妆品专用，清关成功率高。④ ，适合大件/批量囤货。",
         "② 华人集运：¥100/kg，20kg+ 划算，适合日常代购。③ 敏感货专线：保健品/化妆品专用，清关成功率高。④ 空运专线，适合大件/批量囤货。"),
    ]),
    ("en/blog/daigou-shipping-from-usa.html", [
        # 5kg+ → 20kg+，10-20kg → 100kg+（档1降档点）
        ("Consolidated shipping shines at 5kg+; bundling to 10–20kg lowers the per-kg rate.",
         "Consolidated shipping shines at 20kg+; bundling to 100kg+ lowers the per-kg rate."),
        ("2) Chinese consolidated shipping: ¥100/kg, great at 5kg+, for daily daigou.",
         "2) Chinese consolidated shipping: ¥100/kg, great at 20kg+, for daily daigou."),
        ("4) , for large/wholesale, . Most sellers combine",
         "4) Air consolidated line, for large/wholesale shipments. Most sellers combine"),
        # subtitle 段落未闭合 + 缺 section 结构 + h2 CSS 残留
        ("dedicated lines.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px\">4 ways daigou sellers ship from the USA</h2>",
         "dedicated lines.</p></div></section><section class=\"section\"><div class=\"container\" style=\"max-width:820px\"><div style=\"margin:28px 0\"><h2 style=\"font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px\">4 ways daigou sellers ship from the USA</h2>"),
    ]),
]

def run(dry):
    total_files = 0
    total_repl = 0
    for rel, pairs in REPLACEMENTS:
        path = os.path.join(BASE, rel)
        if not os.path.exists(path):
            print(f"  ⚠️ 文件不存在：{rel}")
            continue
        with io.open(path, encoding="utf-8") as f:
            content = f.read()
        orig = content
        n_file = 0
        for old, new in pairs:
            cnt = content.count(old)
            if cnt == 0:
                print(f"  ⚠️ 未匹配 [{rel}]：{old[:50]}…")
                continue
            content = content.replace(old, new)
            n_file += cnt
        if content == orig:
            continue
        total_files += 1
        total_repl += n_file
        if dry:
            print(f"  [dry] {rel} ×{n_file} 处")
        else:
            with io.open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ {rel} ×{n_file} 处")
    print(f"\n{'DRY-RUN' if dry else '完成'}：{total_files} 个文件，{total_repl} 处替换")

if __name__ == "__main__":
    run(DRY)
