import httpx
URL = "https://clinicaltrials.gov/api/v2/studies"
P = {"pageSize": 1, "fields": "NCTId"}
with httpx.Client(http2=True, timeout=30, follow_redirects=True) as c:
    r = c.get(URL, params=P)
    print("httpx http2 ->", r.status_code, "| http_version:", r.http_version)
    if r.status_code == 200:
        print("OK keys:", list(r.json().keys()))
