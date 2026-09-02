#!/usr/bin/env python3
"""
subaog.com 全站 Salesmartly 咨询链接 GA4 转化埋点
给 <a href="https://d.salesmartly.com/fuxikn" ...> 加 onclick consult_click 事件，
带 page_path 落地页标记，根治「客户咨询来源不明」。

用法：
  python3 fix-consult-tracking.py          # dry-run 预览
  python3 fix-consult-tracking.py --run    # 实际执行
"""
import re, sys, glob

BASE_DIRS = ["zh-cn", "en"]

# onclick：window.gtag 短路保护（无 GA4 页面点击不报错），事件带落地页路径
GTAG_ONCLICK = (
    "window.gtag&&gtag('event','consult_click',"
    "{event_category:'conversion',event_label:'salesmartly',page_path:location.pathname})"
)

# 匹配 <a ... href="https://d.salesmartly.com/fuxikn" ... > 开标签（href 可能非首属性）
A_RE = re.compile(r'(<a\b[^>]*href="https://d\.salesmartly\.com/fuxikn"[^>]*)(>)', re.IGNORECASE)


def process(s):
    def add_onclick(m):
        a_open = m.group(1)
        if 'onclick=' in a_open:          # 幂等：已有 onclick 跳过
            return m.group(0)
        return f'{a_open} onclick="{GTAG_ONCLICK}"{m.group(2)}'
    return A_RE.sub(add_onclick, s)


def main():
    run = "--run" in sys.argv
    files = []
    for d in BASE_DIRS:
        files += glob.glob(f"{d}/**/*.html", recursive=True)

    total_links = 0
    changed_files = 0
    already = 0
    for f in files:
        s = open(f, encoding="utf-8").read()
        n_before = len(A_RE.findall(s))
        if n_before == 0:
            continue
        out = process(s)
        n_after = len(A_RE.findall(out))
        added = n_before - len(re.findall(r'onclick="window\.gtag&&gtag', out))
        total_links += n_before
        if out != s:
            changed_files += 1
            if run:
                open(f, "w", encoding="utf-8").write(out)
        else:
            already += n_before
    mode = "✅ 已执行" if run else "[dry-run] 预览"
    print(f"{mode}: {len(files)} 个文件扫描")
    print(f"  Salesmartly 链接总数: {total_links}")
    print(f"  需要埋点的文件: {changed_files}")
    print(f"  已埋点跳过(幂等): {already} 处")


if __name__ == "__main__":
    main()
