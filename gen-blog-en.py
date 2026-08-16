# -*- coding: utf-8 -*-
"""
subaog.com 英文站 Blog 生成器（Stage 5，23 篇）
每篇差异化内容：title/meta/H1/intro/sections/FAQ + Article Schema。
"""
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("gec", "gen-en-content.py")
gec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gec)

EN = gec.EN
render_page = gec.render_page
faq_html = gec.faq_html
faq_schema = gec.faq_schema
cta_html = gec.cta_html

# 每篇：slug, title, desc, h1, intro, [(h2, content)], [(q, a)]
BLOG = [
    {
        "slug": "can-i-ship-supplements-to-china.html",
        "title": "Can I Ship Supplements to China? Rules & Tips (2026) | Subao Global",
        "desc": "Shipping supplements and vitamins to China — what's allowed, duty rates, quantity limits, and how to pack. Complete guide for overseas buyers.",
        "h1": "Can I Ship Supplements to China?",
        "intro": "Supplements and vitamins are among the most-shipped items to China, but the rules aren't always obvious. Here's what you need to know before you ship.",
        "sections": [
            ("Which supplements can I ship?",
             "Most over-the-counter vitamins, fish oil, probiotics, and protein powder are allowed. Prescription medication and items containing controlled ingredients may need documentation. Always share the ingredient list with us before shipping."),
            ("How much duty will I pay?",
             "Supplements fall under the food/health product category with a duty rate around 20%. Personal-use quantities under RMB 1,000 are duty-free. Larger shipments may attract duty — our tax-inclusive service handles this for you."),
            ("How should I pack supplements?",
             "Keep products in original packaging, seal liquids in ziplock bags, and use cushioning to prevent crushing. Declare the full ingredient list to avoid customs delays."),
        ],
        "faq": [
            ("How many supplements can I ship to China?",
             "There's no hard limit for personal use, but very large quantities may be treated as commercial imports and attract higher duty. Keep it reasonable (a few months' supply)."),
            ("How long do supplements take to arrive?",
             "Air freight takes 10–15 working days door-to-door. Sea freight takes 25–35 days."),
        ],
    },
    {
        "slug": "can-i-ship-cosmetics-to-china.html",
        "title": "Can I Ship Cosmetics to China? Complete Guide (2026) | Subao Global",
        "desc": "Shipping cosmetics and skincare to China — what's allowed, duty rates (up to 50%), and packing tips. Avoid customs rejection with this guide.",
        "h1": "Can I Ship Cosmetics to China?",
        "intro": "Cosmetics are hugely popular for China-bound shipments — but they carry one of the highest duty rates and some restrictions. Here's how to ship them right.",
        "sections": [
            ("Which cosmetics can I ship?",
             "Creams, serums, makeup, and skincare are generally allowed. Aerosols (sprays) and large liquid volumes need special handling. Nail polish and perfume are restricted on air freight — ask us first."),
            ("What's the duty rate on cosmetics?",
             "Cosmetics carry a 50% duty rate in China — the highest common category. Personal items under RMB 1,000 are duty-free, but anything over that can get expensive. Our tax-inclusive service covers standard duty."),
            ("Packing tips for cosmetics",
             "Wrap glass bottles in bubble wrap, seal liquids in ziplock bags, and mark the box 'FRAGILE'. Keep items in original packaging to speed up customs."),
        ],
        "faq": [
            ("Can I ship perfume or nail polish to China?",
             "Perfume and nail polish contain alcohol and are restricted on air freight. Sea freight may be an option. Contact us with the specific product for a check."),
            ("How much duty will I pay on cosmetics?",
             "Cosmetics are taxed at 50% on the value above the RMB 1,000 personal allowance. Our tax-inclusive service covers this."),
        ],
    },
    {
        "slug": "can-i-ship-electronics-to-china.html",
        "title": "Can I Ship Electronics to China? Rules & Duty (2026) | Subao Global",
        "desc": "Shipping electronics to China — what's allowed, battery restrictions, duty rates (15%), and packing. Laptops, phones, cameras and more.",
        "h1": "Can I Ship Electronics to China?",
        "intro": "Electronics are one of the most common China-bound shipments, but batteries and import duty need special attention. Here's the complete picture.",
        "sections": [
            ("Which electronics can I ship?",
             "Laptops, phones, cameras, and accessories are allowed. Items with lithium batteries need declaration and are restricted on air freight — built-in batteries are easier than loose batteries."),
            ("What's the duty rate on electronics?",
             "Electronics are taxed at 15% on value above the RMB 1,000 personal allowance. A single personal laptop is usually treated as personal effects and duty-free."),
            ("How to pack electronics safely",
             "Use anti-static bags, original packaging where possible, and plenty of cushioning. Remove or declare batteries. Mark the box 'FRAGILE — ELECTRONICS'."),
        ],
        "faq": [
            ("Can I ship a laptop to China?",
             "Yes. A single personal laptop is usually duty-free. Declare it as personal effects and we'll handle the paperwork."),
            ("Are batteries allowed?",
             "Built-in batteries are generally OK with declaration. Loose lithium batteries are restricted on air freight — ask us for the latest rules."),
        ],
    },
    {
        "slug": "can-i-ship-luxury-bags-to-china.html",
        "title": "Can I Ship Luxury Bags to China? Duty & Rules (2026) | Subao Global",
        "desc": "Shipping luxury handbags and watches to China — duty rates (up to 30%), authenticity documents, and how to ship high-value items safely.",
        "h1": "Can I Ship Luxury Bags to China?",
        "intro": "Luxury goods are a high-value, high-duty category. If you're shipping a designer bag or watch to China, here's what you need to know.",
        "sections": [
            ("What's the duty rate on luxury goods?",
             "Luxury bags and watches are taxed at 30% on value above the RMB 1,000 allowance. On a $2,000 bag, duty could be several hundred dollars — factor this into your decision."),
            ("Do I need authenticity documents?",
             "Yes. Customs may request proof of authenticity and purchase receipts for high-value items. Keep original receipts and authenticity cards."),
            ("Should I insure luxury shipments?",
             "Absolutely. We strongly recommend insurance for items over $500. Ask for coverage details when booking — we'll advise the right level."),
        ],
        "faq": [
            ("How much duty will I pay on a luxury bag?",
             "Luxury goods are taxed at 30% on value above RMB 1,000. A $2,000 bag could attract roughly $300–500 in duty. We'll estimate it for you before shipping."),
            ("Is insurance available?",
             "Yes. Optional insurance is available for high-value items. We recommend it for anything over $500."),
        ],
    },
    {
        "slug": "can-i-ship-baby-formula-to-china.html",
        "title": "Can I Ship Baby Formula to China? Complete Guide (2026) | Subao Global",
        "desc": "Shipping baby formula and infant food to China — quantity limits, duty, and packing. Popular from Australia, the US and Europe.",
        "h1": "Can I Ship Baby Formula to China?",
        "intro": "Baby formula is one of the most-shipped items to China from Australia, the US and Europe. Here's what you need to know about limits and duty.",
        "sections": [
            ("Are there quantity limits?",
             "There's no strict legal limit for personal use, but very large quantities may be treated as commercial imports. A reasonable amount (a few cans/tins) is fine."),
            ("What's the duty on baby formula?",
             "Baby formula is classified as food, taxed at around 20% on value above the RMB 1,000 allowance. Personal quantities are often duty-free."),
            ("How to pack formula",
             "Keep tins in original packaging, cushion them well, and avoid crushing. Declare the product clearly as 'infant formula' to speed up customs."),
        ],
        "faq": [
            ("Can I ship baby formula from Australia to China?",
             "Yes — this is one of our most popular routes. Air freight takes 10–15 working days."),
            ("Is there a duty-free allowance?",
             "Personal items under RMB 1,000 are duty-free. Reasonable personal quantities of formula usually clear without duty."),
        ],
    },
    {
        "slug": "usps-vs-fedex-vs-chinese-courier.html",
        "title": "USPS vs FedEx vs Chinese Courier: Cheapest Way to Ship to China (2026)",
        "desc": "Compare USPS, FedEx, UPS and Chinese consolidated couriers for shipping to China. See cost, speed, and which is cheapest for your package size.",
        "h1": "USPS vs FedEx vs Chinese Courier: Which Is Best?",
        "intro": "Shipping to China? The channel you pick can change your cost by 40–60%. Here's a straight comparison of USPS, FedEx/UPS, and Chinese consolidated couriers.",
        "sections": [
            ("Cost comparison",
             "USPS is cheapest for tiny parcels (under 2kg) at $15–30. FedEx/UPS charge $60–120 for the same weight. Chinese consolidated couriers charge $4–6 per pound for medium and large parcels — the clear winner for anything over 5kg."),
            ("Speed comparison",
             "FedEx/UPS are fastest (3–5 days) but expensive. USPS takes 7–14 days. Chinese couriers take 10–15 working days door-to-door — a good balance of cost and speed."),
            ("When to choose what",
             "Tiny and urgent → USPS. Very urgent and money is no object → FedEx. Medium/large, cost-sensitive, or household goods → Chinese consolidated courier. That's where Subao Global sits."),
        ],
        "faq": [
            ("What's the cheapest way to ship to China?",
             "For parcels over 5kg, Chinese consolidated couriers are 40–60% cheaper than USPS/FedEx. For tiny items under 2kg, USPS is competitive."),
            ("How long does a Chinese courier take?",
             "10–15 working days door-to-door via air freight. Sea freight takes 25–35 days."),
        ],
    },
    {
        "slug": "international-customs-duty-guide.html",
        "title": "China Customs Duty: Complete Guide for Importers (2026) | Subao Global",
        "desc": "Understand China import duty — the RMB 1,000 personal allowance, duty rates by category, and how tax-inclusive shipping works.",
        "h1": "China Customs Duty: A Complete Guide",
        "intro": "China customs duty confuses many first-time shippers. Here's a clear breakdown of allowances, rates, and how to avoid surprise bills.",
        "sections": [
            ("The personal allowance",
             "Personal items valued under RMB 1,000 (about $140) are duty-free. This applies to shipments for personal use. Items above this threshold are taxed on the excess."),
            ("Duty rates by category",
             "Clothing 20%, cosmetics 50%, electronics 15%, luxury goods 30%, books 15%. Used personal items (worn clothes, used books) are usually duty-free."),
            ("How tax-inclusive shipping works",
             "Our tax-inclusive service bundles standard duty into one all-in price. You pay once, and we handle the customs paperwork — no surprise bills at delivery."),
        ],
        "faq": [
            ("What is the duty-free allowance for China?",
             "Personal items under RMB 1,000 (about $140) are duty-free. Hong Kong, Macau and Taiwan shipments have an RMB 800 allowance."),
            ("Will I get a surprise duty bill?",
             "Not with our tax-inclusive service. Standard duty is included in your quote."),
        ],
    },
    {
        "slug": "prohibited-items-complete-guide.html",
        "title": "Prohibited Items to China: Complete List (2026) | Subao Global",
        "desc": "What can't be shipped to China — the complete prohibited and restricted items list. Avoid customs rejection and fines.",
        "h1": "Prohibited Items: What You Can't Ship to China",
        "intro": "Shipping the wrong item can cause rejection, fines, or worse. Here's the definitive list of what can and can't go to China.",
        "sections": [
            ("Absolutely prohibited",
             "Weapons and ammunition, drugs and narcotics, fresh food and meat, live animals, and politically sensitive materials are strictly prohibited — no exceptions."),
            ("Restricted items",
             "Batteries (declaration required), liquids (limited volumes), luxury goods (higher duty), and prescription medication (documentation required). These are shippable with care."),
            ("What happens if I ship a prohibited item?",
             "The shipment can be seized or returned, and you may face fines. Always check with us before shipping anything unusual — it takes 30 seconds."),
        ],
        "faq": [
            ("Can I ship food to China?",
             "Packaged, shelf-stable food is usually fine. Fresh food, meat and fruit are prohibited."),
            ("Can I ship batteries?",
             "Built-in batteries are generally OK with declaration. Loose lithium batteries are restricted on air freight."),
        ],
    },
    {
        "slug": "how-to-pack-for-international-shipping.html",
        "title": "How to Pack for International Shipping to China (2026) | Subao Global",
        "desc": "The complete packing guide — box selection, fragile items, clothes, volumetric weight, and the 6 rules that prevent damage.",
        "h1": "How to Pack for International Shipping",
        "intro": "Good packing is the difference between your items arriving intact or in pieces. Follow these six rules.",
        "sections": [
            ("Choose the right box",
             "Use double-wall corrugated boxes for anything over 10kg. Standard moving boxes (60×40×40cm) work well. Never reuse a damaged box."),
            ("Protect fragile items",
             "Wrap each item in bubble wrap, fill empty space so nothing shifts, and mark the box 'FRAGILE'. If it rattles, it breaks."),
            ("Mind volumetric weight",
             "Volumetric weight = L × W × H (cm) ÷ 5000. Carriers charge the higher of actual or volumetric weight. Vacuum-pack clothes to cut volume."),
        ],
        "faq": [
            ("What is volumetric weight?",
             "It's a measure of how much space a package takes: L × W × H ÷ 5000. You pay for whichever is higher — actual or volumetric weight."),
            ("How heavy can a box be?",
             "Keep each box under 25kg. Overweight boxes risk damage and extra fees."),
        ],
    },
    {
        "slug": "usa-to-china-cheapest-way.html",
        "title": "Cheapest Way to Ship from USA to China (2026) | Subao Global",
        "desc": "The cheapest way to ship from the USA to China — by weight and urgency. Save 40–60% vs USPS/FedEx with consolidated shipping.",
        "h1": "Cheapest Way to Ship from the USA to China",
        "intro": "The cheapest shipping method depends on how much you're sending and how fast you need it. Here's the breakdown.",
        "sections": [
            ("Small parcels (under 2kg)",
             "USPS First Class is cheapest at $15–30. But for anything heavier, the per-pound math changes fast."),
            ("Medium parcels (2–20kg)",
             "Chinese consolidated air freight wins here at roughly $4–6 per pound — 40–60% cheaper than FedEx/UPS."),
            ("Large shipments (50kg+)",
             "Sea freight is the cheapest at $2–4 per pound. Slower (25–35 days) but unbeatable for moving or bulk shipping."),
        ],
        "faq": [
            ("What's the absolute cheapest way to ship to China?",
             "Sea freight for large/heavy shipments (25–35 days), or consolidated air freight for medium parcels (10–15 days)."),
            ("How much can I save vs FedEx?",
             "Typically 40–60% on medium and large parcels."),
        ],
    },
    {
        "slug": "usa-to-china-sea-freight.html",
        "title": "USA to China Sea Freight: Costs & Timeline (2026) | Subao Global",
        "desc": "Sea freight from the USA to China — costs from $6.5/kg, 25–35 day timeline, and when it beats air freight for moving and bulk shipping.",
        "h1": "USA to China Sea Freight",
        "intro": "Sea freight is the cheapest way to move large volumes from the USA to China — if you can wait 25–35 days.",
        "sections": [
            ("What does sea freight cost?",
             "Sea freight starts at about $6.5/kg for shipments over 21kg. For full moves and furniture, per-kg rates drop further with volume."),
            ("How long does sea freight take?",
             "25–35 days door-to-door, including US pickup, ocean transit, China customs, and final delivery. Air freight is 10–15 days for comparison."),
            ("When to choose sea freight",
             "Choose sea freight for furniture, household goods, bulk books, and anything heavy where you don't need speed. Air freight wins when time matters."),
        ],
        "faq": [
            ("How long does sea freight from the USA take?",
             "25–35 days door-to-door. Air freight is 10–15 days."),
            ("Is sea freight cheaper than air?",
             "Yes — roughly 40% cheaper per kg for large shipments."),
        ],
    },
    {
        "slug": "usa-to-china-customs-duty.html",
        "title": "USA to China Customs Duty: What You'll Pay (2026) | Subao Global",
        "desc": "USA to China customs duty explained — the RMB 1,000 allowance, category rates, and how to avoid surprise bills.",
        "h1": "USA to China Customs Duty",
        "intro": "Wondering if your USA shipment will be taxed in China? Here's the simple version.",
        "sections": [
            ("The allowance",
             "Personal items under RMB 1,000 (about $140) are duty-free. This covers most small personal shipments."),
            ("Category rates",
             "Clothing 20%, cosmetics 50%, electronics 15%, luxury goods 30%. Used personal items are usually duty-free."),
            ("Avoid surprises",
             "Ship used items as 'personal effects', keep values reasonable, and use our tax-inclusive service to bundle duty into one price."),
        ],
        "faq": [
            ("Will I pay duty on used clothes?",
             "Usually not. Used personal items are typically duty-free."),
            ("How is duty calculated?",
             "Duty = (declared value − RMB 1,000) × category rate. We'll estimate it for you."),
        ],
    },
    {
        "slug": "usa-to-china-prohibited-items.html",
        "title": "USA to China Prohibited Items: What Not to Ship (2026) | Subao Global",
        "desc": "What you can't ship from the USA to China — prohibited and restricted items list to avoid customs rejection.",
        "h1": "USA to China Prohibited Items",
        "intro": "Some items can't go from the USA to China, period. Here's what to avoid.",
        "sections": [
            ("Prohibited",
             "Weapons, drugs, fresh food and meat, live animals, and politically sensitive materials are strictly banned."),
            ("Restricted",
             "Batteries (declare them), liquids (limited), prescription medication (documentation required), and luxury goods (higher duty)."),
            ("Common mistakes",
             "People often forget that aerosols and loose lithium batteries can't go by air. When in doubt, ask us first."),
        ],
        "faq": [
            ("Can I ship alcohol to China?",
             "Limited quantities are possible, but alcohol is heavily restricted and taxed. Ask us before shipping."),
            ("Can I ship meat or fresh food?",
             "No — fresh food and meat are prohibited."),
        ],
    },
    {
        "slug": "usa-to-china-packaging-guide.html",
        "title": "USA to China Packing Guide (2026) | Subao Global",
        "desc": "How to pack a USA to China shipment — box selection, fragile items, and the rules that prevent damage.",
        "h1": "USA to China Packing Guide",
        "intro": "Your package travels thousands of miles. Pack it right with these rules.",
        "sections": [
            ("Box selection",
             "Double-wall boxes for anything heavy, single-wall for clothes. Keep boxes under 25kg."),
            ("Fragile items",
             "Bubble wrap each item, fill void space, and mark 'FRAGILE'."),
            ("Volumetric weight",
             "L × W × H ÷ 5000. Vacuum-pack clothes to reduce volume and cost."),
        ],
        "faq": [
            ("What size box should I use?",
             "Standard moving boxes (60×40×40cm) work well for most items. Keep each box under 25kg."),
            ("How do I protect fragile items?",
             "Bubble wrap + void fill + 'FRAGILE' label. Nothing should move when you shake the box."),
        ],
    },
    {
        "slug": "usa-moving-to-china-guide.html",
        "title": "Moving from USA to China: Complete Guide (2026) | Subao Global",
        "desc": "Moving from the USA to China — furniture, household goods, costs, timeline, and how sea freight works for a full move.",
        "h1": "Moving from the USA to China",
        "intro": "Moving home is a big job. Here's how to ship furniture and household goods from the USA to China without the stress.",
        "sections": [
            ("What can you move?",
             "Furniture, appliances, clothing, books, kitchenware — essentially everything in a home. Used household goods are usually duty-free."),
            ("Sea vs air for moving",
             "Sea freight is the cost-effective choice for moves (25–35 days). Air freight (10–15 days) suits smaller, time-sensitive moves."),
            ("What does a move cost?",
             "Sea freight from about $6.5/kg, with better rates on large volume. Get a free quote with your item list."),
        ],
        "faq": [
            ("How much does moving from the USA cost?",
             "Sea freight from about $6.5/kg. Large moves get volume discounts."),
            ("Are used household goods taxed?",
             "Usually not — used personal household goods are typically duty-free."),
        ],
    },
    {
        "slug": "student-luggage-shipping-guide.html",
        "title": "Student Luggage to China: Complete Guide (2026) | Subao Global",
        "desc": "Ship student luggage to China — costs, free boxes, student discounts, and how to pack books and clothes for the trip home.",
        "h1": "Student Luggage to China: A Complete Guide",
        "intro": "Heading home after studying abroad? Here's how to ship your books, clothes and personal items to China cheaply and safely.",
        "sections": [
            ("What can students ship?",
             "Books, clothes, shoes, bedding, small electronics and personal effects. Used personal items are usually duty-free."),
            ("What does it cost?",
             "Air freight from about $9/kg (21kg+). Sea freight from $5/kg. Student discounts apply during graduation season."),
            ("Free boxes and pickup",
             "We supply free boxes and packing materials, and offer free pickup from your dorm or apartment."),
        ],
        "faq": [
            ("Is there a student discount?",
             "Yes — special rates apply during graduation season. Ask for a quote."),
            ("How long does student luggage take?",
             "Air freight 10–15 working days. Sea freight 25–35 days."),
        ],
    },
    {
        "slug": "student-luggage-express-comparison.html",
        "title": "Student Luggage: Courier vs Consolidated Shipping (2026) | Subao Global",
        "desc": "Compare express couriers vs consolidated shipping for student luggage to China. Save 40–60% with the right choice.",
        "h1": "Student Luggage: Courier vs Consolidated",
        "intro": "Shipping student luggage home? The choice between express couriers and consolidated shipping can save you hundreds.",
        "sections": [
            ("Express couriers (FedEx/UPS/DHL)",
             "Fast (3–5 days) but expensive — often $8–12 per kg for student luggage. Best only for a few urgent items."),
            ("Consolidated shipping",
             "10–15 working days at $4–6 per kg — 40–60% cheaper. The smart choice for books, clothes and most student luggage."),
            ("Which should you choose?",
             "For most students, consolidated shipping is the clear winner. Reserve express for a single urgent item."),
        ],
        "faq": [
            ("How much can I save?",
             "Typically 40–60% vs FedEx/UPS/DHL on student luggage."),
            ("Is consolidated shipping reliable?",
             "Yes — with full tracking and tax-inclusive customs, it's our most popular student service."),
        ],
    },
    {
        "slug": "how-to-choose-international-shipping-method.html",
        "title": "How to Choose an International Shipping Method (2026) | Subao Global",
        "desc": "Air vs sea vs express — how to choose the right international shipping method for cost, speed, and your items.",
        "h1": "How to Choose a Shipping Method",
        "intro": "Air, sea, or express? The right choice depends on three things: weight, urgency, and item type.",
        "sections": [
            ("Consider weight",
             "Under 2kg → express or USPS. 2–50kg → consolidated air. 50kg+ → sea freight. Weight is the biggest cost driver."),
            ("Consider urgency",
             "Need it in days → express. Can wait 10–15 days → air. Can wait a month → sea. Slower almost always means cheaper."),
            ("Consider item type",
             "Fragile or time-sensitive → air. Bulky furniture → sea. High-value small items → express with insurance."),
        ],
        "faq": [
            ("What's the fastest shipping method?",
             "Express couriers (3–5 days). Consolidated air is 10–15 days, sea 25–35 days."),
            ("What's the cheapest?",
             "Sea freight for heavy items, consolidated air for medium parcels."),
        ],
    },
    {
        "slug": "international-shipping-insurance-guide.html",
        "title": "International Shipping Insurance: Do You Need It? (2026) | Subao Global",
        "desc": "Is international shipping insurance worth it? What it covers, what it costs, and when to insure your China-bound shipment.",
        "h1": "International Shipping Insurance",
        "intro": "Lost or damaged parcels are rare but possible. Here's when insurance is worth it.",
        "sections": [
            ("What insurance covers",
             "Loss, theft, and damage during transit. Coverage is based on declared value."),
            ("What it costs",
             "Typically 1–3% of declared value. A $500 shipment costs about $5–15 to insure."),
            ("When to insure",
             "Insure anything over $500, fragile items, and one-of-a-kind or irreplaceable items. Skip it for low-value, easily replaced goods."),
        ],
        "faq": [
            ("How much does insurance cost?",
             "Usually 1–3% of declared value."),
            ("Is insurance required?",
             "No, but we recommend it for items over $500."),
        ],
    },
    {
        "slug": "japan-to-china-shipping-guide.html",
        "title": "Japan to China Shipping: Complete Guide (2026) | Subao Global",
        "desc": "Ship from Japan to China — costs, timeline, popular items (cosmetics, electronics, snacks), and how the process works.",
        "h1": "Japan to China Shipping Guide",
        "intro": "Japan to China is one of our fastest and most popular routes. Here's everything you need to know.",
        "sections": [
            ("What can you ship from Japan?",
             "Cosmetics, electronics, snacks, clothing, and personal effects. Japanese cosmetics and electronics are the most-shipped categories."),
            ("Cost and timeline",
             "Air freight from about $9/kg (21kg+), 7–12 working days. Sea freight from $5/kg, 18–25 days."),
            ("How it works",
             "Book a pickup in Tokyo, Osaka, Kyoto or other major cities — free of charge. We handle Japan export and China import customs."),
        ],
        "faq": [
            ("How long does Japan to China take?",
             "7–12 working days by air freight."),
            ("Can I ship Japanese cosmetics?",
             "Yes — cosmetics are a core category. Some aerosols and large liquids need special handling."),
        ],
    },
    {
        "slug": "shipping-from-asia-to-china-comparison.html",
        "title": "Shipping from Asia to China: Japan vs Korea vs SE Asia (2026)",
        "desc": "Compare shipping from Japan, Korea and Southeast Asia to China — costs, speed, and which route is best for your items.",
        "h1": "Shipping from Asia to China Compared",
        "intro": "Shipping from Asia to China is faster and cheaper than from the West. Here's how the routes compare.",
        "sections": [
            ("Japan → China",
             "7–12 days, from $9/kg. Best for cosmetics and electronics."),
            ("Korea → China",
             "7–12 days, from $8/kg. Best for K-beauty and fashion."),
            ("Southeast Asia → China",
             "7–12 days, from $8/kg. Best for student luggage and daigou."),
        ],
        "faq": [
            ("Which Asia route is fastest?",
             "All three major routes (Japan, Korea, SE Asia) are 7–12 working days by air."),
            ("Which is cheapest?",
             "Korea and SE Asia are slightly cheaper than Japan, from about $8/kg."),
        ],
    },
    {
        "slug": "shipping-cost-save-money-tips.html",
        "title": "10 Tips to Save Money on International Shipping (2026) | Subao Global",
        "desc": "Practical tips to cut international shipping costs — consolidate, vacuum-pack, choose sea freight, and more.",
        "h1": "10 Tips to Save Money on Shipping",
        "intro": "Shipping doesn't have to be expensive. These ten tips can cut your costs by 30–50%.",
        "sections": [
            ("Consolidate parcels",
             "Combining multiple parcels into one shipment cuts per-kg costs dramatically."),
            ("Reduce volume",
             "Vacuum-pack clothes and disassemble bulky items. Volumetric weight can exceed actual weight."),
            ("Choose sea over air",
             "If you can wait, sea freight is 40% cheaper. For non-urgent heavy items, it's a no-brainer."),
            ("Compare before you ship",
             "Express couriers charge 40–60% more than consolidated shipping for the same route."),
        ],
        "faq": [
            ("What's the biggest money saver?",
             "Choosing consolidated shipping over express couriers — typically 40–60% savings."),
            ("Does sea freight always save money?",
             "Yes for heavy, non-urgent items. Air freight wins when speed matters."),
        ],
    },
]

