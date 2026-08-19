#!/usr/bin/env python3
"""subaog.com 中文城市交叉页程序化生成 v2 — 美国TOP20城市 × 中国TOP18城市
输出：zh-cn/city/（带完整 SEO：hreflang 三件套 + canonical + og + FAQPage schema + lang-switch）
"""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = f'{BASE}/zh-cn/city'
os.makedirs(OUT, exist_ok=True)

DOMAIN = "https://subaog.com"
GA_ID = "G-DJGPMS9MOB"

# 美国出发城市（slug, 中文名）
us_cities = [
    ('new-york', '纽约'), ('los-angeles', '洛杉矶'), ('san-francisco', '旧金山'),
    ('chicago', '芝加哥'), ('houston', '休斯顿'), ('seattle', '西雅图'),
    ('boston', '波士顿'), ('washington-dc', '华盛顿'), ('miami', '迈阿密'), ('dallas', '达拉斯'),
    ('atlanta', '亚特兰大'), ('denver', '丹佛'), ('phoenix', '凤凰城'), ('san-jose', '圣何塞'),
    ('san-diego', '圣地亚哥'), ('portland', '波特兰'), ('las-vegas', '拉斯维加斯'),
    ('austin', '奥斯汀'), ('philadelphia', '费城'), ('detroit', '底特律')
]

# 中国到达城市（slug, 中文名, 机场/清关描述）
cn_cities = [
    ('beijing', '北京', '北京经首都国际机场(PEK)/大兴机场(PKX)清关，一线城市，清关配送最快。双清包税门到门，收件人无需自行处理清关，派送到家。'),
    ('shanghai', '上海', '上海经浦东国际机场(PVG)/虹桥机场(SHA)清关，中国最大空港，清关时效最快。双清包税门到门。'),
    ('guangzhou', '广州', '广州经白云国际机场(CAN)清关，华南门户，跨境电商与代购包裹清关效率高。双清包税门到门。'),
    ('shenzhen', '深圳', '深圳经宝安国际机场(SZX)清关，紧邻香港，科技与电商物流枢纽。双清包税门到门。'),
    ('chengdu', '成都', '成都经天府机场(TFU)/双流机场(CTU)清关，西南航空枢纽，中欧班列节点。双清包税门到门。'),
    ('hangzhou', '杭州', '杭州经萧山国际机场(HGH)清关，长三角电商之都，代购包裹清关便捷。双清包税门到门。'),
    ('nanjing', '南京', '南京经禄口国际机场(NKG)清关，长三角城市群，科教机构密集。双清包税门到门。'),
    ('wuhan', '武汉', '武汉经天河国际机场(WUH)清关，华中交通枢纽，高铁网络发达。双清包税门到门。'),
    ('xiamen', '厦门', '厦门经高崎国际机场(XMN)清关，闽南侨乡，东南亚往来频繁。双清包税门到门。'),
    ('tianjin', '天津', '天津经滨海国际机场(TSN)清关，北方最大港口城市，海运直达天津港。双清包税门到门。'),
    ('chongqing', '重庆', '重庆经江北国际机场(CKG)清关，西南直辖市，中欧班列起点，清关配送便捷。双清包税门到门。'),
    ('suzhou', '苏州', '苏州经上海浦东(PVG)/虹桥(SHA)或硕放机场(WUX)清关，长三角制造业重镇，电子与服装产业密集。双清包税门到门。'),
    ('xian', '西安', '西安经咸阳国际机场(XIY)清关，西北门户城市，历史文化名城，高校众多。双清包税门到门。'),
    ('qingdao', '青岛', '青岛经胶东国际机场(TAO)清关，山东沿海港口城市，海运可直达青岛港。双清包税门到门。'),
    ('changsha', '长沙', '长沙经黄花国际机场(CSX)清关，华中交通枢纽，工程机械与文创产业发达。双清包税门到门。'),
    ('zhengzhou', '郑州', '郑州经新郑国际机场(CGO)清关，中欧班列节点城市，航空港实验区，清关效率高。双清包税门到门。'),
    ('dalian', '大连', '大连经周水子国际机场(DLC)清关，东北沿海城市，海运可直达大连港。双清包税门到门。'),
    ('ningbo', '宁波', '宁波经栎社国际机场(NGB)清关，浙江沿海港口城市，海运可直达宁波舟山港。双清包税门到门。'),
]

