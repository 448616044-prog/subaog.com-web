#!/usr/bin/env python3
"""拉取澳洲/欧洲回国词群 GSC 数据，用代理鉴权（复用 gsc-trend-recent.py 逻辑）"""
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

def q(token, dims, rowLimit, start, end, **kw):
    body = {"startDate": start.isoformat(), "endDate": end.isoformat(), "dimensions": dims, "rowLimit": rowLimit}
    body.update(kw)
    return api_post(token, f"/sites/{urllib.parse.quote(SITE, safe='')}/searchAnalytics/query", body)

def main():
    token = get_token("https://www.googleapis.com/auth/webmasters.readonly")
    today = datetime.now().date()
    d90 = today - timedelta(days=90)

    # 拉取近 90 天 query 维度全量（找含 australia/uk/europe/london 等词的）
    all_q = q(token, ["query"], 5000, d90, today)
    rows = all_q.get("rows", [])

    # 地域关键词池
    au_seeds = ["australia", "melbourne", "sydney", "brisbane", "perth", "adelaide", "澳洲", "墨尔本", "悉尼", "布里斯班", "珀斯"]
    eu_seeds = ["europe", "uk", "london", "paris", "germany", "berlin", "france", "italy", "rome", "milan", "英国", "伦敦", "德国", "法国", "意大利", "欧洲", "巴黎", "柏林", "米兰"]

    au_rows = []
    eu_rows = []
    for r in rows:
        qq = r["keys"][0].lower()
        if any(s.lower() in qq for s in au_seeds):
            au_rows.append(r)
        if any(s.lower() in qq for s in eu_seeds):
            eu_rows.append(r)

    def show(label, data):
        print(f"\n{'='*70}\n{label}（近90天，按展现排序）\n{'='*70}")
        data.sort(key=lambda x: -x.get("impressions", 0))
        print(f"{'关键词':<42}{'点击':>5}{'展现':>7}{'CTR':>7}{'排名':>7}")
        for r in data[:40]:
            qq = r["keys"][0]
            print(f"{qq:<42}{r.get('clicks',0):>5}{r.get('impressions',0):>7}{r.get('ctr',0):>7.2%}{r.get('position',0):>7.1f}")

    show("澳洲词群", au_rows)
    show("欧洲词群", eu_rows)

    out = {
        "pulled_at": today.isoformat(),
        "au_rows": au_rows,
        "eu_rows": eu_rows,
    }
    with open("gsc-au-eu.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 完成 -> gsc-au-eu.json（澳洲 {len(au_rows)} 词，欧洲 {len(eu_rows)} 词）")

if __name__ == "__main__":
    main()