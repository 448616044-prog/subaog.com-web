"""澳洲 + 欧洲 城市×品类 数据映射（en + zh-cn）"""
# 价格档位
TIERS = {
    "australia-to-china": {
        "region_en": "Australia", "region_zh": "澳洲",
        "price_20": 100, "price_100": 90,
        "tier_en": "AU tier", "tier_zh": "澳洲档",
        "region_full_en": "Australia", "region_full_zh": "澳大利亚",
    },
    "europe-to-china": {
        "region_en": "Europe", "region_zh": "欧洲",
        "price_20": 90, "price_100": 80,
        "tier_en": "EU tier", "tier_zh": "欧洲档",
        "region_full_en": "Europe", "region_full_zh": "欧洲",
    },
}

# 城市映射
CITIES = {
    "australia-to-china": {
        "adelaide":   {"en": "Adelaide",   "zh": "阿德莱德", "local_en": "Adelaide is South Australia's capital, home to the University of Adelaide and Flinders University; student and family shipping demand is steady.", "local_zh": "阿德莱德是南澳首府，阿德莱德大学、弗林德斯大学留学生聚集，学生与家庭寄件需求稳定。"},
        "brisbane":   {"en": "Brisbane",   "zh": "布里斯班", "local_en": "Brisbane is Queensland's hub; University of Queensland students and the Sunnybank Chinese community ship frequently.", "local_zh": "布里斯班是昆州枢纽，昆士兰大学留学生与 Sunnybank 华人区寄件高频。"},
        "gold-coast": {"en": "Gold Coast", "zh": "黄金海岸", "local_en": "Gold Coast is a tourist city with a growing Chinese community; gift and personal shipping demand is steady.", "local_zh": "黄金海岸是旅游城市，华人社区持续增长，礼品与个人件寄件需求稳定。"},
        "melbourne":  {"en": "Melbourne",  "zh": "墨尔本",   "local_en": "Melbourne has Australia's largest Chinese community (Box Hill, Glen Waverley); supplement and formula shipping is the highest-volume category.", "local_zh": "墨尔本拥有澳洲最大华人社区（Box Hill、Glen Waverley），保健品与奶粉寄件量最大。"},
        "perth":      {"en": "Perth",      "zh": "珀斯",     "local_en": "Perth is Western Australia's capital, the closest major Australian city to Asia; direct flights shorten transit time.", "local_zh": "珀斯是西澳首府，距离亚洲最近的澳洲大城市，直飞航班缩短时效。"},
        "sydney":     {"en": "Sydney",     "zh": "悉尼",     "local_en": "Sydney is Australia's largest city; the Chatswood, Hurstville and Burwood Chinese communities ship heavily.", "local_zh": "悉尼是澳洲最大城市，Chatswood、Hurstville、Burwood 华人区寄件量大。"},
    },
    "europe-to-china": {
        "amsterdam": {"en": "Amsterdam", "zh": "阿姆斯特丹", "local_en": "Amsterdam is a Netherlands hub; Schiphol airport has dense Asia flights, and Chinese students and traders ship steadily.", "local_zh": "阿姆斯特丹是荷兰枢纽，史基浦机场亚洲航线密集，华人学生与商贸寄件稳定。"},
        "berlin":    {"en": "Berlin",    "zh": "柏林",     "local_en": "Berlin is Germany's capital; Chinese students and engineers ship frequently, especially formula and cosmetics.", "local_zh": "柏林是德国首都，华人学生与工程师寄件高频，尤以奶粉、化妆品为主。"},
        "brussels":  {"en": "Brussels",  "zh": "布鲁塞尔", "local_en": "Brussels is the EU capital; international students and expats ship personal effects regularly.", "local_zh": "布鲁塞尔是欧盟首都，国际学生与外派人员常寄个人物品。"},
        "london":    {"en": "London",    "zh": "伦敦",     "local_en": "London has the UK's largest Chinese community; luxury goods, formula and student luggage are the top categories.", "local_zh": "伦敦拥有英国最大华人社区，奢侈品、奶粉与留学生行李是高频品类。"},
        "madrid":    {"en": "Madrid",    "zh": "马德里",   "local_en": "Madrid is Spain's capital; Chinese students and traders ship wine, ham and personal items.", "local_zh": "马德里是西班牙首都，华人学生与商贸寄红酒、火腿与个人物品。"},
        "milan":     {"en": "Milan",     "zh": "米兰",     "local_en": "Milan is Italy's fashion and luxury hub; luxury bags and clothing to China are core categories.", "local_zh": "米兰是意大利时尚与奢侈品中心，奢侈品包袋与服饰寄中国是核心。"},
        "paris":     {"en": "Paris",     "zh": "巴黎",     "local_en": "Paris is France's capital; luxury goods, wine and pharmacy cosmetics are the top shipping categories.", "local_zh": "巴黎是法国首都，奢侈品、红酒与药妆是高频寄件品类。"},
        "rome":      {"en": "Rome",      "zh": "罗马",     "local_en": "Rome is Italy's capital; Chinese students and families ship personal effects and wine steadily.", "local_zh": "罗马是意大利首都，华人学生与家庭寄个人物品与红酒稳定。"},
    },
}

