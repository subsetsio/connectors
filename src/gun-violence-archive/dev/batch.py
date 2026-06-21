import io, re, time
import pandas as pd
from subsets_utils import get, get_client, configure_http

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
configure_http(headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
BASE = "https://www.gunviolencearchive.org"

slug = "accidental-teen-deaths"
html = get(f"{BASE}/{slug}", timeout=30).text
uuid = re.search(r"query/([a-f0-9-]{36})", html).group(1)
print("uuid", uuid)

# start batch (do not auto-follow redirects manually; client follows but we need the Location chain)
r = get(f"{BASE}/query/{uuid}/export-csv", timeout=60)
print("after export-csv: status", r.status_code, "url", str(r.url))
# r.url should be the batch page after following redirect
body = r.text
mid = re.search(r"id=(\d+)", str(r.url)) or re.search(r"id=(\d+)", body)
bid = mid.group(1) if mid else None
print("batch id", bid)

last_ids = None
for i in range(60):
    rr = get(f"{BASE}/batch", params={"id": bid, "op": "do_nojs"}, timeout=120)
    txt = rr.text
    pct = re.search(r"(\d+)%", txt)
    # detect CSV content
    ctype = rr.headers.get("content-type", "")
    if "csv" in ctype or txt[:50].count(",") > 3 and "<html" not in txt[:100].lower():
        print(f"iter {i}: CSV? ctype={ctype} head={txt[:120]!r}")
        break
    # finished redirect?
    fin = "op=finished" in txt
    print(f"iter {i}: status={rr.status_code} pct={pct.group(1) if pct else '?'} finished_link={fin} url={str(rr.url)[-40:]}")
    if fin:
        rf = get(f"{BASE}/batch", params={"id": bid, "op": "finished"}, timeout=120)
        print("finished ctype", rf.headers.get("content-type"), "len", len(rf.text))
        print("head:", rf.text[:200])
        break
    time.sleep(1)
