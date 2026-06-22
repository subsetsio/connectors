import urllib.parse, httpx
target="https://www.bruegel.org/sites/default/files/2026-06/policy_list_20260616.xlsx"
H={"User-Agent":"Mozilla/5.0"}
tests = {
  "allorigins_raw": "https://api.allorigins.win/raw?url="+urllib.parse.quote(target,safe=""),
  "corsproxy": "https://corsproxy.io/?url="+urllib.parse.quote(target,safe=""),
  "codetabs": "https://api.codetabs.com/v1/proxy/?quest="+target,
  "thingproxy": "https://thingproxy.freeboard.io/fetch/"+target,
}
for name,u in tests.items():
    try:
        r=httpx.get(u,headers=H,timeout=60,follow_redirects=True)
        ct=r.headers.get("content-type","")
        sig=r.content[:4]
        ok = sig[:2]==b"PK"  # xlsx/zip magic
        print(f"{name:16} {r.status_code} len={len(r.content):>9} ct={ct[:30]:30} PKzip={ok}")
    except Exception as e:
        print(f"{name:16} FAIL {type(e).__name__}: {str(e)[:80]}")
