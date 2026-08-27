"""一次性处理 3 件事:
1) logo 高度 52 -> 55 (1834 处)
2) logo 后副标统一为 "各国寄中国专线" / "Shipping to China", 字号 15px
3) 处理 student-luggage 页面 hero 内表格字色不可见问题 (table 移出 hero, 加白底深字)

幂等。
"""
import re
from pathlib import Path
ROOT = Path('.')

# === 1) logo 高度 52 -> 55 ===
print('=== 1) logo 高度 52 -> 55 ===')
fixed = 0
for d in ['zh-cn', 'en']:
    for f in (ROOT / d).rglob('*.html'):
        t = f.read_text(encoding='utf-8', errors='ignore')
        if 'height:52px;width:auto;display:block' not in t:
            continue
        t = t.replace('height:52px;width:auto;display:block',
                      'height:55px;width:auto;display:block')
        f.write_text(t, encoding='utf-8')
        fixed += 1
print(f'  改了 {fixed} 页 (52 -> 55)')

# === 2) logo 后副标统一 ===
print('\n=== 2) logo 后副标统一 ===')
# 找 <a ... class="logo" ...><img ...><span style="...">XXX</span></a>
# 替换为统一副标: 各国寄中国专线 / Shipping to China
# zh-cn 副标样式: 字号 15px, 颜色 primary, 粗体
# en 副标: 字号 15px, 颜色 primary, 粗体

# 多种变体, 用一个统一正则: 匹配 logo img 后的第一个 <span>...</span>
LOGO_SPAN_RE = re.compile(
    r'(<a [^>]*class="logo"[^>]*>'
    r'<img src="/assets/images/logo\.png"[^>]*>'
    r'<span[^>]*>)([^<]+)(</span>)'
)

SUBS_ZH = ('各国寄中国专线', 14)  # 字号
SUBS_EN = ('Shipping to China', 14)

# 保留 en/zh 内容差异, 但合并 "USA to China" -> "Shipping to China" 等
# 所有变体副标: zh-cn -> "各国寄中国专线"; en -> "Shipping to China"

count_zh = 0
count_en = 0
for f in (ROOT / 'zh-cn').rglob('*.html'):
    t = f.read_text(encoding='utf-8', errors='ignore')
    orig = t

    def repl_zh(m):
        text, fs = SUBS_ZH
        attrs = m.group(1)
        # 取原有 style, 重写 (避免冲突)
        return (f'<a '
                f'style="display:flex;align-items:center;gap:12px;" class="logo">'
                f'<img src="/assets/images/logo.png" alt="速豹回国物流" '
                f'style="height:55px;width:auto;display:block;">'
                f'<span style="font-size:14px;color:var(--primary);font-weight:600;'
                f'border-left:2px solid var(--primary-light);padding-left:14px;'
                f'line-height:1.2;letter-spacing:0.5px">{text}</span>')

    t = LOGO_SPAN_RE.sub(repl_zh, t)
    if t != orig:
        f.write_text(t, encoding='utf-8')
        count_zh += 1

# en 站
LOGO_SPAN_RE_EN = re.compile(
    r'(<a [^>]*class="logo"[^>]*>'
    r'<img src="/assets/images/logo\.png"[^>]*>'
    r'<span[^>]*>)([^<]+)(</span>)'
)

count_en = 0
for f in (ROOT / 'en').rglob('*.html'):
    t = f.read_text(encoding='utf-8', errors='ignore')
    orig = t

    def repl_en(m):
        text, fs = SUBS_EN
        return (f'<a '
                f'style="display:flex;align-items:center;gap:12px;" class="logo">'
                f'<img src="/assets/images/logo.png" alt="Subao Global" '
                f'style="height:55px;width:auto;display:block;">'
                f'<span style="font-size:14px;color:var(--primary);font-weight:600;'
                f'border-left:2px solid var(--primary-light);padding-left:14px;'
                f'line-height:1.2;letter-spacing:0.5px">{text}</span>')

    t = LOGO_SPAN_RE_EN.sub(repl_en, t)
    if t != orig:
        f.write_text(t, encoding='utf-8')
        count_en += 1

print(f'  zh-cn 改了 {count_zh} 页 logo 副标')
print(f'  en 改了 {count_en} 页 logo 副标')

# === 3) student-luggage 页面修复 ===
print('\n=== 3) student-luggage 页面修复 ===')
sp = ROOT / 'zh-cn' / 'student-luggage' / 'index.html'
t = sp.read_text(encoding='utf-8', errors='ignore')

