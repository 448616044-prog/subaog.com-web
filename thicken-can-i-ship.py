#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加厚 can-i-ship 物品页正文：在「结论卡片」与「FAQ」之间插入实质长文段落 + 内链。
守红线：只写品类税率/免税额/时效，不写具体价格数字；集运比 FedEx/UPS 便宜 40-60%。
"""
import re, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---- 每个物品的定制内容（zh / en 两份） ----
ITEMS = {
  "kitchenware": {
    "zh": {
      "can_title": "厨具哪些能寄、哪些不能寄？",
      "can_yes": "锅具、平底锅、烘焙工具、非电动餐具、不锈钢/铸铁锅、玻璃器皿（需加固）、陶瓷餐具",
      "can_no": "超长刀具、电池松脱的电动厨具、含易燃燃料的器具",
      "duty_title": "寄厨具回国交多少税？",
      "duty_body": "厨具属于个人物品，行邮税率 <strong>15%</strong>。个人自用、价值在人民币 <strong>1000 元</strong> 免税额以内通常免税，超出部分按 15% 计税。我们的双清包税服务已含基础关税，无需自己跑清关。",
      "pack_title": "厨具怎么打包才不易碎？",
      "pack_body": "陶瓷、玻璃器皿务必逐件包裹：先套原包装，再用气泡膜缠绕，放入硬纸箱后用填充物塞满空隙，箱内不留晃动空间。不锈钢锅具相对耐压，但锅盖与锅体之间建议隔一层软布防止刮花。",
      "cost_title": "厨具寄中国多久到？贵不贵？",
      "cost_body": "空运门到门 <strong>10–15 个工作日</strong>。华人集运比 FedEx/UPS 直寄便宜 <strong>40–60%</strong>，5kg 以上尤其划算。具体运费可看 <a href=\"/zh-cn/pricing\" style=\"color:#0066CC\">运费报价</a>，或先用 <a href=\"/zh-cn/tools/volume-calculator\" style=\"color:#0066CC\">材积计算器</a> 估算体积重。",
    },
    "en": {
      "can_title": "What kitchenware can you ship to China?",
      "can_yes": "pots & pans, bakeware, non-electric cutlery, stainless & cast-iron cookware, glassware (reinforced), ceramic dishes",
      "can_no": "over-length chef's knives, electric appliances with loose batteries, flammable fuels",
      "duty_title": "How much duty will I pay on kitchenware?",
      "duty_body": "Kitchenware falls under personal items with a <strong>15%</strong> duty rate. Personal-use quantities valued under <strong>RMB 1,000</strong> (about $140) are usually duty-free; the excess is taxed at 15%. Our tax-inclusive service covers standard duty, so you don't handle customs yourself.",
      "pack_title": "How should I pack kitchenware to avoid breakage?",
      "pack_body": "Wrap ceramics and glassware individually: keep original packaging, wrap in bubble wrap, place in a rigid box and fill all gaps so nothing shifts. Stainless cookware is more crush-resistant, but place a soft cloth between lids and bodies to avoid scratches.",
      "cost_title": "How long and how much to ship kitchenware to China?",
      "cost_body": "Air freight is <strong>10–15 working days</strong> door-to-door. Chinese consolidated shipping is <strong>40–60% cheaper</strong> than FedEx/UPS direct, especially over 5kg. See our <a href=\"/en/pricing\" style=\"color:#0066CC\">pricing page</a> or estimate volumetric weight with the <a href=\"/en/tools/volume-calculator\" style=\"color:#0066CC\">volume calculator</a>.",
    },
  },
  "tea": {
    "zh": {
      "can_title": "茶叶哪些能寄、哪些不能寄？",
      "can_yes": "密封原包装茶叶（散装茶、袋泡茶）、礼品茶具套装",
      "can_no": "无标识散装茶、含违禁添加剂的茶、临期变质茶",
      "duty_title": "寄茶叶回国交多少税？",
      "duty_body": "茶叶行邮税率 <strong>15%</strong>。个人自用、价值人民币 <strong>1000 元</strong> 以内通常免税，超出部分按 15% 计税。双清包税服务已含基础关税。",
      "pack_title": "茶叶怎么打包寄回国？",
      "pack_body": "保持原密封包装，外加防潮袋，放入硬纸箱并填充缓冲，避免挤压导致碎茶。易碎茶具单独包裹加固。",
      "cost_title": "茶叶寄中国多久到？",
      "cost_body": "空运门到门 <strong>10–15 个工作日</strong>。集运比 FedEx/UPS 直寄便宜 <strong>40–60%</strong>。详见 <a href=\"/zh-cn/pricing\" style=\"color:#0066CC\">运费报价</a>。",
    },
    "en": {
      "can_title": "What tea can you ship to China?",
      "can_yes": "sealed original-packaging tea (loose leaf, tea bags), gift tea sets",
      "can_no": "unlabeled bulk tea, tea with prohibited additives, expired tea",
      "duty_title": "How much duty will I pay on tea?",
      "duty_body": "Tea has a <strong>15%</strong> duty rate. Personal-use quantities under <strong>RMB 1,000</strong> (about $140) are usually duty-free; the excess is taxed at 15%. Our tax-inclusive service covers standard duty.",
      "pack_title": "How should I pack tea for shipping?",
      "pack_body": "Keep tea in its original sealed packaging, add a moisture barrier, and cushion inside a rigid box to prevent crushing. Wrap fragile tea sets individually.",
      "cost_title": "How long to ship tea to China?",
      "cost_body": "Air freight is <strong>10–15 working days</strong> door-to-door. Consolidated shipping is <strong>40–60% cheaper</strong> than FedEx/UPS. See <a href=\"/en/pricing\" style=\"color:#0066CC\">pricing</a>.",
    },
  },
  "perfume": {
    "zh": {
      "can_title": "香水能寄吗？有什么限制？",
      "can_yes": "少量密封原包装香水、香氛（走敏感货专线）",
      "can_no": "大批量商业用途、易燃推进剂气雾罐、无标识分装液",
      "duty_title": "寄香水回国交多少税？",
      "duty_body": "香水属于高税率品类，行邮税率 <strong>50%</strong>（最高档）。个人自用少量、价值人民币 <strong>1000 元</strong> 以内通常免税，超出部分按 50% 计税。",
      "pack_title": "香水怎么打包防漏？",
      "pack_body": "务必防漏密封：瓶口封紧、独立套防水袋、四周缓冲填充，箱内标注易碎。含酒精液体属敏感货，走专线更稳妥。",
      "cost_title": "香水寄中国多久到？",
      "cost_body": "敏感货专线空运门到门 <strong>10–15 个工作日</strong>。具体可看 <a href=\"/zh-cn/pricing\" style=\"color:#0066CC\">运费报价</a> 或咨询客服确认品类。",
    },
    "en": {
      "can_title": "Can you ship perfume to China? Any limits?",
      "can_yes": "small sealed original-packaging perfume & fragrance (via sensitive-goods channel)",
      "can_no": "large commercial quantities, flammable-propellant aerosols, unlabeled liquids",
      "duty_title": "How much duty will I pay on perfume?",
      "duty_body": "Perfume is a high-duty category at <strong>50%</strong> (top tier). Small personal-use quantities under <strong>RMB 1,000</strong> (about $140) are usually duty-free; the excess is taxed at 50%.",
      "pack_title": "How should I pack perfume to avoid leaks?",
      "pack_body": "Seal the cap tightly, bag each bottle in a waterproof pouch, cushion all sides, and mark the box fragile. Alcohol-based liquid is a sensitive item — use a dedicated channel.",
      "cost_title": "How long to ship perfume to China?",
      "cost_body": "Sensitive-goods air freight is <strong>10–15 working days</strong> door-to-door. See <a href=\"/en/pricing\" style=\"color:#0066CC\">pricing</a> or ask our team to confirm the category.",
    },
  },
  "books": {
    "zh": {
      "can_title": "哪些书能寄、哪些不能寄？",
      "can_yes": "教材、个人藏书、小说、学术文献、期刊",
      "can_no": "涉政治敏感内容、盗版书、淫秽出版物",
      "duty_title": "寄书回国交多少税？",
      "duty_body": "书籍行邮税率 <strong>15%</strong>。个人自用、价值人民币 <strong>1000 元</strong> 以内通常免税，超出部分按 15% 计税。",
      "pack_title": "书怎么打包防潮防折？",
      "pack_body": "用防水袋包裹，四角加固，平放装箱避免折角；精装书之间垫软纸防划伤。",
      "cost_title": "书寄中国多久到？",
      "cost_body": "空运门到门 <strong>10–15 个工作日</strong>。集运比 FedEx/UPS 便宜 <strong>40–60%</strong>。详见 <a href=\"/zh-cn/pricing\" style=\"color:#0066CC\">运费报价</a>。",
    },
    "en": {
      "can_title": "Which books can you ship to China?",
      "can_yes": "textbooks, personal books, novels, academic papers, journals",
      "can_no": "politically sensitive content, pirated copies, obscene publications",
      "duty_title": "How much duty will I pay on books?",
      "duty_body": "Books have a <strong>15%</strong> duty rate. Personal-use quantities under <strong>RMB 1,000</strong> (about $140) are usually duty-free; the excess is taxed at 15%.",
      "pack_title": "How should I pack books to avoid moisture & folds?",
      "pack_body": "Wrap in a waterproof bag, reinforce corners, lay flat in the box to avoid folded corners, and place soft paper between hardcovers.",
      "cost_title": "How long to ship books to China?",
      "cost_body": "Air freight is <strong>10–15 working days</strong> door-to-door. Consolidated shipping is <strong>40–60% cheaper</strong> than FedEx/UPS. See <a href=\"/en/pricing\" style=\"color:#0066CC\">pricing</a>.",
    },
  },
  "snacks": {
    "zh": {
      "can_title": "零食哪些能寄、哪些不能寄？",
      "can_yes": "密封包装零食：糖果、薯片、饼干、巧克力（注意温度）",
      "can_no": "肉类/肉干、奶制品、生鲜、蛋类（受动植物检疫限制）",
      "duty_title": "寄零食回国交多少税？",
      "duty_body": "零食行邮税率 <strong>15%</strong>。个人自用、价值人民币 <strong>1000 元</strong> 以内通常免税，超出部分按 15% 计税。",
      "pack_title": "零食怎么打包寄回国？",
      "pack_body": "保留原密封包装，易碎零食（薯片、饼干）单独缓冲，防压防潮；巧克力等怕热食品注意运输温度。",
      "cost_title": "零食寄中国多久到？",
      "cost_body": "空运门到门 <strong>10–15 个工作日</strong>。集运比 FedEx/UPS 便宜 <strong>40–60%</strong>。详见 <a href=\"/zh-cn/pricing\" style=\"color:#0066CC\">运费报价</a>。",
    },
    "en": {
      "can_title": "Which snacks can you ship to China?",
      "can_yes": "sealed packaged snacks: candy, chips, cookies, chocolate (watch temperature)",
      "can_no": "meat/jerky, dairy, fresh produce, eggs (animal & plant quarantine restrictions)",
      "duty_title": "How much duty will I pay on snacks?",
      "duty_body": "Snacks have a <strong>15%</strong> duty rate. Personal-use quantities under <strong>RMB 1,000</strong> (about $140) are usually duty-free; the excess is taxed at 15%.",
      "pack_title": "How should I pack snacks for shipping?",
      "pack_body": "Keep original sealed packaging, cushion fragile snacks (chips, cookies) individually to prevent crushing, and watch temperature for heat-sensitive items like chocolate.",
      "cost_title": "How long to ship snacks to China?",
      "cost_body": "Air freight is <strong>10–15 working days</strong> door-to-door. Consolidated shipping is <strong>40–60% cheaper</strong> than FedEx/UPS. See <a href=\"/en/pricing\" style=\"color:#0066CC\">pricing</a>.",
    },
  },
}

# ---- 锚点 ----
EN_ANCHOR = '<div class="section-title" style="margin-top:40px"><h2>Related questions</h2></div>'
ZH_ANCHOR = '<h2 style="font-size:1.4rem;font-weight:700;margin:24px 0 12px">常见问题</h2>'

def build_block(lang, d):
    """根据语言和内容 dict 生成加厚 HTML 片段"""
    block = ''
    # 1. 能寄/不能寄
    block += f'<h2 style="font-size:1.4rem;font-weight:700;margin:40px 0 14px">{d["can_title"]}</h2>\n'
    yes_label = '✓ 可寄：' if lang == 'zh' else '✓ Allowed: '
    no_label = '✗ 不可寄：' if lang == 'zh' else '✗ Not allowed: '
    block += f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;margin-bottom:8px">\n'
    block += f'  <div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px;font-size:14px;line-height:1.7"><span style="color:#00B900;font-weight:700">{yes_label}</span>{d["can_yes"]}</div>\n'
    block += f'  <div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px;font-size:14px;line-height:1.7"><span style="color:#E53935;font-weight:700">{no_label}</span>{d["can_no"]}</div>\n'
    block += '</div>\n'
    # 2. 税率
    block += f'<h2 style="font-size:1.4rem;font-weight:700;margin:32px 0 12px">{d["duty_title"]}</h2>\n'
    block += f'<p style="color:#64748B;line-height:1.8;margin-bottom:8px">{d["duty_body"]}</p>\n'
    # 3. 打包
    block += f'<h2 style="font-size:1.4rem;font-weight:700;margin:32px 0 12px">{d["pack_title"]}</h2>\n'
    block += f'<p style="color:#64748B;line-height:1.8;margin-bottom:8px">{d["pack_body"]}</p>\n'
    # 4. 时效费用（含内链）
    block += f'<h2 style="font-size:1.4rem;font-weight:700;margin:32px 0 12px">{d["cost_title"]}</h2>\n'
    block += f'<p style="color:#64748B;line-height:1.8;margin-bottom:8px">{d["cost_body"]}</p>\n'
    return block

def main():
    dry = '--dry-run' in sys.argv
    total = 0
    for slug, langs in ITEMS.items():
        for lang, anchor, fname in [
            ('en', EN_ANCHOR, os.path.join(ROOT, 'en/blog/can-i-ship-%s-to-china.html' % slug)),
            ('zh', ZH_ANCHOR, os.path.join(ROOT, 'zh-cn/blog/can-i-ship-%s-to-china.html' % slug)),
        ]:
            if not os.path.exists(fname):
                print('  ❌ 缺失 %s' % fname)
                continue
            c = open(fname, encoding='utf-8').read()
            if anchor not in c:
                print('  ⚠️ 锚点未找到 %s' % fname)
                continue
            block = build_block(lang, langs[lang])
            # 已加厚则跳过（幂等）
            if langs[lang]['can_title'] in c:
                print('  ✓ 已加厚（跳过） %s' % fname)
                continue
            new_c = c.replace(anchor, block + anchor, 1)
            if dry:
                print('  [dry] %s +%d字' % (fname, len(block)))
            else:
                open(fname, 'w', encoding='utf-8').write(new_c)
                print('  ✅ 加厚 %s (+%d字)' % (fname, len(block)))
            total += 1
    print('\n共处理 %d 个文件%s' % (total, '（dry-run）' if dry else ''))

if __name__ == '__main__':
    main()
