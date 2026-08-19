# -*- coding: utf-8 -*-
"""
美淘转运 + 代购场景 5 篇（中英对称，差异化内容）
- 美国海淘转运回国全攻略 / 美国转运公司怎么选 / Amazon 下单寄回国
- 美国代购怎么发货回国 / 代购集运合箱攻略
每篇：10+ FAQ + FAQPage Schema + Article Schema + Person + 作者署名
"""
import json, re, importlib.util
from pathlib import Path

ROOT = Path("/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com")
DOMAIN = "https://subaog.com"
GA_ID = "G-DJGPMS9MOB"

# 复用 gen-en-content.py 的渲染函数
spec = importlib.util.spec_from_file_location("gec", str(ROOT / "gen-en-content.py"))
gec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gec)
render_page = gec.render_page
faq_html = gec.faq_html
faq_schema = gec.faq_schema
cta_html = gec.cta_html

# ============ 5 篇内容数据 ============
ARTICLES = [
# ── 1. 美国海淘转运回国全攻略 ──
{
 "slug": "us-shopping-forwarding-guide",
 "zh_title": "美国海淘转运回国全攻略 2026｜转运流程、运费、避税一次讲透",
 "zh_desc": "美国海淘转运回国怎么做？转运流程6步、运费怎么算（含体积重）、怎么避税、禁运品清单，2026最新攻略 | 速豹回国物流",
 "en_title": "US Shopping Forwarding to China: Complete Guide 2026 | Subao Global",
 "en_desc": "How to forward US online shopping to China: 6-step process, shipping costs (volumetric weight), how to avoid customs duty, and prohibited items. 2026 guide.",
 "zh_h1": "美国海淘转运回国全攻略 2026",
 "en_h1": "US Shopping Forwarding to China: Complete Guide",
 "zh_sections": [
   ("什么是美国海淘转运？",
    "美国海淘转运 = 你在 Amazon、品牌官网、eBay 下单，先寄到美国转运仓（我们提供美国地址），再由转运仓合并打包后寄回中国。相比直邮，转运更便宜（华人渠道比 USPS/FedEx 便宜 40-60%）、能买直邮不发的商品（如部分保健品/鞋服）、还能合箱省运费。"),
   ("转运流程：6 步搞定",
    "① 注册获取美国收货地址 → ② 在电商下单，收件地址填美国转运仓地址 → ③ 包裹到达转运仓（免费代收）→ ④ 需要时合箱打包（多件合并成一箱）→ ⑤ 支付运费（空运 7-10 工作日 / 海运 25-35 天）→ ⑥ 中国清关派送到家。全程可追踪。"),
   ("运费怎么算？体积重是关键",
    "运费 = 实重 和 体积重 取大者。体积重 = 长×宽×高(cm) ÷ 6000（部分渠道 ÷5000）。一双鞋子的鞋盒、一箱衣服的真空压缩，都能显著降低体积重。空运专线约 $5-8/lb，海运约 $2-4/lb（21kg+ 更划算）。"),
   ("怎么避税？3 个实用技巧",
    "① 个人物品控制在人民币 1000 元申报价值内（约 $140）可免税；② 走双清包税渠道（我们含税，不需额外缴）；③ 如实申报品名和数量——瞒报被查验会罚款甚至退运。保健品/化妆品等敏感货建议走专属渠道，清关成功率更高。"),
   ("转运 vs 直邮对比",
    "直邮（Amazon Global 等）：简单但贵、品类受限、税费预收。转运：便宜 40-60%、能买更多品类、可合箱、可控制申报。5kg 以上包裹转运优势明显。"),
 ],
 "zh_faq": [
   ("美国海淘转运要多久？", "空运 7-10 工作日门到门，海运 25-35 天。旺季（黑五/圣诞/春节前）多 3-5 天。"),
   ("美国转运运费多少钱？", "空运约 $5-8/lb，海运约 $2-4/lb（21kg+ 更便宜）。体积重和实重取大者。"),
   ("怎么避免被税？", "申报价值控制在 ¥1000 以内，或走双清包税渠道。如实申报，避免瞒报被查。"),
   ("哪些东西不能转运回国？", "武器弹药、新鲜肉类、种子、违禁药品等禁运。化妆品/保健品走敏感货渠道。"),
   ("转运要身份证吗？", "走个人行邮清关一般需要收件人身份证正反面用于申报，正规公司会加密处理。"),
   ("美国转运地址怎么用？", "注册后我们提供美国仓地址，电商下单时填这个地址即可，包裹到仓自动入库。"),
   ("合箱是什么意思？", "多件包裹合并成一箱再寄，省首重和运费。注意合箱后体积重可能变化。"),
   ("转运会不会丢件？", "正规转运都有入库拍照+全程追踪。高价值商品建议买保险，丢损按保价赔付。"),
   ("走哪个口岸清关快？", "一线城市（北上广深）清关最快，其他城市也支持门到门派送。"),
   ("转运公司靠谱吗？", "看资质、成立年限、赔付条款、客户评价。我们提供全程人工客服+30分钟响应。"),
 ],
 "en_sections": [
   ("What is US shopping forwarding?",
    "US shopping forwarding means you shop on Amazon, brand websites or eBay, ship to a US forwarding warehouse (we give you a US address), then the warehouse consolidates and ships to China. Compared to direct international shipping, forwarding is 40-60% cheaper, lets you buy items that don't ship internationally (like some supplements and shoes), and lets you consolidate multiple orders into one box."),
   ("The 6-step forwarding process",
    "1) Sign up and get a US warehouse address. 2) Order online and use the US address as the delivery address. 3) Your parcels arrive at the warehouse (free receiving). 4) Consolidate and repack when needed. 5) Pay shipping (air 7-10 working days / sea 25-35 days). 6) China customs clearance and door delivery. Fully trackable."),
   ("How is shipping cost calculated? Volumetric weight matters",
    "Cost = the larger of actual weight or volumetric weight. Volumetric weight = length × width × height (cm) ÷ 6000 (some carriers use ÷5000). Vacuum-compress clothing, remove shoe boxes — small changes save a lot. Air freight from about $5-8/lb, sea freight $2-4/lb (cheaper at 21kg+)."),
   ("3 practical tips to avoid customs duty",
    "1) Keep declared value under RMB 1,000 (about $140) for duty-free personal items. 2) Use a tax-inclusive channel (ours covers standard duty). 3) Declare honestly — under-declaring risks fines and return. Sensitive items like cosmetics and supplements should use dedicated channels."),
   ("Forwarding vs direct shipping",
    "Direct shipping (Amazon Global etc.): simple but expensive, limited categories, pre-paid taxes. Forwarding: 40-60% cheaper, more categories, consolidation, controlled declaration. For parcels over 5kg, forwarding clearly wins."),
 ],
 "en_faq": [
   ("How long does US forwarding to China take?", "Air freight 7-10 working days door-to-door; sea freight 25-35 days. Add 3-5 days during peak seasons (Black Friday, Christmas, CNY)."),
   ("How much does US forwarding cost?", "Air freight from about $5-8/lb; sea freight $2-4/lb (cheaper at 21kg+). Billed on actual or volumetric weight, whichever is larger."),
   ("How can I avoid customs duty?", "Keep declared value under RMB 1,000 (about $140), or use a tax-inclusive channel. Always declare honestly."),
   ("What can't I forward to China?", "Weapons, fresh meat, seeds, and illegal drugs are prohibited. Cosmetics and supplements must use sensitive-goods channels."),
   ("Do I need an ID for customs?", "Personal parcels usually require the recipient's ID photo for declaration. Reputable companies handle this securely."),
   ("How do I use the US forwarding address?", "After signup you get a US warehouse address — use it as the shipping address when ordering. Parcels are logged automatically on arrival."),
   ("What is consolidation?", "Multiple parcels merged into one box to save on first-weight and total cost. Note that volumetric weight can change after consolidation."),
   ("Will my parcel get lost?", "Reputable forwarders provide intake photos and full tracking. Buy insurance for high-value items; claims are paid per declared value."),
   ("Which customs port clears fastest?", "First-tier cities (Beijing, Shanghai, Guangzhou, Shenzhen) clear fastest. We deliver door-to-door nationwide."),
   ("Is the forwarding company reliable?", "Check credentials, years in business, claims policy, and customer reviews. We offer human support with 30-minute response."),
 ],
},
# ── 2. 美国转运公司怎么选 ──
{
 "slug": "us-forwarding-company-comparison",
 "zh_title": "美国转运公司怎么选 2026｜5个关键指标避开所有坑",
 "zh_desc": "美国转运公司怎么选？看价格/时效/客服/口岸/增值服务5个指标，附价格陷阱（首重续重/体积重）避坑指南 | 速豹回国物流",
 "en_title": "How to Choose a US Forwarding Company 2026: 5 Key Metrics | Subao Global",
 "en_desc": "How to choose a US forwarding company: 5 key metrics (price, speed, support, ports, add-ons) plus pricing traps to avoid (first-weight, volumetric weight). 2026 guide.",
 "zh_h1": "美国转运公司怎么选？5 个指标避开所有坑",
 "en_h1": "How to Choose a US Forwarding Company",
 "zh_sections": [
   ("指标 1：价格透明（最容易被坑）",
    "低价陷阱集中在：① 首重便宜续重贵；② 体积重系数偷偷调高（÷5000 比 ÷6000 贵 20%）；③ 附加费事后加（合箱费/偏远取件费/仓储费）。签约前让对方把所有费用列清单，拒绝「到仓再算」。"),
   ("指标 2：时效与口岸",
    "空运 7-10 工作日、海运 25-35 天是常态；看它清关走哪个口岸（北上广深最快）。旺季（11 月-1 月）要问是否会爆仓，别选旺季排仓 2 周的。"),
   ("指标 3：客服响应",
    "物流出问题 80% 靠客服解决。看客服响应时间（我们承诺 30 分钟内）、是否有人工（非只有机器人）、赔付流程是否清晰（丢损怎么赔、多久到账）。"),
   ("指标 4：增值服务",
    "免费代收/合箱/加固/拍照、免费仓储天数（一般 15-30 天）、退货处理、敏感货专线（保健品/化妆品）——这些决定了实际成本，不只是运费本身。"),
   ("指标 5：公司资质",
    "看成立年限、仓库实拍（我们提供真实仓库视频）、赔付条款原文、客户评价（小红书/论坛）。避开刚注册没案例的新公司。"),
   ("价格陷阱对照表",
    "常见陷阱：首重 $8 续重 $4（实际小件很贵）→ 破解：直接算 1kg/5kg/10kg 总价对比。体积重 ÷5000 vs ÷6000 → 破解：要求写进合同。免费仓储 3 天 → 破解：问超过后每天多少钱。"),
 ],
 "zh_faq": [
   ("美国转运公司哪家靠谱？", "没有绝对答案。按 5 个指标筛选：价格透明、时效稳定、人工客服、赔付清晰、资质可查。我们提供 30 天免费仓储+全程追踪。"),
   ("转运价格怎么算？", "运费 = 实重/体积重取大 × 单价 + 可能的附加费（偏远/合箱/敏感货）。签约前要完整报价单。"),
   ("体积重是什么？怎么避免？", "体积重 = 长×宽×高÷6000。真空压缩衣物、去鞋盒、合理装箱能显著降低。"),
   ("敏感货（化妆品/保健品）能转运吗？", "可以，走敏感货专线，清关成功率更高。我们支持保健品/化妆品/电子产品等。"),
   ("免费仓储多久？", "我们提供 30 天免费仓储，支持分批到货、集齐再发。超过后少量费用。"),
   ("转运公司倒闭了怎么办？", "选成立久、有实体仓库的公司，避免一次性预付大量运费。我们支持到仓再付。"),
   ("合箱收费吗？", "部分公司收合箱费。我们免费合箱（合理范围内），合箱后按新体积重计费。"),
   ("能寄到中国哪些城市？", "中国大陆主要城市全覆盖，门到门派送，一线城市最快。"),
   ("丢件怎么赔？", "按保价金额赔（买保险后）。我们基础保险覆盖常规运输风险，高价值建议额外保价。"),
   ("怎么判断客服好不好？", "发一条消息看多久回、是否人工、能否解决实际问题。我们承诺 30 分钟响应。"),
 ],
 "en_sections": [
   ("Metric 1: Transparent pricing (the #1 trap)",
    "Price traps: 1) Cheap first-weight but expensive incremental weight. 2) Volumetric divisor quietly changed (÷5000 is 20% pricier than ÷6000). 3) Fees added later (consolidation, remote pickup, storage). Ask for a full price list up front and refuse 'we'll calculate at the warehouse'."),
   ("Metric 2: Speed and customs port",
    "Typical: air 7-10 working days, sea 25-35 days. Check which China customs port they clear (first-tier cities are fastest). Ask about peak-season (Nov-Jan) backlog — avoid carriers that queue 2+ weeks."),
   ("Metric 3: Customer support",
    "80% of shipping problems are solved by support. Check response time (we commit to 30 minutes), whether a human replies, and whether claims are clear (what's covered, payout time)."),
   ("Metric 4: Value-added services",
    "Free receiving/consolidation/repacking/photos, free storage days (15-30 typical), return handling, and sensitive-goods lines (supplements, cosmetics) — these drive real cost beyond the base rate."),
   ("Metric 5: Company credentials",
    "Check years in business, real warehouse footage (we publish ours), the exact claims policy, and customer reviews. Avoid brand-new companies with no track record."),
   ("Pricing trap comparison table",
    "Trap: first-weight $8 + incremental $4 (very expensive for small parcels) → fix: compare total prices at 1kg/5kg/10kg. Volumetric ÷5000 vs ÷6000 → fix: get it in writing. 3-day free storage → fix: ask the daily rate after that."),
 ],
 "en_faq": [
   ("Which US forwarding company is reliable?", "There's no absolute answer. Screen on 5 metrics: transparent pricing, stable speed, human support, clear claims, verifiable credentials. We offer 30-day free storage and full tracking."),
   ("How is forwarding priced?", "Cost = max(actual, volumetric weight) × rate + possible surcharges (remote, consolidation, sensitive goods). Get a full quote before committing."),
   ("What is volumetric weight and how do I reduce it?", "Volumetric weight = L×W×H (cm) ÷ 6000. Vacuum-compress clothing, remove shoe boxes, pack tightly."),
   ("Can sensitive goods (cosmetics, supplements) be forwarded?", "Yes — use a sensitive-goods line for higher clearance success. We support supplements, cosmetics, electronics and more."),
   ("How long is free storage?", "We offer 30 days of free storage so parcels can arrive in batches and ship together."),
   ("What if the forwarder goes out of business?", "Choose established companies with physical warehouses, and avoid paying large prepaid balances. We offer pay-at-warehouse options."),
   ("Is consolidation charged?", "Some companies charge. We consolidate for free (within reason); the new volumetric weight applies after consolidation."),
   ("Which Chinese cities do you deliver to?", "All major cities in mainland China, door-to-door. First-tier cities are fastest."),
   ("How are lost parcels compensated?", "Per insured value (when you buy insurance). Our basic coverage handles standard transit risks; insure high-value items extra."),
   ("How do I judge support quality?", "Send a message and time the reply, check if it's human, and whether problems actually get solved. We commit to 30-minute responses."),
 ],
},
# ── 3. Amazon 下单寄回国教程 ──
{
 "slug": "amazon-shopping-to-china",
 "zh_title": "Amazon 怎么下单寄回国 2026｜直邮 vs 转运全教程",
 "zh_desc": "Amazon 购物怎么寄回中国？直邮（Amazon Global）vs 转运（美国地址）全对比，5步教程+税费计算+值得买的商品清单 | 速豹回国物流",
 "en_title": "How to Shop on Amazon and Ship to China 2026 | Subao Global",
 "en_desc": "How to ship Amazon orders to China: Amazon Global direct vs US forwarding. 5-step tutorial, tax calculation, and what's worth buying. 2026 guide.",
 "zh_h1": "Amazon 购物怎么寄回中国？",
 "en_h1": "How to Shop on Amazon and Ship to China",
 "zh_sections": [
   ("Amazon 能直邮中国吗？",
    "部分商品可以。结算时如果显示「Deliver to China」并带预估关税，就是直邮（Amazon Global）。但很多商品（保健品、部分鞋服、第三方卖家商品）不支持直邮中国——这时候就用转运：填美国地址，Amazon 寄美国仓，我们转寄回国。"),
   ("5 步教程（转运方式）",
    "① 注册转运账号拿美国地址 → ② Amazon 下单，收货地址填美国仓 → ③ 包裹到仓（免费代收+拍照）→ ④ 合箱打包 → ⑤ 付运费寄回国，7-10 工作日门到门。全程可追踪。"),
   ("税费怎么算？直邮 vs 转运",
    "直邮：Amazon 预收关税+运费，通常较贵，且税费按平台预估（偏高）。转运：可以走双清包税渠道（我们含税），或控制申报价值在 ¥1000 内免税。同一样东西，转运通常比直邮便宜 30-50%。"),
   ("哪些商品值得海淘？",
    "美国买更划算：保健品（鱼油/维生素，差价大）、品牌鞋服（打折季）、电子配件、奶粉、化妆品（敏感货走专线）。注意：大件（家具/健身器材）体积重高，建议海运降低成本。"),
   ("退货怎么办？",
    "转运仓提供退货处理：收到后 30 天内（Amazon 退货窗口）可退回 Amazon 或转发给美国朋友。高价值商品建议买运输保险。"),
 ],
 "zh_faq": [
   ("Amazon 直邮中国要多久？", "Amazon Global 直邮一般 5-15 天（预收关税）。转运空运 7-10 工作日，海运 25-35 天。"),
   ("Amazon 直邮中国运费多少？", "直邮按商品+运费+关税打包价，通常比转运贵 30-50%。转运空运 $5-8/lb。"),
   ("Amazon 哪些不能寄中国？", "直邮限制液体/电池类较多；转运可以处理大多数品类，但肉类/种子/违禁药品仍禁运。"),
   ("美国亚马逊需要美国手机号吗？", "不需要。中国手机号+国际信用卡即可注册，转运地址填美国仓地址。"),
   ("直邮被税了怎么办？", "直邮是预收关税制，Amazon 已代收，一般不会二次补税。转运走包税渠道则不用额外缴。"),
   ("转运合箱能省多少？", "多件合箱省首重，通常省 20-40%。注意合箱后体积重可能增加。"),
   ("保健品在 Amazon 买划算吗？", "划算，美国保健品差价大。但保健品属敏感货，走敏感货专线清关更稳。"),
   ("Amazon 会员（Prime）有用吗？", "有用。美国境内免运费+2 天达，适合转运模式（先到美国仓）。直邮中国 Prime 折扣有限。"),
   ("黑五打折值得海淘吗？", "值得。黑五/Prime Day 是美国海淘旺季，但物流也会慢 3-5 天，建议提前下单。"),
   ("下单后多久到中国？", "转运：Amazon 到仓 2-5 天 + 空运 7-10 天 ≈ 2 周内。旺季适当延长。"),
 ],
 "en_sections": [
   ("Can Amazon ship directly to China?",
    "Some items can. If checkout shows 'Deliver to China' with an estimated import tax, that's Amazon Global direct shipping. But many items (supplements, some apparel, third-party sellers) can't ship direct — that's when forwarding helps: use a US address, Amazon ships to the US warehouse, we forward to China."),
   ("5-step tutorial (forwarding)",
    "1) Sign up for forwarding and get a US address. 2) Order on Amazon with the US warehouse as delivery address. 3) Parcels arrive (free receiving + photos). 4) Consolidate and repack. 5) Pay shipping; door-to-door in 7-10 working days. Fully trackable."),
   ("Tax: direct vs forwarding",
    "Direct: Amazon pre-collects tax + shipping, usually pricier and platform-estimated (often higher). Forwarding: use a tax-inclusive channel (we cover standard duty) or keep declared value under RMB 1,000 for duty-free. The same item is typically 30-50% cheaper via forwarding."),
   ("What's worth buying from the US?",
    "Supplements (fish oil, vitamins — big price gaps), branded shoes and apparel on sale, electronics accessories, baby formula, and cosmetics (sensitive line). Note: large items have high volumetric weight — sea freight keeps cost down."),
   ("What about returns?",
    "Forwarding warehouses handle returns: within the 30-day Amazon return window, we can send it back to Amazon or forward to a US friend. Buy insurance for high-value items."),
 ],
 "en_faq": [
   ("How long does Amazon direct shipping to China take?", "Amazon Global direct usually 5-15 days (tax pre-paid). Forwarding air freight 7-10 working days; sea 25-35 days."),
   ("How much does Amazon direct shipping cost?", "Direct includes item + shipping + tax in one price, usually 30-50% more than forwarding. Forwarding air from $5-8/lb."),
   ("What can't Amazon ship to China?", "Direct shipping restricts liquids/batteries; forwarding handles most categories, but meat, seeds and illegal drugs remain prohibited."),
   ("Do I need a US phone number for Amazon?", "No. A Chinese phone number + international credit card works. Use the forwarding US address as the shipping address."),
   ("What if direct-shipped items get taxed?", "Direct is pre-paid duty; Amazon collects it at checkout, so no second bill. Forwarding via a tax-inclusive channel needs no extra payment."),
   ("How much can consolidation save?", "Merging multiple orders saves the first weight — typically 20-40%. Note volumetric weight can rise after consolidation."),
   ("Is it worth buying supplements on Amazon?", "Yes — US supplement price gaps are large. But supplements are sensitive goods; use a sensitive-goods line for smoother clearance."),
   ("Is Amazon Prime useful?", "Yes. Free 2-day US delivery fits forwarding well (ship to the US warehouse first). Prime discounts on direct-to-China shipping are limited."),
   ("Is Black Friday worth it?", "Yes — Black Friday and Prime Day are the peak US shopping seasons, but logistics slow 3-5 days. Order early."),
   ("When will my order arrive in China?", "Forwarding: 2-5 days to the US warehouse + 7-10 days air ≈ within 2 weeks. Longer in peak season."),
 ],
},
# ── 4. 美国代购怎么发货回国 ──
{
 "slug": "daigou-shipping-from-usa",
 "zh_title": "美国代购怎么发货回国 2026｜4种方式对比+避税指南",
 "zh_desc": "美国代购怎么把货发回中国？直邮/集运/专线/海运4种方式对比，申报避税技巧，敏感货（化妆品/保健品）处理方案 | 速豹回国物流",
 "en_title": "How Daigou Sellers Ship from the USA to China (2026) | Subao Global",
 "en_desc": "How US daigou (proxy shopping) sellers ship to China: direct mail, consolidation, dedicated lines, sea freight — plus declaration tips and sensitive-goods handling.",
 "zh_h1": "美国代购怎么发货回国？",
 "en_h1": "How Daigou Sellers Ship from the USA to China",
 "zh_sections": [
   ("代购发货 4 种方式对比",
    "① 国际快递（USPS/UPS/FedEx）：快但贵，$20-40/磅，适合急件小件。② 华人集运：$5-8/磅，5kg+ 划算，适合日常代购。③ 敏感货专线：保健品/化妆品专用，清关成功率高。④ 海运：$2-4/磅，适合大件/批量囤货，25-35 天。多数代购组合使用：小件集运+敏感货专线。"),
   ("合箱集运：省运费的核心",
    "代购是高频多件，每单单独寄很亏。做法：客户下单→全部寄到美国仓→合箱成一箱→一次寄回。合箱省首重，还能统一申报。我们免费代收+合箱+拍照。"),
   ("申报怎么填避免被税？",
    "① 单价如实、总价尽量在 ¥1000 内（超了走包税渠道）；② 品名写清楚（如「维生素」而非「保健品礼盒」）；③ 不要谎报价值——被查验罚款比税贵。④ 敏感货混普货会被查，分开走专线。"),
   ("敏感货（化妆品/保健品）怎么发？",
    "美国代购大头就是保健品、化妆品、奶粉。这些走敏感货专线（我们支持），双清包税，清关成功率 98%+。不要混在普货里，容易整箱被查。"),
   ("代购成本怎么算？",
    "成本 = 商品价 + 美国境内运费（0-5 美元）+ 国际运费（$5-8/磅）+ 可能的关税。包税渠道把关税成本固定化，方便定价。我们提供 30 分钟报价，成本可控。"),
 ],
 "zh_faq": [
   ("代购发货用什么方式最便宜？", "日常小件用华人集运（$5-8/磅），大件/批量用海运（$2-4/磅），敏感货走专线。综合比国际快递省 40-60%。"),
   ("代购一次发多少合适？", "5kg 以上集运优势明显，建议客户凑单或合箱到 10-20kg 降低单价。"),
   ("代购会被税吗？", "个人包裹 ¥1000 内免税；超了走双清包税渠道（我们含税）。如实申报最稳妥。"),
   ("保健品/化妆品能发吗？", "能，走敏感货专线，双清包税，清关成功率 98%+。"),
   ("代购需要营业执照吗？", "个人代购不用，但走量大的建议了解合规要求。我们按个人物品申报。"),
   ("客户能跟踪物流吗？", "可以，全程单号可查，从美国取件到中国派送。"),
   ("多久到客户手里？", "空运 7-10 工作日，海运 25-35 天。一线城市最快。"),
   ("代购发货要哪些资料？", "收件人姓名电话地址+身份证（清关申报用）。我们加密处理。"),
   ("大件代购（家具/器材）怎么发？", "海运专线最省，注意体积重。我们提供上门取件+加固打包。"),
   ("代购丢件/破损怎么办？", "可选保险，按保价赔付。基础保险覆盖常规风险。"),
 ],
 "en_sections": [
   ("4 ways daigou sellers ship from the USA",
    "1) International express (USPS/UPS/FedEx): fast but pricey, $20-40/lb, for urgent small parcels. 2) Chinese consolidated shipping: $5-8/lb, great at 5kg+, for daily daigou. 3) Sensitive-goods line: dedicated for supplements/cosmetics with high clearance success. 4) Sea freight: $2-4/lb, for large/wholesale, 25-35 days. Most sellers combine: consolidated for small items + sensitive line for health/cosmetics."),
   ("Consolidation: the core of saving",
    "Daigou is high-frequency multi-parcel; shipping each order separately is wasteful. Ship all orders to the US warehouse → consolidate into one box → ship once. Consolidation saves first-weight and unifies declaration. We offer free receiving, consolidation and photos."),
   ("How to declare to avoid duty",
    "1) Declare unit prices honestly, keep total under RMB 1,000 if possible (over that, use tax-inclusive). 2) Write clear item names ('vitamins', not 'gift box'). 3) Never under-declare — inspection fines cost more than duty. 4) Don't mix sensitive goods with regular items; use the dedicated line."),
   ("Sensitive goods (cosmetics/supplements)",
    "US daigou is largely supplements, cosmetics and baby formula. These go on the sensitive-goods line (we support it) with tax-inclusive clearance and 98%+ success. Never mix them into regular parcels — the whole box risks inspection."),
   ("How to calculate daigou cost",
    "Cost = product price + US domestic shipping ($0-5) + international freight ($5-8/lb) + possible duty. Tax-inclusive channels fix the duty cost, making pricing easy. We quote within 30 minutes."),
 ],
 "en_faq": [
   ("What's the cheapest way for daigou shipping?", "Daily small items: Chinese consolidated ($5-8/lb). Large/wholesale: sea ($2-4/lb). Sensitive goods: dedicated line. Overall 40-60% cheaper than international express."),
   ("How much should I ship at once?", "Consolidated shipping shines at 5kg+; bundling to 10-20kg lowers the per-kg rate."),
   ("Will daigou parcels be taxed?", "Personal parcels under RMB 1,000 are duty-free; above that use tax-inclusive channels (ours covers standard duty). Honest declaration is safest."),
   ("Can I ship supplements/cosmetics?", "Yes — via the sensitive-goods line, tax-inclusive, 98%+ clearance success."),
   ("Does daigou need a business license?", "Personal daigou doesn't, but high volume may require compliance review. We declare as personal items."),
   ("Can customers track the shipment?", "Yes — full tracking from US pickup to China delivery."),
   ("How long to the customer?", "Air 7-10 working days; sea 25-35 days. First-tier cities fastest."),
   ("What documents are needed?", "Recipient name, phone, address and ID (for customs declaration). We handle it securely."),
   ("How to ship large items (furniture/equipment)?", "Sea freight line is most economical; mind volumetric weight. We offer pickup and reinforced packing."),
   ("What about loss/damage?", "Optional insurance pays per insured value. Basic coverage handles standard transit risk."),
 ],
},
# ── 5. 代购集运合箱攻略 ──
{
 "slug": "daigou-consolidation-guide",
 "zh_title": "代购集运合箱攻略 2026｜合箱规则+省运费技巧",
 "zh_desc": "代购集运合箱怎么做？合箱规则（重量上限/体积重/免费期限）、怎么打包更省、避坑（被税/丢件/破损），2026合箱全攻略 | 速豹回国物流",
 "en_title": "Daigou Consolidation Guide 2026: Rules & Money-Saving Tips | Subao Global",
 "en_desc": "Daigou consolidation guide: rules (weight caps, volumetric weight, free storage), how to pack to save, and pitfalls to avoid (duty, loss, damage). 2026.",
 "zh_h1": "代购集运合箱全攻略",
 "en_h1": "Daigou Consolidation Guide",
 "zh_sections": [
   ("什么是集运合箱？",
    "集运 = 多个包裹集中到仓库统一寄回。合箱 = 把多个小包裹拆开重组进一个大箱。好处：省首重（每个包裹都有首重）、省体积（去掉多余包装）、统一申报。我们提供免费合箱服务。"),
   ("合箱规则（必读）",
    "① 重量上限：单箱一般 30-50kg，超重分箱。② 体积重：合箱后按新尺寸重算，装太满可能体积重超标。③ 免费仓储：一般 15-30 天，超期收费。④ 敏感货不能和普货混箱。"),
   ("怎么打包更省？",
    "① 去鞋盒/礼品盒（体积重最大来源）。② 衣物真空压缩。③ 液体/易碎品独立保护。④ 硬箱+气泡膜防压。⑤ 塞满不留空隙（既省体积重又防破损）。打包技巧能省 20-40% 运费。"),
   ("合箱避坑 4 件事",
    "① 被税：总申报价值控制在 ¥1000 内或走包税渠道。② 丢件：高价值买保险。③ 破损：易碎品单独加固。④ 时效：旺季合箱排队，提前 1-2 周寄。"),
   ("集运报价怎么算？",
    "单价（$/磅）× 实重或体积重大者 + 附加费（偏远/敏感货）。合箱后重量=所有包裹重量和，体积重=新箱尺寸算。我们 30 分钟报价，报价单全透明。"),
 ],
 "zh_faq": [
   ("合箱要钱吗？", "我们免费合箱。部分公司收 $3-5/次，选之前问清楚。"),
   ("合箱后多久到？", "空运 7-10 工作日，海运 25-35 天，从合箱发货日起算。"),
   ("一箱最多多重？", "一般 30-50kg 上限，超重分箱（分箱不收额外费）。"),
   ("合箱会被税吗？", "看总申报价值。¥1000 内免税，超了走包税渠道。我们按品类分开申报降低风险。"),
   ("合箱能省多少？", "通常省 20-40%（省首重+体积）。多件小包裹效果最明显。"),
   ("免费仓储多久？", "30 天。支持分批到货，集齐再发，错峰更划算。"),
   ("敏感货能合箱吗？", "可以，但敏感货单独成箱走专线，不和普货混（混了整箱被查风险高）。"),
   ("合箱后体积重变大怎么办？", "让仓库重新压实包装。我们打包时会优化装箱，避免体积重虚高。"),
   ("丢件/破损赔多少？", "按保价金额赔。建议高价值商品买保险（我们基础保险覆盖常规风险）。"),
   ("新手第一次集运注意什么？", "先小单试水（1-2 件），确认流程和时效，再批量寄。找客服要完整报价单。"),
 ],
 "en_sections": [
   ("What is consolidation?",
    "Consolidation = multiple parcels sent to a warehouse and shipped to China together. Consolidation = unpacking several small parcels and repacking them into one big box. Benefits: save the first-weight on every parcel, save volume (remove excess packaging), and unify declaration. We offer free consolidation."),
   ("Consolidation rules (must-read)",
    "1) Weight cap: usually 30-50kg per box; over that, split. 2) Volumetric weight: recalculated from the new box dimensions; over-packing can push it up. 3) Free storage: typically 15-30 days, then daily fees. 4) Sensitive goods can't mix with regular items in one box."),
   ("How to pack to save more",
    "1) Remove shoe boxes/gift boxes (the biggest volumetric source). 2) Vacuum-compress clothing. 3) Protect liquids/fragile items separately. 4) Use sturdy boxes + bubble wrap. 5) Fill all gaps — it reduces volumetric weight and prevents damage. Good packing saves 20-40%."),
   ("4 pitfalls to avoid",
    "1) Duty: keep total declared value under RMB 1,000 or use tax-inclusive. 2) Loss: insure high-value items. 3) Damage: reinforce fragile items. 4) Time: consolidation queues up in peak season — ship 1-2 weeks early."),
   ("How is consolidated pricing calculated?",
    "Rate ($/lb) × larger of actual/volumetric weight + surcharges (remote, sensitive). After consolidation, weight = sum of all parcels; volumetric = new box dimensions. We quote in 30 minutes with a fully transparent list."),
 ],
 "en_faq": [
   ("Is consolidation free?", "We consolidate for free. Some companies charge $3-5 per time — ask before choosing."),
   ("How long after consolidation?", "Air 7-10 working days; sea 25-35 days, counted from dispatch."),
   ("What's the max weight per box?", "Usually 30-50kg. Over that we split into two boxes (no extra split fee)."),
   ("Will consolidated boxes be taxed?", "Depends on declared value. Under RMB 1,000 duty-free; over that use tax-inclusive. We declare by category to reduce risk."),
   ("How much does consolidation save?", "Typically 20-40% (first-weight + volume savings). Most effective for many small parcels."),
   ("How long is free storage?", "30 days. Parcels can arrive in batches; ship when complete — off-peak is cheaper."),
   ("Can sensitive goods be consolidated?", "Yes, but they go in their own box on the dedicated line — never mixed with regular items (the whole box risks inspection)."),
   ("What if volumetric weight rises after consolidation?", "Ask the warehouse to repack tighter. We optimize packing to avoid inflated volumetric weight."),
   ("How much for loss/damage?", "Paid per insured value. Insure high-value items (our basic coverage handles standard risk)."),
   ("Tips for first-timers?", "Start with a small trial order (1-2 items) to confirm process and speed, then send in bulk. Ask for a full quote first."),
 ],
},
]

