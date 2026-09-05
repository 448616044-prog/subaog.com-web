"""中文 city×item 短 meta description 批量修复 + 扩足长度 + 修复括号破损"""
import os, re, json

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# === 完整中文城市映射（21 个）===
CITY_ZH = {
    "atlanta": "亚特兰大",
    "austin": "奥斯汀",
    "boston": "波士顿",
    "chicago": "芝加哥",
    "dallas": "达拉斯",
    "denver": "丹佛",
    "detroit": "底特律",
    "houston": "休斯顿",
    "las-vegas": "拉斯维加斯",
    "los-angeles": "洛杉矶",
    "miami": "迈阿密",
    "new-york": "纽约",
    "philadelphia": "费城",
    "phoenix": "凤凰城",
    "portland": "波特兰",
    "san-diego": "圣地亚哥",
    "san-francisco": "旧金山",
    "san-jose": "圣何塞",
    "seattle": "西雅图",
    "washington-dc": "华盛顿特区",
}

# === 完整品类中文映射（20 个）===
ITEM_ZH = {
    "auto-parts": "汽车配件",
    "bicycles": "自行车",
    "books": "书籍",
    "coffee": "咖啡",
    "curtains": "窗帘布艺",
    "figurines": "摆件雕塑",
    "furniture": "家具",
    "kitchenware": "厨房用品",
    "medical-devices": "医疗器械",
    "medicine": "中西药品",
    "musical-instruments": "乐器",
    "perfume": "香水",
    "pet-food": "宠物食品",
    "pet-supplies": "宠物用品",
    "shoes": "鞋子",
    "snacks": "零食",
    "tea": "茶叶茶具",
    "tools": "工具",
    "toys": "玩具",
    "wine": "酒",
}

# === 城市本地化描述（每个 80-100 字）===
CITY_LOCAL = {
    "atlanta": "亚特兰大是美国东南部物流枢纽，达美航空总部所在地，空运回中国时效稳定；当地华人聚居 Duluth、Johns Creek，留学生与新移民寄件高频。",
    "austin": "奥斯汀是德州新兴科技城市，德州大学奥斯汀分校、戴尔公司总部所在地，华人工程师与 IT 群体增长迅猛，寄件需求稳步上升。",
    "boston": "波士顿是东北部高等教育重镇，哈佛、MIT、波士顿大学等高校留学生密集，每年毕业季行李回国需求集中。",
    "chicago": "芝加哥地处美中，是中西部空运枢纽，O'Hare 机场航线密集直达亚洲；当地华人工程师、华中科技大学校友会等寄件需求稳定。",
    "dallas": "达拉斯是德州新兴华人聚集城市，Plano、Richardson 区域华人社区快速增长，从德州寄中国的个人件、家庭件、商务件需求都在增长。",
    "denver": "丹佛是科罗拉多华人社区中心，丹佛大学、科罗拉多大学留学生和工程师群体是主要的寄件需求来源。",
    "detroit": "底特律是汽车工业重镇，华人工程师与制造业从业者寄件频繁；安大略机场邻近多伦多可作为加拿大方向的备选起运地。",
    "houston": "休斯顿是德州第一大华人聚居城市，糖城（Sugar Land）、凯蒂（Katy）是核心华人区，空运回国需求常年旺盛。",
    "las-vegas": "拉斯维加斯华人主要从事酒店、餐饮、博彩行业，从赌城寄中国的礼品、保健品、收藏品需求稳定。",
    "los-angeles": "洛杉矶是美国最大华人聚集城市，圣盖博谷、阿罕布拉、蒙特利公园等华人区寄件密度最高；LAX 国际机场直飞中国航班密集，物流时效优势明显。",
    "miami": "迈阿密是佛州门户城市，邻近加勒比海与拉丁美洲，华人主要从事贸易与旅游；迈阿密国际机场直飞中国航线选择丰富。",
    "new-york": "纽约是美国最大都市，法拉盛、布鲁克林八大道是华人核心聚居区，寄件密度全美最高；JFK 机场直飞中国航班数量全美第一。",
    "philadelphia": "费城是宾州历史名城，特拉华河谷华人社区稳定，新泽西州紧邻，社区寄件与商业件需求持续。",
    "phoenix": "凤凰城是亚利桑那州府，亚省阳光地带华人近年快速增长，Tempe、Chandler 是主要华人区。",
    "portland": "波特兰是俄勒冈州最大城市，木材、电子产业集中，华人工程师与留学群体从美西寄中国件需求稳定。",
    "san-diego": "圣地亚哥紧邻墨西哥边境，圣地亚哥大学、加州大学圣地亚哥分校（UCSD）留学群体是重要寄件来源。",
    "san-francisco": "旧金山湾区是全美华人密度最高的城市之一，硅谷科技公司华人员工密集；SFO 直飞中国航班密集。",
    "san-jose": "圣何塞是硅谷核心城市，苹果、谷歌、Adobe 等大厂华人员工密集，从湾区寄中国的高科技产品和家庭件需求稳定。",
    "seattle": "西雅图是微软、亚马逊总部所在地，太平洋西北地区华人工程师扎堆，波音与科技业寄件需求稳定。",
    "washington-dc": "华盛顿特区是政治中心，DC、弗吉尼亚、马里兰华人以政府工作人员、医生、律师为主，华人社区稳定。",
}

