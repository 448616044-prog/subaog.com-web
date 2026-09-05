"""全站 footer 工具页链接补齐：More/更多资源 栏补全 6 个工具页"""
import os, re, subprocess

BASE = "/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com"

# 6 个工具页（每个语言）
TOOL_LINKS_EN = [
    ('/en/tools/can-i-ship', 'Can I Ship?'),
    ('/en/tools/volume-calculator', 'Volume Calc'),
    ('/en/tools/transit-time', 'Transit Time'),
    ('/en/tools/package-consolidation-calculator', 'Consolidation Calc'),
    ('/en/tools/shipping-calculator', 'Shipping Calculator'),
    ('/en/tools/customs-duty-calculator', 'Customs Duty'),
]
TOOL_LINKS_ZH = [
    ('/zh-cn/tools/can-i-ship', '能不能寄'),
    ('/zh-cn/tools/volume-calculator', '材积计算'),
    ('/zh-cn/tools/transit-time', '时效查询'),
    ('/zh-cn/tools/package-consolidation-calculator', '合箱计算'),
    ('/zh-cn/tools/shipping-calculator', '运费计算'),
    ('/zh-cn/tools/customs-duty-calculator', '关税估算'),
]

# 收集所有 HTML
files = subprocess.run(["find", BASE, "-name", "*.html", "-not", "-path", "*/\\.*"],
                        capture_output=True, text=True, timeout=60).stdout.strip().split("\n")
files = [f for f in files if f]

# 匹配 More 栏
# 两种格式：
#   <div><h4>More</h4><a ...>...</a>...</div>
#   <div><h4>更多资源</h4><a ...>...</a>...</div>
MORE_RE = re.compile(r'(<div[^>]*>\s*<h4>(?:More|更多资源)</h4>)(.*?)(</div>)', re.S)

def fill_more_div(content_match, lang):
    """在 More/更多资源 div 里追加缺失的工具页"""
    head, body, tail = content_match.group(1), content_match.group(2), content_match.group(3)
    links = TOOL_LINKS_EN if lang == "en" else TOOL_LINKS_ZH

    # 已存在的 href
    existing = set(re.findall(r'href="([^"]+)"', body))

    new_links_html = ""
    added = 0
    for href, label in links:
        if href not in existing:
            new_links_html += f'<a href="{href}">{label}</a>'
            added += 1

    if added == 0:
        return None  # 无需修改

    new_body = body + new_links_html
    return head + new_body + tail


modified = 0
errors = []
for f in files:
    rel = os.path.relpath(f, BASE)
    # 跳过工具页自身（避免改自身）
    if "/tools/" in rel:
        continue
    with open(f, encoding="utf-8") as fp:
        t = fp.read()
    # 判定语言
    lang = "en" if rel.startswith("en/") or rel == "en/index.html" else "zh-cn"

    m = MORE_RE.search(t)
    if not m:
        continue  # 该页没有 More 栏

    new_div = fill_more_div(m, lang)
    if new_div is None:
        continue

    new_t = t.replace(m.group(0), new_div, 1)
    if new_t != t:
        with open(f, "w", encoding="utf-8") as fp:
            fp.write(new_t)
        modified += 1

print(f"修改文件数: {modified}")