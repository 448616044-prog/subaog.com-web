#!/usr/bin/env python3
"""subaog.com GSC 需求洞察：读 gsc-latest.json，输出高 ROI 动作清单。
配合 gsc-pull-comprehensive.py 使用：先拉数据，再跑本脚本得需求地图。
用法: python3 gsc-demand-report.py
"""
import json, re
from pathlib import Path

ROOT = Path(".")
d = json.load(open(ROOT / "gsc-latest.json"))
q = d["data"]["queries"]
HIGH_INTENT = re.compile(
    r"(ship to china|ship.*china|amazon|ebay|consolidat|forward|daigou|cost|cheapest|can.*send|can.*ship|寄中国|转运|集运)",
    re.I,
)

rows = [(x["keys"][0], x["impressions"], x["clicks"], x["position"]) for x in q]
rows.sort(key=lambda r: -r[1])


def seg(p):
    return "TOP3" if p <= 3 else "TOP10" if p <= 10 else "11-30" if p <= 30 else "31-100"


print(f"=== subaog.com GSC 需求洞察 ({d['pulled_at'][:10]}) ===")
print(f"总词 {len(rows)} | 总展现 {sum(r[1] for r in rows)} | 总点击 {sum(r[2] for r in rows)}")
print(f"排名分段: TOP3={sum(1 for r in rows if r[3]<=3)} TOP10={sum(1 for r in rows if r[3]<=10)} "
      f"11-30={sum(1 for r in rows if 11<=r[3]<=30)} 31-100={sum(1 for r in rows if r[3]>30)}")

print("\n【A. 中词攻坚候选 (11-30 名, 差临门一脚, ROI 最高)】")
for t, imp, clk, pos in rows:
    if 11 <= pos <= 30:
        print(f"  {seg(pos):5} pos{pos:5.1f} {imp}imp {clk}clk  {t}")

print("\n【B. CTR 异常 (有展现但 0 点击且排名<=20, 需优化 title/meta/FAQ)】")
for t, imp, clk, pos in rows:
    if clk == 0 and pos <= 20 and imp >= 1:
        print(f"  pos{pos:5.1f} {imp}imp  {t}")

print("\n【C. 高意图需求词 TOP (转运/集运/价格/物品限制 — 业务核心)】")
for t, imp, clk, pos in rows:
    if HIGH_INTENT.search(t):
        print(f"  {seg(pos):5} pos{pos:5.1f} {imp}imp {clk}clk  {t}")

print("\n【D. 下周高 ROI 动作清单】")
print("  1) 中词攻坚: 对 A 组 15 词对应页做内链加权 + CTR 优化(title 含价格/时效卖点)")
print("  2) CTR 急救: 对 B 组页补 FAQPage 富媒体 + 优化 meta description")
print("  3) 长尾补面: 若 C 组有词无对应页, 批量生成(先查站点是否已覆盖)")
print("  4) 品牌信任: About/作者/仓库视频 YMYL 信号做实")
print("  5) 外链 DR: 第一梯队 8 个待手动提交(流量天花板根因)")
