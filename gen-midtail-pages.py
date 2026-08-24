# -*- coding: utf-8 -*-
"""中词集群生成器：美淘转运子页(3) + cheapest-way(1)，中英对称。
模板复用疑问词页风格（hero + sections + 相关推荐 + FAQ + CTA + schema）。
"""
import json
from pathlib import Path

ROOT = Path(".")
DOMAIN = "https://subaog.com"
GA_ID = "G-DJGPMS9MOB"
PERSON_ZH = {"@type": "Person", "name": "速豹国际物流编辑团队"}
PERSON_EN = {"@type": "Person", "name": "Subao Global Logistics Editorial Team"}

# ===================== 数据 =====================
PAGES = [
# ---------- 1. Amazon 美亚淘 ----------
{
 "slug": "amazon-us-ship-to-china",
 "zh_h1": "从美国 Amazon 买东西寄回中国｜2026 转运全攻略",
 "zh_title": "从美国 Amazon 买东西寄回中国 2026｜转运/直邮对比+避坑",
 "zh_desc": "美国 Amazon 购物寄中国完整攻略：直邮 vs 转运怎么选、6 步流程、运费与体积重、关税避坑、哪些不能买 | 速豹国际物流 12年经验，全美免费取件，双清包税门到门",
 "zh_sections": [
   ("为什么大多数 Amazon 商品需要转运？", "Amazon 美国站很多商品（尤其是大件、第三方卖家、含电池/液体类）不提供直邮中国，或直邮运费高得离谱。转运=先把货寄到美国本地仓库，再由中国线统一发回，通常比直邮便宜 40-60%，也能寄直邮禁运的品类。"),
   ("Amazon 直邮 vs 转运 对比", "直邮：下单填中国地址，省心但运费高、品类受限、不退不换麻烦。转运：先寄美国仓再合箱发中国，便宜、可集货、可寄更多品类，但需要多一步操作。预算敏感、买多件、买大件，选转运。"),
   ("6 步流程", "① 在转运商处注册拿美国仓库地址 → ② Amazon 下单填该地址 → ③ 货到仓后入库（可拍照核对）→ ④ 提交转运订单、选渠道（空运/海运）→ ⑤ 支付运费、申报 → ⑥ 国内清关派送上门。全程可追踪。"),
   ("运费怎么算？体积重是关键", "国际物流按「实际重 vs 体积重」取大值。体积重=长×宽×高(cm)÷6000。泡货（枕头、玩具）体积重远大于实重，下单前用运费计算器预估，避免到仓才发现超预算。"),
   ("关税与申报", "个人自用、合理数量通常走行邮税或跨境电商综合税。如实申报、保留订单截图，不要瞒报。速豹双清包税渠道税费已含在运费里，到手价透明。"),
   ("避坑清单", "① 买前确认是否含电池/液体/粉末（直邮禁运，转运也要走敏感货渠道）② 大件先算体积重 ③ 多件合箱省运费 ④ 保留订单与付款凭证 ⑤ 选有美国仓+中文客服的转运商。"),
 ],
 "zh_faq": [
   ("美国 Amazon 能直邮中国吗？", "部分商品（标注 Ships to China）可以直邮，但运费高、品类受限。绝大多数第三方卖家商品不支持直邮，需要转运。"),
   ("转运安全吗？货会丢吗？", "选有实体美国仓、可入库拍照、全程追踪的转运商基本安全。贵重物品建议加保价，并保留订单凭证。"),
   ("从 Amazon 买的东西多久到？", "美国仓入库 1-3 天 + 国际运输 7-10 个工作日（空运），海运约 25-35 天。"),
   ("哪些 Amazon 商品不能寄中国？", "纯电池、充电宝、液体化妆品超量、刀具、动植物制品等受限制。下单前用「能不能寄」工具核对。"),
   ("转运比直邮能省多少？", "通常省 40-60%，买多件合箱后单位运费更低，大件差距更明显。"),
   ("怎么追踪我的包裹？", "入库后转运商提供单号，可在官网或客服处查询美国段+国际段状态。"),
 ],
 "en_h1": "Buying from Amazon US and Shipping to China: 2026 Guide",
 "en_title": "How to Ship Amazon US Purchases to China 2026 | Forwarding vs Direct",
 "en_desc": "Complete guide to buying on Amazon US and shipping to China: direct shipping vs package forwarding, 6-step process, cost and volumetric weight, customs tips | Subao Global, 12+ years, free US pickup, tax-inclusive door-to-door.",
 "en_sections": [
   ("Why most Amazon items need forwarding", "Many Amazon US items — bulky goods, third-party sellers, items with batteries/liquids — don't ship to China directly, or direct shipping is prohibitively expensive. Forwarding means shipping to a US warehouse first, then consolidating to China, typically 40-60% cheaper and able to carry more categories."),
   ("Direct shipping vs forwarding", "Direct: enter a China address at checkout — easy but costly, limited categories, awkward returns. Forwarding: ship to a US warehouse, consolidate, then forward — cheaper, supports more items, one extra step. Choose forwarding for budget, multiple items, or bulky goods."),
   ("6-step process", "① Register with a forwarder to get a US warehouse address → ② Enter that address on Amazon → ③ Goods arrive and are checked in (photos on request) → ④ Submit a forwarding order, pick air or sea → ⑤ Pay freight, declare → ⑥ Customs clearance and door delivery. Fully trackable."),
   ("Cost: volumetric weight matters", "Carriers bill the greater of actual vs volumetric weight. Volumetric = L×W×H(cm)÷6000. Bulky light items (pillows, toys) weigh far more volumetrically. Estimate with the shipping calculator before buying."),
   ("Customs & declaration", "Personal-use, reasonable quantities go through parcel or cross-border ecommerce tax. Declare truthfully, keep order screenshots. Subao's tax-inclusive line bundles duty into the freight — transparent landed cost."),
   ("Pitfall checklist", "① Check batteries/liquids/powders before buying ② Calculate volumetric weight for bulky items ③ Consolidate multiple items ④ Keep order & payment proof ⑤ Pick a forwarder with a US warehouse and Chinese support."),
 ],
 "en_faq": [
   ("Can Amazon US ship directly to China?", "Some items marked 'Ships to China' do, but costly and limited. Most third-party items don't — you'll need a forwarder."),
   ("Is forwarding safe? Will my goods get lost?", "A forwarder with a physical US warehouse, check-in photos, and full tracking is generally safe. Insure valuables and keep order proof."),
   ("How long does it take?", "Warehouse check-in 1-3 days + international transit 7-10 business days (air), ~25-35 days (sea)."),
   ("What Amazon items can't ship to China?", "Loose batteries, power banks, excess liquid cosmetics, knives, animal/plant products are restricted. Verify with the 'Can I ship?' tool first."),
   ("How much can forwarding save vs direct?", "Typically 40-60%, and more when consolidating multiple items; the gap is largest for bulky goods."),
   ("How do I track my parcel?", "After check-in you get a tracking number usable on the forwarder's site for both US and international legs."),
 ],
},
# ---------- 2. eBay 寄中国 ----------
{
 "slug": "ebay-ship-to-china",
 "zh_h1": "eBay 商品寄中国｜2026 转运攻略（二手/收藏/稀缺品）",
 "zh_title": "eBay 买的东西怎么寄到中国 2026｜转运流程+关税+避坑",
 "zh_desc": "eBay 商品寄中国完整攻略：为什么 eBay 多走转运、6 步流程、运费与关税、二手/收藏品注意、避坑 | 速豹国际物流 12年经验，全美免费取件，双清包税门到门",
 "zh_sections": [
   ("为什么 eBay 商品多走转运？", "eBay 卖家以个人/小商户为主，几乎都不提供直邮中国。无论买二手相机、绝版收藏、还是美国本土稀缺品，都需要先寄到美国转运仓再发回中国。"),
   ("6 步流程", "① 转运商注册拿美国仓地址 → ② eBay 下单填美国仓 → ③ 到仓入库、拍照核对（尤其二手/收藏品要验货）→ ④ 提交转运单、选渠道 → ⑤ 申报（二手按折旧值申报更合理）→ ⑥ 清关派送。"),
   ("二手/收藏品特别注意", "二手物品按「折旧后价值」申报比新品低，税费更省；收藏品、古董确认能否进口；到仓务必要求验货拍照，避免收到与描述不符的货。"),
   ("运费与体积重", "eBay 常见大件（音响、乐器、零件）体积重大，下单前用运费计算器预估。多件合箱能摊薄单件运费。"),
   ("关税申报技巧", "如实申报、保留 eBay 成交记录与付款截图。速豹双清包税渠道税费含在运费，到手价清楚。"),
   ("避坑清单", "① 买前确认卖家是否发美国本土（部分只发本国）② 大件先算体积重 ③ 二手要求折旧申报 ④ 到仓验货拍照 ⑤ 保留成交记录。"),
 ],
 "zh_faq": [
   ("eBay 能直邮中国吗？", "极少数卖家支持，绝大多数不支持。基本都需要转运。"),
   ("二手商品怎么申报关税？", "按折旧后实际价值申报更合理，税费更低；保留成交记录作为凭证。"),
   ("收藏品/古董能寄吗？", "多数可以，但部分受进出口管制，寄前确认品类并保留来源证明。"),
   ("到仓能验货吗？", "正规转运商会提供入库拍照、甚至验货服务，二手/收藏品强烈建议开启。"),
   ("运费大概多少？", "按实际重或体积重取大，多件合箱更划算，具体用运费计算器预估。"),
   ("要多久到？", "美国仓入库 1-3 天 + 空运 7-10 工作日，海运 25-35 天。"),
 ],
 "en_h1": "Shipping eBay Items to China: 2026 Guide",
 "en_title": "How to Ship eBay Purchases to China 2026 | Process, Customs, Tips",
 "en_desc": "Complete guide to shipping eBay items to China: why forwarding is standard, 6-step process, cost and customs for used/collectible goods, pitfalls | Subao Global, 12+ years, free US pickup, tax-inclusive door-to-door.",
 "en_sections": [
   ("Why eBay items almost always use forwarding", "eBay sellers are mostly individuals/small merchants who don't ship to China. Whether it's a used camera, a rare collectible, or a US-only item, goods must go to a US forwarding warehouse first."),
   ("6-step process", "① Register with a forwarder for a US address → ② Enter it on eBay → ③ Check-in and photo verification (essential for used/collectibles) → ④ Submit forwarding order, pick a channel → ⑤ Declare (used items at depreciated value) → ⑥ Clearance and delivery."),
   ("Used & collectible notes", "Declare used items at depreciated value — lower duty. Verify collectibles/antiques are importable. Always request check-in photos to avoid 'not as described' surprises."),
   ("Cost & volumetric weight", "eBay bulky items (audio, instruments, parts) are volume-heavy. Estimate with the calculator first; consolidate multiple items to spread cost."),
   ("Customs tips", "Declare truthfully, keep eBay order and payment records. Subao's tax-inclusive line bundles duty into freight."),
   ("Pitfall checklist", "① Confirm the seller ships within the US ② Calculate volumetric weight for bulky items ③ Request depreciated declaration for used goods ④ Get check-in photos ⑤ Keep transaction records."),
 ],
 "en_faq": [
   ("Does eBay ship directly to China?", "Very few sellers do; almost all require forwarding."),
   ("How to declare used items for duty?", "Declare at depreciated actual value — lower and more reasonable; keep the transaction record as proof."),
   ("Can collectibles/antiques ship?", "Usually yes, but some are import-controlled — confirm the category and keep provenance."),
   ("Can the warehouse inspect my goods?", "Reputable forwarders offer check-in photos and inspection — strongly recommended for used/collectibles."),
   ("How much does shipping cost?", "Billed on actual or volumetric weight, whichever is greater; consolidating multiple items is cheaper."),
   ("How long does it take?", "Check-in 1-3 days + 7-10 business days air, 25-35 days sea."),
 ],
},
# ---------- 3. 美国包裹/集货转运 ----------
{
 "slug": "us-package-forwarding",
 "zh_h1": "美国包裹转运（集货转运）服务是什么？2026 完整指南",
 "zh_title": "美国包裹转运/集货转运服务 2026｜怎么运作+省钱技巧",
 "zh_desc": "美国包裹转运（集货转运）完整指南：什么是转运、怎么运作、转运 vs 直邮对比、合箱省钱、适用人群 | 速豹国际物流 12年经验，全美免费取件，双清包税门到门",
 "zh_sections": [
   ("什么是美国包裹转运？", "转运（Package Forwarding）是给你一个美国本地仓库地址，电商包裹先寄到这个地址入库，再由转运商统一合箱、清关、发回中国。适合在多个美国网站购物后集中发回的人。"),
   ("转运怎么运作？", "注册→拿美国仓地址→各网站下单填该地址→到仓入库（可拍照/验货）→提交转运订单、选渠道→支付运费→清关派送。核心优势是「多件合箱」摊薄运费。"),
   ("转运 vs 直邮 对比", "直邮：单件直接发，方便但贵、品类受限。转运：多件合箱、可寄更多品类、单位运费低，适合买多件或买大件。只买一件小件且支持直邮时，直邮更省事。"),
   ("合箱怎么省钱？", "把 3-5 个包裹合为一个，只算一次国际运费+一次清关，单件成本大幅下降；泡货合箱效果最明显。注意合箱后体积重，避免反而变重。"),
   ("适用人群", "留学生/新移民回国采购、海淘族、代购、买美国本土稀缺品的人。在美有多笔订单、想集中发回中国的，转运最划算。"),
   ("避坑清单", "① 选有实体美国仓+中文客服的转运商 ② 到仓要求入库拍照 ③ 多件务必合箱 ④ 大件先算体积重 ⑤ 保留各网站订单凭证。"),
 ],
 "zh_faq": [
   ("转运和直邮哪个便宜？", "买多件或买大件，转运（尤其合箱）通常便宜 40-60%；单件小件且支持直邮时直邮更省事。"),
   ("合箱会让我多付体积重吗？", "合箱减少的是运费次数，但总体积重可能上升，合箱前用计算器预估，泡货注意。"),
   ("转运安全吗？", "有实体美国仓、可入库拍照、全程追踪的转运商基本安全；贵重物品加保价。"),
   ("谁最适合用转运？", "在美有多笔订单想集中发回、买大件/稀缺品、留学生回国采购的人。"),
   ("多久到？", "入库 1-3 天 + 空运 7-10 工作日，海运 25-35 天。"),
   ("怎么开始？", "注册转运商拿美国仓地址，下单填该地址，到仓后提交转运订单即可。"),
 ],
 "en_h1": "What Is US Package Forwarding? 2026 Complete Guide",
 "en_title": "US Package Forwarding & Consolidation 2026 | How It Works, Save Money",
 "en_desc": "Complete guide to US package forwarding and consolidation: what it is, how it works, forwarding vs direct shipping, consolidation savings, who it's for | Subao Global, 12+ years, free US pickup, tax-inclusive door-to-door.",
 "en_sections": [
   ("What is US package forwarding?", "Forwarding gives you a US warehouse address. E-commerce parcels ship there first, then the forwarder consolidates, clears, and sends them to China. Ideal for shopping across multiple US sites and shipping back together."),
   ("How it works", "Register → get a US address → enter it at checkout → goods checked in (photos/inspection on request) → submit a forwarding order, pick a channel → pay freight → clearance and delivery. The core advantage is consolidation that spreads cost."),
   ("Forwarding vs direct shipping", "Direct: single parcel straight, convenient but pricey and limited. Forwarding: consolidate multiple items, carry more categories, lower unit cost — best for multiple or bulky purchases. For one small direct-shippable item, direct is simpler."),
   ("How consolidation saves", "Merging 3-5 parcels into one means one international freight and one clearance — unit cost drops sharply; bulky items benefit most. Watch total volumetric weight after merging."),
   ("Who it's for", "Students/expats returning home, cross-border shoppers, agents, and anyone buying US-only items. If you have several US orders to send back together, forwarding wins."),
   ("Pitfall checklist", "① Pick a forwarder with a real US warehouse and Chinese support ② Request check-in photos ③ Always consolidate multiple items ④ Calculate volumetric weight for bulky goods ⑤ Keep each site's order proof."),
 ],
 "en_faq": [
   ("Is forwarding or direct cheaper?", "For multiple or bulky items, forwarding (especially consolidated) is typically 40-60% cheaper; for one small direct-shippable item, direct is simpler."),
   ("Will consolidation increase volumetric weight?", "It cuts shipping instances but total volumetric weight may rise — estimate with the calculator; watch bulky items."),
   ("Is forwarding safe?", "A forwarder with a real US warehouse, check-in photos, and full tracking is generally safe; insure valuables."),
   ("Who should use forwarding?", "Anyone with several US orders to send back together, bulky/rare-item buyers, returning students."),
   ("How long does it take?", "Check-in 1-3 days + 7-10 business days air, 25-35 days sea."),
   ("How do I start?", "Register, get a US address, enter it at checkout, then submit a forwarding order after check-in."),
 ],
},
# ---------- 4. cheapest-way ----------
{
 "slug": "cheapest-way-ship-to-china",
 "zh_h1": "美国寄中国最便宜的方式 2026｜5 种渠道对比+省钱技巧",
 "zh_title": "美国寄中国最便宜的方式 2026｜渠道对比+体积重+合箱省钱",
 "zh_desc": "美国寄中国最便宜的方式全解析：5 种渠道对比、什么时候用哪种、体积重怎么算、合箱与省钱技巧 | 速豹国际物流 12年经验，全美免费取件，双清包税门到门",
 "zh_sections": [
   ("5 种渠道一句话对比", "① 华人专线（双清包税）：21kg+ 最便宜，税费含运费 ② USPS：小件便宜但不稳、易丢 ③ FedEx/UPS：快但贵 ④ DHL：文件快、包裹贵 ⑤ 海运拼箱：大件最便宜但慢。追求性价比选华人专线。"),
   ("什么时候用哪种？", "小件<2kg 试试 USPS；急件选 FedEx/UPS；大件/行李/家具走华人专线或海运；文件选 DHL。多数个人寄送，华人专线综合最省。"),
   ("体积重是关键", "国际物流按「实际重 vs 体积重」取大，体积重=长×宽×高÷6000。泡货（枕头、玩具）体积重远大于实重，下单前用运费计算器预估，避免超预算。"),
   ("合箱摊薄运费", "多件合箱只算一次国际运费+一次清关，单件成本大降；泡货合箱效果最明显。注意合箱后总体积重。"),
   ("其他省钱技巧", "① 避开旺季（黑五/春节前运费涨）② 去多余包装减重 ③ 用双清包税渠道避免关税意外 ④ 长期寄送谈协议价 ⑤ 用计算器比价后再下单。"),
   ("为什么华人专线最划算", "华人专线针对中美线路优化，批量清关、包税、全美免费取件，21kg 以上单价远低于国际快递，且门到门省心。"),
 ],
 "zh_faq": [
   ("美国寄中国最便宜的方式是什么？", "21kg 以上走华人专线（双清包税）最便宜，单价远低于 FedEx/UPS/DHL，税费含在运费里。"),
   ("小件怎么寄最省？", "2kg 以下可试 USPS，但稳定性和丢件风险高；重视安全建议仍走专线。"),
   ("体积重怎么算？", "长×宽×高(cm)÷6000，与实际重取大值计费。泡货要特别留意。"),
   ("合箱能省多少？", "多件合箱只算一次国际段运费和清关，单件成本可降 30-50%。"),
   ("关税会额外收吗？", "双清包税渠道税费已含运费，无额外关税；非包税渠道可能到付。"),
   ("怎么比价？", "用运费计算器按实际重/体积重预估，再对比各渠道总价。"),
 ],
 "en_h1": "Cheapest Way to Ship from the USA to China (2026)",
 "en_title": "Cheapest Way to Ship to China from the USA 2026 | Compare & Save",
 "en_desc": "The cheapest way to ship from the USA to China: 5 channels compared, when to use which, volumetric weight, consolidation savings | Subao Global, 12+ years, free US pickup, tax-inclusive door-to-door.",
 "en_sections": [
   ("5 channels in one line", "① Chinese line (tax-inclusive): cheapest above 21kg, duty bundled ② USPS: cheap for small but unreliable, loss-prone ③ FedEx/UPS: fast but pricey ④ DHL: fast docs, pricey parcels ⑤ Sea LCL: cheapest for bulky but slow. For value, the Chinese line wins."),
   ("When to use which", "Small <2kg try USPS; urgent use FedEx/UPS; bulky/luggage/furniture use the Chinese line or sea; documents use DHL. For most personal shipments the Chinese line is the best all-round saver."),
   ("Volumetric weight is key", "Carriers bill the greater of actual vs volumetric weight (L×W×H÷6000). Bulky light items weigh far more volumetrically — estimate with the calculator before buying."),
   ("Consolidation spreads cost", "Merging items bills one international freight and one clearance — unit cost drops; bulky items benefit most. Watch total volumetric weight after merging."),
   ("Other saving tips", "① Avoid peak seasons (Black Friday/pre-Spring-Festival surcharges) ② Strip excess packaging ③ Use tax-inclusive lines to avoid duty surprises ④ Negotiate contract rates for volume ⑤ Compare with the calculator before ordering."),
   ("Why the Chinese line is cheapest", "Optimized for the US-China lane with batch clearance, duty included, and free US pickup — per-kg rates well below express, door-to-door."),
 ],
 "en_faq": [
   ("What's the cheapest way to ship to China?", "Above 21kg the Chinese tax-inclusive line is cheapest — far below FedEx/UPS/DHL, with duty bundled in."),
   ("How to save on small parcels?", "Under 2kg try USPS, but reliability and loss risk are higher; for peace of mind a line is advised."),
   ("How is volumetric weight calculated?", "L×W×H(cm)÷6000, billed as the greater of that and actual weight. Watch bulky items."),
   ("How much does consolidation save?", "One international freight and clearance for multiple items can cut unit cost 30-50%."),
   ("Will I pay duty separately?", "Tax-inclusive lines bundle duty into freight — no surprise charges; non-inclusive lines may collect on delivery."),
   ("How do I compare prices?", "Use the shipping calculator on actual/volumetric weight, then compare total channel cost."),
 ],
},
]