# 美国城市取件描述
us_note = {
    'new-york': '纽约出发主要经肯尼迪国际机场(JFK)/纽瓦克机场(EWR)。美东华人中心，留学生与代购群体最密集。纽约五区及新泽西部分区域支持上门取件。',
    'los-angeles': '洛杉矶出发主要经洛杉矶国际机场(LAX)。全美最大华人聚集区，代购货源集中地。圣盖博谷(San Gabriel Valley)附近设有合作网点，可自送或预约取件。',
    'san-francisco': '旧金山出发主要经旧金山国际机场(SFO)。硅谷华人圈，科技从业者与海归寄件高频。湾区包括圣何塞、伯克利等区域支持上门取件。',
    'chicago': '芝加哥出发主要经奥黑尔国际机场(ORD)。美中物流枢纽，辐射中西部各州。芝加哥市区及周边支持上门取件。',
    'houston': '休斯顿出发主要经乔治·布什洲际机场(IAH)。能源之都，华人社区成熟，大件搬家需求多。休斯顿都会区支持上门取件。',
    'seattle': '西雅图出发主要经西雅图-塔科马国际机场(SEA)。科技公司华人多，亚马逊/微软员工寄件高频。西雅图都会区支持上门取件。',
    'boston': '波士顿出发主要经洛根国际机场(BOS)。大学城，留学生行李寄回国需求最集中。波士顿市区及周边支持上门取件。',
    'washington-dc': '华盛顿出发主要经杜勒斯机场(IAD)/里根机场(DCA)。政府与国际机构华人，文件与个人物品寄件为主。大华府地区支持上门取件。',
    'miami': '迈阿密出发主要经迈阿密国际机场(MIA)。美国东南门户，拉美中转枢纽。迈阿密都会区支持上门取件。',
    'dallas': '达拉斯出发主要经达拉斯-沃斯堡国际机场(DFW)。德州新兴华人社区，性价比寄件需求增长快。达拉斯都会区支持上门取件。',
    'atlanta': '亚特兰大出发主要经哈茨菲尔德-杰克逊国际机场(ATL)。美东南华人新中心，影视与医疗从业者多，搬家回国需求增长。亚特兰大都会区支持上门取件。',
    'denver': '丹佛出发主要经丹佛国际机场(DEN)。科罗拉多华人社区，商务与个人物品寄件为主。丹佛市区及周边支持上门取件。',
    'phoenix': '凤凰城出发主要经凤凰城天港国际机场(PHX)。亚利桑那华人聚集地，气候宜人，适合退休华人搬家回国。凤凰城都会区支持上门取件。',
    'san-jose': '圣何塞出发主要经圣何塞国际机场(SJC)，也可用旧金山国际机场(SFO)。硅谷核心，科技从业者海归寄件高频。圣何塞市区支持上门取件。',
    'san-diego': '圣地亚哥出发主要经圣地亚哥国际机场(SAN)。加州南部华人圈，美墨边境物流枢纽。圣地亚哥都会区支持上门取件。',
    'portland': '波特兰出发主要经波特兰国际机场(PDX)。俄勒冈华人社区，海淘与代购寄件需求活跃。波特兰市区支持上门取件。',
    'las-vegas': '拉斯维加斯出发主要经哈里·里德国际机场(LAS)。内华达华人常住社群，行李寄送需求集中。拉斯维加斯都会区支持上门取件。',
    'austin': '奥斯汀出发主要经奥斯汀-伯格斯特龙国际机场(AUS)。德州科技新贵，华人工程师海归与搬家寄件增长快。奥斯汀市区支持上门取件。',
    'philadelphia': '费城出发主要经费城国际机场(PHL)。美东历史名城，大学城密集，留学生行李需求稳定。费城都会区支持上门取件。',
    'detroit': '底特律出发主要经底特律大都会机场(DTW)。汽车城，华人工程师与制造业从业者寄件为主。底特律都会区支持上门取件。',
}

