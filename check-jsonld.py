"""JSON-LD 校验 - 抽样所有改动的关键文件 + 批量随机"""
import subprocess, json, re, sys, random

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# 1) 必检文件（重要的页面）
must_check = [
    "en/usa-to-china/index.html",
    "zh-cn/usa-to-china/index.html",
    "en/index.html",
    "zh-cn/index.html",
    "en/tools/transit-time.html",
    "zh-cn/tools/transit-time.html",
    "en/tools/customs-duty-calculator.html",
    "en/tools/shipping-calculator.html",
    "en/tools/can-i-ship.html",
    "en/tools/package-consolidation-calculator.html",
    "en/tools/volume-calculator.html",
    "zh-cn/tools/can-i-ship.html",
    "zh-cn/tools/shipping-calculator.html",
    "zh-cn/tools/package-consolidation-calculator.html",
    "zh-cn/usa-to-china/atlanta/auto-parts/index.html",
    "zh-cn/usa-to-china/atlanta/bicycles/index.html",
    "zh-cn/usa-to-china/los-angeles/furniture/index.html",
    "zh-cn/usa-to-china/new-york/wine/index.html",
    "zh-cn/usa-to-china/seattle/tea/index.html",
    "zh-cn/usa-to-china/boston/index.html",
    "zh-cn/usa-to-china/detroit/index.html",
    "zh-cn/seasia-to-china/malaysia/index.html",
    "zh-cn/seasia-to-china/pricing/index.html",
]

bad = []
total_blocks = 0
for rel in must_check:
    p = f"{BASE}/{rel}"
    try:
        t = open(p, encoding="utf-8").read()
    except Exception as e:
        bad.append((rel, str(e)))
        continue
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        raw = m.group(1).strip()
        if not raw:
            continue
        total_blocks += 1
        try:
            json.loads(raw)
        except Exception as e:
            bad.append((rel, str(e)[:80]))

print(f"关键文件检查: {len(must_check)} 文件, {total_blocks} JSON-LD 块")
if bad:
    print(f"错误数: {len(bad)}")
    for r, e in bad[:10]:
        print(f"  {r}: {e}")
else:
    print("✓ 全部通过")

# 2) 全站改动文件随机抽 200 个检查
print("\n=== 全站改动文件随机抽样 ===")
result = subprocess.run(["git", "diff", "--name-only"], cwd=BASE, capture_output=True, text=True)
changed = [f for f in result.stdout.split("\n") if f.endswith(".html")]
print(f"改动 HTML 文件: {len(changed)}")
sample = random.sample(changed, min(200, len(changed)))

bad2 = []
total_blocks2 = 0
for rel in sample:
    p = f"{BASE}/{rel}"
    try:
        t = open(p, encoding="utf-8").read()
    except Exception:
        continue
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        raw = m.group(1).strip()
        if not raw:
            continue
        total_blocks2 += 1
        try:
            json.loads(raw)
        except Exception as e:
            bad2.append((rel, str(e)[:80]))

print(f"抽样 {len(sample)} 文件, {total_blocks2} JSON-LD 块")
if bad2:
    print(f"错误数: {len(bad2)}")
    for r, e in bad2[:10]:
        print(f"  {r}: {e}")
else:
    print("✓ 全部通过")