# ===================== 渲染 =====================
def sections_html(sections):
    out = ""
    for title, body in sections:
        out += f'\n    <div style="margin:28px 0"><h2 style="font-size:1.3rem;font-weight:700;color:var(--primary-dark);margin-bottom:10px">{title}</h2><p style="color:var(--text-secondary);line-height:1.9">{body}</p></div>'
    return out

def faq_html_zh(faq):
    return "".join(f'<div class="faq-item"><button class="faq-q">{q}<span>▼</span></button><div class="faq-a">{a}</div></div>' for q, a in faq)

def faq_schema(faq):
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}, ensure_ascii=False)

HTML_HEAD = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="alternate" hreflang="zh-CN" href="{zh_url}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="x-default" href="{zh_url}">
  <link rel="canonical" href="{canon}">
  <meta property="og:title" content="{h1}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{domain}/assets/images/og-image.jpg">
  <meta property="og:locale" content="{locale}">
  <meta name="lastmod" content="2026-08-22">
  <script type="application/ld+json">{article}</script>
  <script type="application/ld+json">{faq}</script>
  <script type="application/ld+json">{person}</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id={ga}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{ga}');</script>
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
"""

def render_zh(a):
    slug = a["slug"]
    rel = f"blog/{slug}.html"
    zh_url = f"{DOMAIN}/zh-cn/{rel}"
    en_url = f"{DOMAIN}/en/{rel}"
    article = json.dumps({"@context":"https://schema.org","@type":"Article","headline":a["zh_h1"],"description":a["zh_desc"],"datePublished":"2026-08-22","dateModified":"2026-08-22","author":{"@type":"Person","name":"速豹国际物流编辑团队"}}, ensure_ascii=False)
    faq = faq_schema(a["zh_faq"])
    person = json.dumps(PERSON_ZH, ensure_ascii=False)
    head = HTML_HEAD.format(lang="zh-CN", title=a["zh_title"], desc=a["zh_desc"], zh_url=zh_url, en_url=en_url, canon=zh_url, h1=a["zh_h1"], locale="zh_CN", domain=DOMAIN, ga=GA_ID, article=article, faq=faq, person=person)
    related = """
  <div style="background:var(--primary-light);border:1px solid #CDE3F5;border-radius:12px;padding:20px 24px;margin:32px 0">
    <div style="font-size:14px;font-weight:700;color:var(--primary-dark);margin-bottom:10px">📦 相关推荐</div>
    <a href="/zh-cn/blog/us-shopping-forwarding-guide.html" style="display:inline-block;margin:4px 8px 4px 0;padding:6px 14px;background:#fff;border:1px solid var(--primary);border-radius:20px;font-size:13px;color:var(--primary);text-decoration:none;font-weight:600">美国海淘转运全攻略 →</a>
    <a href="/zh-cn/blog/can-i-ship-electronics-to-china.html" style="display:inline-block;margin:4px 8px 4px 0;padding:6px 14px;background:#fff;border:1px solid var(--primary);border-radius:20px;font-size:13px;color:var(--primary);text-decoration:none;font-weight:600">纽约寄电子产品回国 →</a>
    <a href="/zh-cn/tools/shipping-calculator.html" style="display:inline-block;margin:4px 8px 4px 0;padding:6px 14px;background:#fff;border:1px solid var(--primary);border-radius:20px;font-size:13px;color:var(--primary);text-decoration:none;font-weight:600">运费计算器 →</a>
    <a href="/zh-cn/blog/can-i-ship-electronics-to-china.html" style="display:inline-block;margin:4px 8px 4px 0;padding:6px 14px;background:#fff;border:1px solid var(--primary);border-radius:20px;font-size:13px;color:var(--primary);text-decoration:none;font-weight:600">电子产品能不能寄 →</a>
  </div>"""
    faq_html = faq_html_zh(a["zh_faq"])
    body = f"""<body>
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
    {sections_html(a['zh_sections'])}
    {related}
    <div class="section-title" style="margin-top:44px"><h2>常见问题</h2></div>
    {faq_html}
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
</body></html>"""
    (ROOT / "zh-cn" / rel).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "zh-cn" / rel).write_text(head + body, encoding="utf-8")
    print(f"✅ zh-cn/{rel}")

def render_en(a):
    slug = a["slug"]
    rel = f"blog/{slug}.html"
    zh_url = f"{DOMAIN}/zh-cn/{rel}"
    en_url = f"{DOMAIN}/en/{rel}"
    article = json.dumps({"@context":"https://schema.org","@type":"Article","headline":a["en_h1"],"description":a["en_desc"],"datePublished":"2026-08-22","dateModified":"2026-08-22","author":{"@type":"Person","name":"Subao Global Logistics Editorial Team"}})
    faq = faq_schema(a["en_faq"])
    person = json.dumps(PERSON_EN)
    head = HTML_HEAD.format(lang="en", title=a["en_title"], desc=a["en_desc"], zh_url=zh_url, en_url=en_url, canon=en_url, h1=a["en_h1"], locale="en_US", domain=DOMAIN, ga=GA_ID, article=article, faq=faq, person=person)
    related = """
  <div style="background:var(--primary-light);border:1px solid #CDE3F5;border-radius:12px;padding:20px 24px;margin:32px 0">
    <div style="font-size:14px;font-weight:700;color:var(--primary-dark);margin-bottom:10px">📦 Related</div>
    <a href="/en/blog/us-shopping-forwarding-guide.html" style="display:inline-block;margin:4px 8px 4px 0;padding:6px 14px;background:#fff;border:1px solid var(--primary);border-radius:20px;font-size:13px;color:var(--primary);text-decoration:none;font-weight:600">US Shopping Forwarding Guide →</a>
    <a href="/en/blog/can-i-ship-electronics-to-china.html" style="display:inline-block;margin:4px 8px 4px 0;padding:6px 14px;background:#fff;border:1px solid var(--primary);border-radius:20px;font-size:13px;color:var(--primary);text-decoration:none;font-weight:600">Ship Electronics NY→China →</a>
    <a href="/en/tools/shipping-calculator.html" style="display:inline-block;margin:4px 8px 4px 0;padding:6px 14px;background:#fff;border:1px solid var(--primary);border-radius:20px;font-size:13px;color:var(--primary);text-decoration:none;font-weight:600">Shipping calculator →</a>
    <a href="/en/blog/can-i-ship-electronics-to-china.html" style="display:inline-block;margin:4px 8px 4px 0;padding:6px 14px;background:#fff;border:1px solid var(--primary);border-radius:20px;font-size:13px;color:var(--primary);text-decoration:none;font-weight:600">Can I ship electronics? →</a>
  </div>"""
    faq_html = "".join(f'<div class="faq-item"><button class="faq-q">{q}<span>▼</span></button><div class="faq-a">{a}</div></div>' for q, a in a["en_faq"])
    body = f"""<body>
  <header class="header"><div class="container">
    <a href="/en/" class="logo">Subao Global<span style="font-size:11px;color:var(--text-secondary);margin-left:8px">USA to China</span></a>
    <nav class="nav">
      <a href="/en/">Home</a><a href="/en/usa-to-china/">USA to China</a>
      <a href="/en/tools/">Tools</a><a href="/en/blog/" class="active">Guides</a>
      <a href="{zh_url}" class="lang-switch" hreflang="zh-CN">🌐 English / 中文</a>
    </nav>
  </div></header>
  <section class="hero"><div class="container"><h1>{a['en_h1']}</h1><p class="subtitle">{a['en_desc'][:130]}</p></div></section>
  <section class="section"><div class="container" style="max-width:820px">
    {sections_html(a['en_sections'])}
    {related}
    <div class="section-title" style="margin-top:44px"><h2>FAQ</h2></div>
    {faq_html}
    <div style="max-width:800px;margin:32px auto 0;padding:0 24px;font-size:13px;color:#64748B">By <strong>Subao Global Logistics Editorial Team</strong> · 12+ years shipping experience · <a href="/en/about.html" style="color:#0066CC">About us</a></div>
  </div></section>
  <section class="cta-section"><div class="container">
    <h2>Plan in 30 minutes, free pickup</h2>
    <p>Tax-inclusive door-to-door · Free US pickup · Fully trackable</p>
    <a href="https://d.salesmartly.com/fuxikn" class="btn-primary" target="_blank" rel="noopener">💬 Free consult</a>
  </div></section>
  <footer class="footer"><div class="container">© 2026 Subao Global Logistics | <a href="/en/">Home</a> · <a href="/sitemap.xml">Sitemap</a></div></footer>
  <script>
    document.querySelectorAll('.faq-q').forEach(function(q){{q.addEventListener('click',function(){{var a=q.nextElementSibling;a.classList.toggle('show');q.querySelector('span').textContent=a.classList.contains('show')?'▲':'▼';}});}});
  </script>
</body></html>"""
    (ROOT / "en" / rel).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "en" / rel).write_text(head + body, encoding="utf-8")
    print(f"✅ en/{rel}")

def main():
    print(f"共 {len(PAGES)} 个中词页 × 中英")
    for a in PAGES:
        render_zh(a)
        render_en(a)
    print("完成")

if __name__ == "__main__":
    main()
