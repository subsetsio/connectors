import ssl, httpx
URL = "https://clinicaltrials.gov/api/v2/studies"
P = {"pageSize": 1, "fields": "NCTId"}

# 1. httpx with stdlib default SSL context (what urllib3 uses)
ctx = ssl.create_default_context()
try:
    with httpx.Client(verify=ctx, http2=False, timeout=30, follow_redirects=True) as c:
        r = c.get(URL, params=P)
        print("httpx + stdlib ctx        ->", r.status_code)
except Exception as e:
    print("httpx + stdlib ctx EXC", e)

# 2. httpx default
try:
    with httpx.Client(http2=False, timeout=30, follow_redirects=True) as c:
        r = c.get(URL, params=P)
        print("httpx default ctx         ->", r.status_code)
except Exception as e:
    print("httpx default EXC", e)

# 3. httpx with stdlib ctx + set a permissive cipher string like urllib3
ctx2 = ssl.create_default_context()
try:
    ctx2.set_ciphers("DEFAULT")
    with httpx.Client(verify=ctx2, http2=False, timeout=30, follow_redirects=True) as c:
        r = c.get(URL, params=P)
        print("httpx + stdlib ctx DEFAULT ->", r.status_code)
except Exception as e:
    print("httpx + ciphers EXC", e)
