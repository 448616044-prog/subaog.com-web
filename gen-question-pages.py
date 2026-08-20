# -*- coding: utf-8 -*-
"""
A: 疑问词独立页 10 个（中英对称）
- 怎么寄 / 多少钱 / 要多久 / 哪个快递好 / 能寄什么
- 需要什么材料 / 怎么查物流 / 丢件怎么办 / 旺季 / 新手
每页：5-6 差异化章节 + 10 FAQ + Article/FAQPage/Person Schema + 作者署名 + 相关服务回链
"""
import json, importlib.util
from pathlib import Path

ROOT = Path("/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com")
DOMAIN = "https://subaog.com"
GA_ID = "G-DJGPMS9MOB"

spec = importlib.util.spec_from_file_location("gec", str(ROOT / "gen-en-content.py"))
gec = importlib.util.module_from_spec(spec); spec.loader.exec_module(gec)
render_page = gec.render_page
faq_html = gec.faq_html
faq_schema = gec.faq_schema
cta_html = gec.cta_html

PERSON_EN = {"@context": "https://schema.org", "@type": "Person",
    "name": "Subao Global Logistics Editorial Team", "jobTitle": "Cross-border Logistics Content Editor",
    "description": "12+ years of international and cross-border shipping experience.",
    "knowsAbout": ["International Shipping", "US-China Logistics", "Customs Clearance"]}
PERSON_ZH = {"@context": "https://schema.org", "@type": "Person",
    "name": "速豹国际物流编辑团队", "jobTitle": "跨境物流内容编辑",
    "description": "12年国际及跨境物流经验",
    "knowsAbout": ["国际物流", "中美物流", "关税清关"]}

