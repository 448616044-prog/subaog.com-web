#!/usr/bin/env python3
"""截断过长 meta description 与 title"""
import re
from pathlib import Path

ROOT = Path(".")
DESC_MAX = 155
TITLE_MAX = 58


def truncate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    cut = text.rfind(" ", 0, max_len - 2)
    if cut < max_len // 2:
        cut = max_len - 2
    return text[:cut].rstrip(" ，、.") + "…"


def fix_file(path: Path):
    t = path.read_text(encoding="utf-8", errors="ignore")
    changed = False
    desc_changed = title_changed = False

    dm = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', t, flags=re.S | re.I)
    if dm:
        desc = dm.group(1)
        if len(desc) > DESC_MAX:
            new_desc = truncate(desc, DESC_MAX)
            t = t[:dm.start(1)] + new_desc + t[dm.end(1):]
            changed = True
            desc_changed = True

    tm = re.search(r'<title>([^<]*)</title>', t, flags=re.S | re.I)
    if tm:
        title = tm.group(1)
        if len(title) > TITLE_MAX:
            new_title = truncate(title, TITLE_MAX)
            t = t[:tm.start(1)] + new_title + t[tm.end(1):]
            changed = True
            title_changed = True

    if changed:
        path.write_text(t, encoding="utf-8")
    return desc_changed, title_changed


def main():
    files = list(ROOT.rglob("*.html"))
    fixed_desc = fixed_title = 0
    for p in files:
        try:
            dc, tc = fix_file(p)
            if dc: fixed_desc += 1
            if tc: fixed_title += 1
        except Exception as e:
            print(f"  ❌ {p}: {e}")
    print(f"✅ meta description 截断: {fixed_desc} 页 | title 截断: {fixed_title} 页")


if __name__ == "__main__":
    main()
