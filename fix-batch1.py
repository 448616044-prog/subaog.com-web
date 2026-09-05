#!/usr/bin/env python3
"""批次执行：
1) 修复 20 个 zh-cn furniture 页 meta 破损「可寄（，税率」→「可寄（空运专线，税率」
2) 临门一脚词 title/meta 优化（amazon/dhl/wine/kitchenware 英文页，覆盖词变体）
"""
import subprocess

base = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

def read(p):
    return open(base + "/" + p, encoding="utf-8").read()

def write(p, t):
    open(base + "/" + p, "w", encoding="utf-8").write(t)

log = []

# ---- 1) furniture meta 破损修复 ----
furn = subprocess.check_output(
    ["find", "zh-cn/usa-to-china", "-path", "*/furniture/index.html"]
).decode().split()
fixed = 0
for f in furn:
    t = read(f)
    if "可寄（，税率" in t:
        t = t.replace("可寄（，税率", "可寄（空运专线，税率")
        write(f, t)
        fixed += 1
log.append(f"furniture meta 破损修复: {fixed}/{len(furn)} 页")

# ---- 2) 临门一脚 title/meta ----
edits = [
    ("en/blog/amazon-shopping-to-china.html", [
        ("How to Shop on Amazon and Ship to China 2026 | Subao Global",
         "Does Amazon Ship to China? Yes — How to Shop & Forward 2026 | Subao Global"),
    ]),
    ("en/blog/dhl-vs-fedex-vs-ups-china.html", [
        ("DHL vs FedEx vs UPS to China: Cost & Speed Compared (2026) | Subao Global",
         "DHL to China: Cost & Speed vs FedEx & UPS (2026) | Subao Global"),
        ("DHL vs FedEx vs UPS to China: Cost & Speed Compared | Subao Global",
         "DHL to China: Cost & Speed vs FedEx & UPS (2026) | Subao Global"),
    ]),
    ("en/blog/can-i-ship-wine-to-china.html", [
        ("Can I Ship Wine to China? Rules & Duty (2026) | Subao Global",
         "Can I Send or Ship Wine to China? Rules & Duty (2026) | Subao Global"),
    ]),
    ("en/usa-to-china/atlanta/kitchenware/index.html", [
        ("Ship Kitchenware from Atlanta to China",
         "Ship China, Glass & Kitchenware from Atlanta to China"),
    ]),
]

for path, pairs in edits:
    t = read(path)
    for old, new in pairs:
        cnt = t.count(old)
        if cnt == 0:
            log.append(f"⚠️ 未命中: {path} 「{old[:40]}…」")
        else:
            t = t.replace(old, new)
            log.append(f"✅ {path}: 替换 {cnt} 处 「{old[:35]}…」")
    write(path, t)

print("\n".join(log))
print("\n完成")
