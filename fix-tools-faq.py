import re
import json
from pathlib import Path

ROOT = Path('.')

tools_zh_faqs = [
    ('运费怎么算？', '用运费计算器，选出发地档位（美加澳/欧洲/日韩东南亚）和重量，自动算双清包税总价。最低起运 20kg，100kg+ 更优惠。'),
    ('关税怎么算？', '用关税计算器，输入品类和货值估算关税。个人自用物品人民币 1000 元以内免税。'),
    ('体积重怎么算？', '体积重 = 长×宽×高(cm)÷5000，与实际重量取大值计费。泡货（枕头、玩具）要特别留意体积重。'),
]

tools_en_faqs = [
    ('How do I calculate shipping cost?', 'Use the shipping calculator — pick your origin tier (USA/Canada/Australia, Europe, or Japan/Korea/SE Asia) and weight to get an all-inclusive tax-paid total. Minimum 20kg; 100kg+ is cheaper.'),
    ('How do I estimate customs duty?', 'Use the duty calculator — enter the item category and value. Personal-use items under RMB 1,000 are duty-free.'),
    ('How is volumetric weight calculated?', 'Volumetric weight = L×W×H (cm) ÷ 5000, billed as the greater of actual vs volumetric weight. Bulky light items (pillows, toys) cost more by volume.'),
]

def build_ld(faqs):
    return json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs
    ]}, ensure_ascii=False)

def visible(faqs, zh):
    title = '常见问题' if zh else 'FAQ'
    inner = ''.join(
        f'<div style="border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px;margin-bottom:10px"><h3 style="font-size:15px;font-weight:600;margin:0 0 6px">{q}</h3><p style="margin:0;color:#64748B;line-height:1.7">{a}</p></div>'
        for q, a in faqs
    )
    return f'<section style="max-width:1100px;margin:40px auto;padding:0 24px"><h2 style="font-size:22px;font-weight:700;margin-bottom:16px">{title}</h2>{inner}</section>'

def patch(path, faqs, zh):
    p = ROOT / path
    t = p.read_text(encoding='utf-8', errors='ignore')
    t, n1 = re.subn(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>',
                    f'<script type="application/ld+json">{build_ld(faqs)}</script>', t, flags=re.S)
    t, n2 = re.subn(r'<section style="max-width:1100px;margin:40px auto;padding:0 24px"><h2[^>]*>(常见问题|FAQ)</h2>.*?</section>',
                    visible(faqs, zh), t, flags=re.S)
    p.write_text(t, encoding='utf-8')
    print(f'  {"✅" if n1 and n2 else "⚠️"} {path}: JSON-LD{n1} 可见{n2}')

patch('zh-cn/tools/index.html', tools_zh_faqs, zh=True)
patch('en/tools/index.html', tools_en_faqs, zh=False)

# 残留检查（en 破句）
print()
t = (ROOT / 'en/tools/index.html').read_text(encoding='utf-8', errors='ignore')
print('en tools 破句 "kg. Free" 残留:', t.count('kg. Free'))
