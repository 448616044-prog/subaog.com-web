#!/usr/bin/env python3
"""
inject-multilang.py
====================
为 /zh-cn/ 下的所有 HTML 页面注入：
  1) hreflang 三件套（zh-CN / en / x-default）
  2) canonical URL 改写为 /zh-cn/{path}
  3) og:url 同步
  4) 顶部「🌐 中文 / English」语言切换器
  5) lang-switch 相关 CSS

支持幂等：可重复执行不会重复注入（通过 marker 注释识别）。
"""
import re
from pathlib import Path

ROOT = Path("/Users/mac/WorkBuddy/Claw/物流項目/sites/subaog-com")
ZH = ROOT / "zh-cn"
DOMAIN = "https://subaog.com"

# 已有 marker — 已注入则跳过
HREFLANG_MARKER = "<!-- hreflang:auto:subaog-multilang -->"
LANGSW_MARKER = "<!-- lang-switch:auto:subaog-multilang -->"
CANON_MARKER = "<!-- canonical:auto:subaog-multilang -->"

HREFLANG_BLOCK_TPL = """{marker}
<link rel="alternate" hreflang="zh-CN" href="{zh_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{xdef_url}">"""

# 语言切换器 HTML 片段 — 注入到 nav 的最后一个 .dropdown 或 LINE 按钮之前
LANGSW_CSS = """
    /* lang-switch (auto-injected by inject-multilang.py) */
    .lang-switch{display:inline-flex;align-items:center;gap:6px;padding:7px 14px;font-size:13px;font-weight:600;color:var(--primary);border:1.5px solid var(--primary-light);border-radius:var(--radius-pill);background:#fff;transition:all .2s;white-space:nowrap;cursor:pointer;text-decoration:none}
    .lang-switch:hover{background:var(--primary);color:#fff;border-color:var(--primary)}
    .lang-switch .globe{font-size:14px}
    .lang-switch .sep{color:var(--border);margin:0 2px;font-weight:400}
    .lang-switch .lang-cn{color:var(--primary)}
    .lang-switch:hover .lang-cn,.lang-switch:hover .sep{color:#fff}
    @media(max-width:768px){.lang-switch{width:100%;justify-content:flex-start;padding:10px 16px;border-radius:var(--radius);border-color:var(--border);font-size:14px}}
"""

LANGSW_HTML_TPL = """{marker}
      <a href="{other_url}" class="lang-switch" title="Switch to English" hreflang="en">
        <span class="globe">🌐</span>
        <span class="lang-cn">中文</span>
        <span class="sep">/</span>
        <span>English</span>
      </a>
"""


def to_url(rel_to_zh: str) -> str:
    """把 /zh-cn/foo/bar.html → https://subaog.com/zh-cn/foo/bar.html"""
    return f"{DOMAIN}/zh-cn/{rel_to_zh}"


def en_equivalent(rel_to_zh: str) -> str:
    """把 /zh-cn/foo/bar.html → https://subaog.com/en/foo/bar.html"""
    return f"{DOMAIN}/en/{rel_to_zh}"