QUESTIONS = [
{
 "slug": "how-to-ship-from-usa-to-china",
 "zh_title": "美国寄中国怎么寄？2026 完整流程 6 步搞定",
 "zh_desc": "美国寄中国完整流程：从打包、取件、运输到清关派送 6 个步骤，新手也能看懂。美国寄东西回国怎么操作 | 速豹回国物流",
 "en_title": "How to Ship from the USA to China: 6-Step Process (2026) | Subao Global",
 "en_desc": "How to ship from the USA to China in 6 steps: packing, pickup, transit, customs, delivery. A beginner-friendly guide.",
 "zh_h1": "美国寄中国怎么寄？6 步流程",
 "en_h1": "How to Ship from the USA to China (6 Steps)",
 "zh_sections": [
   ("第 1 步：确认能不能寄",
    "先确认物品类型：普货（衣物/书籍/日用品）随时可寄；敏感货（保健品/化妆品/奶粉/电子产品）走专线；禁运品（武器/毒品/新鲜肉类）不能寄。不确定就问客服，30 分钟回复。"),
   ("第 2 步：打包",
    "纸箱选加硬邮政箱（60×40×50 最佳）；衣物真空压缩省体积重；易碎品气泡膜+填充；液体密封防漏。打包好坏直接影响运费（省 20-40%）和破损率。"),
   ("第 3 步：约上门取件",
    "全美免费上门取件（我们覆盖 20 个华人城市 + 全美上门）。预约时间，快递员上门取走，无需自送网点。"),
   ("第 4 步：运输",
    "空运 7-10 工作日 / 海运 25-35 天 / 国际快递 2-6 天。行李 21kg+ 空运最优（¥70-80/kg 双清包税）。全程可追踪。"),
   ("第 5 步：清关",
    "我们走双清包税渠道：中国海关申报、关税缴纳全部代办，收件人零操作。个人物品申报合规即可。"),
   ("第 6 步：派送上门",
    "清关完成后国内快递派送上门，覆盖中国大陆主要城市，一线城市最快。全程一个单号查到底。"),
 ],
 "zh_faq": [
   ("美国寄中国流程复杂吗？", "不复杂。打包→预约取件→我们负责运输/清关/派送，收件人只要在家收货。全程 6 步。"),
   ("美国寄中国怎么收费？", "按实重和体积重取大者计费，空运 ¥70-80/kg（21kg+）双清包税，100kg+ 更优惠。"),
   ("美国寄中国要多久？", "空运 7-10 工作日，海运 25-35 天，国际快递 2-6 天。"),
   ("第一次寄要注意什么？", "① 确认物品可寄 ② 真空压缩省体积 ③ 如实申报 ④ 高价值买保险。"),
   ("寄件需要提供什么？", "收件人姓名/电话/地址 + 身份证（清关申报用，加密处理）。"),
   ("怎么追踪物流？", "全程单号可查，从美国取件到中国派送每一步都有记录。"),
   ("美国寄中国能寄食品吗？", "包装食品（零食/茶叶/保健品）可寄，新鲜肉类/水果/种子禁运。"),
   ("会不会被税？", "双清包税渠道已含关税。个人物品申报合规无额外费用。"),
   ("寄丢了怎么办？", "可选保险按保价赔。基础保险覆盖常规运输风险。"),
   ("中国哪些城市能到？", "大陆主要城市全覆盖，门到门派送，一线城市最快。"),
 ],
 "en_sections": [
   ("Step 1: Check if it can ship",
    "Confirm the item type: regular goods (clothing/books/daily items) ship anytime; sensitive goods (supplements/cosmetics/formula/electronics) use dedicated lines; prohibited items (weapons/drugs/fresh meat) can't ship. Not sure? Ask us — 30-minute response."),
   ("Step 2: Pack",
    "Use sturdy postal cartons (60×40×50cm works best); vacuum-compress clothing to save volumetric weight; bubble-wrap fragile items; seal liquids. Packing quality directly affects cost (save 20–40%) and damage rates."),
   ("Step 3: Book free pickup",
    "Free doorstep pickup across the USA (we cover 20+ Chinese communities plus nationwide pickup). Schedule a window; the courier collects from your door."),
   ("Step 4: Transit",
    "Air 7–10 working days / sea 25–35 days / express 2–6 days. Luggage over 21kg is best by air (¥70–80/kg tax-inclusive). Fully trackable."),
   ("Step 5: Customs",
    "We use double-clearance, tax-inclusive channels: China customs declaration and duty are handled for you — the recipient does nothing."),
   ("Step 6: Door delivery",
    "After clearance, domestic couriers deliver to your door across mainland China; first-tier cities are fastest. One tracking number from pickup to delivery."),
 ],
 "en_faq": [
   ("Is shipping from the USA to China complicated?", "No. Pack → book pickup → we handle transit/customs/delivery; the recipient just receives the parcel. 6 steps total."),
   ("How is shipping charged?", "The larger of actual or volumetric weight; air ¥70–80/kg (21kg+) tax-inclusive; better at 100kg+."),
   ("How long does it take?", "Air 7–10 working days; sea 25–35 days; express 2–6 days."),
   ("First-time shipping tips?", "1) Confirm the item ships 2) Vacuum-compress to save volume 3) Declare honestly 4) Insure high-value items."),
   ("What do I need to provide?", "Recipient name/phone/address + ID (for customs; handled securely)."),
   ("How do I track?", "One tracking number from US pickup to China delivery."),
   ("Can I ship food?", "Packaged food (snacks/tea/supplements) yes; fresh meat/fruit/seeds no."),
   ("Will it be taxed?", "Tax-inclusive channels cover duty. Compliant personal items pay nothing extra."),
   ("What if it's lost?", "Optional insurance pays per insured value. Basic coverage handles standard risk."),
   ("Which Chinese cities?", "All major mainland cities, door-to-door; first-tier cities fastest."),
 ],
},
{
 "slug": "usa-to-china-shipping-cost",
 "zh_title": "美国寄中国多少钱？2026 价格表与省钱技巧",
 "zh_desc": "美国寄中国运费全解：空运/海运/快递价格表（¥70-80/kg 起）、体积重怎么算、5 个省钱技巧、附加费明细 | 速豹回国物流",
 "en_title": "How Much Does It Cost to Ship from the USA to China? (2026) | Subao Global",
 "en_desc": "US to China shipping cost breakdown: air/sea/express rates, volumetric weight, 5 money-saving tips, and surcharges explained.",
 "zh_h1": "美国寄中国多少钱？",
 "en_h1": "How Much Does It Cost to Ship from the USA to China?",
 "zh_sections": [
   ("价格表（2026 行李专线）",
    "空运专线（双清包税）：21kg+ ¥80/kg（美国档）、75/kg（欧洲档）、70/kg（亚档）；100kg+ 每档再降 ¥5。海运：¥45/kg 左右。国际快递（FedEx/DHL）：$29-97/磅，贵 3-5 倍。"),
   ("体积重是隐形费用",
    "运费 = 实重 和 体积重（长×宽×高 cm ÷ 5000）取大者。一件 60×40×50cm 的箱子 = 24kg 体积重——塞满、真空压缩能避免白付钱。"),
   ("附加费明细",
    "① 申报手续费 ¥100/单（清关固定成本）② 单件 >25kg 或单边 >120cm 收超规附加费 ③ 偏远取件 $30 起 ④ 保险费（货值 3%，建议高价值买）。"),
   ("5 个省钱技巧",
    "① 合箱发（几件并一箱，省首重）② 真空压缩衣物 ③ 21kg+ 走专线（单价最优）④ 错峰（避开毕业季/年末）⑤ 提前 1 个月预约锁价。"),
   ("对比：直邮 vs 专线 vs 快递",
    "USPS 直邮：1 磅 $29.9 但 15 天；华人专线：$11/kg 起（5kg+ 就划算）；FedEx：5 磅 $93。30kg 行李：FedEx $600+ vs 专线 $150-200。"),
 ],
 "zh_faq": [
   ("美国寄中国一公斤多少钱？", "空运专线 ¥70-80/kg（21kg+，双清包税），100kg+ 降至 ¥65-75/kg。"),
   ("美国寄中国最小多少起寄？", "专线一般 21kg 起最划算，小件（<5kg）也可寄但单价较高。"),
   ("体积重怎么算？", "长×宽×高(cm)÷5000，与实重取大者。塞满箱子+真空压缩可避免浪费。"),
   ("运费包含关税吗？", "双清包税渠道含基础关税，另有 ¥100/单申报手续费。"),
   ("为什么 FedEx 那么贵？", "商业清关+单件运输+高利润，30kg 行李 $600+。专线合箱+邮政清关成本结构不同。"),
   ("运费什么时候最便宜？", "非旺季（3-4 月/9-10 月）+ 100kg+ 大货最便宜。"),
   ("寄 30kg 行李要多少钱？", "专线约 $150-200 全包（含税含派送），FedEx 约 $600+。"),
   ("有隐藏费用吗？", "正规渠道无隐藏费。专线一口价：取件+运费+清关+派送全含。"),
   ("运费能便宜到多少？", "海运大货可到 ¥45/kg 以下，但时效 25-35 天。"),
   ("价格和什么有关？", "重量、体积、出发国、渠道（空/海/快递）、是否旺季。30 分钟报价。"),
 ],
 "en_sections": [
   ("2026 rate card (luggage line)",
    "Air (tax-inclusive): 21kg+ $11/kg (US tier), $10.5/kg (Europe tier), $9.5/kg (Asia tier); 100kg+ drops $0.5-0.6/kg per tier. Sea: ~¥45/kg. Express (FedEx/DHL): $29–97 per parcel — 3–5x pricier."),
   ("Volumetric weight is the hidden cost",
    "Cost = the larger of actual weight or volumetric (L×W×H cm ÷ 5000). A 60×40×50cm box = 24kg volumetric. Fill the box, vacuum-compress, and you won't pay for air."),
   ("Surcharges explained",
    "1) ¥100/shipment declaration fee (customs fixed cost). 2) Oversize surcharge for single pieces >25kg or one side >120cm. 3) Remote pickup $30+. 4) Insurance (~3% of value, recommended for high-value)."),
   ("5 money-saving tips",
    "1) Consolidate multiple orders (save first-weight). 2) Vacuum-compress clothing. 3) Ship 21kg+ on dedicated lines (best per-kg). 4) Ship off-peak (avoid graduation/year-end). 5) Book a month ahead to lock rates."),
   ("Direct vs line vs express",
    "USPS direct: 1lb $29.9 but 15 days; Chinese line: $11/kg from 5kg+; FedEx: 5lb $93. For 30kg luggage: FedEx $600+ vs line $150–200."),
 ],
 "en_faq": [
   ("How much per kg to China from the USA?", "Air line ¥70–80/kg (21kg+, tax-inclusive); ¥65–75/kg at 100kg+."),
   ("What's the minimum shipment?", "21kg+ is the sweet spot; smaller parcels (<5kg) ship but at higher per-kg."),
   ("How is volumetric weight calculated?", "L×W×H (cm) ÷ 5000, charged on the larger of actual/volumetric. Pack tight to avoid paying for air."),
   ("Does the rate include duty?", "Tax-inclusive channels cover base duty; add ¥100/shipment declaration fee."),
   ("Why is FedEx so expensive?", "Commercial clearance + single-piece transit + margin: 30kg luggage $600+. Lines consolidate and use postal clearance."),
   ("When is shipping cheapest?", "Off-peak (Mar-Apr/Sep-Oct) + 100kg+ volume."),
   ("How much for 30kg luggage?", "≈$150–200 all-in via line; $600+ via FedEx."),
   ("Are there hidden fees?", "Reputable lines quote all-in: pickup + freight + customs + delivery."),
   ("How low can shipping go?", "Sea freight for large volumes drops below ¥45/kg, but takes 25–35 days."),
   ("What drives the price?", "Weight, volume, origin, channel (air/sea/express), and season. 30-minute quotes."),
 ],
},
{
 "slug": "usa-to-china-shipping-time",
 "zh_title": "美国寄中国要多久？2026 时效全解析",
 "zh_desc": "美国寄中国时效全解：空运 7-10 天、海运 25-35 天、国际快递 2-6 天，各渠道对比 + 影响时效的因素（清关/旺季/口岸）| 速豹回国物流",
 "en_title": "How Long Does Shipping from the USA to China Take? (2026) | Subao Global",
 "en_desc": "USA to China transit times: air 7-10 days, sea 25-35 days, express 2-6 days. Plus what affects timing (customs, peak season, port).",
 "zh_h1": "美国寄中国要多久？",
 "en_h1": "How Long Does Shipping from the USA to China Take?",
 "zh_sections": [
   ("各渠道时效对比",
    "国际快递（FedEx/DHL/UPS）：2-6 天，最快最贵。空运专线：7-10 工作日门到门，性价比最优。海运：25-35 天，大件/搬家最省。USPS First Class：约 15 天（小件）。"),
   ("时效组成拆解",
    "全程 = 取件（1-2 天）+ 干线运输（空运 3-5 天/海运 15-25 天）+ 清关（1-3 天）+ 国内派送（1-2 天）。空运 7-10 天是常态，不是承诺下限。"),
   ("影响时效的 4 个因素",
    "① 旺季（毕业季 5-7 月/年末 11-12 月）爆仓+3-5 天 ② 口岸（北上广深最快）③ 敏感货清关多 1-2 天 ④ 偏远地区派送 +1-2 天。"),
   ("怎么寄最快",
    "赶时间：选空运专线（7-10 天）而非海运；避开周五取件（周末不飞）；提前 1 天约取件；敏感货单独走（不拖累普货清关）。"),
   ("什么时候该海运",
    "不赶时间（搬家/大件/批量）海运省 40%；提前 1 个月寄，行李先到仓免费存 30 天再发货。"),
 ],
 "zh_faq": [
   ("美国寄中国空运要多久？", "7-10 个工作日门到门（含清关+派送）。"),
   ("美国寄中国海运要多久？", "25-35 天。美西 25 天左右，美东 30-35 天。"),
   ("FedEx 寄中国几天？", "3-6 天，最快但贵（30kg $600+）。"),
   ("什么时候寄最快？", "避开旺季（毕业季/年末），选空运专线，周一-周四取件。"),
   ("清关要多久？", "普货 1-2 天，敏感货 2-3 天。我们双清包税代办。"),
   ("旺季会慢多久？", "毕业季/年末爆仓，通常 +3-5 天，建议提前 2-3 周寄。"),
   ("USPS 寄中国多久？", "First Class 约 15 天，Priority 约 8 天。"),
   ("海运和空运怎么选？", "急（<2 周）→ 空运；不急/大件 → 海运省 40%。"),
   ("怎么查物流进度？", "全程单号可查：取件→运输→清关→派送每一步都有记录。"),
   ("最快要几天？", "国际快递 2-3 天（DHL），但 30kg 行李建议空运专线 7-10 天性价比最优。"),
 ],
 "en_sections": [
   ("Transit times by channel",
    "Express (FedEx/DHL/UPS): 2–6 days, fastest and priciest. Air line: 7–10 working days door-to-door, best value. Sea: 25–35 days, cheapest for large/moving. USPS First Class: ~15 days (small parcels)."),
   ("Where does the time go?",
    "Total = pickup (1–2 days) + transit (air 3–5 / sea 15–25 days) + customs (1–3 days) + domestic delivery (1–2 days). Air 7–10 days is typical, not a floor."),
   ("4 factors that affect timing",
    "1) Peak season (graduation May-Jul / year-end Nov-Dec) adds 3–5 days. 2) Port (first-tier cities fastest). 3) Sensitive goods add 1–2 days in customs. 4) Remote areas add 1–2 days."),
   ("How to ship fastest",
    "Choose the air line (7–10 days) not sea; avoid Friday pickups (no weekend flights); book a day ahead; ship sensitive goods separately (don't slow the regular parcel's clearance)."),
   ("When to go by sea",
    "Not urgent (moving/large/volume)? Sea saves 40%; ship a month early and store free for 30 days at the warehouse."),
 ],
 "en_faq": [
   ("How long does air take to China?", "7–10 working days door-to-door (incl. customs + delivery)."),
   ("How long does sea take?", "25–35 days. West coast ~25, east coast 30–35."),
   ("How long does FedEx take?", "3–6 days — fastest but pricey (30kg $600+)."),
   ("When is shipping fastest?", "Off-peak, air line, Mon-Thu pickup."),
   ("How long does customs take?", "Regular goods 1–2 days; sensitive 2–3. We handle it tax-inclusive."),
   ("How much slower in peak season?", "Graduation/year-end queues add 3–5 days; ship 2–3 weeks early."),
   ("How long does USPS take?", "First Class ~15 days; Priority ~8."),
   ("Sea or air?", "Urgent (<2 weeks) → air; not urgent/large → sea (save 40%)."),
   ("How do I track?", "One number covers pickup → transit → customs → delivery."),
   ("Fastest possible?", "Express 2–3 days (DHL); but for 30kg luggage the air line's 7–10 days is the value choice."),
 ],
},
{
 "slug": "best-courier-for-china-shipping",
 "zh_title": "美国寄中国哪个快递好？2026 渠道推荐",
 "zh_desc": "美国寄中国选哪个渠道？USPS/FedEx/DHL/UPS/华人快递 5 渠道实测对比 + 按场景推荐（行李/搬家/代购/急件），附决策建议 | 速豹回国物流",
 "en_title": "Which Courier Is Best for Shipping to China from the USA? (2026) | Subao Global",
 "en_desc": "Which courier is best for USA to China: USPS/FedEx/DHL/UPS/Chinese courier compared by scenario (luggage/moving/daigou/urgent) with recommendations.",
 "zh_h1": "美国寄中国哪个快递好？",
 "en_h1": "Which Courier Is Best for Shipping to China?",
 "zh_sections": [
   ("5 大渠道速览",
    "① 华人专线（我们）：¥70-80/kg 双清包税、7-10 天、行李搬家最优。② FedEx：3-6 天、贵 3-5 倍、急件/文件。③ DHL：2-5 天、最快、贵。④ USPS：小件便宜（1 磅 $29.9）但慢（15 天）。⑤ UPS：3-6 天、类似 FedEx。"),
   ("按场景推荐",
    "行李/搬家 → 华人专线（30kg $150 vs FedEx $600）；代购批量 → 华人专线（省 40-60%）；急件/合同 → DHL/FedEx；高价值小件 → FedEx+保险；敏感货（化妆品/保健品）→ 华人专线。"),
   ("三个不要踩的坑",
    "① 小件别用 FedEx（1 磅 $66 vs USPS $30）；② 大件别用 USPS（30 磅 $200+ vs 专线 $150）；③ 敏感货别混普货（整箱被查）。"),
   ("怎么选（3 个问题）",
    "多重？>5kg → 华人专线。多急？>3 天可等 → 华人专线。什么货？敏感货 → 华人专线。3 个选华人就对了。"),
   ("我们的推荐",
    "综合性价比，21kg+ 行李/搬家/代购首选华人专线（双清包税门到门 $11/kg 起）。急件才用国际快递。"),
 ],
 "zh_faq": [
   ("美国寄中国用什么快递好？", "行李/搬家/代购用华人专线（省 40-60%），急件/文件用 FedEx/DHL。"),
   ("FedEx 和 DHL 哪个好？", "DHL 更快（2-5 天），FedEx 略便宜。都贵（30kg $600+）。"),
   ("USPS 寄中国划算吗？", "小件（<4磅）划算（$29.9），大件不划算（30磅 $200+）。"),
   ("华人快递安全吗？", "正规集运有仓库实拍+全程追踪+保险。选成立久、赔付清晰的。"),
   ("寄行李哪个渠道好？", "华人专线：30kg $150-200 全包双清包税，FedEx 同重量 $600+。"),
   ("寄文件用什么？", "DHL/FedEx 有保证时效和追踪，文件建议国际快递。"),
   ("代购用什么快递？", "天天发货必须华人渠道，成本省一半以上。"),
   ("寄保健品用什么？", "敏感货专线（华人），清关成功率高，别混普货。"),
   ("哪个最快？", "DHL 2-5 天最快。"),
   ("哪个最便宜？", "21kg+ 华人专线最便宜（¥70-80/kg 双清包税）。"),
 ],
 "en_sections": [
   ("5 channels at a glance",
    "1) Chinese line (ours): ¥70–80/kg tax-inclusive, 7–10 days, best for luggage/moving. 2) FedEx: 3–6 days, 3–5x pricier, urgent/docs. 3) DHL: 2–5 days, fastest, pricey. 4) USPS: cheap small parcels (1lb $29.9) but slow (15 days). 5) UPS: 3–6 days, like FedEx."),
   ("Recommendation by scenario",
    "Luggage/moving → Chinese line (30kg $150 vs FedEx $600); daigou volume → Chinese line (save 40–60%); urgent contracts → DHL/FedEx; high-value small → FedEx + insurance; sensitive goods → Chinese dedicated line."),
   ("3 traps to avoid",
    "1) Don't use FedEx for small parcels (1lb $66 vs USPS $30). 2) Don't use USPS for large (30lb $200+ vs line $150). 3) Don't mix sensitive goods with regular (whole box inspected)."),
   ("How to choose (3 questions)",
    "How heavy? >5kg → Chinese line. How urgent? Can wait >3 days → Chinese line. What item? Sensitive → Chinese line. Three 'Chinese' answers and you're done."),
   ("Our recommendation",
    "For value, 21kg+ luggage/moving/daigou → Chinese line (tax-inclusive door-to-door from $11/kg). Express only for true urgency."),
 ],
 "en_faq": [
   ("Which courier is best for the USA to China?", "Luggage/moving/daigou → Chinese line (save 40–60%); urgent/docs → FedEx/DHL."),
   ("FedEx or DHL?", "DHL faster (2–5 days); FedEx slightly cheaper. Both pricey (30kg $600+)."),
   ("Is USPS worth it?", "Small (<4lb) yes ($29.9); large no (30lb $200+)."),
   ("Is the Chinese courier safe?", "Reputable consolidators offer warehouse footage, tracking, insurance. Pick established with clear claims."),
   ("Best for luggage?", "Chinese line: 30kg $150–200 all-in tax-inclusive vs FedEx $600+."),
   ("Best for documents?", "DHL/FedEx — guaranteed speed and tracking."),
   ("Best for daigou?", "Daily volume must use Chinese lines — half the cost or less."),
   ("Best for supplements?", "Sensitive-goods line (Chinese), high clearance success; don't mix with regular."),
   ("Fastest?", "DHL 2–5 days."),
   ("Cheapest?", "21kg+ Chinese line (¥70–80/kg tax-inclusive)."),
 ],
},
{
 "slug": "what-can-i-ship-to-china",
 "zh_title": "美国寄中国能寄什么？2026 品类总览",
 "zh_desc": "美国寄中国能寄什么？普货/敏感货/禁运品三大类总览：衣物书籍随时寄、保健品化妆品走专线、武器毒品不能寄。附完整可寄清单 | 速豹回国物流",
 "en_title": "What Can I Ship to China from the USA? (2026 Full List) | Subao Global",
 "en_desc": "What can ship from the USA to China: regular goods, sensitive goods (dedicated lines), and prohibited items. Full allowed list with category guidance.",
 "zh_h1": "美国寄中国能寄什么？",
 "en_h1": "What Can I Ship to China?",
 "zh_sections": [
   ("普货（随时可寄）",
    "衣物鞋帽、书籍文件、日用品、厨房用品、床上用品、体育用品（非电动）、办公文具。普货走标准专线，最快最省。"),
   ("敏感货（走专线）",
    "保健品/维生素、化妆品/护肤品、奶粉/婴儿食品、电子产品（含电池）、奢侈品/名牌包、食品（零食/茶叶）、药品（个人用药）。敏感货走专线，双清包税，清关成功率 98%+。"),
   ("禁运品（不能寄）",
    "武器弹药、毒品/麻醉品、易燃易爆品、新鲜肉类/海鲜/水果、种子/植物、假币/违禁出版物、枪支玩具。寄了会被扣/退运/罚款。"),
   ("限制类（需确认）",
    "酒类（限量+特定渠道）、烟草（严格限制）、宠物食品（含肉成分需确认）、医疗设备（需自用证明）、古董/文物（需许可）。"),
   ("怎么确认能不能寄",
    "不确定就问客服：发物品名称+数量，30 分钟回复。别自己试——违规物品被扣损失更大。"),
 ],
 "zh_faq": [
   ("美国寄中国能寄保健品吗？", "能，走敏感货专线，双清包税，清关成功率 98%+。"),
   ("能寄化妆品吗？", "能，走敏感货专线。液体需密封打包。"),
   ("能寄奶粉吗？", "能，限个人自用合理数量，走专线。"),
   ("能寄电子产品吗？", "能，含电池产品走敏感货专线（电池单独申报）。"),
   ("能寄食品吗？", "包装食品可寄（零食/茶叶/糖果），新鲜肉类/水果禁运。"),
   ("能寄药品吗？", "个人自用药品可寄（需申报），处方药需处方或说明。"),
   ("什么绝对不能寄？", "武器、毒品、易燃品、新鲜肉类、种子、假币、违禁出版物。"),
   ("能寄家具吗？", "能，海运大件渠道，注意体积重。"),
   ("能寄书吗？", "能，普货随时寄，重书分箱避免超重。"),
   ("不确定能不能寄怎么办？", "问客服，发物品名称+数量，30 分钟确认。"),
 ],
 "en_sections": [
   ("Regular goods (ship anytime)",
    "Clothing, shoes, books, documents, daily items, kitchenware, bedding, sports gear (non-electric), office supplies. These go on the standard line — fastest and cheapest."),
   ("Sensitive goods (dedicated line)",
    "Supplements/vitamins, cosmetics/skincare, baby formula, electronics (incl. batteries), luxury bags, packaged food, personal medicine. These need the sensitive-goods line, tax-inclusive, 98%+ clearance."),
   ("Prohibited (can't ship)",
    "Weapons, drugs/narcotics, flammable goods, fresh meat/seafood/fruit, seeds/plants, counterfeit currency, prohibited publications, gun-shaped toys. Shipping these risks seizure, return, or fines."),
   ("Restricted (check first)",
    "Alcohol (limited + specific channel), tobacco (strict), pet food with meat (confirm), medical devices (self-use proof), antiques (permit)."),
   ("How to confirm",
    "Not sure? Ask us — send the item name + quantity and get an answer in 30 minutes. Don't self-test: seized items cost more than the answer."),
 ],
 "en_faq": [
   ("Can I ship supplements?", "Yes, via the sensitive-goods line, tax-inclusive, 98%+ clearance."),
   ("Can I ship cosmetics?", "Yes, sensitive-goods line. Seal liquids properly."),
   ("Can I ship baby formula?", "Yes, reasonable personal quantity, dedicated line."),
   ("Can I ship electronics?", "Yes; battery items go on the sensitive line (battery declared separately)."),
   ("Can I ship food?", "Packaged food yes (snacks/tea/candy); fresh meat/fruit no."),
   ("Can I ship medicine?", "Personal-use medicine yes (declared); prescriptions need a note."),
   ("What's absolutely prohibited?", "Weapons, drugs, flammables, fresh meat, seeds, counterfeit, prohibited publications."),
   ("Can I ship furniture?", "Yes, via sea freight for large items; mind volumetric weight."),
   ("Can I ship books?", "Yes, regular goods; split heavy boxes."),
   ("Unsure about an item?", "Ask us — item name + quantity, 30-minute answer."),
 ],
},
{
 "slug": "usa-to-china-required-documents",
 "zh_title": "美国寄中国需要什么材料？2026 清关文件清单",
 "zh_desc": "美国寄中国清关需要哪些材料？收件人身份证、物品清单、申报单、个人自用证明——完整清单 + 双清包税渠道零材料操作说明 | 速豹回国物流",
 "en_title": "Documents Needed to Ship from the USA to China (2026) | Subao Global",
 "en_desc": "What documents are needed for USA to China shipping: recipient ID, item list, declaration, self-use proof — plus how tax-inclusive lines need zero documents.",
 "zh_h1": "美国寄中国需要什么材料？",
 "en_h1": "Documents Needed for USA to China Shipping",
 "zh_sections": [
   ("基础材料（必填）",
    "① 收件人姓名+电话+详细地址（中国大陆）② 物品清单（品名+数量+价值）③ 收件人身份证正反面照片（清关申报用，我们加密处理）。"),
   ("双清包税渠道：几乎零材料",
    "走我们双清包税渠道：只需收件人三要素（姓名/电话/地址）+ 简要物品描述。清关、申报、关税全部代办，不用护照/不用发票/不用税号。"),
   ("自主清关材料（如果自己清关）",
    "本人回国自主清关需：护照+签证、机票行程单、机场领取的行李申报单、个人自用证明。可享 ¥5000 行李免税额度。"),
   ("特殊物品材料",
    "品牌奢侈品：购买凭证（防知产纠纷）；处方药：处方或医生说明；医疗设备：自用证明；木材家具：熏蒸证明（整木）。"),
   ("材料安全说明",
    "身份证等敏感材料仅用于海关申报，加密存储、用完即删。正规渠道不会索要多余材料（警惕要护照原件/银行卡的骗子）。"),
 ],
 "zh_faq": [
   ("美国寄中国要身份证吗？", "走个人行邮清关需要收件人身份证照片（申报用），双清包税渠道也要（部分口岸）。正规公司加密处理。"),
   ("要发票吗？", "双清包税渠道不需要发票。自主清关/高价值物品建议保留。"),
   ("要护照吗？", "双清包税不用护照。自主清关需要本人护照+签证。"),
   ("要税号吗？", "个人物品不需要税号（公司货需要）。"),
   ("物品清单怎么写？", "品名写清楚（维生素/衣物/电子产品），数量如实，价值按实际（别瞒报）。"),
   ("没有身份证怎么办？", "用收件人本人身份证，或直系亲属代收（需说明关系）。"),
   ("敏感货要什么材料？", "处方药要处方；品牌包要购买凭证；医疗设备要自用说明。"),
   ("留学生行李要什么材料？", "自主清关：护照+申报单；包清关：三要素+物品描述。"),
   ("材料会被泄露吗？", "正规公司加密存储。警惕索要护照原件/银行卡的不法渠道。"),
   ("公司货要什么？", "营业执照副本、报关委托书、发票/合同（走贸易渠道）。"),
 ],
 "en_sections": [
   ("Basic documents (required)",
    "1) Recipient name + phone + full address (mainland China). 2) Item list (name + quantity + value). 3) Recipient ID photos (for customs declaration; handled securely)."),
   ("Tax-inclusive line: near zero documents",
    "On our double-clearance line you only need recipient details (name/phone/address) + a brief item description. Customs, declaration and duty are handled for you — no passport, no invoice, no tax number."),
   ("Self-clearance documents (if you clear yourself)",
    "Returning yourself? You'll need passport + visa, flight itinerary, baggage declaration form from the airport, and a self-use statement. You get a ¥5,000 luggage allowance."),
   ("Special items",
    "Branded luxury: purchase receipts (IP protection); prescriptions: prescription/doctor's note; medical devices: self-use statement; solid wood furniture: fumigation certificate."),
   ("Document security",
    "Sensitive documents are used only for customs, encrypted in storage, and deleted after use. Legitimate channels never ask for passport originals or bank cards."),
 ],
 "en_faq": [
   ("Do I need an ID?", "Personal parcels need recipient ID photos for declaration (also on tax-inclusive lines at some ports). Reputable companies handle this securely."),
   ("Do I need an invoice?", "Not on tax-inclusive lines. Keep receipts for self-clearance/high-value."),
   ("Do I need a passport?", "Not for tax-inclusive lines. Self-clearance needs your passport + visa."),
   ("Do I need a tax number?", "Not for personal items (corporate shipments do)."),
   ("How to write the item list?", "Clear names (vitamins/clothing/electronics), honest quantities, actual value (don't under-declare)."),
   ("No ID available?", "Use the recipient's own ID, or a family member as receiver (state the relationship)."),
   ("What for sensitive goods?", "Prescription for meds; purchase receipts for branded bags; self-use note for medical devices."),
   ("What for student luggage?", "Self-clearance: passport + declaration form; agent clearance: three details + item description."),
   ("Are documents safe?", "Reputable companies encrypt storage. Beware of channels asking for passport originals/bank cards."),
   ("What for corporate shipments?", "Business license copy, customs power of attorney, invoice/contract (trade channel)."),
 ],
},
{
 "slug": "usa-to-china-tracking",
 "zh_title": "美国寄中国怎么查物流？2026 追踪指南",
 "zh_desc": "美国寄中国物流怎么查？全程单号追踪方法（取件→运输→清关→派送）、常见状态解读、查不到怎么办，附我们的追踪说明 | 速豹回国物流",
 "en_title": "How to Track a Shipment from the USA to China (2026) | Subao Global",
 "en_desc": "How to track USA to China shipments: full tracking from pickup to delivery, common status meanings, and what to do if tracking stalls.",
 "zh_h1": "美国寄中国怎么查物流？",
 "en_h1": "How to Track a Shipment to China",
 "zh_sections": [
   ("追踪方式",
    "① 我们提供全程单号：从美国取件到中国派送一个号查到底。② 微信/在线客服可查（Salesmartly 客服直接问）。③ 邮件同步：关键节点自动推送（取件/起飞/清关/派送）。"),
   ("常见状态解读",
    "「已取件」=快递员收到包裹；「仓库入库」=包裹到我们美国仓（拍照留证）；「已发运」=国际干线运输中；「清关中」=中国海关处理中（1-3 天）；「派送中」=国内快递送货；「已签收」=完成。"),
   ("查不到物流怎么办",
    "① 确认单号输入无误；② 刚取件 24h 内可能未更新（正常）；③ 跨境段有 1-2 天静默（在飞机/船上）；④ 超过 72h 无更新 → 联系客服人工查询（30 分钟回复）。"),
   ("追踪异常处理",
    "「清关异常」：我们代办处理，无需你操作；「地址错误」：联系客服改址（国内段免费）；「滞留」：旺季正常+3-5 天，客服会给预计时间。"),
   ("我们的承诺",
    "全流程可查可溯：仓库入库拍照、每段物流有记录、客服 30 分钟响应。高价值建议买保险（按保价赔）。"),
 ],
 "zh_faq": [
   ("美国寄中国怎么查物流？", "用我们提供的全程单号查，取件→运输→清关→派送一个号到底，也可微信问客服。"),
   ("物流显示清关中要多久？", "普货 1-2 天，敏感货 2-3 天，我们代办无需操作。"),
   ("查不到单号怎么办？", "确认单号无误；刚取件 24h 内正常；超 72h 无更新找客服人工查。"),
   ("物流停住不动了？", "跨境段有 1-2 天静默（飞机/船期），旺季 +3-5 天，超时找客服。"),
   ("地址错了怎么办？", "发运前改免费；发运后国内段改派免费，联系客服即可。"),
   ("怎么确认包裹安全？", "仓库入库拍照留证 + 全程追踪 + 可选保险。"),
   ("丢件了怎么赔？", "按保价金额赔（买了保险后），基础保险覆盖常规风险。"),
   ("签收后发现破损？", "签收后 48 小时内反馈，拍照+单号，按流程理赔。"),
   ("邮件提醒怎么开？", "下单时留邮箱，关键节点自动推送（取件/起飞/清关/派送）。"),
   ("客服多久回复？", "30 分钟内人工回复（工作时间），紧急问题优先处理。"),
 ],
 "en_sections": [
   ("How to track",
    "1) We give you one end-to-end number from US pickup to China delivery. 2) Ask our live chat (Salesmartly) anytime. 3) Email updates at key milestones (pickup, dispatch, customs, delivery)."),
   ("Common status meanings",
    "'Picked up' = courier has it. 'Warehouse received' = at our US warehouse (photo taken). 'Dispatched' = in international transit. 'In customs' = China customs (1–3 days). 'Out for delivery' = domestic courier. 'Delivered' = done."),
   ("Tracking shows nothing",
    "1) Double-check the number. 2) Within 24h of pickup there may be no update (normal). 3) Cross-border legs go quiet 1–2 days (on the plane/ship). 4) No update for 72h → contact support for a manual check (30-min response)."),
   ("Anomaly handling",
    "'Customs issue': we handle it — you do nothing. 'Wrong address': contact us to change (free domestically). 'Delayed': normal +3–5 days in peak season; support will give an ETA."),
   ("Our commitment",
    "Fully trackable: intake photos, per-leg records, 30-minute support response. Insure high-value items (paid per insured value)."),
 ],
 "en_faq": [
   ("How do I track a US-to-China shipment?", "Use the end-to-end number we provide, or ask our live chat."),
   ("How long is 'in customs'?", "Regular goods 1–2 days; sensitive 2–3. We handle it — you do nothing."),
   ("Tracking number not found?", "Check the number; no update within 24h of pickup is normal; >72h — contact support."),
   ("Tracking stalled?", "Cross-border legs go quiet 1–2 days; peak season +3–5; contact support if overdue."),
   ("Wrong address?", "Free to change before dispatch; free domestic re-delivery after — contact support."),
   ("How do I know my parcel is safe?", "Warehouse intake photo + full tracking + optional insurance."),
   ("Lost parcel compensation?", "Paid per insured value (if insured); basic coverage handles standard risk."),
   ("Damaged on delivery?", "Report within 48h with photos + tracking number for claims."),
   ("How do email updates work?", "Leave your email at booking; key milestones auto-send."),
   ("Support response time?", "30-minute human response during business hours; urgent issues prioritized."),
 ],
},
{
 "slug": "usa-to-china-lost-package",
 "zh_title": "美国寄中国丢件/破损怎么办？2026 理赔指南",
 "zh_desc": "美国寄中国丢件/破损怎么赔？理赔流程 4 步、保险怎么买（保价 3%）、常见理赔问题、防丢 5 招，收件人/寄件人必读 | 速豹回国物流",
 "en_title": "Lost or Damaged Package from the USA to China: Claims Guide (2026) | Subao Global",
 "en_desc": "What to do if a USA-to-China shipment is lost or damaged: 4-step claims process, how insurance works, common claim issues, and 5 loss-prevention tips.",
 "zh_h1": "美国寄中国丢件/破损怎么办？",
 "en_h1": "Lost or Damaged Package: What to Do",
 "zh_sections": [
   ("理赔流程 4 步",
    "① 发现问题：签收时检查，破损当场拍照（含面单）。② 联系客服：48 小时内反馈（提供单号+照片）。③ 提供凭证：物品价值证明（购买记录/截图）。④ 核实赔付：按保价金额赔付，一般 7-15 个工作日到账。"),
   ("保险怎么买",
    "基础保险：下单默认覆盖常规运输风险（丢损按走货 100 美金）。额外保价：货值 ×3%，高价值（奢侈品/电子产品）强烈建议，丢损按保价全赔。"),
   ("常见理赔问题",
    "① 没买保险 → 按基础赔付标准（有限）。② 破损没当场发现 → 48h 内反馈有效。③ 价值证明缺失 → 影响赔付额。④ 易碎品没加固 → 可能拒赔（包装责任）。"),
   ("防丢 5 招",
    "① 高价值买保价（货值 3% 换安心）。② 易碎品加固+警示标识。③ 外箱不要写贵重字眼。④ 保号拍照留证。⑤ 选有仓库实拍+全程追踪的正规渠道。"),
   ("我们的承诺",
    "仓库入库拍照留证、全程可追溯、客服 30 分钟响应、理赔流程透明。正规渠道赔付条款清晰，不推诿。"),
 ],
 "zh_faq": [
   ("美国寄中国丢件怎么赔？", "买了保险按保价金额赔；没买按基础赔付标准（走货 100 美金）。"),
   ("破损怎么申请理赔？", "签收时检查，48 小时内拍照（含面单）+ 联系客服 + 提供价值凭证。"),
   ("保险多少钱？", "基础保险含在服务里；额外保价货值×3%，高价值建议买。"),
   ("理赔要多久？", "核实后一般 7-15 个工作日到账。"),
   ("没买保险能赔吗？", "按基础标准有限赔付，所以高价值一定要买保价。"),
   ("易碎品破损谁的责任？", "正常加固的按流程赔；完全没加固可能按包装不当处理。"),
   ("丢件概率大吗？", "正规渠道丢件率极低（全程追踪+入库拍照），主要是防破损。"),
   ("外箱能写贵重吗？", "不能，写「贵重/易碎」反而招贼，用警示标识即可。"),
   ("理赔需要什么材料？", "单号+破损/丢失照片+购买凭证（价值证明）。"),
   ("客服不处理怎么办？", "正规公司有升级渠道，条款透明。选渠道前先看赔付条款。"),
 ],
 "en_sections": [
   ("4-step claims process",
    "1) Spot the issue: inspect on delivery; photograph damage immediately (with the label). 2) Contact support within 48h (tracking number + photos). 3) Provide proof of value (purchase records/screenshots). 4) Payout per insured value, usually 7–15 working days."),
   ("How insurance works",
    "Basic coverage: included by default for standard transit risk (up to $100 per shipment). Additional coverage: ~3% of declared value — strongly recommended for luxury/electronics; pays full insured value on loss/damage."),
   ("Common claim issues",
    "1) No insurance → limited basic payout. 2) Damage not reported on delivery → only valid within 48h. 3) Missing value proof → lower payout. 4) Fragile items packed without reinforcement → may be treated as packing error."),
   ("5 loss-prevention tips",
    "1) Insure high-value items (~3% for peace of mind). 2) Reinforce fragile items + warning labels. 3) Never write 'valuable' on the box. 4) Photograph the parcel with the label. 5) Pick channels with warehouse footage + full tracking."),
   ("Our commitment",
    "Intake photos, full traceability, 30-minute support, transparent claims. Legitimate channels have clear policies and don't deflect."),
 ],
 "en_faq": [
   ("How are lost packages compensated?", "Per insured value if insured; otherwise basic coverage (up to $100)."),
   ("How do I claim damage?", "Inspect on delivery; within 48h send photos (with label) + tracking number + proof of value."),
   ("How much is insurance?", "Basic coverage is included; additional ~3% of value — recommended for high-value."),
   ("How long do claims take?", "Usually 7–15 working days after verification."),
   ("What if I didn't buy insurance?", "Limited basic payout — which is why high-value items should be insured."),
   ("Who's liable for fragile damage?", "Properly packed items claim normally; unpacked fragile items may be treated as packing error."),
   ("How likely is loss?", "Very low on legitimate channels (full tracking + intake photos); damage is the bigger risk."),
   ("Can I write 'valuable' on the box?", "No — it attracts thieves. Use warning labels only."),
   ("What documents for claims?", "Tracking number + damage/loss photos + purchase proof (value)."),
   ("What if support won't help?", "Legitimate companies have escalation paths and clear terms. Check the claims policy before choosing."),
 ],
},
{
 "slug": "usa-to-china-peak-season",
 "zh_title": "美国寄中国旺季注意事项 2026｜避坑指南",
 "zh_desc": "美国寄中国旺季（毕业季/黑五/年末）避坑：提前多久寄、会不会涨价、爆仓怎么办、怎么错峰省钱，旺季寄件必看 | 速豹回国物流",
 "en_title": "USA to China Shipping in Peak Season: What to Know (2026) | Subao Global",
 "en_desc": "Peak-season (graduation/Black Friday/year-end) shipping tips: how early to ship, rate rises, backlog, and how to save by shipping off-peak.",
 "zh_h1": "美国寄中国旺季注意事项",
 "en_h1": "Peak-Season Shipping: What to Know",
 "zh_sections": [
   ("旺季什么时候（3 个高峰）",
    "① 毕业季（5-7 月）：北美留学生回国高峰。② 黑五/圣诞（11-12 月）：海淘代购高峰。③ 春节前（1 月）：华人寄年货高峰。"),
   ("旺季的影响",
    "仓位紧张（爆仓）、时效 +3-5 天、价格可能上浮 10-20%。毕业季 30kg 行李需求激增，仓库排队。"),
   ("怎么错峰省钱",
    "① 提前 2-3 周寄（毕业季 5 月初就动手）；② 行李先到仓免费存 30 天再发货；③ 非高峰月（3-4 月/9-10 月）寄最便宜；④ 提前预约锁价。"),
   ("旺季避坑 5 条",
    "① 别临时抱佛脚（临回国才寄 = 爆仓+贵）；② 确认报价含旺季附加费没；③ 留足 1-2 周缓冲；④ 敏感货提前走（清关排队）；⑤ 高价值早买保险。"),
   ("我们的旺季保障",
    "30 天免费仓储错峰、仓位预留（老客户优先）、价格透明（报价含所有附加费）、客服旺季 7×12 小时。"),
 ],
 "zh_faq": [
   ("旺季寄中国会不会涨价？", "可能上浮 10-20%，提前预约可锁价。"),
   ("旺季要提前多久寄？", "建议提前 2-3 周，毕业季 5 月初就开始。"),
   ("旺季时效慢多少？", "通常 +3-5 天（爆仓排队），特殊年份更长。"),
   ("怎么避开旺季？", "行李提前寄到仓（30 天免费存），或 3-4 月/9-10 月错峰寄。"),
   ("旺季会爆仓吗？", "高峰期会，所以我们提供仓位预留（老客户优先）。"),
   ("旺季寄敏感货注意什么？", "提前走（清关排队），单独申报，别混普货。"),
   ("旺季还能免费取件吗？", "能，全美免费上门取件照常，就是排期要提前约。"),
   ("旺季买保险有用吗？", "有用，旺季物流量大，高价值买保价更稳。"),
   ("黑五海淘什么时候寄最划算？", "黑五当天下单，但物流挤；建议黑五前一周或圣诞后寄。"),
   ("旺季和淡季价格差多少？", "可能差 10-20%，100kg+ 大货淡季更划算。"),
 ],
 "en_sections": [
   ("When is peak season (3 waves)",
    "1) Graduation (May-Jul): North American students heading home. 2) Black Friday/Christmas (Nov-Dec): shopping and daigou peak. 3) Pre-Chinese-New-Year (January): festive gifting peak."),
   ("What peak season does",
    "Tight capacity (backlogs), +3–5 days transit, and rates that can rise 10–20%. Graduation-season 30kg luggage demand fills warehouses."),
   ("How to ship off-peak and save",
    "1) Ship 2–3 weeks early (start in early May for graduation). 2) Send luggage to the warehouse early (30-day free storage) and dispatch later. 3) Off-peak months (Mar-Apr/Sep-Oct) are cheapest. 4) Book early to lock rates."),
   ("5 peak-season traps",
    "1) Don't wait until the last minute (backlog + higher rates). 2) Confirm whether quotes include peak surcharges. 3) Leave 1–2 weeks of buffer. 4) Ship sensitive goods early (customs queues). 5) Insure high-value items early."),
   ("Our peak-season safeguards",
    "30-day free storage to smooth timing, reserved capacity (returning customers first), transparent quotes (all surcharges included), and extended support hours."),
 ],
 "en_faq": [
   ("Do rates rise in peak season?", "They can rise 10–20%; booking early locks the rate."),
   ("How early should I ship?", "2–3 weeks ahead; start in early May for graduation."),
   ("How much slower is peak season?", "Usually +3–5 days (backlog); longer in extreme years."),
   ("How do I avoid the peak?", "Send luggage to the warehouse early (30-day free storage), or ship in Mar-Apr/Sep-Oct."),
   ("Do warehouses run out of space?", "Peak demand fills them — we reserve capacity (returning customers first)."),
   ("Sensitive goods in peak season?", "Ship early (customs queues), declare separately, don't mix with regular."),
   ("Is free pickup still available?", "Yes, nationwide free pickup continues — just book your window earlier."),
   ("Is insurance worth it in peak season?", "Yes — higher volume means higher risk; insure high-value items."),
   ("Best time for Black Friday hauls?", "Order on Black Friday but expect queues; ship the week before or after Christmas instead."),
   ("How much is the peak vs off-peak gap?", "10–20%; 100kg+ volume is especially better off-peak."),
 ],
},
{
 "slug": "usa-to-china-for-beginners",
 "zh_title": "美国寄中国新手攻略 2026｜第一次寄件避坑指南",
 "zh_desc": "第一次从美国寄中国？新手避坑攻略：先问 5 个问题、打包入门、选渠道不踩坑、常见误区（包清关≠包税），小白也能寄明白 | 速豹回国物流",
 "en_title": "First-Time Shipping from the USA to China: Beginner's Guide (2026) | Subao Global",
 "en_desc": "First time shipping to China from the USA? Ask 5 questions first, basic packing, choosing a channel, and common myths (agent clearance ≠ tax-free).",
 "zh_h1": "美国寄中国新手攻略",
 "en_h1": "First-Time Shipping: Beginner's Guide",
 "zh_sections": [
   ("先问自己 5 个问题",
    "① 寄什么？（品类决定渠道）② 多重？（>5kg 走专线）③ 多急？（<2 周选空运）④ 预算？（省 40-60% 选华人）⑤ 到哪？（城市决定时效）。5 个答案出来，渠道基本定了。"),
   ("打包入门（第一次就做对）",
    "加硬纸箱 + 真空压缩衣物 + 气泡膜包易碎 + 液体密封 + 塞满不留空隙。箱子选 60×40×50 邮政箱，别用超市破纸箱。"),
   ("选渠道不踩坑",
    "别只看首重价（续重/体积重才是大头）；问清是不是双清包税（包清关≠包税）；看赔付条款（丢损怎么赔）；确认有没有隐藏费（偏远/合箱/仓储）。"),
   ("5 个新手常见误区",
    "① 包清关=不用交税（错，包清关只是代办手续）；② 越便宜越好（低价陷阱多）；③ 申报越低越好（瞒报被查罚款更贵）；④ 国际快递最快最稳（贵 3-5 倍）；⑤ 随便找个转运就行（正规看资质/赔付/口碑）。"),
   ("第一次寄件流程",
    "发物品清单 → 客服报价（30 分钟）→ 打包 → 约取件 → 我们运输/清关/派送 → 收件人收货。全程一个单号。"),
 ],
 "zh_faq": [
   ("第一次寄中国要注意什么？", "先确认品类可寄、选对渠道（21kg+ 专线最划算）、如实申报、高价值买保险。"),
   ("新手选哪个渠道？", "行李/搬家/代购选华人专线（双清包税省心），急件文件选国际快递。"),
   ("包清关和包税区别？", "包清关=代办清关手续；包税=税费含运费。双清包税才是全包。"),
   ("第一次寄多少钱？", "空运 ¥70-80/kg（21kg+ 双清包税），先发清单让客服精准报价。"),
   ("怎么打包最省？", "真空压缩+塞满+合箱，省 20-40% 运费。"),
   ("需要提前准备什么？", "收件人三要素（姓名/电话/地址）+ 物品清单，30 分钟出报价。"),
   ("新手最容易踩什么坑？", "只看首重价（体积重是大头）、信「包清关不用交税」、申报瞒报。"),
   ("第一次寄几天能到？", "空运 7-10 工作日，海运 25-35 天。"),
   ("怎么确认渠道靠谱？", "看资质（成立年限）、仓库实拍、赔付条款、客户口碑。我们提供真实仓库视频。"),
   ("寄完怎么跟踪？", "全程单号 + 客服 30 分钟响应 + 邮件节点提醒。"),
 ],
 "en_sections": [
   ("Ask yourself 5 questions first",
    "1) What are you shipping? (category → channel). 2) How heavy? (>5kg → consolidated line). 3) How urgent? (<2 weeks → air). 4) Budget? (save 40–60% → Chinese line). 5) Where to? (city → transit time). Five answers and the channel is basically decided."),
   ("Basic packing (right the first time)",
    "Sturdy carton + vacuum-compressed clothes + bubble-wrapped fragile items + sealed liquids + fill all gaps. Use a 60×40×50cm postal box, not a supermarket box."),
   ("Choosing a channel without traps",
    "Don't judge by first-weight only (incremental/volumetric is the real cost). Ask if it's double-clearance tax-inclusive (agent clearance ≠ tax-free). Check the claims policy. Confirm no hidden fees (remote/consolidation/storage)."),
   ("5 common beginner myths",
    "1) Agent clearance = no duty (wrong; it just handles the paperwork). 2) Cheapest is best (low-price traps abound). 3) Declare lower (under-declaring costs more when caught). 4) Express is fastest and safest (3–5x the price). 5) Any forwarder works (check credentials/claims/reviews)."),
   ("First shipment flow",
    "Send your item list → quote in 30 min → pack → book pickup → we handle transit/customs/delivery → recipient receives. One tracking number throughout."),
 ],
 "en_faq": [
   ("What should first-timers know?", "Confirm the item ships, choose the right channel (21kg+ line is best value), declare honestly, insure high-value."),
   ("Which channel for beginners?", "Luggage/moving/daigou → Chinese line (tax-inclusive, easy); urgent/docs → express."),
   ("Agent clearance vs tax-inclusive?", "Agent clearance = paperwork handled; tax-inclusive = duty in the price. Double-clearance tax-inclusive is the full package."),
   ("How much for a first shipment?", "Air ¥70–80/kg (21kg+, tax-inclusive). Send your list for an exact quote."),
   ("How to pack to save?", "Vacuum-compress + fill gaps + consolidate: save 20–40%."),
   ("What to prepare?", "Recipient three details (name/phone/address) + item list; quote in 30 min."),
   ("Biggest beginner traps?", "Judging by first-weight only (volumetric is the real cost), believing 'agent clearance = no tax', under-declaring."),
   ("First shipment transit time?", "Air 7–10 working days; sea 25–35 days."),
   ("How to verify a channel?", "Check years in business, warehouse footage, claims policy, and reviews. We publish real warehouse videos."),
   ("Tracking after shipping?", "End-to-end number + 30-min support + email milestone updates."),
 ],
},
]

