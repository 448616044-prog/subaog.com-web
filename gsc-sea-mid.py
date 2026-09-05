#!/usr/bin/env python3
"""精确定位：海运回国词落地页 + 英文站 11-30 名高展现词（临门一脚清单）。"""
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
    d90 = today - timedelta(days=90)
    d28 = today - timedelta(days=28)

    # 1) 海运回国词 落地页 (query×page, 90天)
    qp = q(token, ["query", "page"], 1000, d90, today)
    rows = qp.get("rows", [])
    sea = [r for r in rows if "海运" in r["keys"][0]]
    print("=== 海运回国词 → 落地页（90天）===")
    for r in sorted(sea, key=lambda x: -x.get("impressions", 0)):
        q_, p_ = r["keys"]
        print(f"  {r.get('impressions',0):>3}imp {r.get('clicks',0)}clk pos{r.get('position',0):>4.1f}  「{q_}」 -> {p_.replace('https://subaog.com','')}")

    # 2) 英文站 11-30 名高展现词（近28天）
    qq = q(token, ["query"], 500, d28, today)
    qrows = qq.get("rows", [])
    mid = [r for r in qrows if 11 <= r.get("position", 0) <= 30 and r.get("impressions", 0) >= 3]
    mid.sort(key=lambda x: -x.get("impressions", 0))
    print(f"\n=== 英文站 11-30 名高展现词（近28天，imp>=3，共{len(mid)}个）===")
    for r in mid:
        print(f"  {r.get('impressions',0):>3}imp {r.get('clicks',0)}clk pos{r.get('position',0):>4.1f}  「{r['keys'][0]}」")

    # 3) 中文词 11-30 名（近28天）
    cn_mid = [r for r in qrows if 11 <= r.get("position", 0) <= 30 and any('\u4e00' <= ch <= '\u9fff' for ch in r["keys"][0])]
    cn_mid.sort(key=lambda x: -x.get("impressions", 0))
    print(f"\n=== 中文词 11-30 名（近28天，共{len(cn_mid)}个）===")
    for r in cn_mid:
        print(f"  {r.get('impressions',0):>3}imp {r.get('clicks',0)}clk pos{r.get('position',0):>4.1f}  「{r['keys'][0]}」")

if __name__ == "__main__":
    main()
