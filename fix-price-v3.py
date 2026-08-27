#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
subaog.com — 价格统一 v3 (最新价 2026-08-27)
新价(起重20kg, 清关费100元申报手续费):
  档1 美/加/墨/澳/新: ¥100/kg, ¥90/kg
  档2 欧洲: ¥90/kg, ¥80/kg
  档3 日/韩/泰/新/菲/台/马: ¥80/kg, ¥70/kg
重新生成 62 个 zh-cn 嵌入页的 price-block(新价 + 服务包含精简无含清关 + 无轨迹行)
"""
import re
from pathlib import Path

ROOT = Path(".")

PATH_TIER = {
    "usa-to-china": 1, "canada-to-china": 1, "australia-to-china": 1,
    "europe-to-china": 2,
    "japan-to-china": 3, "korea-to-china": 3, "seasia-to-china": 3,
}

ROWS = [
    (1, "美国 / 加拿大 / 墨西哥 / 澳大利亚 / 新西兰", "¥100 /kg", "¥90 /kg"),
    (2, "英国 / 德国 / 法国 / 意大利 / 西班牙 / 爱尔兰 + 欧洲国家", "¥90 /kg", "¥80 /kg"),
    (3, "日本 / 韩国 / 泰国 / 新加坡 / 菲律宾 / 中国台湾 / 马来西亚", "¥80 /kg", "¥70 /kg"),
]

BLOCK_RE = re.compile(r'<div class="price-block".*?</div>\n</div>', re.S)


def detect_tier(path: str) -> int:
    for pfx, tier in PATH_TIER.items():
        if f"/{pfx}/" in path:
            return tier
    return 1


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
    <p style="margin:6px 0"><strong style="color:var(--primary-dark)">服务包含：</strong>双清包税 / 门到门 / 时效 10-15 工作日</p>
    <p style="margin:6px 0"><strong style="color:var(--primary-dark)">计算：</strong>整票 1KG 取整进位；材积重 = 长×宽×高 cm ÷ 5000，实际重与体积重取大数。</p>
    <p style="margin:6px 0"><strong style="color:var(--primary-dark)">超规附加：</strong>单件 &gt; 25KG 或单边 &gt; 120CM 或周长 &gt; 266CM 有附加费。</p>
    <p style="margin:6px 0"><strong style="color:var(--primary-dark)">严禁：</strong>武器/毒品/易燃物；动植物/食品/烟酒/化妆品/电子元件/未授权新品等（详情咨询客服）。</p>
    <p style="margin:6px 0"><strong style="color:var(--primary-dark)">赔偿：</strong>自行包装；内件损坏或液体污染不赔；单箱丢货最高 100 美金；走货默认赔付标准。</p>
  </div>
</div>'''


def main():
    fixed = 0
    for pfx in PATH_TIER:
        for f in (ROOT / "zh-cn" / pfx).rglob("*.html"):
            t = f.read_text(encoding="utf-8", errors="ignore")
            if "price-block" not in t:
                continue
            tier = detect_tier(str(f))
            new = BLOCK_RE.sub(build_block(tier), t, count=1)
            if new != t:
                f.write_text(new, encoding="utf-8")
                fixed += 1
    print(f"修复 {fixed} 页")


if __name__ == "__main__":
    main()
