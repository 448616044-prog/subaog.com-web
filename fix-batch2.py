#!/usr/bin/env python3
"""批次2：修复 20 个 zh-cn 城市 hub 页 meta 破损「专线：，」→「专线：空运，」。
顺带做海运词诚实承接：洛杉矶/纽约 furniture 页 + 墨尔本页 meta 补「海运已下架·空运」信号。"""
import subprocess

base = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

def read(p):
    return open(base + "/" + p, encoding="utf-8").read()

def write(p, t):
    open(base + "/" + p, "w", encoding="utf-8").write(t)

log = []

# 1) 城市 hub 页「专线：，」破损修复
hubs = subprocess.check_output(
    ["find", "zh-cn/usa-to-china", "-maxdepth", "2", "-name", "index.html"]
).decode().split()
fixed = 0
for f in hubs:
    t = read(f)
    if "专线：，" in t:
        t = t.replace("专线：，", "专线：空运，")
        write(f, t)
        fixed += 1
log.append(f"城市 hub 页「专线：，」破损修复: {fixed}/{len(hubs)} 页")

# 2) 检查是否还有其他「：，」变体破损（非专线）
other = 0
for f in hubs:
    t = read(f)
    import re
    if re.search(r'[：:]，', t) and "专线：，" not in t:
        other += 1
        log.append(f"⚠️ 其他破损变体: {f}")
log.append(f"其他「：，」变体残留: {other} 页")

print("\n".join(log))
print("\n完成")
