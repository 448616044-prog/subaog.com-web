"""扫描并展示各类短 meta 模式，确认能批量生成的模板"""
import os, re
from collections import defaultdict

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# 中文城市名映射（基于 usa-to-china 子目录名）
# 简化版（实际只用基础 20 个美国城市，因为只有这 20 个有 city×item 子目录）
CITY_ZH = {
    "atlanta": "亚特兰大",
    "boston": "波士顿",
    "chicago": "芝加哥",
    "dallas": "达拉斯",
    "denver": "丹佛",
    "detroit": "底特律",
    "houston": "休斯顿",
    "las-vegas": "拉斯维加斯",
    "los-angeles": "洛杉矶",
    "miami": "迈阿密",
    "minneapolis": "明尼阿波利斯",
    "new-york": "纽约",
    "philadelphia": "费城",
    "phoenix": "凤凰城",
    "portland": "波特兰",
    "san-diego": "圣地亚哥",
    "san-francisco": "旧金山",
    "seattle": "西雅图",
    "tampa": "坦帕",
    "washington": "华盛顿",
}

# 品类中文名 + 通用提示
ITEM_ZH = {
    "furniture": "家具",
    "kitchenware": "厨房用品",
    "electronics": "电子产品",
    "clothing": "服装衣物",
    "cosmetics": "化妆品",
    "tea": "茶叶茶具",
    "books": "书籍",
    "documents": "证件文件",
    "toys": "玩具",
    "shoes": "鞋子",
    "bags": "箱包",
    "laptop": "笔记本电脑",
    "medicine": "药品",
    "milk-powder": "奶粉",
    "art": "艺术品",
    "instruments": "乐器",
    "auto-parts": "汽车配件",
}

# 本地化描述（按城市 + 品类特点短描述，每个城市有几条共享 + 品类微调）
CITY_LOCAL = {
    "atlanta": "亚特兰大是美国东南部物流枢纽，达美航空总部所在地，空运回中国时效稳定；当地华人聚居 Duluth 和 Johns Creek，留学生与新移民寄件高频。",
    "boston": "波士顿是东北部高等教育重镇，哈佛、MIT、波士顿大学等高校留学生密集，每年毕业季行李回国需求集中。",
    "chicago": "芝加哥地处美中，是中西部空运枢纽，O'Hare 机场航线密集直达亚洲；当地华人工程师、华中科技大学校友会等寄件需求稳定。",
    "dallas": "达拉斯是德州新兴华人聚集城市，Plano、Richardson 区域华人社区快速增长，从德州寄中国的个人件、家庭件、商务件需求都在增长。",
    "denver": "丹佛是科罗拉多华人社区中心，丹佛大学、科罗拉多大学留学生和工程师群体是主要的寄件需求来源。",
    "detroit": "底特律是汽车工业重镇，华人工程师与制造业从业者寄件频繁；安大略机场（YQG）邻近多伦多可作为加拿大方向的备选起运地。",
    "houston": "休斯顿是德州第一大华人聚居城市，糖城（Sugar Land）、凯蒂（Katy）是核心华人区，空运回国需求常年旺盛。",
    "las-vegas": "拉斯维加斯华人主要从事酒店、餐饮、博彩行业，从赌城寄中国的礼品、保健品、收藏品需求稳定。",
    "los-angeles": "洛杉矶是美国最大华人聚集城市，圣盖博谷、阿罕布拉、蒙特利公园等华人区寄件密度最高；LAX 国际机场直飞中国航班密集，物流时效优势明显。",
    "miami": "迈阿密是佛州门户城市，邻近加勒比海与拉丁美洲，华人主要从事贸易与旅游；迈阿密国际机场（MIA）直飞中国航线选择丰富。",
    "minneapolis": "明尼阿波利斯是明州双城，3M、Target 等大企业总部所在地；当地华人以工程师、医生为主，从美中寄中国快递服务需求稳定。",
    "new-york": "纽约是美国最大都市，法拉盛、布鲁克林八大道是华人核心聚居区，寄件密度全美最高；JFK 机场直飞中国航班数量全美第一。",
    "philadelphia": "费城是宾州历史名城，特拉华河谷华人社区稳定，新泽西州紧邻，社区寄件与商业件需求持续。",
    "phoenix": "凤凰城是亚利桑那州府，亚省阳光地带华人近年快速增长，Tempe、Chandler 是主要华人区。",
    "portland": "波特兰是俄勒冈州最大城市，木材、电子产业集中，华人工程师与留学群体从美西寄中国件需求稳定。",
    "san-diego": "圣地亚哥紧邻墨西哥边境，圣地亚哥大学、加州大学圣地亚哥分校（UCSD）留学群体是重要寄件来源。",
    "san-francisco": "旧金山湾区是全美华人密度最高的城市之一，硅谷科技公司华人员工密集；SFO 直飞中国航班密集。",
    "seattle": "西雅图是微软、亚马逊总部所在地，太平洋西北地区华人工程师扎堆，波音与科技业寄件需求稳定。",
    "tampa": "坦帕是佛州西海岸城市，当地华人主要从事旅游、医疗、贸易，从佛州寄中国的需求平稳。",
    "washington": "华盛顿特区是政治中心，DC、弗吉尼亚、马里兰华人以政府工作人员、医生、律师为主，华人社区稳定。",
}

