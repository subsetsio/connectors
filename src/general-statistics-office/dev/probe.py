import httpx, re
H={"User-Agent":"Mozilla/5.0"}
with httpx.Client(timeout=40, follow_redirects=True, headers=H) as c:
    js = c.get("https://pxweb.nso.gov.vn/Resources/Scripts/pcaxis.web.client.js").text
    print("js len", len(js))
    # find url-ish strings and aspx endpoints, format/output keywords
    for pat in [r'"[^"]*\.aspx[^"]*"', r'"[^"]*[Dd]ata[^"]*"', r'outputformat\w*', r'"[^"]*[Ee]xport[^"]*"', r'url\s*:\s*[^,]+', r'"/[^"]+"']:
        hits = re.findall(pat, js)
        hits = list(dict.fromkeys(hits))[:12]
        if hits: print(f"\n[{pat}]:"); [print("  ", h[:100]) for h in hits]
