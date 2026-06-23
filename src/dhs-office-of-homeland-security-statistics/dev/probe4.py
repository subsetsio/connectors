from subsets_utils import get
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
H={"User-Agent":UA,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"en-US,en;q=0.9"}
url="https://ohss.dhs.gov/topics/immigration/yearbook"

# 1: explicit AKA_A2 cookie
r=get(url, timeout=(10,60), headers={**H,"Cookie":"AKA_A2=A"})
print("cookie-AKA_A2=A:", r.status_code, len(r.content))

# 2: try the bigip/ greenhouse? just retry twice with same client? subsets get is stateless.
# Try httpx directly with http2 to compare fingerprint
import httpx
for h2 in (False, True):
    try:
        with httpx.Client(http2=h2, headers=H, follow_redirects=True, timeout=60) as c:
            rr=c.get(url)
            # retry with returned cookies
            rr2=c.get(url)
            print(f"httpx h2={h2}:", rr.status_code, "->retry", rr2.status_code, len(rr2.content))
    except Exception as e:
        print(f"httpx h2={h2}: ERR", type(e).__name__, str(e)[:60])