css = '''<style>
:root{--primary:#0066CC;--primary-dark:#004C99;--primary-light:#E6F0FA;--accent:#E65100;--bg:#F5F7FA;--bg-white:#FFFFFF;--text:#1A1A2E;--text-secondary:#64748B;--border:#E2E8F0;--radius:10px;--nav-height:68px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:var(--text);line-height:1.8;font-size:16px;background:var(--bg)}
a{text-decoration:none;color:inherit}
.container{max-width:1200px;margin:0 auto;padding:0 20px}
.header{position:fixed;top:0;left:0;right:0;height:var(--nav-height);background:rgba(255,255,255,.96);backdrop-filter:blur(12px);z-index:1000;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.header .container{display:flex;align-items:center;justify-content:space-between;height:100%}
.logo{font-size:19px;font-weight:700;color:var(--primary)}
.nav{display:flex;align-items:center;gap:2px}
.nav a{padding:7px 13px;font-size:13px;font-weight:500;color:var(--text-secondary);border-radius:24px;white-space:nowrap}
.nav a:hover{color:var(--primary);background:var(--primary-light)}
.lang-switch{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;font-size:13px;font-weight:600;color:var(--primary);border:1.5px solid var(--primary-light);border-radius:24px;background:#fff}
@media(max-width:768px){.nav{display:none}}
.city-hero{background:linear-gradient(135deg,#0066CC,#004C99);color:#fff;padding:110px 20px 50px;text-align:center}
.city-hero h1{font-size:clamp(1.4rem,2.4vw,2rem);font-weight:700;margin-bottom:8px}
.city-hero .subtitle{font-size:14px;opacity:.92}
.content{max-width:900px;margin:0 auto;padding:36px 20px}
.info-box{padding:16px 20px;border-radius:var(--radius);margin:20px 0;font-size:15px}
.info-box.primary{background:var(--primary-light);color:var(--primary-dark);border:1px solid #CDE3F5}
h2{font-size:1.2rem;font-weight:700;margin:28px 0 14px;color:var(--primary-dark)}
table{width:100%;border-collapse:collapse;margin:14px 0;background:#fff;border-radius:var(--radius);overflow:hidden}
th{background:var(--primary);color:#fff;padding:12px;font-size:14px;text-align:left}
td{padding:11px 12px;font-size:14px;border-bottom:1px solid var(--border)}
.cta-bar{background:linear-gradient(135deg,#004C99,#0066CC);color:#fff;padding:28px;border-radius:var(--radius);text-align:center;margin:28px 0}
.cta-bar h3{font-size:1.1rem;margin-bottom:4px}
.btn-primary{display:inline-flex;align-items:center;gap:6px;background:#E65100;color:#fff;padding:12px 28px;border-radius:24px;font-weight:600;font-size:15px}
.links-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin:14px 0}
.link-card{display:block;padding:14px 18px;background:var(--bg-white);border:1px solid var(--border);border-radius:var(--radius)}
.link-card h4{font-size:14px;font-weight:600;color:var(--primary)}
.link-card p{font-size:12px;color:var(--text-secondary);margin:2px 0 0}
.footer{background:#1A1A2E;color:#fff;padding:48px 24px 24px;margin-top:64px}
.footer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:32px;max-width:1200px;margin:0 auto}
.footer h4{font-size:13px;color:#ccc;margin-bottom:12px}
.footer a,.footer p{display:block;color:#999;font-size:12px;margin-bottom:6px}
.footer a:hover{color:#fff}
.footer-bottom{text-align:center;padding-top:24px;margin-top:24px;border-top:1px solid rgba(255,255,255,0.1);font-size:11px;color:#666}
</style>'''

count = 0
for us_slug, us_name in us_cities:
    for cn_slug, cn_name, cn_note in cn_cities:
        slug = f'{us_slug}-to-{cn_slug}'
        zh_url = f'{DOMAIN}/zh-cn/city/{slug}.html'
        en_url = f'{DOMAIN}/en/city/{slug}.html'
        h1 = f'{us_name}寄{cn_name} | 美国{us_name}到中国{cn_name}物流专线'
        title = f'{h1} | 速豹国际物流'
        desc = f'从美国{us_name}寄快递到中国{cn_name}。空运7-10天、海运25-35天门到门。{us_name}上门取件，{cn_name}派送到家。免费估价 | 12年国际物流经验，全美免费上门取件，双清包税门到门。'

        # 其他城市寄同一目的地（内链网格）
        related = ''
        for u2, u2_name in us_cities:
            if u2 != us_slug:
                related += f'<a href="/zh-cn/city/{u2}-to-{cn_slug}.html" class="link-card"><h4>{u2_name}寄{cn_name}</h4><p>{cn_name}物流专线</p></a>'

        # FAQ（4 条 + FAQPage schema）
        faq = [
            (f'从{us_name}寄{cn_name}要多久？',
             f'空运专线 7-10 个工作日，海运专线 25-35 天，国际快递 3-5 天。{us_name}出发空运直飞或中转，{cn_name}清关后派送。实际时效受清关和旺季影响。'),
            (f'从{us_name}寄{cn_name}多少钱？',
             f'空运专线约 $5-8/lb，海运专线约 $2-4/lb（大件更划算），国际快递 $10-25/lb。具体按重量、体积重和物品类型报价，可先用运费计算器免费估算。'),
            (f'从{us_name}寄{cn_name}能寄什么？',
             f'留学生行李、代购包裹（保健品/化妆品/电子产品）、搬家家具、商业样品等均可。禁运品（肉类、种子、违禁药品）除外，具体可查「能不能寄」工具。'),
            (f'从{us_name}寄{cn_name}怎么取件？',
             f'{us_note[us_slug]} 取件后门到门配送至{cn_name}收件地址，全程物流追踪。'),
        ]
        faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
            ensure_ascii=False)

        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="applicable-device" content="pc,mobile">
  <title>{title}</title><meta name="description" content="{desc}">
  <link rel="alternate" hreflang="zh-CN" href="{zh_url}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="x-default" href="{zh_url}">
  <link rel="canonical" href="{zh_url}">
  <meta property="og:title" content="{h1}"><meta property="og:description" content="{desc[:80]}">
  <meta property="og:type" content="website"><meta property="og:image" content="{DOMAIN}/assets/images/og-image.jpg"><meta property="og:locale" content="zh_CN"><meta name="lastmod" content="2026-08-19">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"{DOMAIN}/zh-cn/"}},{{"@type":"ListItem","position":2,"name":"美国寄中国","item":"{DOMAIN}/zh-cn/usa-to-china/"}},{{"@type":"ListItem","position":3,"name":"{us_name}→{cn_name}","item":"{zh_url}"}}]}}</script>
  <script type="application/ld+json">{faq_schema}</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
  {css}
