# -*- coding: utf-8 -*-
"""
subaog.com 英文站补充生成器（Stage 3 补东南亚场景页 + Stage 4 工具页）
复用 gen-en-content.py 的模板函数。
"""
import importlib.util
from pathlib import Path
import shutil

# 复用 gen-en-content 的模板函数
spec = importlib.util.spec_from_file_location("gec", "gen-en-content.py")
gec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gec)

EN = gec.EN
render_page = gec.render_page
process_html = gec.process_html
can_ship_html = gec.can_ship_html
faq_html = gec.faq_html
faq_schema = gec.faq_schema
routes_html = gec.routes_html
cta_html = gec.cta_html


# ---------------- 1) 删除误生成的 seasia 城市页 ----------------
def cleanup():
    for d in ["kuala-lumpur", "penang", "johor-bahru"]:
        p = EN / "seasia-to-china" / d
        if p.exists():
            shutil.rmtree(p)
            print(f"  删除误生成: seasia-to-china/{d}/")


# ---------------- 2) 东南亚场景页 ----------------
SCENARIOS = {
    "student": {
        "title": "Student Luggage from {city} to China",
        "h1": "Student Luggage from {city} to China",
        "subtitle": ("Returning home after studying in {city}? Ship your books, clothes and personal items "
                     "door-to-door in 7–12 working days. Free boxes, free pickup, and tax-inclusive customs."),
        "features": [
            ("📦", "Free boxes", "We supply free boxes and packing materials for students."),
            ("🎓", "Student discounts", "Special rates during graduation season — ask us."),
            ("🛡️", "Tax-inclusive", "Used personal items are usually duty-free."),
            ("🚚", "Free pickup", "Free pickup from your dorm or apartment."),
        ],
        "faq": [
            ("How much does student luggage cost from {city} to China?",
             "Air freight from about $8/kg (21kg+). Sea freight from $4.5/kg. Student discounts apply during graduation season."),
            ("What can I ship as a student?",
             "Books, clothes, shoes, bedding, small electronics and personal effects. Used personal items are usually duty-free."),
            ("How long does student luggage take to arrive?",
             "Air freight takes 7–12 working days. Sea freight takes 12–18 days."),
        ],
    },
    "moving": {
        "title": "Moving from {city} to China",
        "h1": "Moving from {city} to China",
        "subtitle": ("Moving home from {city}? Ship furniture, appliances and household goods door-to-door. "
                     "Sea freight from 12–18 days with tax-inclusive customs and free pickup."),
        "features": [
            ("🛋️", "Furniture & appliances", "Large-item handling with care."),
            ("🚢", "Sea freight", "Cost-effective for large volume moves."),
            ("🛡️", "Tax-inclusive", "Used household goods are usually duty-free."),
            ("🚚", "Free pickup", "Free pickup across {city}."),
        ],
        "faq": [
            ("How much does moving from {city} to China cost?",
             "Sea freight from about $4.5/kg (21kg+). Large volume moves get better rates. Request a free quote."),
            ("How long does a move take?",
             "Sea freight takes 12–18 days door-to-door. Air freight (smaller moves) takes 7–12 days."),
            ("Can I move furniture and appliances?",
             "Yes. We handle furniture and appliances. Volume weight applies to large items."),
        ],
    },
    "shopping": {
        "title": "Shopping & Daigou from {city} to China",
        "h1": "Shopping & Daigou from {city} to China",
        "subtitle": ("Shipping cosmetics, electronics and fashion from {city} to China? We offer consolidated "
                     "shipping for daigou sellers and shoppers — combine multiple parcels, save on freight."),
        "features": [
            ("💄", "Cosmetics & electronics", "Expert handling for high-demand categories."),
            ("📦", "Parcel consolidation", "Combine multiple parcels to save on freight."),
            ("⚡", "Fast transit", "7–12 working days door-to-door."),
            ("🛡️", "Tax-inclusive", "One all-in price, no surprise fees."),
        ],
        "faq": [
            ("Can I consolidate multiple parcels?",
             "Yes — we consolidate multiple parcels into one shipment to save on freight and customs handling."),
            ("How much does daigou shipping cost from {city}?",
             "Air freight from about $8/kg (21kg+). Small parcels start around $10. Request a quote."),
            ("Which items are popular to ship?",
             "Cosmetics, skincare, electronics, fashion and snacks are the most-shipped categories."),
        ],
    },
}

