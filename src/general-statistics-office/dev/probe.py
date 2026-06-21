import httpx, re
with httpx.Client(timeout=40, follow_redirects=True, headers={"User-Agent":"Mozilla/5.0"}) as c:
    # establish session at menu
    r = c.get("https://pxweb.nso.gov.vn/pxweb/en/")
    print("menu:", r.status_code, "cookies:", dict(c.cookies))
    print("final url:", str(r.url))
    # find rxid
    m = re.search(r'rxid=([0-9a-fA-F-]+)', r.text)
    print("rxid in page:", m.group(1) if m else None)
    # look for api/script references
    scripts = re.findall(r'src="([^"]+\.js[^"]*)"', r.text)
    print("scripts:", scripts[:10])
    # try the table viewer with rxid to capture data endpoint hints
    refs = re.findall(r'(api/v1[^"\' ]*|/PXWeb/[^"\' ]*|saveQuery|GetTableData|TableData|\.px[^"\' ]{0,30})', r.text)
    print("refs:", list(dict.fromkeys(refs))[:20])