# ============ 渲染 ============
PERSON_EN = {"@context": "https://schema.org", "@type": "Person",
    "name": "Subao Global Logistics Editorial Team", "jobTitle": "Cross-border Logistics Content Editor",
    "description": "12+ years of international and cross-border shipping experience.",
    "knowsAbout": ["International Shipping", "US-China Logistics", "Customs Clearance", "Shopping Forwarding", "Daigou"]}
PERSON_ZH = {"@context": "https://schema.org", "@type": "Person",
    "name": "速豹国际物流编辑团队", "jobTitle": "跨境物流内容编辑",
    "description": "12年国际及跨境物流经验",
    "knowsAbout": ["国际物流", "中美物流", "关税清关", "海淘转运", "代购"]}

def sections_html(sections, zh=True):
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
    {sections_html(a['en_sections'], zh=False)}
    <div class="section-title" style="margin-top:44px"><h2>Frequently asked questions</h2></div>
    {faq_html(faq)}
    <div style="max-width:800px;margin:32px auto 0;padding:0 24px;font-size:13px;color:#64748B">Written by <strong>Subao Global Logistics Editorial Team</strong> · 12+ years international shipping experience · <a href="/en/about.html" style="color:#0066CC">About us</a></div>
  </div></section>
  {cta_html()}"""
    # Article + FAQPage + Person schema
    article = {"@context": "https://schema.org", "@type": "Article",
        "headline": a["en_h1"], "description": a["en_desc"],
        "datePublished": "2026-08-19", "dateModified": "2026-08-19",
        "author": {"@type": "Person", "name": "Subao Global Logistics Editorial Team"}}
    schema = f'{json.dumps(article)}\n  {faq_schema(faq)}\n  {json.dumps(PERSON_EN)}'
    Path(ROOT / "en" / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(ROOT / "en" / rel).write_text(render_page(rel, a["en_title"], a["en_desc"], body, schema), encoding="utf-8")
    print(f"✅ en/{rel}")

def gen_zh(a):
    slug = a["slug"]
    rel = f"blog/{slug}.html"
    zh_url = f"{DOMAIN}/zh-cn/{rel}"
    en_url = f"{DOMAIN}/en/{rel}"
    faq = a["zh_faq"]
    faq_schema_zh = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": aq}} for q, aq in faq]},
        ensure_ascii=False)
    article_zh = json.dumps({"@context": "https://schema.org", "@type": "Article",
        "headline": a["zh_h1"], "description": a["zh_desc"],
        "datePublished": "2026-08-19", "dateModified": "2026-08-19",
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
  <meta name="lastmod" content="2026-08-19">
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
    Path(ROOT / "zh-cn" / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(ROOT / "zh-cn" / rel).write_text(page, encoding="utf-8")
    print(f"✅ zh-cn/{rel}")

def main():
    print(f"共 {len(ARTICLES)} 篇 × 中英文")
    for a in ARTICLES:
        gen_en(a)
        gen_zh(a)
    print("完成")

if __name__ == "__main__":
    main()
