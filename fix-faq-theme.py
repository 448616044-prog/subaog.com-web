import re
import json
from pathlib import Path

ROOT = Path('.')

# routes 页专属 FAQ（中文）
routes_zh_faqs = [
    ('从哪个国家寄回中国最便宜？', '日韩、东南亚（泰国/新加坡/菲律宾/马来西亚）¥80/kg 起最便宜；欧洲 ¥90/kg 起；美国、加拿大、澳洲、墨西哥、新西兰 ¥100/kg 起。以上均为 20-99kg 双清包税价，100kg+ 更优惠。'),
    ('各国寄回中国的时效一样吗？', '空运统一 10-15 个工作日门到门，各出发国基本相同，已含清关与末端派送。'),
    ('怎么选择适合我的线路？', '点击对应出发地线路页，查看该线路专属运费、时效与清关方案；拿不准可直接免费咨询客服，30 分钟给方案。'),
]

# routes 页专属 FAQ（英文）
routes_en_faqs = [
    ('Which origin country is cheapest to ship to China?', 'Japan/Korea/SE Asia (Thailand/Singapore/Philippines/Malaysia) start from ¥80/kg; Europe from ¥90/kg; USA/Canada/Australia/Mexico/New Zealand from ¥100/kg. All are 20-99kg tax-inclusive rates; 100kg+ is cheaper.'),
    ('Is transit time the same from every country?', 'Yes — air freight is a uniform 10-15 working days door-to-door from all origin regions, including customs clearance and final delivery.'),
    ('How do I choose the right route?', 'Click your origin route page to see route-specific pricing, transit time and customs guidance, or contact us for a free quote — we reply within 30 minutes.'),
]

# can-i-ship-index 页专属 FAQ（中文）
ship_zh_faqs = [
    ('什么物品绝对不能寄到中国？', '武器、毒品、易燃易爆品、新鲜动植物、肉制品、政治敏感出版物、仿冒品等绝对禁运。'),
    ('保健品和化妆品能寄吗？', '能。需密封零售包装、个人自用数量（每款 5-10 件），我们代办中国海关申报。'),
    ('寄回中国要交多少税？', '个人自用物品人民币 1000 元以内免税；超出部分按品类：服装 20%、化妆品 50%、电子产品 15%、书籍 0%。'),
]

# can-i-ship-index 页专属 FAQ（英文）
ship_en_faqs = [
    ('What items are absolutely prohibited?', 'Weapons, narcotics, flammable/explosive materials, fresh plants and animals, meat products, politically sensitive publications and counterfeit goods are strictly prohibited.'),
    ('Can I ship supplements and cosmetics?', 'Yes — sealed retail packaging and personal-use quantities (5-10 units per SKU) are required. We handle China customs declaration for you.'),
    ('How much duty will I pay?', 'Personal-use items under RMB 1,000 are duty-free. Above that, rates vary by category: clothing 20%, cosmetics 50%, electronics 15%, books 0%.'),
]

def build_faq_ld(faqs):
    obj = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
            for q, a in faqs
        ]
    }
    return json.dumps(obj, ensure_ascii=False)

def build_faq_visible(faqs):
    inner = ''.join(
        f'<div style="border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px;margin-bottom:10px"><h3 style="font-size:15px;font-weight:600;margin:0 0 6px">{q}</h3><p style="margin:0;color:#64748B;line-height:1.7">{a}</p></div>'
        for q, a in faqs
    )
    return f'<section style="max-width:1100px;margin:40px auto;padding:0 24px"><h2 style="font-size:22px;font-weight:700;margin-bottom:16px">常见问题</h2>{inner}</section>'

def build_faq_visible_en(faqs):
    inner = ''.join(
        f'<div style="border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px;margin-bottom:10px"><h3 style="font-size:15px;font-weight:600;margin:0 0 6px">{q}</h3><p style="margin:0;color:#64748B;line-height:1.7">{a}</p></div>'
        for q, a in faqs
    )
    return f'<section style="max-width:1100px;margin:40px auto;padding:0 24px"><h2 style="font-size:22px;font-weight:700;margin-bottom:16px">FAQ</h2>{inner}</section>'

def replace_faqs(path, faqs, zh=True):
    p = ROOT / path
    if not p.exists():
        print(f'  MISSING {path}')
        return
    t = p.read_text(encoding='utf-8', errors='ignore')
    # 1) 替换 JSON-LD FAQPage
    new_ld = build_faq_ld(faqs)
    t, n1 = re.subn(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>',
                    f'<script type="application/ld+json">{new_ld}</script>', t, flags=re.S)
    # 2) 替换可见 FAQ section
    visible = build_faq_visible(faqs) if zh else build_faq_visible_en(faqs)
    t, n2 = re.subn(r'<section style="max-width:1100px;margin:40px auto;padding:0 24px"><h2[^>]*>(常见问题|FAQ)</h2>.*?</section>',
                    visible, t, flags=re.S)
    p.write_text(t, encoding='utf-8')
    print(f'  ✅ {path}: JSON-LD替换{n1} 可见替换{n2}')

# routes 页
replace_faqs('zh-cn/routes/index.html', routes_zh_faqs, zh=True)
replace_faqs('en/routes/index.html', routes_en_faqs, zh=False)

# can-i-ship-index 页
replace_faqs('zh-cn/can-i-ship-index/index.html', ship_zh_faqs, zh=True)
replace_faqs('en/can-i-ship-index/index.html', ship_en_faqs, zh=False)

print('\nP1 FAQ 主题化完成（routes + can-i-ship-index）')
