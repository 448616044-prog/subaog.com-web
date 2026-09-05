"""修复 zh-cn hub 短 meta + seasia 短 meta + 旧价格违规 ¥70/¥65"""
import os, re

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# 美国城市本地化（精简版，与 city×item 不同，更聚焦城市特点）
USA_HUB_LOCAL = {
    "atlanta": "亚特兰大是美国东南部门户，达美航空总部所在地，空运回中国时效稳定；当地华人聚居 Duluth、Alpharetta，留学生与新移民寄件高频。",
    "austin": "奥斯汀是德州新兴科技城市，德州大学奥斯汀分校、戴尔公司总部所在地，华人工程师与 IT 群体增长迅猛。",
    "boston": "波士顿是东北部高等教育重镇，哈佛、MIT、波士顿大学等高校留学生密集，每年毕业季行李回国需求集中。",
    "chicago": "芝加哥地处美中，是中西部空运枢纽，O'Hare 机场航线密集直达亚洲；当地华人工程师、华中科技大学校友会等寄件需求稳定。",
    "dallas": "达拉斯是德州新兴华人聚集城市，Plano、Richardson 区域华人社区快速增长，从德州寄中国的个人件、家庭件、商务件需求都在增长。",
    "denver": "丹佛是科罗拉多华人社区中心，丹佛大学、科罗拉多大学留学生和工程师群体是主要的寄件需求来源。",
    "detroit": "底特律是汽车工业重镇，华人工程师与制造业从业者寄件频繁；安大略机场邻近多伦多可作为加拿大方向的备选起运地。",
    "houston": "休斯顿是德州第一大华人聚居城市，糖城（Sugar Land）、凯蒂（Katy）是核心华人区，空运回国需求常年旺盛。",
    "las-vegas": "拉斯维加斯华人主要从事酒店、餐饮、博彩行业，从赌城寄中国的礼品、保健品、收藏品需求稳定。",
    "los-angeles": "洛杉矶是美国最大华人聚集城市，圣盖博谷、阿罕布拉、蒙特利公园等华人区寄件密度全美最高；LAX 机场直飞中国航班密集，物流时效优势明显。",
    "miami": "迈阿密是佛州门户城市，邻近加勒比海与拉丁美洲，华人主要从事贸易与旅游；MIA 直飞中国航线选择丰富。",
    "new-york": "纽约是美国最大都市，法拉盛、布鲁克林八大道是华人核心聚居区，寄件密度全美最高；JFK 机场直飞中国航班数量全美第一。",
    "philadelphia": "费城是宾州历史名城，特拉华河谷华人社区稳定，新泽西州紧邻，社区寄件与商业件需求持续。",
    "phoenix": "凤凰城是亚利桑那州府，阳光地带华人近年快速增长，Tempe、Chandler 是主要华人区。",
    "portland": "波特兰是俄勒冈州最大城市，木材、电子产业集中，华人工程师与留学群体从美西寄中国件需求稳定。",
    "san-diego": "圣地亚哥紧邻墨西哥边境，UCSD、SDSU 留学群体是重要寄件来源。",
    "san-francisco": "旧金山湾区是全美华人密度最高的城市之一，硅谷科技公司华人员工密集；SFO 直飞中国航班密集。",
    "san-jose": "圣何塞是硅谷核心城市，苹果、谷歌、Adobe 等大厂华人员工密集，从湾区寄中国的高科技产品和家庭件需求稳定。",
    "seattle": "西雅图是微软、亚马逊总部所在地，太平洋西北地区华人工程师扎堆，波音与科技业寄件需求稳定。",
    "washington-dc": "华盛顿特区是政治中心，DC、弗吉尼亚、马里兰华人以政府工作人员、医生、律师为主，华人社区稳定。",
}

CITY_ZH = {
    "atlanta": "亚特兰大", "austin": "奥斯汀", "boston": "波士顿",
    "chicago": "芝加哥", "dallas": "达拉斯", "denver": "丹佛",
    "detroit": "底特律", "houston": "休斯顿", "las-vegas": "拉斯维加斯",
    "los-angeles": "洛杉矶", "miami": "迈阿密", "new-york": "纽约",
    "philadelphia": "费城", "phoenix": "凤凰城", "portland": "波特兰",
    "san-diego": "圣地亚哥", "san-francisco": "旧金山", "san-jose": "圣何塞",
    "seattle": "西雅图", "washington-dc": "华盛顿特区",
}

USA_SUFFIX = (
    "全美免费上门取件，10-15 个工作日门到门，双清包税无后顾之忧。"
    "比 FedEx/UPS 直营便宜 40% 以上。"
)

# 东南亚 T3 档：¥80/kg（20-99kg）/¥70/kg（100kg+）
SEASIA_LOCAL = {
    "malaysia": "马来西亚寄中国回国专线，新山、槟城、吉隆坡华人聚居城市空运回中国需求稳定。",
    "singapore": "新加坡寄中国回国专线，牛车水、宏茂桥等华人聚居区寄件高频。",
    "thailand": "泰国寄中国专线，华人聚居的曼谷、普吉、清迈寄件需求稳定。",
    "philippines": "菲律宾寄中国专线，马尼拉、宿务华人聚居区寄件需求稳定。",
}

