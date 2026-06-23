import httpx

URL = "https://clinicaltrials.gov/api/v2/studies"
P = {"pageSize": 1, "fields": "NCTId"}

# Hypothesis: Akamai flags httpx's lowercase header names / ordering.
# Try forcing capitalized names in requests-like order via an explicit Headers obj.
def trial(desc, headers):
    try:
        with httpx.Client(http2=False, timeout=30, follow_redirects=True) as c:
            # default_headers off: build request manually so ONLY our headers go
            req = c.build_request("GET", URL, params=P, headers=headers)
            # drop httpx auto-added lowercase dups by overriding
            r = c.send(req)
            print(f"{desc:40s} -> {r.status_code} | sent: {list(req.headers.items())}")
            return r.status_code
    except Exception as e:
        print(f"{desc:40s} EXC {e}")
        return None

# requests-like exact headers, capitalized
trial("cap requests-like", {
    "User-Agent": "python-requests/2.32.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "keep-alive",
})

# only override accept-encoding to drop br/zstd, keep httpx defaults otherwise
trial("drop-br-encoding", {"Accept-Encoding": "gzip, deflate"})