# 品类映射（slug -> 通用数据 + 按地域定制）
# verdict: 品类结论（可寄/限量可寄）
# packing: 包装建议
# faq_q1: FAQ 第1问「能寄吗」的答案（品类定制）
# blog: 关联博客页 slug（无则 None）
ITEMS_COMMON = {
    "cosmetics": {
        "en": "Cosmetics", "zh": "化妆品",
        "blog": "can-i-ship-cosmetics-to-china",
        "faq_q1_en": "Yes — cosmetics ship routinely; seal liquids to prevent leaks and declare accurately.",
        "faq_q1_zh": "可寄。化妆品属常规品类，液体类密封包装并如实申报。",
    },
    "electronics": {
        "en": "Electronics", "zh": "电子产品",
        "blog": None,
        "faq_q1_en": "Yes — electronics with batteries (laptops, cameras) ship via our battery line; keep original packaging and invoices.",
        "faq_q1_zh": "可寄。带电池的电子产品（笔记本、相机）走含电池专线，保留原包装与发票。",
    },
    "books": {
        "en": "Books", "zh": "书籍",
        "blog": None,
        "faq_q1_en": "Yes — books are light cargo; pack tightly to lower volumetric weight and avoid moisture.",
        "faq_q1_zh": "可寄。书籍属轻货，紧凑打包降低体积重并防潮。",
    },
    "luggage": {
        "en": "Luggage", "zh": "行李",
        "blog": None,
        "faq_q1_en": "Yes — student luggage and personal effects are our core route; consolidate boxes and mark personal items.",
        "faq_q1_zh": "可寄。留学生行李与个人物品是我们的核心线路，合箱打包并标注个人物品。",
    },
    "furniture": {
        "en": "Furniture", "zh": "家具",
        "blog": None,
        "faq_q1_en": "Yes — large items charge by volumetric weight (L×W×H÷5000); disassemble to save on freight.",
        "faq_q1_zh": "可寄。大件按体积重计费（长×宽×高÷5000），拆装更省运费。",
    },
}

ITEMS_AU = {
    "milk-powder": {
        "en": "Baby Formula", "zh": "奶粉",
        "blog": "can-i-ship-baby-formula-to-china",
        "verdict_en": "Allowed. Australian formula (a2, Bellamy's, Aptamil) is one of our most-shipped categories. Declare brand and quantity accurately.",
        "verdict_zh": "可寄。澳洲奶粉（a2、贝拉米、爱他美）是高频寄件品类，如实申报品牌与数量即可。",
        "packing_en": "Keep original tins sealed, use air cushioning, and declare brand and quantity clearly.",
        "packing_zh": "罐装保持原封、做好缓冲防压，如实申报品牌与数量。",
        "faq_q1_en": "Yes — Australian baby formula (a2, Bellamy's, Aptamil) is a core category; declare brand and quantity.",
        "faq_q1_zh": "可寄。澳洲奶粉（a2、贝拉米、爱他美）是核心品类，如实申报品牌与数量。",
    },
    "supplements": {
        "en": "Supplements & Vitamins", "zh": "保健品",
        "blog": "can-i-ship-supplements-to-china",
        "verdict_en": "Allowed. Blackmores, Swisse and vitamins are core categories; we handle ingredient restrictions and customs paperwork.",
        "verdict_zh": "可寄。Blackmores、Swisse 等保健品是核心品类，成分限制与清关文件我们协助把关。",
        "packing_en": "Keep original packaging, avoid heat and moisture, and declare ingredients accurately.",
        "packing_zh": "保留原包装、避免高温受潮，如实申报成分。",
        "faq_q1_en": "Yes — supplements and vitamins (Blackmores, Swisse) are a core category; we handle ingredient restrictions.",
        "faq_q1_zh": "可寄。Blackmores、Swisse 等保健品是核心品类，成分限制我们协助把关。",
    },
    "wine": {
        "en": "Australian Wine", "zh": "葡萄酒",
        "blog": "can-i-ship-wine-to-china",
        "verdict_en": "Limited. Australian wine is allowed within personal-use limits (a few bottles); declare value accurately.",
        "verdict_zh": "限量可寄。澳洲葡萄酒个人用量内可寄（限几瓶），如实申报价值。",
        "packing_en": "Seal and cushion each bottle, use divider boxes, and mark as fragile.",
        "packing_zh": "单瓶密封+缓冲，用隔断箱，标注易碎。",
        "faq_q1_en": "Yes, within personal-use limits (a few bottles) — Australian wine ships by air; declare value accurately.",
        "faq_q1_zh": "可寄（个人用量内，限几瓶）。澳洲葡萄酒空运，如实申报价值。",
    },
}