SEASIA_SUFFIX = (
    "空运 ¥80/kg（20-99kg）/¥70/kg（100kg+），10-15 个工作日门到门，"
    "双清包税无后顾之忧。微信一键下单，拆箱合箱全程跟踪。"
)


def build_hub_meta(city_dir, region):
    """构建 hub 页 meta description"""
    if region == "usa-to-china":
        city_zh = CITY_ZH.get(city_dir)
        local = USA_HUB_LOCAL.get(city_dir)
        if not city_zh or not local:
            return None
        head = f"从美国{city_zh}寄中国专线：空运，10-15 个工作日。"
        suffix = USA_SUFFIX
    elif region == "seasia-to-china":
        city_zh = city_dir  # 用目录名
        local = SEASIA_LOCAL.get(city_dir)
        if not local:
            return None
        head = f"{city_zh}寄中国回国行李攻略："
        suffix = SEASIA_SUFFIX
    else:
        return None
    return head + local + suffix


# === 修 USA hub 短 meta ===
usa_base = f"{BASE}/zh-cn/usa-to-china"
fixed_usa = 0
for city_dir in sorted(os.listdir(usa_base)):
    idx = f"{usa_base}/{city_dir}/index.html"
    if not os.path.isfile(idx):
        continue
    new_desc = build_hub_meta(city_dir, "usa-to-china")
    if not new_desc:
        continue
    if len(new_desc) > 165:
        new_desc = new_desc[:162] + "…"
    with open(idx, encoding="utf-8") as f:
        t = f.read()
    m = re.search(r'(<meta name="description" content=")([^"]*)(")', t)
    if not m:
        continue
    cur_desc = m.group(2)
    if len(cur_desc) >= 130:
        continue
    new_t = t.replace(m.group(0), m.group(1) + new_desc + m.group(3), 1)
    with open(idx, "w", encoding="utf-8") as f:
        f.write(new_t)
    fixed_usa += 1

# === 修 SEASIA 短 meta ===
seasia_base = f"{BASE}/zh-cn/seasia-to-china"
fixed_seasia = 0
for entry in sorted(os.listdir(seasia_base)):
    idx = f"{seasia_base}/{entry}/index.html"
    if not os.path.isfile(idx):
        continue
    # 跳过 hub 城市，只修 hub
    new_desc = build_hub_meta(entry, "seasia-to-china")
    if not new_desc:
        continue
    if len(new_desc) > 165:
        new_desc = new_desc[:162] + "…"
    with open(idx, encoding="utf-8") as f:
        t = f.read()
    m = re.search(r'(<meta name="description" content=")([^"]*)(")', t)
    if not m:
        continue
    cur_desc = m.group(2)
    if len(cur_desc) >= 130:
        continue
    new_t = t.replace(m.group(0), m.group(1) + new_desc + m.group(3), 1)
    with open(idx, "w", encoding="utf-8") as f:
        f.write(new_t)
    fixed_seasia += 1

# === 修 seasia pricing 旧价违规 ¥70/¥65 → ¥80/¥70 ===
# 这是一个特殊修复文件（seasia-to-china/pricing/index.html）
pricing_idx = f"{BASE}/zh-cn/seasia-to-china/pricing/index.html"
with open(pricing_idx, encoding="utf-8") as f:
    t = f.read()
# 替换所有 ¥70/kg、¥65/kg 为 ¥80/kg、¥70/kg（按 T3 档映射）
# 旧价：¥80/¥75/¥70/¥65（已废弃）
# 新价：¥100/¥90（美/加/墨/澳/新 T1）/ ¥90/¥80（欧 T2）/ ¥80/¥70（日/韩/泰/新/菲/台/马 T3）
# seasia 是 T3：¥70/kg → ¥80/kg，¥65/kg → ¥70/kg
old_t = t
new_t = t
# 注意：避免连环替换，先一次性把所有 "¥70/kg" 替换为 placeholder，再换
new_t = new_t.replace("100kg+ 65元/kg", "100kg+ ¥70/kg")
new_t = new_t.replace("20kg+ 70元/kg", "20-99kg ¥80/kg")
new_t = new_t.replace("70元/kg", "¥80/kg")
new_t = new_t.replace("65元/kg", "¥70/kg")
# meta description 也重写
fixed_pricing_meta = False
m = re.search(r'(<meta name="description" content=")([^"]*)(")', new_t)
if m:
    desc = m.group(2)
    # 完整重写
    new_desc = (
        "东南亚寄中国回国行李价格全透明：新加坡、马来西亚 20kg+ 起运，"
        "¥80/kg（20-99kg）/¥70/kg（100kg+），10-15 个工作日门到门，"
        "双清包税无后顾之忧。费用估算、计费规则、省钱技巧、免税额度解读，"
        "微信一键下单，拆箱合箱全程跟踪。"
    )
    if len(desc) != len(new_desc) or "65元" in desc or "70元" in desc:
        new_t = new_t.replace(m.group(0), m.group(1) + new_desc + m.group(3), 1)
        fixed_pricing_meta = True

if new_t != old_t:
    with open(pricing_idx, "w", encoding="utf-8") as f:
        f.write(new_t)
    print(f"  pricing/index.html 旧价违规已修复")
print(f"USA hub 修复: {fixed_usa}")
print(f"SEASIA hub 修复: {fixed_seasia}")
print(f"SEASIA pricing 修复: {fixed_pricing_meta}")