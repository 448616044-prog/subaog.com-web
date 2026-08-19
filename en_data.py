# -*- coding: utf-8 -*-
"""
subaog.com 英文站内容数据层
每国线路的数据驱动内容：价格、时效、城市、特色、FAQ。
价格单位：USD/kg（国际用户习惯），后续可校准。
"""

BASE_URL = "https://subaog.com"

# ============ 9 条线路数据 ============
COUNTRIES = {
    "usa-to-china": {
        "name_en": "USA to China",
        "name_zh": "美国寄中国",
        "flag": "🇺🇸",
        "short": "USA",
        "h1": "Ship from the USA to China — Door-to-Door, Tax-Inclusive",
        "subtitle": ("Consolidated shipping from anywhere in the USA to China, with tax-inclusive customs "
                     "clearance and door-to-door delivery in 10–15 working days. Built for students, families "
                     "moving home, and shoppers — 40–60% cheaper than USPS/UPS/FedEx with full tracking."),
        "cities": [
            {"en": "Los Angeles", "zh": "洛杉矶"},
            {"en": "New York", "zh": "纽约"},
            {"en": "San Francisco", "zh": "旧金山"},
            {"en": "Chicago", "zh": "芝加哥"},
            {"en": "Houston", "zh": "休斯顿"},
            {"en": "Boston", "zh": "波士顿"},
            {"en": "Seattle", "zh": "西雅图"},
            {"en": "Dallas", "zh": "达拉斯"},
            {"en": "Miami", "zh": "迈阿密"},
            {"en": "Washington DC", "zh": "华盛顿"},
            {"en": "Atlanta", "zh": "亚特兰大"},
            {"en": "Denver", "zh": "丹佛"},
            {"en": "Phoenix", "zh": "凤凰城"},
            {"en": "San Jose", "zh": "圣何塞"},
            {"en": "San Diego", "zh": "圣地亚哥"},
            {"en": "Portland", "zh": "波特兰"},
            {"en": "Las Vegas", "zh": "拉斯维加斯"},
            {"en": "Austin", "zh": "奥斯汀"},
            {"en": "Philadelphia", "zh": "费城"},
            {"en": "Detroit", "zh": "底特律"},
        ],
        "price_air": "from $10.5/kg (21kg+)",
        "price_sea": "from $6.5/kg (21kg+)",
        "transit": "10–15 working days",
        "features": [
            {"icon": "🛡️", "title": "Tax-inclusive", "desc": "One price covers US pickup, freight, China customs, and final delivery."},
            {"icon": "🚚", "title": "Free US pickup", "desc": "Free doorstep pickup across all 50 states — no need to drop off."},
            {"icon": "📍", "title": "Full tracking", "desc": "Track every leg from US origin to China doorstep."},
            {"icon": "💰", "title": "40–60% cheaper", "desc": "Consolidated channels beat USPS/UPS/FedEx published rates."},
        ],
        "faq": [
            ("How much does it cost to ship from the USA to China?",
             "Air freight starts at about $10.5/kg for shipments over 21kg, and sea freight from $6.5/kg. "
             "Small parcels (under 2kg) cost $15–30 via USPS-style channels. Final price depends on weight, "
             "volume, and item type — request a free quote for an exact figure."),
            ("How long does USA to China shipping take?",
             "Air freight takes 10–15 working days door-to-door. Sea freight takes 25–35 days. During peak "
             "seasons (Christmas, Chinese New Year) add 3–5 days."),
            ("Will I have to pay customs duty in China?",
             "Personal items under RMB 1,000 are duty-free. Used clothing and books are usually not taxed. "
             "Our tax-inclusive service already covers standard duties — you pay one all-in price."),
            ("What can I ship from the USA to China?",
             "Most personal items: clothing, shoes, supplements, cosmetics, electronics, books, baby formula, "
             "and household goods. Prohibited items include weapons, drugs, fresh food, and politically "
             "sensitive publications. Ask us first if you are unsure."),
            ("Is there free pickup in my city?",
             "Yes — we offer free doorstep pickup across the USA. Just tell us your address and preferred "
             "pickup window when you book."),
        ],
    },
    "japan-to-china": {
        "name_en": "Japan to China",
        "name_zh": "日本寄中国",
        "flag": "🇯🇵",
        "short": "Japan",
        "h1": "Ship from Japan to China — Fast, Safe, Tax-Inclusive",
        "subtitle": ("Door-to-door shipping from Japan to China in 7–12 working days. Popular for cosmetics, "
                     "electronics, snacks, and personal effects. Free pickup in major cities, tax-inclusive "
                     "customs, and full tracking."),
        "cities": [
            {"en": "Tokyo", "zh": "东京"},
            {"en": "Osaka", "zh": "大阪"},
            {"en": "Kyoto", "zh": "京都"},
            {"en": "Nagoya", "zh": "名古屋"},
            {"en": "Yokohama", "zh": "横滨"},
            {"en": "Kobe", "zh": "神户"},
            {"en": "Sapporo", "zh": "札幌"},
            {"en": "Fukuoka", "zh": "福冈"},
        ],
        "price_air": "from $9/kg (21kg+)",
        "price_sea": "from $5/kg (21kg+)",
        "transit": "7–12 working days",
        "features": [
            {"icon": "⚡", "title": "7–12 day delivery", "desc": "One of the fastest China-bound routes we run."},
            {"icon": "🛡️", "title": "Tax-inclusive", "desc": "All-in price covering pickup, freight, customs, delivery."},
            {"icon": "🎁", "title": "Cosmetics & electronics", "desc": "Expert handling for Japan's most-shipped categories."},
            {"icon": "🚚", "title": "Free pickup", "desc": "Free pickup across major Japanese cities."},
        ],
        "faq": [
            ("How long does Japan to China shipping take?",
             "Air freight takes 7–12 working days door-to-door. Sea freight takes 18–25 days."),
            ("Can I ship Japanese cosmetics to China?",
             "Yes — cosmetics are one of our most popular categories. Some items (aerosols, large liquid "
             "volumes) need special handling. Send us the item list for a check."),
            ("How much does shipping from Japan to China cost?",
             "Air freight from about $9/kg (21kg+). Small parcels start around $12. Request a free quote for "
             "an exact price."),
            ("Do you offer pickup in Japan?",
             "Yes, free pickup is available in Tokyo, Osaka, Kyoto, Nagoya, Yokohama, Kobe, Sapporo and Fukuoka."),
        ],
    },
    "korea-to-china": {
        "name_en": "Korea to China",
        "name_zh": "韩国寄中国",
        "flag": "🇰🇷",
        "short": "Korea",
        "h1": "Ship from Korea to China — Cosmetics & Fashion Specialist",
        "subtitle": ("Door-to-door shipping from South Korea to China in 7–12 working days. We specialise in "
                     "Korean cosmetics, fashion, and personal effects — with tax-inclusive customs and free "
                     "pickup in major cities."),
        "cities": [
            {"en": "Seoul", "zh": "首尔"},
            {"en": "Busan", "zh": "釜山"},
            {"en": "Incheon", "zh": "仁川"},
            {"en": "Daegu", "zh": "大邱"},
            {"en": "Daejeon", "zh": "大田"},
            {"en": "Gwangju", "zh": "光州"},
        ],
        "price_air": "from $8/kg (21kg+)",
        "price_sea": "from $4.5/kg (21kg+)",
        "transit": "7–12 working days",
        "features": [
            {"icon": "💄", "title": "Cosmetics expert", "desc": "Specialist handling for K-beauty products."},
            {"icon": "⚡", "title": "Fast transit", "desc": "7–12 working days door-to-door."},
            {"icon": "🛡️", "title": "Tax-inclusive", "desc": "One all-in price, no surprise fees."},
            {"icon": "🚚", "title": "Free pickup", "desc": "Free pickup in Seoul, Busan, Incheon and more."},
        ],
        "faq": [
            ("How long does Korea to China shipping take?",
             "Air freight takes 7–12 working days. Sea freight takes 15–22 days."),
            ("Can I ship Korean cosmetics to China?",
             "Yes. Korean cosmetics are a core category for us. We handle the customs paperwork and any "
             "restrictions."),
            ("How much does Korea to China shipping cost?",
             "Air freight from about $8/kg (21kg+). Small parcels start around $10. Request a free quote."),
        ],
    },
    "europe-to-china": {
        "name_en": "Europe to China",
        "name_zh": "欧洲寄中国",
        "flag": "🇪🇺",
        "short": "Europe",
        "h1": "Ship from Europe to China — Door-to-Door, Tax-Inclusive",
        "subtitle": ("Shipping from the UK, Germany, France, Italy, Spain, the Netherlands and Belgium to "
                     "China. Door-to-door delivery in 10–15 working days with tax-inclusive customs clearance."),
        "cities": [
            {"en": "London", "zh": "伦敦"},
            {"en": "Paris", "zh": "巴黎"},
            {"en": "Berlin", "zh": "柏林"},
            {"en": "Rome", "zh": "罗马"},
            {"en": "Milan", "zh": "米兰"},
            {"en": "Madrid", "zh": "马德里"},
            {"en": "Amsterdam", "zh": "阿姆斯特丹"},
            {"en": "Brussels", "zh": "布鲁塞尔"},
        ],
        "price_air": "from $9.5/kg (21kg+)",
        "price_sea": "from $5.5/kg (21kg+)",
        "transit": "10–15 working days",
        "features": [
            {"icon": "🌍", "title": "8+ countries", "desc": "Coverage across Western Europe's major markets."},
            {"icon": "🛡️", "title": "Tax-inclusive", "desc": "All-in price, no surprise customs bills."},
            {"icon": "📦", "title": "Luxury & fashion", "desc": "Expert handling for luxury goods and fashion."},
            {"icon": "🚚", "title": "Free pickup", "desc": "Free pickup in major European cities."},
        ],
        "faq": [
            ("How long does Europe to China shipping take?",
             "Air freight takes 10–15 working days. Sea freight takes 30–40 days."),
            ("Can I ship luxury goods from Europe to China?",
             "Yes. We handle luxury bags, watches and fashion with care — note that luxury items may attract "
             "higher duty. We will advise you before shipping."),
            ("How much does Europe to China shipping cost?",
             "Air freight from about $9.5/kg (21kg+). Sea freight from $5.5/kg. Request a free quote."),
        ],
    },
    "canada-to-china": {
        "name_en": "Canada to China",
        "name_zh": "加拿大寄中国",
        "flag": "🇨🇦",
        "short": "Canada",
        "h1": "Ship from Canada to China — Door-to-Door, Tax-Inclusive",
        "subtitle": ("Shipping from across Canada to China in 10–15 working days. Student luggage, household "
                     "goods and personal effects — with tax-inclusive customs and free pickup in major cities."),
        "cities": [
            {"en": "Toronto", "zh": "多伦多"},
            {"en": "Vancouver", "zh": "温哥华"},
            {"en": "Montreal", "zh": "蒙特利尔"},
            {"en": "Calgary", "zh": "卡尔加里"},
            {"en": "Edmonton", "zh": "埃德蒙顿"},
            {"en": "Ottawa", "zh": "渥太华"},
        ],
        "price_air": "from $10/kg (21kg+)",
        "price_sea": "from $6/kg (21kg+)",
        "transit": "10–15 working days",
        "features": [
            {"icon": "🛡️", "title": "Tax-inclusive", "desc": "One price covers everything, door to door."},
            {"icon": "🚚", "title": "Free pickup", "desc": "Free pickup across Canada's major cities."},
            {"icon": "🎓", "title": "Student specialist", "desc": "Popular with returning students and families."},
            {"icon": "💰", "title": "Cheaper than couriers", "desc": "Save vs. Canada Post / UPS / FedEx rates."},
        ],
        "faq": [
            ("How long does Canada to China shipping take?",
             "Air freight takes 10–15 working days. Sea freight takes 30–40 days."),
            ("How much does Canada to China shipping cost?",
             "Air freight from about $10/kg (21kg+). Sea freight from $6/kg. Request a free quote."),
            ("Can I ship household goods from Canada to China?",
             "Yes — furniture, appliances and household goods are supported. Volume weight applies to large "
             "items."),
        ],
    },
    "australia-to-china": {
        "name_en": "Australia to China",
        "name_zh": "澳洲寄中国",
        "flag": "🇦🇺",
        "short": "Australia",
        "h1": "Ship from Australia to China — Door-to-Door, Tax-Inclusive",
        "subtitle": ("Shipping from Australia to China in 10–15 working days. Popular for supplements, "
                     "baby formula, and personal effects — with tax-inclusive customs and free pickup in "
                     "major cities."),
        "cities": [
            {"en": "Sydney", "zh": "悉尼"},
            {"en": "Melbourne", "zh": "墨尔本"},
            {"en": "Brisbane", "zh": "布里斯班"},
            {"en": "Perth", "zh": "珀斯"},
            {"en": "Adelaide", "zh": "阿德莱德"},
            {"en": "Gold Coast", "zh": "黄金海岸"},
        ],
        "price_air": "from $9.5/kg (21kg+)",
        "price_sea": "from $5.5/kg (21kg+)",
        "transit": "10–15 working days",
        "features": [
            {"icon": "💊", "title": "Supplements expert", "desc": "Specialist handling for vitamins and health products."},
            {"icon": "🍼", "title": "Baby formula", "desc": "One of our most-shipped categories to China."},
            {"icon": "🛡️", "title": "Tax-inclusive", "desc": "All-in price, no surprise fees."},
            {"icon": "🚚", "title": "Free pickup", "desc": "Free pickup in major Australian cities."},
        ],
        "faq": [
            ("How long does Australia to China shipping take?",
             "Air freight takes 10–15 working days. Sea freight takes 25–35 days."),
            ("Can I ship Australian supplements to China?",
             "Yes — supplements and vitamins are a core category. We handle customs documentation and any "
             "restrictions on specific ingredients."),
            ("How much does Australia to China shipping cost?",
             "Air freight from about $9.5/kg (21kg+). Sea freight from $5.5/kg. Request a free quote."),
        ],
    },
    "seasia-to-china": {
        "name_en": "Southeast Asia to China",
        "name_zh": "东南亚寄中国",
        "flag": "🌏",
        "short": "Southeast Asia",
        "h1": "Ship from Singapore & Malaysia to China — Door-to-Door",
        "subtitle": ("Door-to-door shipping from Singapore and Malaysia to China in 7–12 working days. "
                     "Student luggage, moving home, and shopping — with tax-inclusive customs and free pickup."),
        "cities": [],  # 东南亚用 singapore/malaysia 两个国家 + 场景页，由 gen-en-content-2.py 生成
        "price_air": "from $8/kg (21kg+)",
        "price_sea": "from $4.5/kg (21kg+)",
        "transit": "7–12 working days",
        "features": [
            {"icon": "⚡", "title": "Fast transit", "desc": "7–12 working days door-to-door."},
            {"icon": "🎓", "title": "Student specialist", "desc": "Trusted by returning students across SEA."},
            {"icon": "🛡️", "title": "Tax-inclusive", "desc": "One all-in price, no surprise fees."},
            {"icon": "🚚", "title": "Free pickup", "desc": "Free pickup in Singapore and Malaysia."},
        ],
        "faq": [
            ("How long does Southeast Asia to China shipping take?",
             "Air freight takes 7–12 working days. Sea freight takes 12–18 days."),
            ("How much does shipping from Singapore/Malaysia to China cost?",
             "Air freight from about $8/kg (21kg+). Request a free quote for an exact price."),
            ("Do you handle student luggage?",
             "Yes — student luggage is a core service. We offer free boxes and packing guidance for students."),
        ],
    },
    "student-luggage": {
        "name_en": "Student Luggage to China",
        "name_zh": "留学生行李",
        "flag": "🎓",
        "short": "Student Luggage",
        "h1": "Student Luggage Shipping to China — Stress-Free",
        "subtitle": ("Returning home after studying abroad? Ship your books, clothes and personal items back "
                     "to China door-to-door in 10–15 working days. Free boxes, free pickup, and tax-inclusive "
                     "customs."),
        "cities": [],
        "price_air": "from $9/kg (21kg+)",
        "price_sea": "from $5/kg (21kg+)",
        "transit": "10–15 working days",
        "features": [
            {"icon": "📦", "title": "Free boxes", "desc": "We supply free boxes and packing materials."},
            {"icon": "🎓", "title": "Student discounts", "desc": "Special rates during graduation season."},
            {"icon": "🛡️", "title": "Tax-inclusive", "desc": "Used personal items are usually duty-free."},
            {"icon": "🚚", "title": "Free pickup", "desc": "Free pickup from your dorm or apartment."},
        ],
        "faq": [
            ("How much does student luggage shipping cost?",
             "Air freight from about $9/kg (21kg+). Sea freight from $5/kg. Student discounts apply during "
             "graduation season — ask for a quote."),
            ("What can I ship as a student?",
             "Books, clothes, shoes, bedding, small electronics and personal effects. Used personal items are "
             "usually duty-free."),
            ("How long does student luggage take to arrive in China?",
             "Air freight takes 10–15 working days. Sea freight takes 25–35 days."),
        ],
    },
    "usa-moving-to-china": {
        "name_en": "Moving from the USA to China",
        "name_zh": "美国搬家回国",
        "flag": "🏠",
        "short": "USA Moving",
        "h1": "Moving from the USA to China — Furniture & Household Goods",
        "subtitle": ("Moving home? Ship furniture, appliances and household goods from the USA to China "
                     "door-to-door. Sea freight from 25–35 days with tax-inclusive customs and free pickup."),
        "cities": [],
        "price_air": "from $10.5/kg (21kg+)",
        "price_sea": "from $6.5/kg (21kg+)",
        "transit": "Sea 25–35 days",
        "features": [
            {"icon": "🛋️", "title": "Furniture & appliances", "desc": "Large-item handling with care."},
            {"icon": "🚢", "title": "Sea freight", "desc": "Cost-effective for large volume moves."},
            {"icon": "🛡️", "title": "Tax-inclusive", "desc": "Used household goods are usually duty-free."},
            {"icon": "🚚", "title": "Free pickup", "desc": "Free pickup across the USA."},
        ],
        "faq": [
            ("How much does moving from the USA to China cost?",
             "Sea freight from about $6.5/kg (21kg+). Large volume moves get better rates. Request a free "
             "quote with your item list."),
            ("How long does a USA to China move take?",
             "Sea freight takes 25–35 days door-to-door. Air freight (for smaller moves) takes 10–15 days."),
            ("Can I move furniture and appliances?",
             "Yes. We handle furniture, appliances and household goods. Volume weight applies to large items."),
        ],
    },
}