# === 品类特色（每个 50-70 字）===
ITEM_TIPS = {
    "auto-parts": "汽车配件按实重或体积重计费；油液类需单独处理。",
    "bicycles": "自行车属大件物品，按体积重计费（长×宽×高÷5000）；拆解前后轮可节省运费。",
    "books": "书籍属轻货，按体积重计费，建议紧凑打包；古旧书籍建议单独保价。",
    "coffee": "咖啡属常规干货，建议真空密封防潮；咖啡豆、胶囊咖啡建议整箱打包。",
    "curtains": "窗帘布艺按体积重计费，建议压缩包装；易勾丝需用纸箱加固。",
    "figurines": "摆件雕塑属易碎品，按实重计费；建议用气泡膜单独包装防碎。",
    "furniture": "家具属大件物品，按体积重计费（长×宽×高÷5000），建议拆解或整装以节省运费。",
    "kitchenware": "厨房用品含瓷器、刀具属敏感货，需如实申报；玻璃器皿注意包装防碎。",
    "medical-devices": "医疗器械属敏感货，需品牌型号与使用说明；建议保留购物凭证。",
    "medicine": "中西药属敏感货，需处方与成分说明；个人用量在合理范围内可邮寄。",
    "musical-instruments": "乐器按体积重计费，吉他、提琴属轻货；钢琴、电子琴属大件。",
    "perfume": "香水属敏感液体货，限量邮寄（个人用量内）；建议密封防漏包装。",
    "pet-food": "宠物食品按实重计费，整箱打包最划算；建议保留购物小票。",
    "pet-supplies": "宠物用品按实重或体积重计费；含电池类（如自动喂食器）走敏感货通道。",
    "shoes": "鞋子属轻货，整箱打包节省运费；奢侈鞋款建议单独保价。",
    "snacks": "零食按实重计费，整箱打包最划算；含液体零食建议密封防漏。",
    "tea": "茶叶属常规干货，建议真空密封防潮；普洱茶饼需如实申报价值。",
    "tools": "工具按实重计费；电动工具内含电池需走敏感货通道，如实申报。",
    "toys": "玩具按实重或体积重计费，电子玩具含电池需走敏感货通道。",
    "wine": "酒属敏感液体货，限量邮寄（个人用量内）；建议密封防漏包装。",
}

# === 固定后缀（标准化卖点，避免每次组合都不同）===
SUFFIX = (
    "20kg 起运，¥100/kg（20-99kg）/¥90/kg（100kg+），全美免费上门取件，"
    "10-15 个工作日门到门，双清包税无后顾之忧。比 FedEx/UPS 直营便宜 40% 以上。"
)


def fix_meta(current, city_zh, item_zh, city_local, item_tip):
    """扩写 meta：保留头部 + 修破损 + 补足长度到 150-160 字"""
    # 先修常见破损
    fixed = current
    fixed = fixed.replace("税率15%。", "税率15%）。")
    fixed = fixed.replace("税率50%。", "税率50%）。")
    # 头部以 "10-15 个工作日" 结尾或以 "。" 结尾，标准化
    if not fixed.rstrip().endswith(("。", "！", "？")):
        fixed = fixed.rstrip() + "。"

    # 取原 meta 的第一段（城市 + 品类 + 税率段）
    head = fixed

    # 拼接后缀（含本地化 + 品类 + 价格 + 取件 + 时效）
    new_meta = f"{head}{city_local}{item_tip}{SUFFIX}"

    # 截断到 160 字（避免过长）
    if len(new_meta) > 165:
        new_meta = new_meta[:162] + "…"
    return new_meta


base = f"{BASE}/zh-cn/usa-to-china"
modified = 0
unchanged = 0
missing = []

for city_dir in sorted(os.listdir(base)):
    city_path = f"{base}/{city_dir}"
    if not os.path.isdir(city_path):
        continue
    city_zh = CITY_ZH.get(city_dir)
    city_local = CITY_LOCAL.get(city_dir)
    if not city_zh or not city_local:
        missing.append(city_dir)
        continue
    for item in sorted(os.listdir(city_path)):
        idx = f"{city_path}/{item}/index.html"
        if not os.path.isfile(idx):
            continue
        item_zh = ITEM_ZH.get(item)
        item_tip = ITEM_TIPS.get(item)
        if not item_zh or not item_tip:
            missing.append(f"{city_dir}/{item}")
            continue

        with open(idx, encoding="utf-8") as f:
            t = f.read()
        m = re.search(r'(<meta name="description" content=")([^"]*)(")', t)
        if not m:
            continue
        cur_desc = m.group(2)
        if len(cur_desc) >= 130:
            unchanged += 1
            continue

        new_desc = fix_meta(cur_desc, city_zh, item_zh, city_local, item_tip)
        # 检查最终长度
        if len(new_desc) < 130:
            # 仍不够就再追加一句通用提示
            new_desc = new_desc + "微信下单全程跟踪，支持拆箱合箱。"

        # 替换
        new_t = t.replace(m.group(0), m.group(1) + new_desc + m.group(3), 1)
        with open(idx, "w", encoding="utf-8") as f:
            f.write(new_t)
        modified += 1

print(f"修改: {modified}")
print(f"未改（已足够长）: {unchanged}")
print(f"缺映射: {missing[:20]}")
print(f"共缺: {len(set(missing))}")