CITY_NAMES = {"singapore": "Singapore", "malaysia": "Malaysia"}


def gen_seasia_scenario(city_slug: str, scenario: str):
    data = SCENARIOS[scenario]
    city = CITY_NAMES[city_slug]
    rel = f"seasia-to-china/{city_slug}/{scenario}/index.html"
    title = data["title"].format(city=city) + " | Subao Global"
    desc = data["subtitle"].format(city=city)
    faq = [(q.format(city=city), a.format(city=city)) for q, a in data["faq"]]
    features = "".join(
        f'<div class="feature"><div class="icon">{ic}</div><h3>{t.format(city=city)}</h3><p>{d.format(city=city)}</p></div>'
        for ic, t, d in data["features"]
    )
    body = f"""  <section class="hero">
    <div class="container">
      <h1>{data["h1"].format(city=city)}</h1>
      <p class="subtitle">{data["subtitle"].format(city=city)}</p>
      <div class="hero-cta">
        <a href="/en/contact.html" class="btn-primary">📦 Get a quote</a>
        <a href="/en/seasia-to-china/" class="btn-outline">All SE Asia routes →</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-title"><h2>How it works</h2></div>
      {process_html()}
    </div>
  </section>

  <section class="section" style="background:#fff">
    <div class="container">
      <div class="section-title"><h2>Why choose Subao Global</h2></div>
      <div class="features">{features}</div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-title"><h2>Frequently asked questions</h2></div>
      {faq_html(faq)}
    </div>
  </section>

  {routes_html("seasia-to-china")}
  {cta_html()}"""
    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body, faq_schema(faq)), encoding="utf-8")


def gen_seasia_malaysia_pillar():
    rel = "seasia-to-china/malaysia/index.html"
    title = "Ship from Malaysia to China — Door-to-Door | Subao Global"
    desc = "Ship from Malaysia to China with Subao Global. Door-to-door in 7–12 working days, tax-inclusive, from $8/kg. Free pickup. Get a free quote."
    faq = [
        ("How long does Malaysia to China shipping take?",
         "Air freight takes 7–12 working days. Sea freight takes 12–18 days."),
        ("How much does Malaysia to China shipping cost?",
         "Air freight from about $8/kg (21kg+). Sea freight from $4.5/kg. Request a free quote."),
        ("Which Malaysian cities do you cover?",
         "We cover Kuala Lumpur, Penang, Johor Bahru and most of Peninsular Malaysia with free pickup."),
    ]
    body = f"""  <section class="hero">
    <div class="container">
      <h1>Ship from Malaysia to China</h1>
      <p class="subtitle">Door-to-door shipping from Malaysia to China in 7–12 working days. Student luggage, moving home, and shopping — with tax-inclusive customs and free pickup.</p>
      <div class="hero-cta">
        <a href="/en/contact.html" class="btn-primary">📦 Get a quote</a>
        <a href="#services" class="btn-outline">View services ↓</a>
      </div>
    </div>
  </section>

  <section class="section" id="services">
    <div class="container">
      <div class="info-grid">
        <div class="info-card"><div class="big">$8</div><div class="label">Air freight /kg (21kg+)</div></div>
        <div class="info-card"><div class="big">7–12</div><div class="label">Days door-to-door</div></div>
        <div class="info-card"><div class="big">Tax-incl.</div><div class="label">One all-in price</div></div>
        <div class="info-card"><div class="big">Free</div><div class="label">Pickup across Malaysia</div></div>
      </div>
      <div class="section-title"><h2>Popular services</h2></div>
      <div class="features">
        <div class="feature"><div class="icon">🎓</div><h3>Student luggage</h3><p>Returning students — free boxes and discounts.</p><a href="/en/seasia-to-china/malaysia/student/" style="color:var(--primary);font-weight:600;font-size:14px">Learn more →</a></div>
        <div class="feature"><div class="icon">🏠</div><h3>Moving home</h3><p>Furniture and household goods by sea.</p><a href="/en/seasia-to-china/malaysia/moving/" style="color:var(--primary);font-weight:600;font-size:14px">Learn more →</a></div>
        <div class="feature"><div class="icon">🛍️</div><h3>Shopping & daigou</h3><p>Consolidated shipping for shoppers.</p><a href="/en/seasia-to-china/malaysia/shopping/" style="color:var(--primary);font-weight:600;font-size:14px">Learn more →</a></div>
      </div>
    </div>
  </section>

  <section class="section" style="background:#fff">
    <div class="container">
      <div class="section-title"><h2>Frequently asked questions</h2></div>
      {faq_html(faq)}
    </div>
  </section>

  {routes_html("seasia-to-china")}
  {cta_html()}"""
    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body, faq_schema(faq)), encoding="utf-8")


