import sys, time, json
sys.path.insert(0, ".")
import httpx
H={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

def cdx(url):
    r=httpx.get("https://web.archive.org/cdx/search/cdx",params={"url":url,"output":"json","limit":"-5","filter":"statuscode:200","fl":"timestamp,original"},timeout=60,headers=H)
    r.raise_for_status()
    return r.json()

# Test: can wayback serve a bruegel FILE directly?
fileurl="https://www.bruegel.org/sites/default/files/2026-06/policy_list_20260616.xlsx"
t0=time.time()
try:
    rows=cdx(fileurl)
    print("FILE cdx rows:", len(rows), "t=%.1f"%(time.time()-t0))
    if len(rows)>1:
        ts=rows[-1][0]
        r=httpx.get(f"https://web.archive.org/web/{ts}id_/{fileurl}",timeout=120,headers=H,follow_redirects=True)
        print("FILE fetch:", r.status_code, len(r.content), "bytes")
except Exception as e:
    print("FILE FAIL", type(e).__name__, str(e)[:120])
