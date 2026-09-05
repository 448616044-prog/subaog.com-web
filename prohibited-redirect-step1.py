#!/usr/bin/env python3
"""
subaog.com 禁运品类 301 重定向 + luxury-goods 改写
用户 2026-09-05 决策：
- 澳洲+欧洲 milk-powder/wine/supplements → 301 到对应城市 hub
- 欧洲 luxury-goods → 改写为「二手/个人自用」导向
- 美国 wine/milk-powder 等用户未明确，本次不动

执行步骤：
1. 物理删除禁运品类目录（git rm）
2. _redirects 加通配符 301 规则
3. sitemap.xml 移除 URL
4. 城市 hub 清理品类导航（移除 milk-powder/wine/supplements 链接）
5. luxury-goods 16 页改写
"""
import os
import re
import subprocess

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# 禁运品类（按用户决策：仅澳洲+欧洲）
PROHIBITED_ITEMS = ["milk-powder", "wine", "supplements"]
PROHIBITED_REGIONS = ["australia-to-china", "europe-to-china"]

# 城市 hub 路径中需要保留的品类（从 8 类 → 5 类）
KEEP_ITEMS = {
    "australia-to-china": ["books", "cosmetics", "electronics", "luggage"],  # 去掉 milk-powder, supplements, wine, furniture（家具也按行李定位保留——但这里之前用户决策"聚焦行李"可能要删）
    "europe-to-china": ["books", "cosmetics", "electronics", "luggage"],  # 去掉 milk-powder, wine, luxury-goods(改写不删), furniture
}
# 家具按用户「收缩聚焦行李」应一并删，但用户没明确指示先保留

def main():
    # 阶段 1：物理删除禁运品类目录（澳洲+欧洲）
    deleted = []
    for region in PROHIBITED_REGIONS:
        for item in PROHIBITED_ITEMS:
            for lang in ["en", "zh-cn"]:
                d = f"{BASE}/{lang}/{region}"
                if not os.path.isdir(d):
                    continue
                for city in os.listdir(d):
                    p = f"{d}/{city}/{item}"
                    if os.path.isdir(p):
                        # 物理删除
                        subprocess.run(["rm", "-rf", p], check=True)
                        deleted.append(f"{lang}/{region}/{city}/{item}")

    print(f"=== 阶段 1：物理删除完成 ===")
    print(f"删除品类页目录数: {len(deleted)}")
    print(f"按区域统计:")
    from collections import Counter
    by_region = Counter()
    for d in deleted:
        parts = d.split('/')
        by_region[f"{parts[1]}/{parts[3]}"] += 1
    for k, v in sorted(by_region.items()):
        print(f"  {k}: {v}")


if __name__ == '__main__':
    main()