def process_html(html: str, rel_path: str) -> str:
    """对一个 HTML 字符串做注入，返回修改后的字符串。"""
    zh_url = to_url(rel_path)
    en_url = en_equivalent(rel_path)
    xdef_url = zh_url  # 默认走中文

    # ---- 1) hreflang 注入到 <head> ----
    hreflang_block = HREFLANG_BLOCK_TPL.format(
        marker=HREFLANG_MARKER,
        zh_url=zh_url,
        en_url=en_url,
        xdef_url=xdef_url,
    )
    if HREFLANG_MARKER in html:
        # 已注入过：替换原有块（保留三个 link）
        html = re.sub(
            re.escape(HREFLANG_MARKER) + r"\s*<link[^>]*>\s*<link[^>]*>\s*<link[^>]*>",
            hreflang_block.replace("\n", " ").strip(),
            html,
        )
    else:
        # 首次注入：插到 <title> 之后第一个 <link rel="canonical"> 之前
        # 策略：找到 <head> 内的第一个 meta/link，插在它前面
        if re.search(r"<link[^>]*rel=[\"']canonical[\"']", html):
            html = re.sub(
                r"(<link[^>]*rel=[\"']canonical[\"'][^>]*>)",
                hreflang_block + "\n\\1",
                html,
                count=1,
            )
        else:
            # 退化：插到 </head> 前
            html = html.replace("</head>", hreflang_block + "\n</head>", 1)

    # ---- 2) canonical URL 改写为 /zh-cn/{path} ----
    canonical_new = (
        f'<link rel="canonical" href="{zh_url}">{CANON_MARKER}'
    )
    if CANON_MARKER in html:
        # 已标记：直接替换
        html = re.sub(
            r'<link rel="canonical" href="[^"]*">'
            + re.escape(CANON_MARKER),
            canonical_new,
            html,
        )
    elif re.search(r'<link[^>]*rel=[\"\']canonical[\"\']', html):
        # 有 canonical 但无 marker：补 marker
        html = re.sub(
            r'<link rel="canonical" href="[^"]*">',
            canonical_new,
            html,
            count=1,
        )
    else:
        # 完全没有 canonical（罕见，404 等）：插到 hreflang 块之后
        # 策略：找到 </head> 之前第一个出现的 hreflang 块尾部，加 canonical
        html = html.replace(
            f'<link rel="alternate" hreflang="x-default" href="{xdef_url}">',
            f'<link rel="alternate" hreflang="x-default" href="{xdef_url}">\n  {canonical_new}',
            1,
        )

    # ---- 3) og:url 同步 ----
    html = re.sub(
        r'<meta property="og:url" content="[^"]*">',
        f'<meta property="og:url" content="{zh_url}">',
        html,
    )

    # ---- 4) 注入 lang-switch CSS（放到 .header 的 CSS 后）----
    if LANGSW_MARKER + "-css" not in html:
        # 在 .nav .btn-line:hover 之后注入 CSS
        anchor = ".nav .btn-line:hover{background:#009900;color:#fff}"
        if anchor in html:
            html = html.replace(
                anchor,
                anchor + LANGSW_CSS,
                1,
            )
        else:
            # 退化：放到 </style> 之前
            html = html.replace("</style>", LANGSW_CSS + "\n</style>", 1)

    # ---- 5) 注入 lang-switch HTML 按钮到 nav 内 ----
    langsw_html = LANGSW_HTML_TPL.format(
        marker=LANGSW_MARKER,
        other_url=en_url,
    )
    if LANGSW_MARKER in html and LANGSW_MARKER + "-css" not in html and False:
        pass  # placeholder
    elif LANGSW_MARKER in html and "<a " in html.split(LANGSW_MARKER, 1)[1][:2000] and 'class="lang-switch"' in html:
        # 已注入：跳过
        pass
    else:
        # 找到 LINE 按钮或 nav 的最末子节点之前插入
        # 优先：插在 .btn-line (LINE 按钮) 之前
        line_pattern = r'(<a[^>]*class=[\"\']btn-line[\"\'][^>]*>)'
        if re.search(line_pattern, html):
            html = re.sub(
                line_pattern,
                langsw_html + r"\1",
                html,
                count=1,
            )
        else:
            # 退化：插到 </nav> 之前
            html = html.replace("</nav>", langsw_html + "</nav>", 1)

    return html


def main():
    zh_files = sorted(ZH.rglob("*.html"))
    total = len(zh_files)
    changed = 0
    skipped = 0
    failed = []

    for f in zh_files:
        rel = f.relative_to(ZH).as_posix()  # e.g. "index.html" or "blog/foo.html"
        try:
            original = f.read_text(encoding="utf-8")
            modified = process_html(original, rel)
            if modified != original:
                f.write_text(modified, encoding="utf-8")
                changed += 1
            else:
                skipped += 1
        except Exception as e:
            failed.append((rel, str(e)))

    print(f"\n{'='*60}")
    print(f"  扫描总数: {total}")
    print(f"  已修改:   {changed}")
    print(f"  无变化:   {skipped} (已注入或无需改)")
    print(f"  失败:     {len(failed)}")
    if failed:
        for rel, err in failed:
            print(f"    ❌ {rel}: {err}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()