#!/usr/bin/env python3
"""拉 11 个临门一脚词的精确落地页。"""
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

def main():
    token = get_token("https://www.googleapis.com/auth/webmasters.readonly")
    today = datetime.now().date()
    d90 = today - timedelta(days=90)
    body = {"startDate": d90.isoformat(), "endDate": today.isoformat(),
            "dimensions": ["query", "page"], "rowLimit": 5000}
    r = api_post(token, f"/sites/{urllib.parse.quote(SITE, safe='')}/searchAnalytics/query", body)
    rows = r.get("rows", [])

    targets = ["dhl to china", "san diego to hangzhou", "china & glass", "sending wine",
               "does amazon", "ebay from china", "ebay china", "ebay sellers",
               "ups us to china", "shipping to xian"]
    print("=== 11 个临门一脚词 → 落地页（90天）===")
    seen = set()
    for r in rows:
        q_ = r["keys"][0]
        if any(t in q_.lower() for t in targets):
            p_ = r["keys"][1].replace("https://subaog.com", "")
            key = (q_, p_)
            if key in seen: continue
            seen.add(key)
            print(f"  {r.get('impressions',0):>3}imp {r.get('clicks',0)}clk pos{r.get('position',0):>4.1f}  「{q_}」 -> {p_}")

if __name__ == "__main__":
    main()
