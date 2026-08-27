#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAQ 区域(JSON-LD FAQPage + 可见 faq 区块) 海运 -> 空运, 保留正文海运概念(选择1)
"""
import re
from pathlib import Path

ROOT = Path(".")

ZH = [
    ("海运和空运怎么选", "空运专线怎么选"),
    ("海运 vs 空运", "空运专线"),
    ("海运vs空运", "空运专线"),
    ("海运要多久", "空运要多久"),
    ("海运怎么操作", "空运怎么操作"),
    ("海运怎么寄", "空运怎么寄"),
    ("海运搬家", "空运搬家"),
    ("海运", "空运"),
]
EN = [
    ("sea freight vs air freight", "air freight"),
    ("Sea freight takes", "Air freight takes"),
    ("Sea freight", "Air freight"),
    ("sea freight", "air freight"),
]


def fix_faq_block(t: str, pairs) -> str:
    def repl_block(m):
        blk = m.group(0)
        for old, new in pairs:
            blk = blk.replace(old, new)
        return blk
    return t


def main():
    fixed = 0
    for d, pairs in [("zh-cn", ZH), ("en", EN)]:
        for f in sorted((ROOT / d).rglob("*.html")):
            t = f.read_text(encoding="utf-8", errors="ignore")
            orig = t

            def sub_faq(m):
                blk = m.group(0)
                for old, new in pairs:
                    blk = blk.replace(old, new)
                return blk

            # FAQPage JSON-LD 块
            t = re.sub(
                r'<script type="application/ld\+json">(.*?"@type"\s*:\s*"FAQPage".*?)</script>',
                sub_faq,
                t,
                flags=re.S,
            )
            # 可见 FAQ 区块(faq-item/faq-a/faq-q)
            t = re.sub(
                r'(<div class="faq-(?:item|a|q)"[^>]*>.*?</div>)',
                sub_faq,
                t,
                flags=re.S,
            )
            if t != orig:
                f.write_text(t, encoding="utf-8")
                fixed += 1
    print(f"修复 {fixed} 页")


if __name__ == "__main__":
    main()
