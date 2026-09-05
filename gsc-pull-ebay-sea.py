#!/usr/bin/env python3
"""专项拉取：ebay 词群 + 海运/空运词群 + 对应 page（query x page 交叉）。"""
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

def q(token, dims, rowLimit=100, start=None, end=None):
    if start is None:
        end = datetime.now().date(); start = end - timedelta(days=28)
    body = {"startDate": start.isoformat(), "endDate": end.isoformat(),
            "dimensions": dims, "rowLimit": rowLimit}
    return api_post(token, f"/sites/{urllib.parse.quote(SITE, safe='')}/searchAnalytics/query", body)

def main():
    token = get_token("https://www.googleapis.com/auth/webmasters.readonly")
    out = {"pulled_at": datetime.now().isoformat(), "site": SITE}

    # 全量关键词 rowLimit 2000
    qr = q(token, ["query"], 2000)
    qrows = qr.get("rows", [])
    out["query_count"] = len(qrows)

    # 全量 query x page 交叉（找 ebay/海运词的落地页）
    qp = q(token, ["query", "page"], 2000)
    qprows = qp.get("rows", [])
    out["query_page_count"] = len(qprows)

    # ebay 词群
    ebay_kw = [r for r in qrows if "ebay" in r["keys"][0].lower()]
    # 海运/空运/货运词群
    sea_pat = ["sea freight", "ocean freight", "shipping by sea", "海运", "海运回国",
               "by ship", "freight forwarder", "sea shipping", "船运"]
    sea_kw = [r for r in qrows if any(p in r["keys"][0].lower() for p in sea_pat)]
    # 空运词群
    air_kw = [r for r in qrows if any(p in r["keys"][0].lower() for p in ["air freight", "by air", "空运", "air shipping"])]

    # ebay/海运词的落地页（从 query x page 交叉里找）
    def find_pages(kwlist):
        res = {}
        for r in qprows:
            qk = r["keys"][0].lower()
            if any(r2["keys"][0].lower() == qk for r2 in kwlist):
                pg = r["keys"][1]
                res.setdefault(qk, []).append({"page": pg, "clicks": r.get("clicks",0),
                                                "impressions": r.get("impressions",0),
                                                "position": round(r.get("position",0),1)})
        return res

    out["ebay_keywords"] = ebay_kw
    out["sea_keywords"] = sea_kw
    out["air_keywords"] = air_kw
    out["ebay_pages"] = find_pages(ebay_kw)
    out["sea_pages"] = find_pages(sea_kw)

    with open("gsc-ebay-sea.json","w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"✅ 拉取完成 -> gsc-ebay-sea.json | 全量词 {len(qrows)} | query×page {len(qprows)}")
    print(f"\n=== ebay 词群 ({len(ebay_kw)}) ===")
    for r in sorted(ebay_kw, key=lambda x:-x['impressions']):
        print(f"  {r['keys'][0]:45s} 点击{r.get('clicks',0)} 曝光{r.get('impressions',0)} pos{r.get('position',0):.1f}")
    print(f"\n=== 海运/货运词群 ({len(sea_kw)}) ===")
    for r in sorted(sea_kw, key=lambda x:-x['impressions']):
        print(f"  {r['keys'][0]:45s} 点击{r.get('clicks',0)} 曝光{r.get('impressions',0)} pos{r.get('position',0):.1f}")
    print(f"\n=== 空运词群 ({len(air_kw)}) ===")
    for r in sorted(air_kw, key=lambda x:-x['impressions']):
        print(f"  {r['keys'][0]:45s} 点击{r.get('clicks',0)} 曝光{r.get('impressions',0)} pos{r.get('position',0):.1f}")

if __name__ == "__main__":
    main()
