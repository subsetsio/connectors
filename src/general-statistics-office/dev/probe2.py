import httpx, re
c=httpx.Client(timeout=40, follow_redirects=True, headers={"User-Agent":"Mozilla/5.0 Chrome/120"})
js=c.get("https://pxweb.nso.gov.vn/Resources/Scripts/pcaxis.web.controls.js").text
print("controls.js len", len(js))
i=js.lower().find('table.aspx')
print("context around Table.aspx:")
while i!=-1:
    print("  ...", js[max(0,i-120):i+60].replace('\n',' '))
    i=js.lower().find('table.aspx', i+1)
    if i>20000: break
# look for ajax/get/post/load calls
for pat in [r'\.load\([^)]*\)', r'\.get\([^)]*\)', r'\.post\([^)]*\)', r'\.ajax\(\{[^}]*\}', r'url\s*:\s*[^,\n]+']:
    h=re.findall(pat, js)
    if h: print(f"\n[{pat[:15]}]:", [x[:80] for x in h[:6]])