# ============ 渲染 ============
def sections_html(sections):
    out = ""
    for title, body in sections:
        out += f'\n    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">{title}</h2><p style="color:var(--text-secondary);line-height:1.9">{body}</p></div>'
    return out

def gen_en(a):
    slug = a["slug"]
    rel = f"blog/{slug}.html"
    faq = a["en_faq"]
    body = f"""  <section class="hero" style="padding-bottom:48px"><div class="container">
      <h1>{a['en_h1']}</h1>
      <p class="subtitle">{a['en_desc'][:150]}</p>
    </div></section>
  <section class="section"><div class="container" style="max-width:820px">
    {sections_html(a['en_sections'])}
    <div style="background:var(--primary-light);border:1px solid #CDE3F5;border-radius:12px;padding:20px 24px;margin:32px 0">
      <div style="font-size:14px;font-weight:700;color:var(--primary-dark);margin-bottom:6px">📦 Related service</div>
      <a href="/en/usa-to-china/" style="font-size:15px;font-weight:700;color:var(--primary);text-decoration:underline">Ship from the USA to China →</a>
      <p style="font-size:13px;color:var(--text-secondary);margin-top:4px">Tax-inclusive line from $11/kg (21kg+), free US pickup, 7–10 days door-to-door</p>
    </div>
    <div class="section-title" style="margin-top:44px"><h2>Frequently asked questions</h2></div>
    {faq_html(faq)}
    <div style="max-width:800px;margin:32px auto 0;padding:0 24px;font-size:13px;color:#64748B">Written by <strong>Subao Global Logistics Editorial Team</strong> · 12+ years international shipping experience · <a href="/en/about.html" style="color:#0066CC">About us</a></div>
  </div></section>
  {cta_html()}"""
    article = {"@context": "https://schema.org", "@type": "Article",
        "headline": a["en_h1"], "description": a["en_desc"],
        "datePublished": "2026-08-20", "dateModified": "2026-08-20",
        "author": {"@type": "Person", "name": "Subao Global Logistics Editorial Team"}}
    schema = f'{json.dumps(article)}\n  {faq_schema(faq)}\n  {json.dumps(PERSON_EN)}'
    (ROOT / "en" / rel).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "en" / rel).write_text(render_page(rel, a["en_title"], a["en_desc"], body, schema), encoding="utf-8")
    print(f"✅ en/{rel}")

