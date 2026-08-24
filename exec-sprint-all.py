#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""subaog.com SEO Sprint 全量执行 (2026-08-24)
1) 全站 footer 增补「更多资源」列 -> 链 routes/ + can-i-ship-index/ + 3 弱链工具 (解孤儿聚合页 + 赋权工具)
2) 明星页注入「相关线路」内链簇 (强化起点城市/线路聚类)
3) 聚合页反向链明星页 (双向权威)
幂等：已含标记则跳过。
"""
import re
from pathlib import Path

BASE = Path(".")
FOOTER_MARK = '<div class="footer-bottom">'

# ---------------- 语言判定 ----------------
def detect_lang(t, path):
    m = re.search(r'<html[^>]*lang="([^"]+)"', t, re.I)
    if m and m.group(1).lower().startswith("en"):
        return "en"
    if str(path).startswith("en/"):
        return "en"
    return "zh-cn"

# ---------------- Part1: 全站 footer 增补 ----------------
def footer_col(lang):
    if lang == "zh-cn":
        links = [
            ("/zh-cn/routes/", "全部线路"),
            ("/zh-cn/can-i-ship-index/", "能不能寄·分类"),
            ("/zh-cn/tools/customs-duty-calculator.html", "关税估算"),
            ("/zh-cn/tools/volume-calculator.html", "材积计算"),
            ("/zh-cn/tools/transit-time.html", "时效查询"),
        ]
        title = "更多资源"
    else:
        links = [
            ("/en/routes/", "All Routes"),
            ("/en/can-i-ship-index/", "Can I Ship·Index"),
            ("/en/tools/customs-duty-calculator.html", "Customs Duty"),
            ("/en/tools/volume-calculator.html", "Volume Calc"),
            ("/en/tools/transit-time.html", "Transit Time"),
        ]
        title = "More"
    a = "".join(f'<a href="{u}">{t}</a>' for u, t in links)
    return f'<div><h4>{title}</h4>{a}</div>'

def part1():
    done = skip = fail = 0
    for p in BASE.rglob("*.html"):
        if "node_modules" in p.parts:
            continue
        try:
            t = p.read_text(encoding="utf-8")
        except Exception:
            fail += 1
            continue
        lang = detect_lang(t, str(p))
        if f"/{lang}/routes/" in t:        # 已注入则跳过（幂等）
            skip += 1
            continue
        col = footer_col(lang)
        if FOOTER_MARK in t:
            t = t.replace(FOOTER_MARK, col + "\n    " + FOOTER_MARK, 1)
        elif "</footer>" in t:
            t = t.replace("</footer>", col + "\n  </footer>", 1)
        elif "</body>" in t:
            t = t.replace("</body>", col + "\n</body>", 1)
        else:
            fail += 1          # 无 body 的非内容页，跳过
            continue
        p.write_text(t, encoding="utf-8")
        done += 1
    print(f"[Part1] footer 增补: 新增 {done} | 已存在 {skip} | 失败 {fail}")
    return done

# ---------------- Part2: 明星页相关线路内链簇 ----------------
STARS = [
    "zh-cn/city/denver-to-beijing.html",
    "zh-cn/city/miami-to-shanghai.html",
    "en/city/miami-to-shanghai.html",
    "en/city/boston-to-shanghai.html",
    "en/city/miami-to-chengdu.html",
    "en/city/seattle-to-hangzhou.html",
    "en/city/seattle-to-xiamen.html",
    "en/europe-to-china/berlin/index.html",
    "zh-cn/europe-to-china/berlin/index.html",
    "en/korea-to-china/gwangju/index.html",
    "zh-cn/korea-to-china/gwangju/index.html",
    "en/seasia-to-china/singapore/index.html",
    "zh-cn/seasia-to-china/singapore/index.html",
    "en/canada-to-china/toronto/index.html",
    "zh-cn/canada-to-china/toronto/index.html",
    "en/blog/usps-to-china-complete-guide.html",
    "en/blog/amazon-shopping-to-china.html",
    "en/blog/dhl-vs-fedex-vs-ups-china.html",
    "en/blog/us-shopping-forwarding-guide.html",
]

def url_of(sib: Path, self: Path):
    if sib.name == "index.html":
        return "/" + sib.parent.as_posix() + "/"
    return "/" + sib.as_posix()

def humanize(stem):
    s = stem.replace("-to-", " → ").replace("-", " ").strip()
    return s[:60]

def star_clean(s):
    """STARS 原始路径 -> (clean_url, 显示标签)，符合 canonical clean-URL 规范"""
    parts = s.split("/")
    if parts[-1] == "index.html":
        dir_stem = parts[-2]
        url = "/" + "/".join(parts[:-1]) + "/"
        label = humanize(dir_stem)
    else:
        stem = parts[-1].replace(".html", "")
        url = "/" + "/".join(parts[:-1]) + "/" + stem
        label = humanize(stem)
    return url, label

def related_block(path: Path, lang):
    parent = path.parent
    links = []
    # 兄弟页（同目录）最多 4
    for sib in sorted(parent.glob("*.html")):
        if sib == path:
            continue
        links.append((url_of(sib, path), humanize(sib.stem)))
        if len(links) >= 4:
            break
    # 聚合枢纽
    hub = ("/zh-cn/routes/" if lang == "zh-cn" else "/en/routes/")
    idx = ("/zh-cn/can-i-ship-index/" if lang == "zh-cn" else "/en/can-i-ship-index/")
    title = "相关线路" if lang == "zh-cn" else "Related routes"
    alllinks = [(hub, "全部线路" if lang == "zh-cn" else "All routes"),
                (idx, "能不能寄·分类" if lang == "zh-cn" else "Can I Ship")]
    alllinks += links
    a = "".join(
        f'<a href="{u}" style="display:inline-block;margin:5px 6px;padding:7px 15px;background:#fff;border:1px solid var(--border);border-radius:20px;font-size:13px;color:var(--text);text-decoration:none;font-weight:500">{t} →</a>'
        for u, t in alllinks)
    return f'''  <section class="section" style="background:#F5F7FA">
    <div class="container">
      <div class="section-title"><h2>{title}</h2></div>
      <div style="text-align:center;line-height:2.4">{a}</div>
    </div>
  </section>'''

def part2():
    done = skip = fail = 0
    for sp in STARS:
        p = BASE / sp
        if not p.exists():
            print("  缺失:", sp)
            fail += 1
            continue
        t = p.read_text(encoding="utf-8")
        if "相关线路" in t or "Related routes" in t:
            skip += 1
            continue
        lang = detect_lang(t, sp)
        block = related_block(p, lang)
        fi = t.rfind("</footer>")
        if fi < 0:
            fail += 1
            continue
        t = t[:fi] + block + "\n" + t[fi:]
        p.write_text(t, encoding="utf-8")
        done += 1
        print("  ✅", sp)
    print(f"[Part2] 明星页相关线路: 新增 {done} | 已存在 {skip} | 失败 {fail}")

# ---------------- Part3: 聚合页反向链明星页 ----------------
def part3():
    done = skip = fail = 0
    for lang in ["zh-cn", "en"]:
        for agg in ["routes", "can-i-ship-index"]:
            p = BASE / lang / agg / "index.html"
            if not p.exists():
                continue
            t = p.read_text(encoding="utf-8")
            # 移除旧 block 后重生成（幂等+可重跑）
            if "data-sprint-star" in t:
                t = re.sub(r'\n*  <section class="section" style="background:#fff" data-sprint-star>.*?</section>', "", t, flags=re.S)
            star_pairs = [star_clean(s) for s in STARS if s.startswith(lang + "/")]
            if not star_pairs:
                continue
            items = "".join(
                f'<a href="{u}" style="display:inline-block;margin:5px 6px;padding:7px 15px;background:#fff;border:1px solid var(--border);border-radius:20px;font-size:13px;color:var(--text);text-decoration:none;font-weight:500">{label} →</a>'
                for u, label in star_pairs)
            title = "热门线路" if lang == "zh-cn" else "Popular routes"
            block = f'''  <section class="section" style="background:#fff" data-sprint-star>
    <div class="container">
      <div class="section-title"><h2>{title}</h2></div>
      <div style="text-align:center;line-height:2.4">{items}</div>
    </div>
  </section>'''
            fi = t.rfind("</footer>")
            if fi < 0:
                fail += 1
                continue
            t = t[:fi] + block + "\n" + t[fi:]
            p.write_text(t, encoding="utf-8")
            done += 1
            print(f"  ✅ {lang}/{agg} 反向链 {len(star_pairs)} 明星页")
    print(f"[Part3] 聚合页反向链: 新增 {done} | 已存在 {skip} | 失败 {fail}")

if __name__ == "__main__":
    print("=== subaog.com Sprint 全量执行 ===")
    part1()
    part2()
    part3()
    print("=== 完成 ===")
