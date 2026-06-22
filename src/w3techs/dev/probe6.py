import time
import httpx
from subsets_utils import get, configure_http

configure_http(headers={"User-Agent": "subsets.io-connector/1.0 (+https://subsets.io)"})

# Hit several /all/y pages back-to-back with NO delay to provoke the block,
# capturing the exact HTTP status of each failure.
slugs = ["programming_language", "web_server", "operating_system", "web_hosting",
         "data_center", "dns_server", "email_server", "markup_language"]

print("=== rapid, no delay ===")
for slug in slugs:
    url = f"https://w3techs.com/technologies/history_overview/{slug}/all/y"
    try:
        r = get(url, timeout=(30.0, 120.0))
        status = r.status_code
        ra = r.headers.get("Retry-After")
        print(f"{slug:22} {status}  Retry-After={ra}  len={len(r.text)}")
    except httpx.HTTPStatusError as e:
        print(f"{slug:22} HTTPStatusError {e.response.status_code}")
    except Exception as e:
        print(f"{slug:22} EXC {type(e).__name__}: {e}")

print("\n=== same slugs, 5s delay between ===")
for slug in slugs:
    url = f"https://w3techs.com/technologies/history_overview/{slug}/all/y"
    try:
        r = get(url, timeout=(30.0, 120.0))
        print(f"{slug:22} {r.status_code}  len={len(r.text)}")
    except Exception as e:
        print(f"{slug:22} EXC {type(e).__name__}: {getattr(getattr(e,'response',None),'status_code',None)}")
    time.sleep(5)