def gen_packing_guide():
    rel = "seasia-to-china/packing-guide/index.html"
    title = "How to Pack for International Shipping to China | Subao Global"
    desc = "A complete packing guide for shipping to China — box selection, fragile items, clothes, volumetric weight, and common mistakes. Pack right, ship safe."
    faq = [
        ("What is volumetric weight?",
         "Volumetric weight = length × width × height (cm) ÷ 5000. Carriers charge whichever is higher — actual or volumetric weight."),
        ("What boxes should I use?",
         "Use double-wall corrugated boxes for heavy items. Keep each box under 25kg for easy handling. Standard moving boxes (60×40×40cm) work well."),
        ("How do I pack fragile items?",
         "Wrap each item in bubble wrap, fill empty space with packing peanuts or crumpled paper, and mark the box 'FRAGILE'."),
    ]
    tips = [
        ("📦", "Choose the right box", "Double-wall corrugated boxes for heavy items; single-wall is fine for clothes and light items."),
        ("🍾", "Protect fragile items", "Bubble wrap + void fill. Nothing should move inside the box when shaken."),
        ("👕", "Vacuum-pack clothes", "Vacuum bags cut clothing volume by up to 60%, lowering volumetric weight."),
        ("⚖️", "Mind the weight limit", "Keep each box under 25kg. Overweight boxes risk damage and extra fees."),
        ("🚫", "Check prohibited items", "Remove batteries, aerosols and liquids before packing."),
        ("🏷️", "Label every box", "Write the destination and your tracking number on each box."),
    ]
    features = "".join(f'<div class="feature"><div class="icon">{i}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in tips)
    body = f"""  <section class="hero">
    <div class="container">
      <h1>How to Pack for International Shipping to China</h1>
      <p class="subtitle">Pack right and your items arrive safe. This guide covers box selection, fragile items, clothes, volumetric weight, and the mistakes to avoid.</p>
      <div class="hero-cta"><a href="/en/contact.html" class="btn-primary">📦 Get a quote</a></div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-title"><h2>6 packing rules that prevent damage</h2></div>
      <div class="features">{features}</div>
    </div>
  </section>

  <section class="section" style="background:#fff">
    <div class="container">
      <div class="section-title"><h2>Frequently asked questions</h2></div>
      {faq_html(faq)}
    </div>
  </section>

  {cta_html()}"""
    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body, faq_schema(faq)), encoding="utf-8")


def gen_seasia_pricing():
    rel = "seasia-to-china/pricing/index.html"
    title = "Southeast Asia to China Shipping Rates | Subao Global"
    desc = "Compare Singapore and Malaysia to China shipping rates. Air freight from $8/kg, sea from $4.5/kg. Tax-inclusive door-to-door pricing."
    faq = [
        ("Are these prices final?",
         "These are reference rates. Final price depends on weight, volume and item type. Request a free quote for an exact figure."),
        ("Is there a minimum charge?",
         "Small parcels (under 5kg) have a minimum charge of about $15. Larger shipments are priced per kg."),
    ]
    body = f"""  <section class="hero">
    <div class="container">
      <h1>Southeast Asia to China — Shipping Rates</h1>
      <p class="subtitle">Transparent, tax-inclusive pricing for Singapore and Malaysia to China. No hidden fees — one all-in price.</p>
      <div class="hero-cta"><a href="/en/contact.html" class="btn-primary">📦 Get a quote</a></div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-title"><h2>Singapore & Malaysia → China</h2></div>
      <table class="price-table">
        <thead><tr><th>Weight</th><th>Air freight</th><th>Sea freight</th><th>Transit time</th></tr></thead>
        <tbody>
          <tr><td style="font-weight:600">1–20 kg</td><td>$10/kg</td><td>—</td><td>Air 7–12 days</td></tr>
          <tr><td style="font-weight:600">21–99 kg</td><td style="color:var(--primary);font-weight:700">$8/kg</td><td>$4.5/kg</td><td>Air 7–12 / Sea 12–18 days</td></tr>
          <tr><td style="font-weight:600">100 kg+</td><td style="color:var(--primary);font-weight:700">$7.5/kg</td><td>$4/kg</td><td>Air 7–12 / Sea 12–18 days</td></tr>
        </tbody>
      </table>
      <p class="note">* All-inclusive door-to-door price covering pickup + freight + China customs + final delivery.</p>
    </div>
  </section>

  <section class="section" style="background:#fff">
    <div class="container">
      <div class="section-title"><h2>Frequently asked questions</h2></div>
      {faq_html(faq)}
    </div>
  </section>

  {cta_html()}"""
    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body, faq_schema(faq)), encoding="utf-8")


