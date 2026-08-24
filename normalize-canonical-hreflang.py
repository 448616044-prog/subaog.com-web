#!/usr/bin/env python3
"""全站 canonical + hreflang + og:url 标准化修复
目标：目录页用尾斜杠，文件页用无扩展名；补全自引用与互反 hreflang；修复 city-item 生成器导致的残缺标签。
"""
import re
from pathlib import Path

SITE = "https://subaog.com"
ROOT = Path(".")


def final_url(path: Path) -> str:
    """返回文件在 Cloudflare Pages 上的最终 200 URL 路径（带前导 /）"""
    rel = "/" + str(path)
    if path.name == "index.html":
        # /zh-cn/usa-to-china/los-angeles/ 保留尾斜杠
        return "/" + str(path.parent).rstrip("/") + "/"
    # /zh-cn/blog/x
    if rel.endswith(".html"):
        return rel[:-5]
    return rel


def counterpart_path(path: Path) -> Path | None:
    """返回 zh<->en 镜像路径；根页返回 None"""
    rel = str(path)
    if rel.startswith("zh-cn/"):
        return Path("en/" + rel[6:])
    if rel.startswith("en/"):
        return Path("zh-cn/" + rel[3:])
    return None


def clean_block(own_url: str, lang: str, cp_url: str | None) -> str:
    """生成干净的 canonical + hreflang 块"""
    lines = [f'<link rel="canonical" href="{SITE}{own_url}">']
    if cp_url:
        zh = own_url if lang == "zh" else cp_url
        en = own_url if lang == "en" else cp_url
        lines += [
            f'<link rel="alternate" hreflang="zh-CN" href="{SITE}{zh}">',
            f'<link rel="alternate" hreflang="en" href="{SITE}{en}">',
            f'<link rel="alternate" hreflang="x-default" href="{SITE}{zh}">',
        ]
    return "\n  ".join(lines)


def normalize_file(path: Path):
    t = path.read_text(encoding="utf-8", errors="ignore")
    own = final_url(path)
    lang = "zh" if str(path).startswith("zh-cn/") else ("en" if str(path).startswith("en/") else "root")

    cp_path = counterpart_path(path)
    cp_url = final_url(cp_path) if cp_path and cp_path.exists() else None

    # 1) 移除所有旧的 canonical / alternate link（包括残缺标签）
    t = re.sub(r'<link\s+rel="(?:canonical|alternate)"[^>]*>\s*', '', t, flags=re.S | re.I)

    # 2) 修正 og:url
    t = re.sub(r'<meta\s+property="og:url"\s+content="[^"]*"\s*/?>', '', t, flags=re.S | re.I)

    # 3) 组装新块
    block = clean_block(own, lang, cp_url)

    # 4) 插入位置：优先放在 description meta 之后，否则 title 之后
    desc_re = re.compile(r'(<meta\s+name="description"\s+content="[^"]*"\s*/?>)', re.S | re.I)
    m = desc_re.search(t)
    if m:
        insert_pos = m.end()
        new_t = t[:insert_pos] + "\n  " + block + t[insert_pos:]
    else:
        title_re = re.compile(r'(</title>)', re.S | re.I)
        m2 = title_re.search(t)
        if m2:
            insert_pos = m2.end()
            new_t = t[:insert_pos] + "\n  " + block + t[insert_pos:]
        else:
            new_t = t  # 不应该发生

    # 5) 在 head 末尾前补 og:url（若被删了）
    og = f'<meta property="og:url" content="{SITE}{own}">'
    # 放到 charset/viewport 附近或 block 后面：简单插到 block 后面
    # 由于上面已经插了 block，现在把 og 追加到 block 同一位置
    new_t = new_t.replace(block, block + "\n  " + og, 1)

    path.write_text(new_t, encoding="utf-8")


def main():
    files = sorted([p for p in ROOT.rglob("*.html") if p.is_file()])
    fixed = 0
    for p in files:
        try:
            normalize_file(p)
            fixed += 1
        except Exception as e:
            print(f"  ❌ {p}: {e}")
    print(f"✅ 标准化完成：{fixed} 个 HTML 文件")


if __name__ == "__main__":
    main()