# 品类特色（每品类的核心提示）
ITEM_TIPS = {
    "furniture": "家具属大件物品，按体积重计费（长×宽×高÷5000），建议拆解或整装以节省运费；旧家具需如实申报避免关税争议。",
    "kitchenware": "厨房用品含瓷器、刀具属敏感货，需如实申报；玻璃器皿注意包装防碎。",
    "electronics": "电子产品带电池（笔记本、相机、平板）属敏感货，需走含电池专线；建议保留原包装与发票。",
    "clothing": "服装衣物按实重计费，整箱打包最划算；奢侈品类建议单独保价。",
    "cosmetics": "化妆品属敏感货，液体类需密封包装；品牌商品保留购买凭证方便清关。",
    "tea": "茶叶属常规干货，建议真空密封防潮；普洱茶饼需如实申报价值。",
    "books": "书籍属轻货，按体积重计费，建议紧凑打包；古旧书籍建议单独保价。",
    "documents": "证件文件时效要求高，10-15 个工作日上门送达；纸质文件注意防水包装。",
    "toys": "玩具按实重或体积重计费，电子玩具含电池需走敏感货通道。",
    "shoes": "鞋子属轻货，整箱打包节省运费；奢侈鞋款建议单独保价。",
    "bags": "箱包属轻货整装便利；奢侈品类（LV、Chanel）建议保价申报。",
    "laptop": "笔记本电脑含电池属敏感货，建议走含电池专线；保留原包装降低体积重。",
    "medicine": "中西药属敏感货，需处方与成分说明；个人用量在合理范围内可邮寄。",
    "milk-powder": "奶粉按实重计费，整箱打包最划算；建议保留购物小票。",
    "art": "艺术品属贵重物品，建议保价申报并单独包装；古董类需提供来源证明。",
    "instruments": "乐器按体积重计费，吉他、提琴属轻货；钢琴、电子琴属大件。",
    "auto-parts": "汽车配件按实重或体积重计费；油液类需单独处理。",
}

# 短 meta 样本（按城市 × 品类扫描）
base = f"{BASE}/zh-cn/usa-to-china"
short_files = []
for city_dir in sorted(os.listdir(base)):
    city_path = f"{base}/{city_dir}"
    if not os.path.isdir(city_path):
        continue
    for item in os.listdir(city_path):
        idx = f"{city_path}/{item}/index.html"
        if not os.path.isfile(idx):
            continue
        with open(idx, encoding="utf-8") as f:
            t = f.read()
        m = re.search(r'<meta name="description" content="([^"]*)"', t)
        if m and len(m.group(1)) < 80:
            short_files.append((city_dir, item, m.group(1)))

print(f"Total short: {len(short_files)}")
print("\n=== 5 个样本 ===")
for c, i, d in short_files[:5]:
    print(f"\n[{c}/{i}] {len(d)} 字")
    print(f"  现有: {d}")
    # 生成新版本
    city_zh = CITY_ZH.get(c, c)
    item_zh = ITEM_ZH.get(i, i)
    city_local = CITY_LOCAL.get(c, f"{city_zh}是华人聚居城市，空运回国需求稳定。")
    item_tip = ITEM_TIPS.get(i, "建议保留购物凭证方便清关。")
    new_desc = (
        f"从{city_zh}寄{item_zh}回国：可寄（空运专线，税率15%）。{city_local}"
        f"{item_tip}20kg 起运，¥100/kg（20-99kg）/¥90/kg（100kg+），"
        f"全美免费上门取件，10-15 个工作日门到门，双清包税无后顾之忧。"
        f"比 FedEx/UPS 直营便宜 40% 以上。"
    )
    print(f"  新: {len(new_desc)} 字")
    print(f"  -> {new_desc[:200]}...")