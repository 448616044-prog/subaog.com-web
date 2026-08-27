#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
subaog.com — 替换旧"美国寄中国 运费价格表"(1-20/21-99/100kg 三行) 为
新"包税渠道价格表"(3 档国家 + 起重 20kg + 双清包税 + 清关费 100 元申报手续费 + 完整服务说明)
按页面路径自动判断档位高亮
"""
import re
from pathlib import Path

ROOT = Path(".")

# 路径前缀 -> 档位
PATH_TIER = {
    "usa-to-china": 1,
    "canada-to-china": 1,
    "australia-to-china": 1,
    "europe-to-china": 2,
    "japan-to-china": 3,
    "korea-to-china": 3,
    "seasia-to-china": 3,
}

# 旧表匹配: 含"重量段"或"1 - 20 kg"的 <table>...</table>
OLD_TABLE = re.compile(
    r'<table[^>]*>(?:(?!</table>).)*?(?:重量段|1 - 20 kg|1-20 kg)(?:(?!</table>).)*?</table>',
    re.S,
)

ROWS = [
    (1, "美国 / 加拿大 / 墨西哥 / 澳大利亚 / 新西兰", "¥80 /kg", "¥75 /kg"),
    (2, "英国 / 德国 / 法国 / 意大利 / 西班牙 / 爱尔兰 + 欧洲国家", "¥75 /kg", "¥70 /kg"),
    (3, "日本 / 韩国 / 泰国 / 新加坡 / 菲律宾 / 中国台湾 / 马来西亚", "¥70 /kg", "¥65 /kg"),
]


def detect_tier(path: str) -> int:
    for prefix, tier in PATH_TIER.items():
        if f"/{prefix}/" in path:
            return tier
    return 1  # 兜底


def build_block(tier: int) -> str:
    body = ""
    for t, name, p1, p2 in ROWS:
        hl = ' style="background:#FFF8E1;font-weight:700"' if t == tier else ""
        body += f'<tr{hl}><td style="padding:10px;border-bottom:1px solid #E2E8F0">{name}</td>'
        body += f'<td style="padding:10px;border-bottom:1px solid #E2E8F0;text-align:center">{p1}</td>'
        body += f'<td style="padding:10px;border-bottom:1px solid #E2E8F0;text-align:center">{p2}</td>'
        body += '<td style="padding:10px;border-bottom:1px solid #E2E8F0;text-align:center">清单+100元申报手续费</td></tr>'
    return f'''<div class="price-block" style="margin:24px 0;padding:20px;background:#fff;border-radius:12px;border:1px solid #E2E8F0">
  <h3 style="text-align:center;font-size:20px;font-weight:700;margin-bottom:8px;color:var(--primary-dark)">包税渠道价格表（双清包税 · 门到门 · 时效 10-15 工作日）</h3>
  <p style="text-align:center;color:#92400e;background:#FEF3C7;padding:8px 12px;border-radius:8px;margin-bottom:14px;font-weight:600">⚠️ 本价格表只接行李物品 2026-6-30 · 起重 20kg，不足 20kg 按 20kg 算</p>
  <table style="width:100%;border-collapse:collapse;font-size:14px">
    <thead><tr style="background:var(--primary);color:#fff">
      <th style="padding:10px;text-align:left">出发国家/地区</th>
      <th style="padding:10px;text-align:center">20-99 kg</th>
      <th style="padding:10px;text-align:center">100 kg+</th>
      <th style="padding:10px;text-align:center">资料</th>
    </tr></thead>
    <tbody>{body}</tbody>
  </table>
  <div style="margin-top:16px;font-size:13px;color:#475569;line-height:1.7">
    <p style="margin:6px 0"><strong style="color:var(--primary-dark)">服务包含：</strong>双清包税 / 门到门 / 时效 10-15 工作日，含清关 + 100元申报手续费。</p>
    <p style="margin:6px 0"><strong style="color:var(--primary-dark)">计算：</strong>整票 1KG 取整进位；材积重 = 长×宽×高 cm ÷ 5000，实际重与体积重取大数。</p>
    <p style="margin:6px 0"><strong style="color:var(--primary-dark)">超规附加：</strong>单件 &gt; 25KG 或单边 &gt; 120CM 或周长 &gt; 266CM 有附加费。</p>
    <p style="margin:6px 0"><strong style="color:var(--primary-dark)">轨迹：</strong><a href="https://m.qianxunimport.com/index/track/" target="_blank" rel="noopener" style="color:var(--primary);font-weight:600">m.qianxunimport.com</a></p>
    <p style="margin:6px 0"><strong style="color:var(--primary-dark)">严禁：</strong>武器/毒品/易燃物；动植物/食品/烟酒/化妆品/电子元件/未授权新品等（详情咨询客服）。</p>
    <p style="margin:6px 0"><strong style="color:var(--primary-dark)">赔偿：</strong>自行包装；内件损坏或液体污染不赔；单箱丢货最高 100 美金；走货默认赔付标准。</p>
  </div>
</div>'''


def main():
    targets = []
    for prefix in PATH_TIER:
        for p in (ROOT / "zh-cn" / prefix).rglob("*.html"):
            targets.append(p)

    fixed = skip = 0
    for f in targets:
        t = f.read_text(encoding="utf-8", errors="ignore")
        if "重量段" not in t and "1 - 20 kg" not in t and "1-20 kg" not in t:
            skip += 1
            continue
        tier = detect_tier(str(f))
        new = OLD_TABLE.sub(build_block(tier), t, count=1)
        if new != t:
            f.write_text(new, encoding="utf-8")
            fixed += 1
            print(f"  ✅ {f.relative_to(ROOT)}  档{tier}")
    print(f"\n修复 {fixed} | 跳过(无旧表) {skip}")


if __name__ == "__main__":
    main()
