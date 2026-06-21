import httpx, re
H={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
c=httpx.Client(timeout=40, follow_redirects=True, headers=H)
m=c.get("https://pxweb.nso.gov.vn/pxweb/en/")
rxid=re.search(r'rxid=([0-9a-fA-F-]+)', m.text)
rxid=rxid.group(1) if rxid else None
print("session cookie:", dict(c.cookies), "rxid:", rxid)
# navigate to table in SAME session
for path in [
  f"https://pxweb.nso.gov.vn/pxweb/en/Industry/Industry__E07/E07.09.px/?rxid={rxid}",
  f"https://pxweb.nso.gov.vn/pxweb/en/Industry/Industry__E07/E07.09.px/table/tableViewLayout1/?rxid={rxid}",
]:
    r=c.get(path)
    err = "ErrorGeneral" in str(r.url)
    print(f"\nGET {path[38:80]} -> {r.status_code} err={err} len={len(r.text)}")
    if not err:
        # find download/export/save links & form actions
        links=re.findall(r'(?:href|action|onclick)=["\']([^"\']*(?:px/|format|Save|save|export|download|outputvalues|\.aspx)[^"\']*)["\']', r.text)
        for l in list(dict.fromkeys(links))[:25]: print("   L:", l[:130])
        print("   td count:", r.text.count('<td'), "has __VIEWSTATE:", '__VIEWSTATE' in r.text)
c.close()