ITEMS_EU = {
    "luxury-goods": {
        "en": "Luxury Goods", "zh": "奢侈品",
        "blog": "can-i-ship-luxury-bags-to-china",
        "verdict_en": "Allowed. Luxury bags, watches and accessories (LV, Chanel, Hermès) — declare value and insure high-value items.",
        "verdict_zh": "可寄。奢侈品包表配饰（LV、Chanel、爱马仕），申报价值并对高价值物品保价。",
        "packing_en": "Keep receipts and certificates, cushion carefully, and insure high-value items.",
        "packing_zh": "保留票据与证书，仔细缓冲，高价值建议保价。",
        "faq_q1_en": "Yes — luxury bags, watches and accessories (LV, Chanel) ship by air; declare value and insure.",
        "faq_q1_zh": "可寄。奢侈品包表配饰（LV、Chanel）空运，申报价值并保价。",
    },
    "wine": {
        "en": "Wine", "zh": "红酒",
        "blog": "can-i-ship-wine-to-china",
        "verdict_en": "Limited. French and Italian wine is allowed within personal-use limits (a few bottles); declare value accurately.",
        "verdict_zh": "限量可寄。法国、意大利红酒个人用量内可寄（限几瓶），如实申报价值。",
        "packing_en": "Seal and cushion each bottle, use divider boxes, and mark as fragile.",
        "packing_zh": "单瓶密封+缓冲，用隔断箱，标注易碎。",
        "faq_q1_en": "Yes, within personal-use limits (a few bottles) — French and Italian wine ships by air; declare value.",
        "faq_q1_zh": "可寄（个人用量内，限几瓶）。法国、意大利红酒空运，如实申报价值。",
    },
    "milk-powder": {
        "en": "Baby Formula", "zh": "奶粉",
        "blog": "can-i-ship-baby-formula-to-china",
        "verdict_en": "Allowed. German formula (Aptamil, Hipp) is a core Europe-to-China category; declare brand and quantity accurately.",
        "verdict_zh": "可寄。德国奶粉（爱他美、喜宝）是欧洲寄中国核心品类，如实申报品牌与数量。",
        "packing_en": "Keep original tins sealed, use air cushioning, and declare brand and quantity clearly.",
        "packing_zh": "罐装保持原封、做好缓冲防压，如实申报品牌与数量。",
        "faq_q1_en": "Yes — German formula (Aptamil, Hipp) is a core Europe-to-China category; declare brand and quantity.",
        "faq_q1_zh": "可寄。德国奶粉（爱他美、喜宝）是欧洲寄中国核心品类，如实申报品牌与数量。",
    },
}

# 组装每个 region 的品类清单（保留顺序）
def build_items(region):
    if region == "australia-to-china":
        items = {}
        for slug, d in ITEMS_AU.items():
            items[slug] = d
        for slug, d in ITEMS_COMMON.items():
            items[slug] = d
        return items
    else:
        items = {}
        for slug, d in ITEMS_EU.items():
            items[slug] = d
        for slug, d in ITEMS_COMMON.items():
            items[slug] = d
        return items

# 通用 verdict（common 品类没有单独的 verdict，用 faq_q1 生成）
COMMON_VERDICT = {
    "cosmetics":   {"verdict_en": "Allowed. Cosmetics are routine cargo; liquids need sealed packaging.", "verdict_zh": "可寄。化妆品属常规品类，液体类需密封包装。", "packing_en": "Keep original packaging, seal liquids, and retain purchase receipts.", "packing_zh": "保留原包装、液体密封，留存购物凭证。"},
    "electronics": {"verdict_en": "Allowed. Electronics with batteries (laptops, cameras) ship via our battery line.", "verdict_zh": "可寄。带电池的电子产品（笔记本、相机）走含电池专线。", "packing_en": "Keep original packaging, retain invoices, and declare the model accurately.", "packing_zh": "保留原包装与发票，如实申报型号。"},
    "books":       {"verdict_en": "Allowed. Books are light cargo; pack tightly to cut volumetric weight.", "verdict_zh": "可寄。书籍属轻货，紧凑打包降低体积重。", "packing_en": "Pack tightly, avoid moisture, and declare antique titles separately.", "packing_zh": "紧凑打包、防潮，古旧书籍单独申报。"},
    "luggage":     {"verdict_en": "Allowed. Student luggage and personal effects are our core route.", "verdict_zh": "可寄。留学生行李与个人物品是我们的核心线路。", "packing_en": "Consolidate boxes, seal and reinforce, and mark personal effects.", "packing_zh": "合箱打包、密封加固，标注个人物品。"},
    "furniture":   {"verdict_en": "Allowed. Large items charge by volumetric weight (L×W×H÷5000); disassemble to save.", "verdict_zh": "可寄。大件按体积重计费（长×宽×高÷5000），拆装更省。", "packing_en": "Disassemble, cushion the corners, and mind volumetric weight.", "packing_zh": "拆装、边角缓冲，注意体积重。"},
}

def get_verdict(region, slug, d):
    if "verdict_en" in d:
        return d
    cv = COMMON_VERDICT.get(slug)
    if cv:
        return cv
    return {"verdict_en": d["faq_q1_en"], "verdict_zh": d["faq_q1_zh"], "packing_en": "", "packing_zh": ""}
