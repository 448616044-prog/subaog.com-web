#!/usr/bin/env python3
"""注入内链枢纽：
1) pillar /usa-to-china/ 补「全部美国城市」网格 → 链 20 个 city hub（解决 city hub 孤儿）
2) 20 个 city hub 补「可寄品类」网格 → 链各自 ~24 个组合页（解决 800 组合页孤儿）
中英双语。插入位置：<footer class="footer"> 之前。
"""
import re
from pathlib import Path

BASE = Path(".")
LANGS = {"zh-cn": "zh", "en": "en"}

CITIES = {
    "atlanta": ("亚特兰大", "Atlanta"), "austin": ("奥斯汀", "Austin"),
    "boston": ("波士顿", "Boston"), "chicago": ("芝加哥", "Chicago"),
    "dallas": ("达拉斯", "Dallas"), "denver": ("丹佛", "Denver"),
    "detroit": ("底特律", "Detroit"), "houston": ("休斯顿", "Houston"),
    "las-vegas": ("拉斯维加斯", "Las Vegas"), "los-angeles": ("洛杉矶", "Los Angeles"),
    "miami": ("迈阿密", "Miami"), "new-york": ("纽约", "New York"),
    "philadelphia": ("费城", "Philadelphia"), "phoenix": ("凤凰城", "Phoenix"),
    "portland": ("波特兰", "Portland"), "san-diego": ("圣地亚哥", "San Diego"),
    "san-francisco": ("旧金山", "San Francisco"), "san-jose": ("圣何塞", "San Jose"),
    "seattle": ("西雅图", "Seattle"), "washington-dc": ("华盛顿", "Washington DC"),
}
ITEMS = {
    "auto-parts": ("汽车零件", "Auto Parts"), "baby-formula": ("奶粉", "Baby Formula"),
    "bicycles": ("自行车", "Bicycles"), "books": ("书籍", "Books"),
    "coffee": ("咖啡", "Coffee"), "cosmetics": ("化妆品", "Cosmetics"),
    "curtains": ("窗帘", "Curtains"), "electronics": ("电子产品", "Electronics"),
    "figurines": ("摆件手办", "Figurines"), "furniture": ("家具", "Furniture"),
    "kitchenware": ("厨具", "Kitchenware"), "luxury-bags": ("奢侈品包", "Luxury Bags"),
    "medical-devices": ("医疗器械", "Medical Devices"), "medicine": ("中药材", "Medicine"),
    "musical-instruments": ("乐器", "Musical Instruments"), "perfume": ("香水", "Perfume"),
    "pet-food": ("宠物食品", "Pet Food"), "pet-supplies": ("宠物用品", "Pet Supplies"),
    "shoes": ("鞋子", "Shoes"), "snacks": ("零食", "Snacks"),
    "supplements": ("保健品", "Supplements"), "tea": ("茶叶", "Tea"),
    "tools": ("工具", "Tools"), "toys": ("玩具", "Toys"), "wine": ("红酒", "Wine"),
}

def lbl(slug, lang):
    d = ITEMS.get(slug)
    if d: return d[0] if lang == "zh-cn" else d[1]
    return slug.replace("-", " ").title()

def city_lbl(slug, lang):
    d = CITIES.get(slug)
    if d: return d[0] if lang == "zh-cn" else d[1]
    return slug.replace("-", " ").title()

def grid_block(lang, city):
    """city hub 的品类导航网格"""
    city_slug = city
    cn = city_lbl(city_slug, lang)
    title = f"从{cn}寄中国 · 可寄品类" if lang == "zh-cn" else f"Ship from {city_lbl(city_slug,'en')} · Categories"
    sub = "按物品选专线，点击查看运费与时效" if lang == "zh-cn" else "Pick a category for rates & transit time"
    # 实际组合页（该城市目录下含 index.html 的子目录）
    items = []
    d = BASE / lang / "usa-to-china" / city_slug
    if d.is_dir():
        for sub_d in sorted(d.iterdir()):
            if sub_d.is_dir() and (sub_d / "index.html").exists():
                items.append(sub_d.name)
    links = "".join(
        f'<a href="/{lang}/usa-to-china/{city_slug}/{it}/" style="display:inline-block;margin:5px 6px;padding:7px 15px;background:#fff;border:1px solid var(--border);border-radius:20px;font-size:13px;color:var(--text);text-decoration:none;font-weight:500;transition:.2s" onmouseover="this.style.borderColor=\'var(--primary)\';this.style.color=\'var(--primary)\'" onmouseout="this.style.borderColor=\'var(--border)\';this.style.color=\'var(--text)\'">{lbl(it,lang)} →</a>'
        for it in items)
    return f'''
  <section class="section" style="background:#fff">
    <div class="container">
      <div class="section-title"><h2>{title}</h2><p>{sub}</p></div>
      <div style="text-align:center;line-height:2.4">{links}</div>
    </div>
  </section>'''

def cities_block(lang):
    title = "全部美国出发城市" if lang == "zh-cn" else "All US Origin Cities"
    sub = "选您的城市，查看专属运费与时效" if lang == "zh-cn" else "Pick your city for dedicated rates & transit"
    links = "".join(
        f'<a href="/{lang}/usa-to-china/{c}/" style="display:inline-block;margin:5px 6px;padding:8px 16px;background:var(--primary-light);border:1px solid var(--primary-light);border-radius:20px;font-size:14px;color:var(--primary);text-decoration:none;font-weight:600" onmouseover="this.style.background=\'var(--primary)\';this.style.color=\'#fff\'" onmouseout="this.style.background=\'var(--primary-light)\';this.style.color=\'var(--primary)\'">{city_lbl(c,lang)} →</a>'
        for c in CITIES)
    return f'''
  <section class="section" style="background:#F5F7FA">
    <div class="container">
      <div class="section-title"><h2>{title}</h2><p>{sub}</p></div>
      <div style="text-align:center;line-height:2.6">{links}</div>
    </div>
  </section>'''

def inject_before_footer(path, block):
    t = path.read_text(encoding="utf-8")
    import re as _re
    m = _re.search(r'^\s*<footer class="footer">', t, _re.M)
    if not m:
        return False
    if "全部美国出发城市" in t or "可寄品类" in t or "All US Origin Cities" in t or ("Ship from" in t and "Categories" in t):
        return "skip"  # already injected
    t = t[:m.start()] + block + "\n" + t[m.start():]
    path.write_text(t, encoding="utf-8")
    return True

done = skip = fail = 0
# 1) pillar 城市网格
for lang in LANGS:
    p = BASE / lang / "usa-to-china" / "index.html"
    if p.exists():
        r = inject_before_footer(p, cities_block(lang))
        if r is True: done += 1
        elif r == "skip": skip += 1
        else: fail += 1
        print(f"  pillar {lang}: {r}")
# 2) city hub 品类导航
for lang in LANGS:
    for c in CITIES:
        p = BASE / lang / "usa-to-china" / c / "index.html"
        if p.exists():
            r = inject_before_footer(p, grid_block(lang, c))
            if r is True: done += 1
            elif r == "skip": skip += 1
            else: fail += 1
print(f"\n注入完成: 新增 {done} | 已存在跳过 {skip} | 失败 {fail}")
