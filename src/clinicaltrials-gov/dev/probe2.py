import httpx, requests

URL = "https://clinicaltrials.gov/api/v2/studies"
P = {"pageSize": 1, "fields": "NCTId"}

# 1. requests
try:
    r = requests.get(URL, params=P, timeout=30)
    print("requests           ->", r.status_code)
except Exception as e:
    print("requests EXC", e)

# 2. httpx http1.1
try:
    with httpx.Client(http2=False, timeout=30, follow_redirects=True) as c:
        r = c.get(URL, params=P)
        print("httpx http1.1      ->", r.status_code)
except Exception as e:
    print("httpx http1.1 EXC", e)

# 3. httpx http2
try:
    with httpx.Client(http2=True, timeout=30, follow_redirects=True) as c:
        r = c.get(URL, params=P)
        print("httpx http2        ->", r.status_code)
except Exception as e:
    print("httpx http2 EXC", e)

# 4. httpx http1.1 with explicit browser-ish headers
try:
    h = {"User-Agent": "Mozilla/5.0", "Accept": "*/*", "Accept-Encoding": "gzip, deflate"}
    with httpx.Client(http2=False, timeout=30, follow_redirects=True, headers=h) as c:
        r = c.get(URL, params=P)
        print("httpx h1 minimal hdrs ->", r.status_code)
except Exception as e:
    print("httpx h1 minimal EXC", e)
