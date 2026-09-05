#!/usr/bin/env python3
"""补拉：中文站 /zh-cn/ 表现 + 高展现词排名分段 + 近28天页面点击。回答微信来源与阶段核心。"""
import json, time, base64, ssl, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timedelta

PROXY = "http://127.0.0.1:17891"
CRED = json.loads(open("/Users/mac/WorkBuddy/Claw/SEO/subao-seo-service-account.json").read())
TOKEN_URI = "https://oauth2.googleapis.com/token"
SC_API = "https://www.googleapis.com/webmasters/v3"
SITE = "sc-domain:subaog.com"

def urlopen_with_proxy(req, timeout=30):
    ctx = ssl.create_default_context()
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}),
        urllib.request.HTTPSHandler(context=ctx))
    return opener.open(req, timeout=timeout)

def create_jwt(scope):
    header = {"alg": "RS256", "typ": "JWT"}
    now = int(time.time())
    claim = {"iss": CRED["client_email"], "scope": scope, "aud": TOKEN_URI, "exp": now+3600, "iat": now}
    b64 = lambda d: base64.urlsafe_b64encode(d).rstrip(b"=").decode()
    h, c = b64(json.dumps(header).encode()), b64(json.dumps(claim).encode())
    from cryptography.hazmat.primitives.serialization import load_pem_private_key
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes
    key = load_pem_private_key(CRED["private_key"].encode(), password=None)
    sig = key.sign(f"{h}.{c}".encode(), padding.PKCS1v15(), hashes.SHA256())
    return f"{h}.{c}.{b64(sig)}"

def get_token(scope):
    jwt = create_jwt(scope)
    data = urllib.parse.urlencode({"grant_type":"urn:ietf:params:oauth:grant-type:jwt-bearer","assertion":jwt}).encode()
    req = urllib.request.Request(TOKEN_URI, data=data, method="POST")
    req.add_header("Content-Type","application/x-www-form-urlencoded")
    return json.loads(urlopen_with_proxy(req).read())["access_token"]

def api_post(token, path, body):
    req = urllib.request.Request(f"{SC_API}{path}", data=json.dumps(body).encode(), method="POST")
    req.add_header("Content-Type","application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        return json.loads(urlopen_with_proxy(req).read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode()}

def q(token, dims, rowLimit, start, end):
    body = {"startDate": start.isoformat(), "endDate": end.isoformat(), "dimensions": dims, "rowLimit": rowLimit}
    return api_post(token, f"/sites/{urllib.parse.quote(SITE, safe='')}/searchAnalytics/query", body)

def main():
    token = get_token("https://www.googleapis.com/auth/webmasters.readonly")
    today = datetime.now().date()
    d28 = today - timedelta(days=28)

    # 近28天 全部 query，按展现排序看排名分段
    qq = q(token, ["query"], 500, d28, today)
    rows = qq.get("rows", [])

    print("=== 近28天 高展现词 TOP30（展现>10）===")
    big = [r for r in rows if r.get("impressions", 0) >= 10]
    big.sort(key=lambda x: -x.get("impressions", 0))
    for r in big[:30]:
        print(f"  {r.get('impressions',0):>4}imp {r.get('clicks',0):>2}clk pos{r.get('position',0):>4.1f}  「{r['keys'][0]}」")

    # 排名分段统计（有展现的词）
    seg = {"TOP3":0,"TOP10":0,"11-30":0,"31-100":0}
    for r in rows:
        p = r.get("position", 0)
        if p <= 3: seg["TOP3"] += 1
        elif p <= 10: seg["TOP10"] += 1
        elif p <= 30: seg["11-30"] += 1
        else: seg["31-100"] += 1
    print(f"\n排名分段(有展现词总数 {len(rows)}): {seg}")

    # 中文词 vs 英文词
    cn = [r for r in rows if any('\u4e00' <= ch <= '\u9fff' for ch in r["keys"][0])]
    cn.sort(key=lambda x: -x.get("impressions", 0))
    print(f"\n=== 中文词（{len(cn)} 个，微信客户来源）TOP30 ===")
    for r in cn[:30]:
        print(f"  {r.get('impressions',0):>4}imp {r.get('clicks',0):>2}clk pos{r.get('position',0):>4.1f}  「{r['keys'][0]}」")

    # 近28天 页面维度，看 /zh-cn/ 页面表现
    pg = q(token, ["page"], 300, d28, today)
    prows = pg.get("rows", [])
    zh = [r for r in prows if "/zh-cn/" in r["keys"][0]]
    en = [r for r in prows if "/en/" in r["keys"][0] or r["keys"][0].rstrip("/").endswith(".com")]
    zh.sort(key=lambda x: -x.get("impressions", 0))
    en.sort(key=lambda x: -x.get("impressions", 0))
    print(f"\n=== /zh-cn/ 页面 TOP20（中文站流量）===")
    for r in zh[:20]:
        print(f"  {r.get('impressions',0):>4}imp {r.get('clicks',0):>2}clk pos{r.get('position',0):>4.1f}  {r['keys'][0]}")
    print(f"\n=== /en/ 页面 TOP20 ===")
    for r in en[:20]:
        print(f"  {r.get('impressions',0):>4}imp {r.get('clicks',0):>2}clk pos{r.get('position',0):>4.1f}  {r['keys'][0]}")

    print(f"\n中文站页面数(有数据): {len(zh)} | 英文站页面数(有数据): {len(en)}")

if __name__ == "__main__":
    main()