# ============ 美国→中国 城市交叉页（Stage 6） ============
US_CITIES = [
    "New York", "Los Angeles", "San Francisco", "Chicago", "Houston", "Boston",
    "Seattle", "Dallas", "Miami", "Washington DC",
    "Atlanta", "Denver", "Phoenix", "San Jose", "San Diego",
    "Portland", "Las Vegas", "Austin", "Philadelphia", "Detroit",
]
CN_CITIES = [
    "Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu", "Hangzhou",
    "Nanjing", "Wuhan", "Tianjin", "Xiamen",
    "Chongqing", "Suzhou", "Xian", "Qingdao", "Changsha", "Zhengzhou", "Dalian", "Ningbo",
]

# ============ 通用英文文案 ============
COMMON_PROCESS = [
    ("Free consultation", "Tell us what you are shipping and where it is going. We reply within 30 minutes."),
    ("Doorstep pickup", "Book a pickup window — we collect from your address, free of charge."),
    ("International transit", "Air or sea freight with full tracking on every leg."),
    ("Customs & delivery", "We clear China customs and deliver to your door."),
]

COMMON_CAN_SHIP = [
    ("Clothing & shoes", True),
    ("Books & documents", True),
    ("Supplements & vitamins", True),
    ("Cosmetics & skincare", True),
    ("Electronics", True),
    ("Baby formula & food", True),
    ("Household goods", True),
    ("Furniture & appliances", True),
    ("Weapons & ammunition", False),
    ("Drugs & narcotics", False),
    ("Fresh food & meat", False),
    ("Politically sensitive materials", False),
]

# 常见 FAQ（兜底，具体线路覆盖）
COMMON_FAQ = [
    ("Is my shipment tracked?",
     "Yes — every shipment has a tracking number you can follow from pickup to delivery."),
    ("Is the price really all-inclusive?",
     "Yes. Our quoted price includes pickup, freight, China customs clearance, and final delivery. "
     "There are no hidden fees."),
    ("Do you offer insurance?",
     "Yes. Optional insurance is available for high-value items. Ask for coverage details when booking."),
    ("What payment methods do you accept?",
     "We accept major credit cards, PayPal, and bank transfer. Chinese customers can also pay via WeChat "
     "or Alipay."),
]
