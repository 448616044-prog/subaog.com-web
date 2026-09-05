#!/usr/bin/env python3
"""拉取 subaog.com 近期流量趋势 + 昨天点击来源（query×page×country），回答"微信添加从哪来"。"""
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
    d28 = today - timedelta(days=28)
    d7 = today - timedelta(days=7)
    yesterday = today - timedelta(days=1)

    out = {"pulled_at": today.isoformat(), "site": SITE}

    # 1) 每日趋势 (28天)
    tr = q(token, ["date"], 60, d28, today)
    out["daily"] = tr.get("rows", [])

    # 2) 近7天 query×page 明细
    qp = q(token, ["query", "page"], 1000, d7, today)
    out["query_page_7d"] = qp.get("rows", [])

    # 3) 近7天 国家
    ct = q(token, ["country"], 15, d7, today)
    out["country_7d"] = ct.get("rows", [])

    # 4) 昨天 query×page×country (点击来源归因)
    qpc = q(token, ["query", "page", "country"], 500, yesterday, yesterday)
    out["yesterday_qpc"] = qpc.get("rows", [])

    # 5) 昨天 query (单维度，看点击词)
    yq = q(token, ["query"], 200, yesterday, yesterday)
    out["yesterday_queries"] = yq.get("rows", [])

    with open("gsc-trend-recent.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    # ---- 打印摘要 ----
    daily = out["daily"]
    print("=== 每日趋势（近28天，点击/展现）===")
    for r in sorted(daily, key=lambda x: x["keys"][0]):
        print(f"  {r['keys'][0]}  点击{r.get('clicks',0):>3}  展现{r.get('impressions',0):>5}  均位{r.get('position',0):.1f}")

    print("\n=== 近7天 点击来源 TOP（query × page）===")
    qp_rows = sorted(qp.get("rows", []), key=lambda x: -x.get("clicks", 0))[:25]
    for r in qp_rows:
        q_, p_ = r["keys"]
        print(f"  {r.get('clicks',0):>2}clk {r.get('impressions',0):>4}imp pos{r.get('position',0):.1f}  「{q_}」 -> {p_}")

    print("\n=== 近7天 国家分布 ===")
    for r in sorted(ct.get("rows", []), key=lambda x: -x.get("clicks", 0)):
        print(f"  {r['keys'][0]:<20} 点击{r.get('clicks',0):>3} 展现{r.get('impressions',0):>5}")

    print("\n=== 昨天 点击词（query）TOP ===")
    yq_rows = sorted(yq.get("rows", []), key=lambda x: -x.get("clicks", 0))[:30]
    for r in yq_rows:
        print(f"  {r.get('clicks',0):>2}clk {r.get('impressions',0):>4}imp pos{r.get('position',0):.1f}  「{r['keys'][0]}」")

    print("\n=== 昨天 词×页×国家（含点击的）===")
    qpc_rows = [r for r in qpc.get("rows", []) if r.get("clicks", 0) > 0]
    qpc_rows.sort(key=lambda x: -x.get("clicks", 0))
    for r in qpc_rows[:30]:
        q_, p_, c_ = r["keys"]
        print(f"  {r.get('clicks',0)}clk  [{c_}] 「{q_}」 -> {p_}")

    print("\n✅ 完成 -> gsc-trend-recent.json")

if __name__ == "__main__":
    main()
