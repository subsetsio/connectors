from subsets_utils import get
import time
# hammer to trigger the limit, report status + headers
last=None
for i in range(120):
    r = get("https://api.beta.ons.gov.uk/v1/datasets/TS009", timeout=(10,60))
    if r.status_code != 200 or not r.text.strip():
        print(f"req {i}: status={r.status_code} len={len(r.text)} retry-after={r.headers.get('Retry-After')} ratelimit={r.headers.get('RateLimit-Remaining') or r.headers.get('X-RateLimit-Remaining')}")
        print("  body head:", repr(r.text[:120]))
        last=r
        break
else:
    print("no failure in 120 reqs")