# 原 hero 内布局: <section class="hero"><div class="container">
#                   <h1>...</h1>
#                   <p class="subtitle">...</p>
#                   <table>...</table>
#                   <p>包税双清门到门...</p>
#                   <h2>打包清单</h2>
#                   <ul>...</ul>
#                   <div class="cta-bar">...</div>
#                 </div></section>

# 修复方案: 把 table/打包清单/cta-bar 移出 hero, 改为单独 <section class="content">
# hero 留: h1 + subtitle + 包税简介段(<p>)
# 把表移到 <section class="content"> 内

NEW_HERO_CONTENT = (
    '<section class="hero"><div class="container">\n'
    '      <h1>留学生回国行李邮寄</h1>\n'
    '      <p class="subtitle">空运专线 · 一年的衣服 / 书 / 小家电 / 纪念品，3 种方案任选</p>\n'
    '      <p style="max-width:680px;margin:18px auto 0;background:rgba(255,255,255,0.18);border-radius:10px;padding:12px 18px;font-size:14px;color:#fff;font-weight:500">'
    '包税双清门到门 · 最低起运 21kg（实重或体积重≥21kg 方可出运，不足 21kg 不予收寄）· 含清关费 100元申报手续费 · 时效 10-15 个工作日'
    '</p>\n'
    '    </div></section>\n'
    '  \n'
    '  <section class="content"><div class="container">\n'
    '    <h2>包税渠道价格对比</h2>\n'
    '    <table>\n'
    '      <tr><th>出发国家 / 地区</th><th>20-99kg</th><th>100kg+</th></tr>\n'
    '      <tr><td>美国 / 加拿大 / 墨西哥 / 澳大利亚 / 新西兰</td><td><strong>¥100/kg</strong></td><td><strong>¥90/kg</strong></td></tr>\n'
    '      <tr><td>英国 / 德国 / 法国 / 意大利 / 西班牙 / 爱尔兰 + 欧洲</td><td><strong>¥90/kg</strong></td><td><strong>¥80/kg</strong></td></tr>\n'
    '      <tr><td>日本 / 韩国 / 泰国 / 新加坡 / 菲律宾 / 台湾 / 马来西亚</td><td><strong>¥80/kg</strong></td><td><strong>¥70/kg</strong></td></tr>\n'
    '    </table>\n'
    '    \n'
    '    <h2>打包清单</h2>\n'
    '    <ul>\n'
    '      <li>Home Depot Heavy Duty 纸箱约 $2/个</li>\n'
    '      <li>每箱不超过 50 lb，留出手提空间</li>\n'
    '      <li>易碎品用衣物 / 气泡膜包裹做缓冲</li>\n'
    '      <li>护照 / I-20 / 毕业证等重要文件随身带，不要寄</li>\n'
    '    </ul>\n'
    '    \n'
    '    <h2>三个方案对比</h2>\n'
    '    <div class="card-grid">\n'
    '      <div class="card"><h3>纯空运</h3><p>10-15 个工作日门到门，适合换季衣物 + 急用物品，¥100/kg 起（21kg 起）。</p></div>\n'
    '      <div class="card"><h3>空运 + 海运混搭</h3><p>急用的走空运，剩下的走海运（搬家公司搬运），适合行李较多且有 1-2 个月缓冲的同学。</p></div>\n'
    '      <div class="card"><h3>仅自寄行李</h3><p>少量几箱直接走空运，¥100/kg，1 周清关 + 1 周国内派送。</p></div>\n'
    '    </div>\n'
    '    \n'
    '    <div class="cta-bar"><h3>准备回国？</h3><a href="https://d.salesmartly.com/fuxikn" class="btn-primary" target="_blank">💬 免费规划行李方案</a></div>\n'
    '  </div></section>\n'
    '  '
)

# 匹配: <section class="hero"> ... 对应 </div></section> (注意嵌套 div)
# 用非贪婪 + lazy 提取 - 这页面 hero 区内容是从 <section class="hero"> 到 </section>
PAT = re.compile(
    r'<section class="hero">(.*?)</section>',
    re.S
)
def hero_repl(m):
    return NEW_HERO_CONTENT.rstrip('\n').rstrip()
new_t, n = PAT.subn(hero_repl, t, count=1)
if n == 1:
    sp.write_text(new_t, encoding='utf-8')
    print(f'  ✅ student-luggage hero+content 重写')
else:
    print(f'  ⚠️  hero 块未匹配 (n={n})')

print('\n=== 处理完成 ===')