BLOG_INDEX = {
    "slug": "index.html",
    "title": "International Shipping Blog & Guides | Subao Global",
    "desc": "Guides on shipping to China — prohibited items, customs duty, packing, and route comparisons. Practical advice from Subao Global.",
    "h1": "Shipping Guides & Blog",
    "intro": "Practical guides to shipping from the USA, Japan, Korea, Europe and more to China.",
}


def article_schema(b):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": b["h1"],
        "description": b["desc"],
        "inLanguage": "en",
        "publisher": {"@type": "Organization", "name": "Subao Global Logistics"},
    })


def gen_blog():
    # blog index
    cards = "".join(
        f'<div class="feature"><h3>{b["h1"]}</h3><p style="font-size:13px;color:var(--text-secondary);margin:8px 0">{b["desc"][:110]}…</p>'
        f'<a href="/en/blog/{b["slug"]}" style="color:var(--primary);font-weight:600;font-size:14px">Read more →</a></div>'
        for b in BLOG
    )
    body = f"""  <section class="hero"><div class="container"><h1>{BLOG_INDEX["h1"]}</h1><p class="subtitle">{BLOG_INDEX["intro"]}</p></div></section>
  <section class="section"><div class="container"><div class="features" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">{cards}</div></div></section>
  {cta_html()}"""
    rel = f'blog/{BLOG_INDEX["slug"]}'
    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, BLOG_INDEX["title"], BLOG_INDEX["desc"], body), encoding="utf-8")

    for b in BLOG:
        rel = f"blog/{b['slug']}"
        sections = "".join(
            f'<div style="margin-bottom:28px"><h2 style="font-size:1.4rem;font-weight:700;margin-bottom:10px;color:var(--primary-dark)">{h}</h2>'
            f'<p style="color:var(--text-secondary);line-height:1.8">{c}</p></div>'
            for h, c in b["sections"]
        )
        body = f"""  <section class="hero" style="padding-bottom:48px"><div class="container">
      <h1>{b["h1"]}</h1>
      <p class="subtitle">{b["intro"]}</p>
    </div></section>

  <section class="section"><div class="container" style="max-width:800px">
    <div style="background:#fff;border:1px solid var(--border);border-radius:16px;padding:36px">
      {sections}
    </div>
    <div class="section-title" style="margin-top:48px"><h2>Related questions</h2></div>
    {faq_html(b["faq"])}
  </div></section>

  {cta_html()}"""
        Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
        Path(EN / rel).write_text(render_page(rel, b["title"], b["desc"], body, article_schema(b)), encoding="utf-8")


def main():
    gen_blog()
    print(f"✅ Blog 生成完成：1 index + {len(BLOG)} 篇 = {len(BLOG) + 1} 页")


if __name__ == "__main__":
    main()
