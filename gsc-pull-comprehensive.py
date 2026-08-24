#!/usr/bin/env python3
"""subaog.com 全面 GSC 拉取：sitemap + 关键词 + 页面 + 设备/国家 + 排名分段。
输出 JSON 到 gsc-latest.json，供 SEO 分析。"""
import json, time, base64, ssl, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timedelta

PROXY = "http://127.0.0.1:17891"
CRED = json.loads(open("/Users/mac/WorkBuddy/Claw/SEO/subao-seo-service-account.json").read())
TOKEN_URI = "https://oauth2.googleapis.com/token"
SC_API = "https://www.googleapis.com/webmasters/v3"
SITE = "sc-domain:subaog.com"

def urlopen_with_proxy(req, timeout=30):
    ctx = ssl.create_default_context()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}), urllib.request.HTTPSHandler(context=ctx))
    return opener.open(req, timeout=timeout)

def create_jwt(scope):
    header = {"alg": "RS256", "typ": "JWT"}
    now = int(time.time())
    claim = {"iss": CRED["client_email"], "scope": scope, "aud": TOKEN_URI, "exp": now+3600, "iat": now}
    b64 = lambda d: base64.urlsafe_b64encode(d).rstrip(b"=").decode()
    h, c = b64(json.dumps(header).encode()), b64(json.dumps(claim).encode())
    key = __import__("cryptography.hazmat.primitives.serialization", fromlist=["load_pem_private_key"]).load_pem_private_key(CRED["private_key"].encode(), password=None)
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes
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

def q(token, dims, rowLimit=100, start=None, end=None):
    if start is None:
        end = datetime.now().date(); start = end - timedelta(days=28)
    body = {"startDate": start.isoformat(), "endDate": end.isoformat(), "dimensions": dims, "rowLimit": rowLimit}
    return api_post(token, f"/sites/{urllib.parse.quote(SITE, safe='')}/searchAnalytics/query", body)

def main():
    token = get_token("https://www.googleapis.com/auth/webmasters.readonly")
    out = {"pulled_at": datetime.now().isoformat(), "site": SITE, "data": {}}

    # sitemap status
    sm = api_post(token, f"/sites/{urllib.parse.quote(SITE, safe='')}/sitemaps", {})
    out["sitemap"] = sm

    # queries top100 by impressions
    qry = q(token, ["query"], 100)
    out["data"]["queries"] = qry.get("rows", [])
    # pages top100 by impressions
    pg = q(token, ["page"], 100)
    out["data"]["pages"] = pg.get("rows", [])
    # device
    dv = q(token, ["device"], 10)
    out["data"]["devices"] = dv.get("rows", [])
    # country
    ct = q(token, ["country"], 15)
    out["data"]["countries"] = ct.get("rows", [])

    # aggregate summary
    qrows = qry.get("rows", [])
    prows = pg.get("rows", [])
    out["summary"] = {
        "queries_with_data": len(qrows),
        "pages_with_data": len(prows),
        "total_clicks_q": sum(r.get("clicks",0) for r in qrows),
        "total_impr_q": sum(r.get("impressions",0) for r in qrows),
        "total_clicks_p": sum(r.get("clicks",0) for r in prows),
        "total_impr_p": sum(r.get("impressions",0) for r in prows),
    }

    # position buckets for queries
    buckets = {"top3":0,"top10":0,"11_30":0,"31_100":0}
    for r in qrows:
        p = r.get("position", 0)
        if p <= 3: buckets["top3"] += 1
        elif p <= 10: buckets["top10"] += 1
        elif p <= 30: buckets["11_30"] += 1
        else: buckets["31_100"] += 1
    out["position_buckets"] = buckets

    with open("gsc-latest.json","w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("✅ 拉取完成 -> gsc-latest.json")
    print(f"   关键词有数据: {len(qrows)} | 页面有数据: {len(prows)}")
    s = out["summary"]
    print(f"   点击(词): {s['total_clicks_q']} | 展现(词): {s['total_impr_q']}")
    print(f"   排名分段: {buckets}")

if __name__ == "__main__":
    main()
