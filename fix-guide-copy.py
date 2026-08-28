import re
from pathlib import Path

ROOT = Path('.')

# routes 引导文案（含价格差异）
routes_zh = ('<div class="section-title"><h2>全部回国线路</h2>'
             '<p>覆盖 7 大出发地区域 · 空运 10-15 个工作日 · 双清包税门到门 · '
             '美/加/澳 ¥100/kg 起、欧洲 ¥90/kg 起、日韩东南亚 ¥80/kg 起（20kg 起）</p></div>')

routes_en = ('<div class="section-title"><h2>All routes to China</h2>'
             '<p>7 origin regions · air freight 10-15 working days · tax-inclusive door-to-door · '
             'USA/Canada/Australia from ¥100/kg, Europe from ¥90/kg, Japan/Korea/SE Asia from ¥80/kg (20kg+)</p></div>')

# can-i-ship-index 引导文案（品类说明）
ship_zh = ('<div class="section-title"><h2>按品类查能不能寄</h2>'
           '<p>25 类物品清关要求、禁运清单与税率一页汇总 · 拿不准的品类免费咨询，30 分钟给方案</p></div>')

ship_en = ('<div class="section-title"><h2>Check by category</h2>'
           '<p>Customs rules, prohibited lists and duty rates for 25 item categories — contact us for anything unclear, we reply within 30 minutes</p></div>')

def patch(path, old_h2, new_block):
    p = ROOT / path
    t = p.read_text(encoding='utf-8', errors='ignore')
    # 匹配 section-title 块
    t2, n = re.subn(r'<div class="section-title">.*?</div>', new_block, t, count=1, flags=re.S)
    p.write_text(t2, encoding='utf-8')
    print(f'  {"✅" if n else "❌"} {path} ({n} 处)')

patch('zh-cn/routes/index.html', '全部回国线路', routes_zh)
patch('en/routes/index.html', 'All routes to China', routes_en)
patch('zh-cn/can-i-ship-index/index.html', '按品类查能不能寄', ship_zh)
patch('en/can-i-ship-index/index.html', 'Check by category', ship_en)

print('\n聚合页引导文案加厚完成')