def gen_zh(a):
    slug = a["slug"]
    rel = f"blog/{slug}.html"
    zh_url = f"{DOMAIN}/zh-cn/{rel}"
    en_url = f"{DOMAIN}/en/{rel}"
    faq = a["zh_faq"]
    faq_schema_zh = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": aq}} for q, aq in faq]}, ensure_ascii=False)
    article_zh = json.dumps({"@context": "https://schema.org", "@type": "Article",
        "headline": a["zh_h1"], "description": a["zh_desc"],
        "datePublished": "2026-08-20", "dateModified": "2026-08-20",
        "author": {"@type": "Person", "name": "速豹国际物流编辑团队"}}, ensure_ascii=False)
    person_zh = json.dumps(PERSON_ZH, ensure_ascii=False)
    body = sections_html(a["zh_sections"])
    faq_html_zh = ''.join(f'<div class="faq-item"><button class="faq-q">{q}<span>▼</span></button><div class="faq-a">{aq}</div></div>' for q, aq in faq)

    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{a['zh_title']}</title>
  <meta name="description" content="{a['zh_desc']}">
  <link rel="alternate" hreflang="zh-CN" href="{zh_url}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="x-default" href="{zh_url}">
  <link rel="canonical" href="{zh_url}">
  <meta property="og:title" content="{a['zh_h1']}">
  <meta property="og:description" content="{a['zh_desc'][:100]}">
  <meta property="og:url" content="{zh_url}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{DOMAIN}/assets/images/og-image.jpg">
  <meta property="og:locale" content="zh_CN">
  <meta name="lastmod" content="2026-08-20">
  <script type="application/ld+json">{article_zh}</script>
  <script type="application/ld+json">{faq_schema_zh}</script>
  <script type="application/ld+json">{person_zh}</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
  <style>
