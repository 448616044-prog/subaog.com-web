#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
subaog.com — about 页修复:
1. 总部: 台湾 → 深圳 + "在全球均有物流站点" (zh-cn)
2. 起源: 去 "Taiwan ↔ mainland China" → "深圳总部+全球节点" (en)
3. 布局: zh-cn eat-section(12年经验+数据卡片+承诺+联系) 从 </footer> 后移到 footer 前
"""
import re
from pathlib import Path

ROOT = Path(".")


def fix_zh():
    p = ROOT / "zh-cn" / "about.html"
    t = p.read_text(encoding="utf-8", errors="ignore")
    changes = []

    # 1) 总部文案: 台湾 → 深圳 + 全球节点
    old1 = "总部位于台湾，覆盖美国、日本、欧洲、澳洲、东南亚等主要华人聚集国家"
    new1 = "总部位于深圳，在全球均有物流站点。覆盖美国、日本、欧洲、澳洲、东南亚等主要华人聚集国家"
    if old1 in t:
        t = t.replace(old1, new1, 1)
        changes.append("总部:台湾→深圳+全球")

    # 2) 移动 eat-section: 从 </footer> 后 → footer 前
    sec_match = re.search(r'(<section class="eat-section">.*?</section>)', t, re.S)
    if sec_match:
        sec = sec_match.group(1)
        if t.count(sec) >= 1:
            t = t.replace(sec, "", 1)
            # 插到 <footer class="footer"> 之前
            new_pos = sec + '\n\n  <footer class="footer">'
            old_pos = '<footer class="footer">'
            if old_pos in t:
                t = t.replace(old_pos, new_pos, 1)
                changes.append("布局:eat-section 移到 footer 前")

    p.write_text(t, encoding="utf-8")
    print(f"✅ zh-cn/about.html: {', '.join(changes) if changes else '无改动'}")


def fix_en():
    p = ROOT / "en" / "about.html"
    t = p.read_text(encoding="utf-8", errors="ignore")
    changes = []

    # 1) 起源: Taiwan ↔ mainland China → 深圳总部+全球
    old1 = "has been moving shipments across borders for over 12 years. We started with one corridor — Taiwan ↔ mainland China — and built the operational expertise that lets us now serve seven origin regions: the USA, Japan, Korea, Europe, Australia, Canada, and Southeast Asia."
    new1 = "has been moving shipments across borders for over 12 years. Headquartered in Shenzhen with logistics nodes across origin regions worldwide, we now serve seven regions: the USA, Japan, Korea, Europe, Australia, Canada, and Southeast Asia."
    if old1 in t:
        t = t.replace(old1, new1, 1)
        changes.append("起源:台湾→深圳总部+全球")
    else:
        # 兜底: 单独替换
        if "Taiwan ↔ mainland China" in t:
            t = t.replace(
                "Taiwan ↔ mainland China",
                "the original cross-border corridor",
                1,
            )
            changes.append("兜底去 Taiwan")

    p.write_text(t, encoding="utf-8")
    print(f"✅ en/about.html: {', '.join(changes) if changes else '无改动'}")


if __name__ == "__main__":
    fix_zh()
    fix_en()
