#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站 header logo 文字 -> 图片(assets/images/logo.png), 保留副标 span
"""
import re
from pathlib import Path

ROOT = Path(".")

IMG_ZH = '<img src="/assets/images/logo.png" alt="速豹回国物流" style="height:44px;width:auto;display:block">'
IMG_EN = '<img src="/assets/images/logo.png" alt="Subao Global" style="height:44px;width:auto;display:block">'


def fix(t, lang):
    img = IMG_ZH if lang == "zh-cn" else IMG_EN
    href = "/" if lang == "zh-cn" else "/en/"
    # 有副标: 文字<span> -> img<span>
    t = re.sub(
        rf'<a href="{href}" class="logo">[^<]*<span>',
        f'<a href="{href}" class="logo">{img}<span>',
        t,
    )
    # 无副标: 文字</a> -> img</a>
    t = re.sub(
        rf'<a href="{href}" class="logo">[^<]*</a>',
        f'<a href="{href}" class="logo">{img}</a>',
        t,
    )
    return t


def main():
    fixed = 0
    for d in ["zh-cn", "en"]:
        lang = d
        for f in sorted((ROOT / d).rglob("*.html")):
            t = f.read_text(encoding="utf-8", errors="ignore")
            new = fix(t, lang)
            if new != t:
                f.write_text(new, encoding="utf-8")
                fixed += 1
    print(f"修复 {fixed} 页")


if __name__ == "__main__":
    main()