:root{{--primary:#0066CC;--primary-dark:#004C99;--primary-light:#E6F0FA;--green:#00B900;--bg:#F5F7FA;--text:#1A1A2E;--text-secondary:#64748B;--border:#E2E8F0;--radius-lg:16px;--radius-pill:24px;--nav-height:68px}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:var(--text);line-height:1.7;font-size:16px;background:var(--bg)}}
a{{text-decoration:none;color:inherit}}
.container{{max-width:1100px;margin:0 auto;padding:0 24px}}
.header{{position:fixed;top:0;left:0;right:0;height:var(--nav-height);background:rgba(255,255,255,.96);backdrop-filter:blur(12px);z-index:1000;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
.header .container{{display:flex;align-items:center;justify-content:space-between;height:100%}}
.logo{{font-size:20px;font-weight:700;color:var(--primary)}}
.nav{{display:flex;align-items:center;gap:2px}}
.nav a{{padding:7px 13px;font-size:13px;font-weight:500;color:var(--text-secondary);border-radius:var(--radius-pill);white-space:nowrap}}
.nav a:hover{{color:var(--primary);background:var(--primary-light)}}
.lang-switch{{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;font-size:13px;font-weight:600;color:var(--primary);border:1.5px solid var(--primary-light);border-radius:var(--radius-pill);background:#fff}}
@media(max-width:768px){{.nav{{display:none}}}}
.hero{{background:linear-gradient(135deg,#0066CC,#004C99);color:#fff;padding:110px 24px 56px}}
.hero h1{{font-size:clamp(1.5rem,2.6vw,2.1rem);font-weight:700;margin-bottom:10px}}
.hero .subtitle{{font-size:15px;opacity:.92}}
.section{{padding:48px 0}}
.section-title{{text-align:center;margin-bottom:24px}}
.section-title h2{{font-size:1.5rem;font-weight:700}}
.faq-item{{border-bottom:1px solid var(--border)}}
.faq-q{{width:100%;padding:16px 0;text-align:left;background:none;border:none;font-size:15px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;font-family:inherit;color:var(--text)}}
.faq-a{{padding:0 0 16px;font-size:14px;color:var(--text-secondary);line-height:1.7;display:none}}
.faq-a.show{{display:block}}
.cta-section{{background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;padding:64px 24px;text-align:center;border-radius:var(--radius-lg);margin:0 24px}}
@media(min-width:1200px){{.cta-section{{margin:0}}}}
.cta-section h2{{font-size:1.6rem;margin-bottom:12px}}
.cta-section p{{opacity:.9;margin-bottom:24px;max-width:500px;margin-left:auto;margin-right:auto}}
.btn-primary{{display:inline-flex;align-items:center;gap:6px;background:#fff;color:var(--primary);padding:14px 34px;border-radius:var(--radius-pill);font-weight:700;font-size:15px}}
.footer{{background:#1A1A2E;color:#fff;padding:40px 24px;text-align:center}}
.footer a{{color:#999}}
  </style>
</head>
<body>
  <header class="header"><div class="container">
    <a href="/zh-cn/" class="logo">速豹回国物流<span style="font-size:11px;color:var(--text-secondary);margin-left:8px">美国寄中国</span></a>
    <nav class="nav">
      <a href="/zh-cn/">首页</a><a href="/zh-cn/usa-to-china/">美国寄中国</a>
      <a href="/zh-cn/tools/">工具</a><a href="/zh-cn/blog/" class="active">攻略</a>
      <a href="{en_url}" class="lang-switch" hreflang="en">🌐 中文 / English</a>
    </nav>
  </div></header>
  <section class="hero"><div class="container"><h1>{a['zh_h1']}</h1><p class="subtitle">{a['zh_desc'][:130]}</p></div></section>
  <section class="section"><div class="container" style="max-width:820px">
    {body}
    <div style="background:var(--primary-light);border:1px solid #CDE3F5;border-radius:12px;padding:20px 24px;margin:32px 0">
      <div style="font-size:14px;font-weight:700;color:var(--primary-dark);margin-bottom:6px">📦 相关服务</div>
      <a href="/zh-cn/usa-to-china/" style="font-size:15px;font-weight:700;color:var(--primary);text-decoration:underline">美国寄中国专线 →</a>
      <p style="font-size:13px;color:var(--text-secondary);margin-top:4px">双清包税门到门 ¥70-80/kg（21kg+），全美免费取件，7-10 工作日</p>
    </div>
    <div class="section-title" style="margin-top:44px"><h2>常见问题</h2></div>
    {faq_html_zh}
    <div style="max-width:800px;margin:32px auto 0;padding:0 24px;font-size:13px;color:#64748B">作者：<strong>速豹国际物流编辑团队</strong> · 12年国际物流经验 · <a href="/zh-cn/about.html" style="color:#0066CC">关于我们</a></div>
  </div></section>
  <section class="cta-section"><div class="container">
    <h2>30 分钟出方案，免费上门估价</h2>
    <p>双清包税门到门 · 全美免费取件 · 全程可追踪</p>
    <a href="https://d.salesmartly.com/fuxikn" class="btn-primary" target="_blank" rel="noopener">💬 免费咨询</a>
  </div></section>
  <footer class="footer"><div class="container">© 2026 速豹回国物流 | <a href="/zh-cn/">首页</a> · <a href="/sitemap.xml">Sitemap</a></div></footer>
  <script>
    document.querySelectorAll('.faq-q').forEach(function(q){{q.addEventListener('click',function(){{var a=q.nextElementSibling;a.classList.toggle('show');q.querySelector('span').textContent=a.classList.contains('show')?'▲':'▼';}});}});
  </script>
</body>
</html>"""
    (ROOT / "zh-cn" / rel).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "zh-cn" / rel).write_text(page, encoding="utf-8")
    print(f"✅ zh-cn/{rel}")

def main():
    print(f"共 {len(QUESTIONS)} 个疑问词 × 中英")
    for a in QUESTIONS:
        gen_en(a)
        gen_zh(a)
    print("完成")

if __name__ == "__main__":
    main()