</head>
<body>
  <header class="header"><div class="container"><a href="/zh-cn/" class="logo">速豹国际<span style="font-size:11px;color:var(--text-secondary);font-weight:400;margin-left:8px">美国寄中国</span></a><nav class="nav"><a href="/zh-cn/">首页</a><a href="/zh-cn/usa-to-china/">美国寄中国</a><a href="/zh-cn/pricing.html">运费报价</a><a href="/zh-cn/tools/">工具</a>
      <a href="{en_url}" class="lang-switch" title="Switch to English" hreflang="en"><span class="globe">🌐</span><span class="lang-cn">中文</span><span class="sep">/</span><span>English</span></a>
</nav></div></header>
  <section class="city-hero"><div class="container"><h1>美国{us_name}寄中国{cn_name}</h1><p class="subtitle">空运7-10天 · 海运25-35天 · 门到门专线</p></div></section>
  <div class="content">
    <div class="info-box primary">📍 速豹国际提供美国{us_name}到中国{cn_name}的物流专线服务：{us_name}上门取件 → 中国{cn_name}派送到家。留学生行李、代购包裹、搬家货运均可。</div>
    <h2>运输方式与价格</h2>
    <table><tr><th>运输方式</th><th>价格/lb</th><th>时效</th><th>适合物品</th></tr><tr><td>空运专线</td><td>$5-8</td><td>7-10天</td><td>中小包裹、行李、代购</td></tr><tr><td>海运专线</td><td>$2-4</td><td>25-35天</td><td>搬家、大件家具、批量货运</td></tr><tr><td>国际快递</td><td>$10-25</td><td>3-5天</td><td>急件、文件、高价值物品</td></tr></table>
    <h2>{us_name}出发：机场与取件</h2><p>{us_note[us_slug]}</p>
    <h2>{cn_name}到达：清关与配送</h2><p>{cn_note}</p>
    <div class="cta-bar"><h3>{us_name}寄{cn_name}，立即获取报价</h3><p style="color:var(--text-secondary);margin-bottom:12px">30分钟出方案，免费上门估价</p><a href="https://d.salesmartly.com/fuxikn" class="btn-primary" target="_blank">💬 免费咨询</a></div>
    <h2>其他城市寄{cn_name}</h2><div class="links-grid">{related}</div>
    <h2>常见问题</h2>{''.join(f'<div style="margin:16px 0"><p style="font-weight:700;margin:0 0 4px">Q：{q}</p><p style="margin:0;color:var(--text-secondary)">{a}</p></div>' for q, a in faq)}
    <h2>更多攻略</h2><div class="links-grid"><a href="/zh-cn/usa-to-china/" class="link-card"><h4>美国寄中国全攻略</h4><p>空运/海运/快递对比</p></a><a href="/zh-cn/tools/shipping-calculator.html" class="link-card"><h4>运费计算器</h4><p>免费估算运费</p></a></div>
  </div>
  <footer class="footer"><div class="footer-grid"><div><h4>速豹国际物流</h4><p>美国寄中国专线</p></div><div><h4>核心服务</h4><a href="/zh-cn/usa-to-china/">美国寄中国</a><a href="/zh-cn/blog/student-luggage-shipping-guide.html">留学生行李</a></div><div><h4>工具</h4><a href="/zh-cn/tools/shipping-calculator.html">运费计算器</a><a href="/zh-cn/tools/can-i-ship.html">能不能寄</a></div><div><h4>联系</h4><p>在线客服：<a href="https://d.salesmartly.com/fuxikn" style="color:#999">点击咨询</a></p></div></div><div class="footer-bottom"><p>&copy; 2026 速豹国际物流</p></div></footer>
</body></html>'''

        with open(f'{OUT}/{slug}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1

print(f'✅ 中文城市交叉页生成完成：{count} 页 ({len(us_cities)}美国城市 × {len(cn_cities)}中国城市)')
print(f'   输出目录：{OUT}')
