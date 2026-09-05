"""扫描 city×item 品类页 + canonical 无内链 + 海运残留 + 短 meta 大规模扫描"""
import os, re, json
from collections import Counter

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

def meta_len(t):
    m = re.search(r'<meta name="description" content="([^"]*)"', t)
    if not m:
        return None
    return len(m.group(1))

def scan_dir(lang, region, sub_items=None):
    base_path = f"{BASE}/{lang}/{region}"
    if not os.path.isdir(base_path):
        return
    total = 0; miss = 0; short_n = 0; bucket = Counter()
    miss_list = []
    short_list = []
    for city_dir in sorted(os.listdir(base_path)):
        city_path = f"{base_path}/{city_dir}"
        if not os.path.isdir(city_path):
            continue
        if sub_items is not None:
            # city×item 模式
            for item in sub_items:
                idx = f"{city_path}/{item}/index.html"
                if not os.path.isfile(idx):
                    continue
                total += 1
                with open(idx, encoding="utf-8") as f:
                    t = f.read()
                ml = meta_len(t)
                if ml is None:
                    miss += 1
                    miss_list.append(idx)
                elif ml < 80:
                    short_n += 1
                    short_list.append((idx, ml))
                    bucket[(ml//20)*20] += 1
        else:
            idx = f"{city_path}/index.html"
            if not os.path.isfile(idx):
                continue
            total += 1
            with open(idx, encoding="utf-8") as f:
                t = f.read()
            ml = meta_len(t)
            if ml is None:
                miss += 1; miss_list.append(idx)
            elif ml < 80:
                short_n += 1; short_list.append((idx, ml))
                bucket[(ml//20)*20] += 1
    if total == 0:
        return
    print(f"{lang}/{region}: total={total}, missing={miss}, short(<80)={short_n}")
    if bucket:
        for k in sorted(bucket.keys()):
            print(f"  len bucket [{k}-{k+19}]: {bucket[k]}")
    if miss_list:
        print(f"  Missing samples: {[os.path.relpath(f, BASE) for f in miss_list[:3]]}")
    return total, miss, short_n

print("=== USA city×item 品类组合页（核心批量页）===")
USA_ITEMS = ["furniture","kitchenware","electronics","clothing","cosmetics","tea","books","documents","toys","shoes","bags","laptop","medicine","milk-powder","art","instruments","auto-parts"]
for lang in ["en", "zh-cn"]:
    scan_dir(lang, "usa-to-china", USA_ITEMS)

print("\n=== 其他国家 city×item 品类组合页 ===")
for lang in ["en", "zh-cn"]:
    for region, items in [
        ("canada-to-china", USA_ITEMS),
        ("australia-to-china", USA_ITEMS),
        ("europe-to-china", USA_ITEMS),
        ("uk-to-china", USA_ITEMS),
        ("japan-to-china", ["furniture","kitchenware","electronics","clothing","cosmetics","tea","books","documents","toys","shoes","bags","laptop"]),
        ("korea-to-china", ["furniture","kitchenware","electronics","clothing","cosmetics","tea","books","documents","toys","shoes","bags","laptop"]),
        ("seasia-to-china", ["furniture","kitchenware","electronics","clothing","cosmetics","tea","books","documents","toys","shoes","bags","laptop"]),
        ("taiwan-to-china", USA_ITEMS),
        ("mexico-to-china", USA_ITEMS),
        ("newzealand-to-china", USA_ITEMS),
    ]:
        scan_dir(lang, region, items)

print("\n=== 总计缺失 meta description 的页面（前 10）===")
total_miss = []
for lang in ["en", "zh-cn"]:
    base_lang = f"{BASE}/{lang}"
    for root, dirs, files in os.walk(base_lang):
        if ".git" in root or "node_modules" in root:
            continue
        for fn in files:
            if not fn.endswith(".html"):
                continue
            idx = os.path.join(root, fn)
            with open(idx, encoding="utf-8") as f:
                t = f.read()
            if meta_len(t) is None:
                total_miss.append(idx)
print(f"  Total missing: {len(total_miss)}")
for f in total_miss[:10]:
    print(f"    {os.path.relpath(f, BASE)}")