#!/usr/bin/env python3
"""subaog.com — Sprint 新增/优化页 Indexing API 批量提交（聚焦高价值页，省配额）"""
import json
import time
import base64
import ssl
import urllib.request
import urllib.parse
import urllib.error

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

PROXY = "http://127.0.0.1:17891"
CRED = json.loads(open("/Users/mac/WorkBuddy/Claw/SEO/subao-seo-service-account.json").read())
TOKEN_URI = "https://oauth2.googleapis.com/token"
INDEXING_API = "https://indexing.googleapis.com/v3/urlNotifications:publish"

base = "https://subaog.com"
URLS = []

# 1) 6 个新对比落地页（USPS-vs-UPS / FedEx-vs-UPS / DHL-vs-USPS × zh/en）
for slug in ["usps-vs-ups-china", "fedex-vs-ups-china", "dhl-vs-usps-china"]:
    URLS += [f"{base}/zh-cn/blog/{slug}", f"{base}/en/blog/{slug}"]

# 2) 4 个新聚合页（can-i-ship-index / routes × zh/en）
URLS += [f"{base}/zh-cn/can-i-ship-index/", f"{base}/en/can-i-ship-index/",
         f"{base}/zh-cn/routes/", f"{base}/en/routes/"]

# 3) 4 个中词推首页优化页（已补 FAQ + 内链）
URLS += [f"{base}/en/blog/dhl-vs-fedex-vs-ups-china",
         f"{base}/en/city/san-diego-to-hangzhou",
         f"{base}/zh-cn/city/miami-to-shanghai",
         f"{base}/zh-cn/seasia-to-china/singapore/"]

# 4) 20 个 city hub（本次注入品类导航，需重爬）— 取部分高分城市避免超配额
top_cities = ["los-angeles", "new-york", "san-francisco", "chicago", "houston",
              "boston", "seattle", "dallas", "miami", "san-diego",
              "atlanta", "austin", "washington-dc", "philadelphia", "phoenix"]
for c in top_cities:
    URLS += [f"{base}/zh-cn/usa-to-china/{c}/", f"{base}/en/usa-to-china/{c}/"]


def urlopen_with_proxy(req, timeout=30):
    ctx = ssl.create_default_context()
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}),
        urllib.request.HTTPSHandler(context=ctx))
    return opener.open(req, timeout=timeout)


def create_jwt(scope):
    header = {"alg": "RS256", "typ": "JWT"}
    now = int(time.time())
    claim = {"iss": CRED["client_email"], "scope": scope, "aud": TOKEN_URI, "exp": now + 3600, "iat": now}
    def b64url(d):
        return base64.urlsafe_b64encode(d).rstrip(b"=").decode()
    h = b64url(json.dumps(header).encode()); c = b64url(json.dumps(claim).encode())
    key = serialization.load_pem_private_key(CRED["private_key"].encode(), password=None)
    sig = key.sign(f"{h}.{c}".encode(), padding.PKCS1v15(), hashes.SHA256())
    return f"{h}.{c}.{b64url(sig)}"


def get_token(scope):
    jwt = create_jwt(scope)
    data = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}).encode()
    req = urllib.request.Request(TOKEN_URI, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    return json.loads(urlopen_with_proxy(req).read())["access_token"]


def submit(token, url):
    body = json.dumps({"url": url, "type": "URL_UPDATED"}).encode()
    req = urllib.request.Request(INDEXING_API, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        return urlopen_with_proxy(req).status, "ok"
    except urllib.error.HTTPError as e:
        return e.code, (e.read().decode() if e.fp else str(e))[:100]


def main():
    print(f"subaog.com Indexing API — 提交 {len(URLS)} 个 Sprint 新页/优化页")
    token = get_token("https://www.googleapis.com/auth/indexing")
    ok = err = 0
    for i, url in enumerate(URLS, 1):
        status, msg = submit(token, url)
        if status == 200:
            ok += 1
            print(f"  ✅ [{i:03d}/{len(URLS)}] {url.replace(base, '')}")
        else:
            err += 1
            print(f"  ❌ [{i:03d}/{len(URLS)}] {url.replace(base, '')} → {status} {msg}")
            if status in (429, 403):
                print("  ⚠️ 配额/权限中断，停止")
                break
        time.sleep(0.3)
    print(f"\n结果: ✅ {ok} 成功 | ❌ {err} 失败")


if __name__ == "__main__":
    main()
