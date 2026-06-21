import httpx
with httpx.Client(timeout=40, follow_redirects=False) as c:
    # establish session
    c.get("https://pxweb.nso.gov.vn/pxweb/en/", headers={"User-Agent":"Mozilla/5.0"})
    url="https://pxweb.nso.gov.vn/api/v1/en/Industry/E07.09.px"
    meta=httpx.get(url, timeout=30).json()
    q=[{"code":v["code"],"selection":{"filter":"all","values":["*"]}} for v in meta["variables"]]
    body={"query":q,"response":{"format":"json-stat2"}}
    hdrs={
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
      "Accept":"application/json, text/plain, */*",
      "Content-Type":"application/json",
      "Origin":"https://pxweb.nso.gov.vn",
      "Referer":"https://pxweb.nso.gov.vn/pxweb/en/Industry/Industry__E07/E07.09.px/",
      "X-Requested-With":"XMLHttpRequest",
    }
    r=c.post(url, json=body, headers=hdrs)
    print("browser-emulated POST:", r.status_code, r.headers.get("content-type","")[:25])
    if r.status_code==200 and "json" in r.headers.get("content-type",""):
        j=r.json(); print("  isdict:",isinstance(j,dict),"value?", isinstance(j,dict) and "value" in j, str(j)[:120])
    else:
        print("  body:", r.text[:90])
    # also try lowercase host api without /api: maybe /pxweb/api
    r2=c.post("https://pxweb.nso.gov.vn/pxweb/api/v1/en/Industry/E07.09.px", json=body, headers=hdrs)
    print("/pxweb/api POST:", r2.status_code)
