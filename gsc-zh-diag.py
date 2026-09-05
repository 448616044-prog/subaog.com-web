#!/usr/bin/env python3
"""诊断中文站：sitemap 提交/索引状态 + /zh-cn/ 近90天展现页面全貌。"""
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

def api_get(token, path):
    req = urllib.request.Request(f"{SC_API}{path}", method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        return json.loads(urlopen_with_proxy(req).read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode()}

def api_post(token, path, body):
    req = urllib.request.Request(f"{SC_API}{path}", data=json.dumps(body).encode(), method="POST")
    req.add_header("Content-Type","application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        return json.loads(urlopen_with_proxy(req).read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode()}

def main():
    token = get_token("https://www.googleapis.com/auth/webmasters.readonly")
    sq = urllib.parse.quote(SITE, safe='')

    # sitemap 状态
    sm = api_get(token, f"/sites/{sq}/sitemaps")
    print("=== sitemap 提交/索引状态 ===")
    for s in sm.get("sitemap", []):
        path = s.get("path","")
        last_sub = s.get("lastSubmitted","")
        status = s.get("isPending","?")
        print(f"  {path}  提交:{last_sub}  pending:{status}")
        contents = s.get("contents", [])
        for c in contents:
            print(f"    类型:{c.get('type')} 提交:{c.get('submitted')} 已索引:{c.get('indexed')}")

    # 近90天 /zh-cn/ page 全貌
    today = datetime.now().date()
    d90 = today - timedelta(days=90)
    body = {"startDate": d90.isoformat(), "endDate": today.isoformat(),
            "dimensions": ["page"], "rowLimit": 25000}
    pg = api_post(token, f"/sites/{sq}/searchAnalytics/query", body)
    prows = pg.get("rows", [])
    zh = [r for r in prows if "/zh-cn/" in r["keys"][0]]
    en = [r for r in prows if "/en/" in r["keys"][0]]
    print(f"\n=== 近90天 页面展现全貌 ===")
    print(f"  /zh-cn/ 有展现页面数: {len(zh)}")
    print(f"  /en/ 有展现页面数: {len(en)}")
    print(f"  中文站总展现: {sum(r.get('impressions',0) for r in zh)} | 点击: {sum(r.get('clicks',0) for r in zh)}")
    print(f"  英文站总展现: {sum(r.get('impressions',0) for r in en)} | 点击: {sum(r.get('clicks',0) for r in en)}")

    # 中文站有展现的页面明细（全部列出）
    zh.sort(key=lambda x: -x.get("impressions", 0))
    print(f"\n=== /zh-cn/ 有展现页面明细（{len(zh)} 页）===")
    for r in zh:
        print(f"  {r.get('impressions',0):>4}imp {r.get('clicks',0):>2}clk pos{r.get('position',0):>4.1f}  {r['keys'][0]}")

    # 中文站页面类型分布
    from collections import Counter
    types = Counter()
    for r in zh:
        p = r["keys"][0].replace("https://subaog.com/zh-cn/","")
        if p.startswith("city/"): types["city城市对"] += 1
        elif p.startswith("blog/"): types["blog博客"] += 1
        elif "/to-china/" in p: types["usa-to-china城市×品类"] += 1
        elif p.startswith("tools/"): types["tools工具"] += 1
        elif p == "" or p == "index.html": types["首页"] += 1
        else: types["其他"] += 1
    print(f"\n=== 中文站有展现页面类型分布 ===")
    for k, v in types.most_common():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
