import sys, time
sys.path.insert(0, ".")
import httpx, re
H={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

def cdx(url, **extra):
    p={"url":url,"output":"json","filter":"statuscode:200","fl":"timestamp,original,statuscode"}
    p.update(extra)
    r=httpx.get("https://web.archive.org/cdx/search/cdx",params=p,timeout=60,headers=H)
    r.raise_for_status()
    return r.json()

# broad prefix query: any archived files under the energy crisis dataset
for label, url in [
  ("policy_list prefix", "bruegel.org/sites/default/files/*/policy_list*"),
  ("divisia prefix", "bruegel.org/sites/default/files/*/Divisia*"),
  ("reer prefix", "bruegel.org/sites/default/files/*/REER*"),
]:
    t0=time.time()
    try:
        rows=cdx(url, matchType="prefix", collapse="urlkey", limit="20")
        print(f"{label}: {len(rows)-1 if rows else 0} rows  t={time.time()-t0:.1f}")
        for r in (rows[1:] if rows else [])[:5]:
            print("   ", r[0], r[1][:100])
    except Exception as e:
        print(f"{label}: FAIL {type(e).__name__} {str(e)[:100]}")
