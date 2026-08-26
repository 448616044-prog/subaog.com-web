#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
subaog.com — 批量去 AI 味 / 修复中文站 meta 堆砌 + A/B 组 CTR 优化清单
依赖: gsc-latest.json (GSC 需求数据)
用法: python3 optimize-zh-meta-detone.py

设计原则（安全优先，不伤 SEO）:
- 只清理「重复的营销套话」和「结尾垃圾串」，保留页面真实首句信息，不臆测价格
- 幂等: 已清理的页再次运行不重复改动
- 仅改 <meta name="description"> 与 <meta property="og:description"> 的 content
"""
import re
import json
from pathlib import Path

ROOT = Path(".")
GSC = ROOT / "gsc-latest.json"

# ---------- 中文站 meta 去堆砌 ----------
# 检测并清理以下堆砌/垃圾模式（出现多次即视为模板瑕疵）
JUNK = [
    r"\s*\|\s*12年国际物流经验[^|＜]*双清包税门到门[^|＜]*",
    r"\s*\|\s*12年国际物流经验[^|＜]*",
    r"\s*双清包税门到门\.?\s*\|?\s*…?",
    r"速豹国际物流 subaog\.com\s*\|?…?",
    r"\s*\|\s*速豹(国际|回国)物流\s*[:：]?",
    r"速豹(国际|回国)物流\s*[:：]?\s*$",
    r"\s*\|\s*…",
    r"…\s*$",
    r"，{2,}",
    r"\s*\|\s*\|+",
    r"\s*\|\s*$",
    r"[:：]\s*$",
    r"12年经验[^|＜]*$",
    r"，\。",
]


def clean_content(content: str) -> str:
    """清理单个 description content 字符串。"""
    c = content
    for p in JUNK:
        c = re.sub(p, "", c, flags=re.S)
    # 合并多余空格/竖线
    c = re.sub(r"\s*\|\s*\|+", " | ", c)
    c = re.sub(r"\s{2,}", " ", c)
    c = c.strip().strip("|").strip()
    # 若仍以营销句重复收尾，截断到第一个句号后合理长度（中文 meta ≤ ~90 字）
    if "12年国际物流经验" in c:
        # 极端兜底：截断到首次出现的营销串之前
        c = re.split(r"12年国际物流经验", c)[0].strip().rstrip("|").strip()
    if len(c) > 110:
        # 在句号处安全截断
        cut = c[:110]
        last = cut.rfind("。")
        if last > 40:
            cut = cut[: last + 1]
        c = cut
    return c


def part_zh_meta():
    print("=== Part A: 中文站 meta/og description 去堆砌 ===")
    fixed = 0
    checked = 0
    for f in sorted(ROOT.rglob("zh-cn/**/*.html")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        new_t = t
        for tag in ['name="description"', 'property="og:description"']:
            pat = re.compile(
                r'(<meta[^>]*?{tag}[^>]*?content=")([^"]*)(")'.format(tag=tag),
                re.S,
            )

            def repl(m, _f=f):
                before, content, after = m.group(1), m.group(2), m.group(3)
                cleaned = clean_content(content)
                if cleaned and cleaned != content:
                    return before + cleaned + after
                return m.group(0)

            new_t = pat.sub(repl, new_t)
        checked += 1
        if new_t != t:
            f.write_text(new_t, encoding="utf-8")
            fixed += 1
            # 输出样例
            m = re.search(r'name="description" content="([^"]*)"', new_t)
            print(f"  ✅ {f.relative_to(ROOT)} -> {m.group(1)[:70] if m else ''}")
    print(f"  检查 {checked} 页 | 修复 {fixed} 页")


# ---------- A/B 组 CTR 优化清单 ----------
def slugify(q: str) -> str:
    q = q.lower()
    # 常见词 -> 站点 slug 片段（粗映射，供人工/二次脚本定位）
    repl = {
        "ship from ": "", "ship to china": "to-china", "to china": "to-china",
        "shipping to china": "to-china", "china": "china",
    }
    return q.replace(" ", "-").replace("'", "")


def part_ctr_plan():
    print("\n=== Part B: A/B 组 CTR 优化清单 (基于 GSC) ===")
    if not GSC.exists():
        print("  ⚠️ 无 gsc-latest.json，跳过")
        return
    d = json.loads(GSC.read_text(encoding="utf-8"))
    qs = d["data"]["queries"]
    A, B = [], []
    for x in qs:
        qy = x["keys"][0]
        pos = x["position"]
        imp = x["impressions"]
        clk = x["clicks"]
        if 11 <= pos <= 30 and imp >= 2:
            A.append((qy, pos, imp, clk))
        if pos <= 20 and clk == 0 and imp >= 1:
            B.append((qy, pos, imp, clk))
    A.sort(key=lambda r: -r[2])
    B.sort(key=lambda r: r[1])
    print(f"\n-- A 组 中词攻坚 (11-30名, 展现≥2): {len(A)} 个 --")
    for qy, pos, imp, clk in A:
        print(f"  [{pos:5.1f}] {imp}imp {clk}clk  {qy}  -> slug: {slugify(qy)}")
    print(f"\n-- B 组 CTR 急救 (≤20名, 0点击): {len(B)} 个 --")
    for qy, pos, imp, clk in B:
        print(f"  [{pos:5.1f}] {imp}imp {clk}clk  {qy}  -> slug: {slugify(qy)}")
    # 写出清单供后续精准改写
    out = ROOT / "ctr-optimize-plan.md"
    lines = ["# subaog.com CTR 优化清单 (A/B 组)", ""]
    lines.append("## A 组 中词攻坚 (title 加卖点钩子: 价格/时效/Free Quote)")
    for qy, pos, imp, clk in A:
        lines.append(f"- `{slugify(qy)}` | pos {pos:.1f} | {imp} imp | query: {qy}")
    lines.append("")
    lines.append("## B 组 CTR 急救 (meta 重写含意图+卖点, 确认 FAQPage 富媒体)")
    for qy, pos, imp, clk in B:
        lines.append(f"- `{slugify(qy)}` | pos {pos:.1f} | {imp} imp | query: {qy}")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  ✅ 清单已写入 {out.name}")


if __name__ == "__main__":
    part_zh_meta()
    part_ctr_plan()
    print("\n完成。待 Bash 恢复后运行本脚本即可批量生效。")
