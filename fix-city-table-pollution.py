#!/usr/bin/env python3
"""
修复 zh-cn/city 342 页表格污染：
FAQ 答案文字（"怎么取件"）被错误混入价格表格第三行，形成
  <tr><td>。...支持上门取件。</p>
且导致 <table> 缺 </table> 闭合。
修复 = 删除污染行 + 补 </table>。
幂等：修复后不再有 <tr><td>。 模式。
"""
import re, glob, sys, json

DRY = "--run" not in sys.argv
PAT = re.compile(r'<tr><td>。.*?</p>', re.S)

fixed = 0
skipped = 0
for f in glob.glob('zh-cn/city/*.html'):
    s = open(f, encoding='utf-8').read()
    m = PAT.search(s)
    if not m:
        continue
    if s.count('<table') != s.count('</table>') + 1:
        # 结构性异常，跳过人工检查
        print(f"  ⚠️ 结构异常跳过: {f} (<table={s.count('<table')} </table={s.count('</table>')})")
        skipped += 1
        continue
    new_s = PAT.sub('</table>', s, count=1)
    if not DRY:
        open(f, 'w', encoding='utf-8').write(new_s)
    fixed += 1
    if DRY and fixed <= 5:
        frag = m.group(0)
        print(f"  [DRY] {f}")
        print(f"        {frag[:70]}... → </table>")

print(f"\n{'DRY-RUN 预览' if DRY else '执行完成'}: 修复 {fixed} 个文件，跳过 {skipped} 个异常")
if DRY:
    print("加 --run 实际执行")
