"""BreadcrumbList 补全：为缺失的页面生成面包屑 JSON-LD 并注入 <head>。
推导规则：
- 语言前缀 zh-cn/en
- 美国寄中国线：usa-to-china/{city}/{item}/
- 攻略：blog/{slug}.html
- 城市对：city/{x-to-y}.html
- 其他结构段用 STRUCT 映射
末级用页面 <h1> 文本（最准）。
"""
import re, json
from pathlib import Path

DOMAIN = "https://subaog.com"

CITY_ZH = {"atlanta":"亚特兰大","austin":"奥斯汀","boston":"波士顿","chicago":"芝加哥","dallas":"达拉斯",
    "denver":"丹佛","detroit":"底特律","houston":"休斯顿","las-vegas":"拉斯维加斯","los-angeles":"洛杉矶",
    "miami":"迈阿密","new-york":"纽约","philadelphia":"费城","phoenix":"凤凰城","portland":"波特兰",
    "san-diego":"圣地亚哥","san-francisco":"旧金山","san-jose":"圣何塞","seattle":"西雅图","washington-dc":"华盛顿"}
CITY_EN = {k: v.title() for k, v in CITY_ZH.items()}

ITEM_ZH = {"auto-parts":"汽车配件","baby-formula":"婴儿奶粉","bicycles":"自行车","books":"书籍","coffee":"咖啡",
    "cosmetics":"化妆品","curtains":"窗帘布艺","electronics":"电子产品","figurines":"手办","furniture":"家具",
    "kitchenware":"厨具","luxury-bags":"奢侈包袋","medical-devices":"医疗器械","medicine":"药品","musical-instruments":"乐器",
    "perfume":"香水","pet-food":"宠物食品","pet-supplies":"宠物用品","shoes":"鞋子","snacks":"零食",
    "supplements":"保健品","tea":"茶叶","tools":"工具","toys":"玩具","wine":"红酒"}
ITEM_EN = {k: v.title() for k, v in ITEM_ZH.items()}

STRUCT_ZH = {"usa-to-china":"美国寄中国","blog":"攻略","city":"城市对","student-luggage":"留学生行李",
    "usa-moving-to-china":"搬家回国","tools":"工具","japan-to-china":"日本寄中国","korea-to-china":"韩国寄中国",
    "europe-to-china":"欧洲寄中国","canada-to-china":"加拿大寄中国","australia-to-china":"澳洲寄中国",
    "seasia-to-china":"东南亚寄中国","pricing":"价格","about":"关于我们","contact":"联系我们","faq":"常见问题",
    "report":"数据报告","seasia":"东南亚寄中国"}
STRUCT_EN = {k: v for k, v in {"usa-to-china":"Ship from USA to China","blog":"Guides","city":"City Pairs",
    "student-luggage":"Student Luggage","usa-moving-to-china":"Moving to China","tools":"Tools",
    "japan-to-china":"Japan to China","korea-to-china":"Korea to China","europe-to-china":"Europe to China",
    "canada-to-china":"Canada to China","australia-to-china":"Australia to China","seasia-to-china":"SE Asia to China",
    "pricing":"Pricing","about":"About","contact":"Contact","faq":"FAQ","report":"Report","seasia":"SE Asia to China"}.items()}

def get_h1(file_path):
    t = Path(file_path).read_text(encoding="utf-8")
    m = re.search(r"<h1[^>]*>(.*?)</h1>", t, flags=re.DOTALL)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return None

def build_crumbs(file_path):
    rel = str(file_path)
    lang = "zh" if rel.startswith("zh-cn/") else "en"
    CITY = CITY_ZH if lang == "zh" else CITY_EN
    ITEM = ITEM_ZH if lang == "zh" else ITEM_EN
    STRUCT = STRUCT_ZH if lang == "zh" else STRUCT_EN
    HOME = "首页" if lang == "zh" else "Home"
    parts = rel.split("/")
    segs = parts[1:-1]          # 目录段
    filename = parts[-1]
    base = DOMAIN + "/" + ("zh-cn" if lang == "zh" else "en")
    crumbs = [{"name": HOME, "url": base + "/"}]
    acc = base
    if segs and segs[0] == "usa-to-china":
        acc += "/usa-to-china"
        crumbs.append({"name": STRUCT["usa-to-china"], "url": acc + "/"})
        if len(segs) > 1:
            acc += "/" + segs[1]
            crumbs.append({"name": CITY.get(segs[1], segs[1].replace("-", " ").title()), "url": acc + "/"})
            if len(segs) > 2:
                acc += "/" + segs[2]
                crumbs.append({"name": ITEM.get(segs[2], segs[2].replace("-", " ").title()), "url": acc + "/"})
    elif segs and segs[0] == "blog":
        acc += "/blog"
        crumbs.append({"name": STRUCT["blog"], "url": acc + "/"})
        if filename != "index.html":
            slug = filename[:-5]
            name = get_h1(file_path) or slug
            crumbs.append({"name": name, "url": base + "/blog/" + slug + ".html"})
    elif segs and segs[0] == "city":
        acc += "/city"
        crumbs.append({"name": STRUCT["city"], "url": acc + "/"})
        if filename != "index.html":
            slug = filename[:-5]
            name = get_h1(file_path) or slug
            crumbs.append({"name": name, "url": base + "/city/" + slug + ".html"})
    else:
        for seg in segs:
            acc += "/" + seg
            crumbs.append({"name": STRUCT.get(seg, seg.replace("-", " ").title()), "url": acc + "/"})
        if filename != "index.html":
            slug = filename[:-5]
            name = get_h1(file_path) or slug
            crumbs.append({"name": name, "url": base + "/" + "/".join(segs) + "/" + slug + ".html"})
    return crumbs

def breadcrumb_jsonld(crumbs):
    items = [{"@type":"ListItem","position":i+1,"name":c["name"],"item":c["url"]} for i, c in enumerate(crumbs)]
    return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}, ensure_ascii=False)

n = 0
for d in ["zh-cn", "en"]:
    for f in Path(d).rglob("*.html"):
        t = f.read_text(encoding="utf-8")
        if "BreadcrumbList" in t:
            continue
        crumbs = build_crumbs(f)
        if len(crumbs) < 2:
            continue
        js = f'<script type="application/ld+json">{breadcrumb_jsonld(crumbs)}</script>'
        # 注入到 </head> 前
        if "</head>" in t:
            t = t.replace("</head>", "  " + js + "\n</head>", 1)
            f.write_text(t, encoding="utf-8")
            n += 1
print(f"✅ BreadcrumbList 注入: {n} 页")