# ---------------- 3) 工具页 ----------------
def gen_tools():
    # tools index
    rel = "tools/index.html"
    title = "Free International Shipping Tools & Calculators | Subao Global"
    desc = "Free shipping tools: cost calculator, customs duty estimator, volumetric weight calculator, and prohibited items checker. Plan your China shipment."
    tools = [
        ("📦", "Shipping cost calculator", "Estimate air and sea freight costs.", "shipping-calculator.html"),
        ("💰", "Customs duty estimator", "Estimate China import duty by category.", "customs-duty-calculator.html"),
        ("📐", "Volumetric weight calculator", "Calculate volumetric weight (÷5000).", "volume-calculator.html"),
        ("✅", "Can I ship it?", "Check if your item can be shipped to China.", "can-i-ship.html"),
    ]
    cards = "".join(
        f'<div class="feature"><div class="icon">{i}</div><h3>{t}</h3><p>{d}</p>'
        f'<a href="/en/tools/{u}" style="color:var(--primary);font-weight:600;font-size:14px">Open tool →</a></div>'
        for i, t, d, u in tools
    )
    body = f"""  <section class="hero">
    <div class="container">
      <h1>Free Shipping Tools & Calculators</h1>
      <p class="subtitle">Plan your China shipment with our free tools — cost, customs duty, volumetric weight, and prohibited items.</p>
    </div>
  </section>
  <section class="section"><div class="container"><div class="features">{cards}</div></div></section>
  {cta_html()}"""
    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body), encoding="utf-8")

    # 1) shipping calculator
    rel = "tools/shipping-calculator.html"
    title = "International Shipping Cost Calculator | Subao Global"
    desc = "Estimate shipping costs from the USA, Japan, Korea, Europe, Canada and Australia to China. Air and sea freight rates."
    body = f"""  <section class="hero"><div class="container"><h1>Shipping Cost Calculator</h1><p class="subtitle">Estimate door-to-door shipping costs to China.</p></div></section>
  <section class="section"><div class="container" style="max-width:600px">
    <div style="background:#fff;border:1px solid var(--border);border-radius:16px;padding:28px">
      <label style="font-size:13px;font-weight:600">Origin route</label>
      <select id="route" style="width:100%;padding:11px 14px;border:1px solid var(--border);border-radius:10px;font-size:15px;margin:6px 0 16px">
        <option value="10.5">USA → China ($10.5/kg)</option>
        <option value="9">Japan → China ($9/kg)</option>
        <option value="8">Korea → China ($8/kg)</option>
        <option value="9.5">Europe → China ($9.5/kg)</option>
        <option value="10">Canada → China ($10/kg)</option>
        <option value="9.5">Australia → China ($9.5/kg)</option>
        <option value="8">SE Asia → China ($8/kg)</option>
      </select>
      <label style="font-size:13px;font-weight:600">Weight (kg)</label>
      <input type="number" id="weight" value="21" min="1" style="width:100%;padding:11px 14px;border:1px solid var(--border);border-radius:10px;font-size:15px;margin:6px 0 16px">
      <button onclick="calc()" style="width:100%;background:var(--primary);color:#fff;border:none;padding:13px;border-radius:24px;font-weight:700;font-size:15px;cursor:pointer">Calculate</button>
      <div id="result" style="margin-top:16px;padding:16px;background:var(--primary-light);border-radius:10px;text-align:center;display:none"></div>
    </div>
  </div></section>
  {cta_html()}
  <script>
    function calc(){{
      var r = parseFloat(document.getElementById('route').value);
      var w = parseFloat(document.getElementById('weight').value);
      if (!w || w < 1) {{ alert('Please enter a valid weight.'); return; }}
      var est = r * w;
      document.getElementById('result').style.display = 'block';
      document.getElementById('result').innerHTML = '<div style="font-size:1.8rem;font-weight:800;color:var(--primary)">$' + est.toFixed(2) + '</div><div style="font-size:13px;color:var(--text-secondary)">Estimated all-in cost for ' + w + ' kg (air freight)</div>';
    }}
  </script>"""
    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body), encoding="utf-8")

    # 2) customs duty calculator
    rel = "tools/customs-duty-calculator.html"
    title = "China Customs Duty Estimator | Subao Global"
    desc = "Estimate China import duty by category. Duty-free allowance for personal items is RMB 1,000. Calculate clothing, cosmetics, electronics and more."
    body = f"""  <section class="hero"><div class="container"><h1>China Customs Duty Estimator</h1><p class="subtitle">Estimate import duty for personal items shipped to China.</p></div></section>
  <section class="section"><div class="container" style="max-width:600px">
    <div style="background:#fff;border:1px solid var(--border);border-radius:16px;padding:28px">
      <label style="font-size:13px;font-weight:600">Item category</label>
      <select id="cat" style="width:100%;padding:11px 14px;border:1px solid var(--border);border-radius:10px;font-size:15px;margin:6px 0 16px">
        <option value="20">Clothing / textiles (20%)</option>
        <option value="50">Cosmetics (50%)</option>
        <option value="15">Electronics (15%)</option>
        <option value="15">Books (15%)</option>
        <option value="30">Luxury bags / watches (30%)</option>
        <option value="0">Used personal items (usually duty-free)</option>
      </select>
      <label style="font-size:13px;font-weight:600">Declared value (RMB)</label>
      <input type="number" id="val" value="1000" min="0" style="width:100%;padding:11px 14px;border:1px solid var(--border);border-radius:10px;font-size:15px;margin:6px 0 16px">
      <button onclick="calc()" style="width:100%;background:var(--primary);color:#fff;border:none;padding:13px;border-radius:24px;font-weight:700;font-size:15px;cursor:pointer">Estimate</button>
      <div id="result" style="margin-top:16px;padding:16px;background:var(--primary-light);border-radius:10px;text-align:center;display:none"></div>
      <p class="note" style="margin-top:12px">* Personal items under RMB 1,000 are duty-free. This is an estimate only.</p>
    </div>
  </div></section>
  {cta_html()}
  <script>
    function calc(){{
      var rate = parseFloat(document.getElementById('cat').value);
      var val = parseFloat(document.getElementById('val').value);
      if (isNaN(val)) {{ alert('Please enter a valid value.'); return; }}
      var duty = (val - 1000) * rate / 100;
      if (duty < 0) duty = 0;
      document.getElementById('result').style.display = 'block';
      document.getElementById('result').innerHTML = '<div style="font-size:1.8rem;font-weight:800;color:var(--primary)">¥' + duty.toFixed(0) + '</div><div style="font-size:13px;color:var(--text-secondary)">Estimated duty on value above the RMB 1,000 allowance</div>';
    }}
  </script>"""
    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body), encoding="utf-8")

    # 3) volume calculator
    rel = "tools/volume-calculator.html"
    title = "Volumetric Weight Calculator | Subao Global"
    desc = "Calculate volumetric weight for international shipping. Formula: length × width × height (cm) ÷ 5000. Free tool."
    body = f"""  <section class="hero"><div class="container"><h1>Volumetric Weight Calculator</h1><p class="subtitle">Carriers charge the higher of actual or volumetric weight.</p></div></section>
  <section class="section"><div class="container" style="max-width:600px">
    <div style="background:#fff;border:1px solid var(--border);border-radius:16px;padding:28px">
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px">
        <div><label style="font-size:13px;font-weight:600">Length (cm)</label><input type="number" id="l" value="60" style="width:100%;padding:11px;border:1px solid var(--border);border-radius:10px;font-size:15px;margin:6px 0 16px"></div>
        <div><label style="font-size:13px;font-weight:600">Width (cm)</label><input type="number" id="w" value="40" style="width:100%;padding:11px;border:1px solid var(--border);border-radius:10px;font-size:15px;margin:6px 0 16px"></div>
        <div><label style="font-size:13px;font-weight:600">Height (cm)</label><input type="number" id="h" value="40" style="width:100%;padding:11px;border:1px solid var(--border);border-radius:10px;font-size:15px;margin:6px 0 16px"></div>
      </div>
      <button onclick="calc()" style="width:100%;background:var(--primary);color:#fff;border:none;padding:13px;border-radius:24px;font-weight:700;font-size:15px;cursor:pointer">Calculate</button>
      <div id="result" style="margin-top:16px;padding:16px;background:var(--primary-light);border-radius:10px;text-align:center;display:none"></div>
      <p class="note" style="margin-top:12px">Formula: (L × W × H) ÷ 5000 = volumetric weight in kg</p>
    </div>
  </div></section>
  {cta_html()}
  <script>
    function calc(){{
      var l = parseFloat(document.getElementById('l').value);
      var w = parseFloat(document.getElementById('w').value);
      var h = parseFloat(document.getElementById('h').value);
      if (!l || !w || !h) {{ alert('Please enter valid dimensions.'); return; }}
      var vw = l * w * h / 5000;
      document.getElementById('result').style.display = 'block';
      document.getElementById('result').innerHTML = '<div style="font-size:1.8rem;font-weight:800;color:var(--primary)">' + vw.toFixed(2) + ' kg</div><div style="font-size:13px;color:var(--text-secondary)">Volumetric weight</div>';
    }}
  </script>"""
    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body), encoding="utf-8")

    # 4) can-i-ship
    rel = "tools/can-i-ship.html"
    title = "Can I Ship It to China? — Prohibited Items Checker | Subao Global"
    desc = "Check if your item can be shipped to China. Search common categories — supplements, cosmetics, electronics, food, and more."
    body = f"""  <section class="hero"><div class="container"><h1>Can I Ship It to China?</h1><p class="subtitle">Check whether your item is allowed before you ship.</p></div></section>
  <section class="section"><div class="container">
    <div style="max-width:600px;margin:0 auto 32px">
      <input type="text" id="q" placeholder="Type an item, e.g. 'cosmetics' or 'wine'" style="width:100%;padding:13px 16px;border:1.5px solid var(--border);border-radius:24px;font-size:15px" onkeyup="filter()">
    </div>
    <div class="can-ship" id="list" style="max-width:700px;margin:0 auto"></div>
  </div></section>
  {cta_html()}
  <script>
    var items = [
      ['Clothing & shoes', true], ['Books & documents', true], ['Supplements & vitamins', true],
      ['Cosmetics & skincare', true], ['Electronics', true], ['Baby formula & food', true],
      ['Household goods', true], ['Furniture & appliances', true], ['Luxury bags (higher duty)', true],
      ['Batteries (declaration required)', true], ['Wine & alcohol (limited)', true],
      ['Weapons & ammunition', false], ['Drugs & narcotics', false], ['Fresh food & meat', false],
      ['Politically sensitive materials', false], ['Large cash amounts', false]
    ];
    function render(filter){{
      var html = '';
      items.forEach(function(it){{
        if (filter && it[0].toLowerCase().indexOf(filter.toLowerCase()) === -1) return;
        var mark = it[1] ? '<span class="yes">✓ Allowed</span>' : '<span class="no">✗ Prohibited</span>';
        html += '<li>' + mark + it[0] + '</li>';
      }});
      document.getElementById('list').innerHTML = html || '<li>No matches.</li>';
    }}
    function filter(){{ render(document.getElementById('q').value); }}
    render('');
  </script>"""
    Path(EN / rel).parent.mkdir(parents=True, exist_ok=True)
    Path(EN / rel).write_text(render_page(rel, title, desc, body), encoding="utf-8")


# ---------------- 主入口 ----------------
def main():
    print("=== 清理误生成页 ===")
    cleanup()
    print("=== 生成东南亚场景页 ===")
    gen_seasia_malaysia_pillar()
    for city in ["singapore", "malaysia"]:
        for scenario in ["student", "moving", "shopping"]:
            gen_seasia_scenario(city, scenario)
    gen_packing_guide()
    gen_seasia_pricing()
    print("=== 生成工具页 ===")
    gen_tools()
    print("✅ 补充生成完成")


if __name__ == "__main__":
    main()
