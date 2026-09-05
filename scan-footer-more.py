"""扫描全站 footer More 栏覆盖 + 工具页是否被链"""
import os, re, subprocess
from collections import Counter

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# 收集所有 HTML 页
files = subprocess.run(["find", BASE, "-name", "*.html", "-not", "-path", "*/\\.*"],
                        capture_output=True, text=True, timeout=60).stdout.strip().split("\n")
files = [f for f in files if f]

# 工具页清单
TOOLS_EN = [
    "/en/tools/can-i-ship",
    "/en/tools/volume-calculator",
    "/en/tools/transit-time",
    "/en/tools/package-consolidation-calculator",
    "/en/tools/shipping-calculator",
    "/en/tools/customs-duty-calculator",
]
TOOLS_ZH = [
    "/zh-cn/tools/can-i-ship",
    "/zh-cn/tools/volume-calculator",
    "/zh-cn/tools/transit-time",
    "/zh-cn/tools/package-consolidation-calculator",
    "/zh-cn/tools/shipping-calculator",
    "/zh-cn/tools/customs-duty-calculator",
]

# 每个工具页被多少页面引用
tool_inbound = {t: 0 for t in TOOLS_EN + TOOLS_ZH}

# 统计每个页面 footer 的 More 栏
has_more = 0
no_more = 0
no_more_files = []
lang_buckets = Counter()

for f in files:
    rel = os.path.relpath(f, BASE)
    with open(f, encoding="utf-8") as fp:
        t = fp.read()
    # 检测 More 栏（en: "More" h4 / zh: "更多" h4）
    if re.search(r'<h4>More</h4>|<h4>更多</h4>', t):
        has_more += 1
    else:
        no_more += 1
        no_more_files.append(rel)
        lang_buckets[rel.split("/")[0] if "/" in rel else "(root)"] += 1
    # 工具页被链次数
    for tool in TOOLS_EN + TOOLS_ZH:
        if tool in t:
            tool_inbound[tool] += 1

print(f"全站页面: {len(files)}")
print(f"有 More 栏: {has_more}")
print(f"无 More 栏: {no_more}")
print(f"无 More 分布: {dict(lang_buckets)}")
print(f"\n=== 各工具页被多少页面引用 ===")
for t, n in tool_inbound.items():
    print(f"  {t}: {n} 次")

print(f"\n=== 前 20 个无 More 栏页面 ===")
for f in no_more_files[:20]:
    print(f"  {f}")