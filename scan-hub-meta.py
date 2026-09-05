"""扫描二线城市 hub 页 meta description 状态 + 找 meta 短/缺失的文件清单"""
import os, re, json

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# 知名美国二线城市（覆盖 hub 页可能的城市）
CITIES = [
    "dallas","houston","phoenix","san-diego","austin","jacksonville",
    "fort-worth","charlotte","indianapolis","san-antonio","denver",
    "washington","boston","el-paso","detroit","seattle","portland",
    "nashville","oklahoma-city","memphis","baltimore","milwaukee",
    "albuquerque","tucson","fresno","sacramento","mesa","kansas-city",
    "atlanta","omaha","minneapolis","tulsa","arlington","new-orleans",
    "cleveland","long-beach","virginia-beach","oakland","miami",
    "raleigh","colorado-springs","orlando","plano","lexington",
    "henderson","stockton","lincoln","cincinnati","santa-ana","newark",
    "irvine","buffalo","jersey-city","chula-vista","fort-wayne","gilbert",
    "laredo","chandler","madison","lubbock","winston-salem","garland",
    "glendale","hialeah","reno","baton-rouge","chesapeake","norfolk",
    "fremont","scottsdale","san-jose","tampa","pittsburgh","cincinnati",
]

def scan(lang, sub):
    path = f"{BASE}/{lang}/usa-to-china"
    if not os.path.isdir(path):
        return
    total = 0; miss_list = []; short_list = []
    for city_dir in sorted(os.listdir(path)):
        idx = f"{path}/{city_dir}/index.html"
        if not os.path.isfile(idx):
            continue
        total += 1
        with open(idx, encoding="utf-8") as f:
            t = f.read()
        m = re.search(r'<meta name="description" content="([^"]*)"', t)
        if not m:
            miss_list.append(idx)
            continue
        desc = m.group(1)
        if len(desc) < 80:
            short_list.append((idx, len(desc), desc))
    print(f"\n--- {lang} usa-to-china/*/index.html hub pages ---")
    print(f"  Total: {total}, Missing meta: {len(miss_list)}, Short meta (<80): {len(short_list)}")
    if miss_list:
        print(f"  Sample missing:")
        for f in miss_list[:5]:
            print(f"    {os.path.relpath(f, BASE)}")
    if short_list:
        print(f"  Sample short:")
        for f, n, d in short_list[:5]:
            print(f"    {os.path.relpath(f, BASE)}: len={n} -> {d[:60]}...")

for lang in ["en", "zh-cn"]:
    scan(lang, "usa-to-china")

# 同时扫描其他语言 hub
print("\n=== 其他国家/区域 hub ===")
for lang in ["en", "zh-cn"]:
    for region in ["canada-to-china", "australia-to-china", "europe-to-china",
                   "japan-to-china", "korea-to-china", "seasia-to-china",
                   "uk-to-china", "taiwan-to-china", "mexico-to-china",
                   "newzealand-to-china", "uk-to-china"]:
        path = f"{BASE}/{lang}/{region}"
        if not os.path.isdir(path):
            continue
        total = 0; miss = 0; short_n = 0
        miss_list = []
        for city_dir in sorted(os.listdir(path)):
            idx = f"{path}/{city_dir}/index.html"
            if not os.path.isfile(idx):
                continue
            total += 1
            with open(idx, encoding="utf-8") as f:
                t = f.read()
            m = re.search(r'<meta name="description" content="([^"]*)"', t)
            if not m:
                miss += 1
                miss_list.append(idx)
                continue
            if len(m.group(1)) < 80:
                short_n += 1
        if total > 0 and (miss > 0 or short_n > 0):
            print(f"  {lang}/{region}: total={total}, missing={miss}, short(<80)={short_n}")