import httpx, re, html
from urllib.parse import urljoin
H={"User-Agent":"Mozilla/5.0 AppleWebKit/537.36 Chrome/120 Safari/537.36"}
c=httpx.Client(timeout=60, follow_redirects=False, headers=H)
def cL(t, base):
    return list(dict.fromkeys(urljoin(base, html.unescape(h)) for h in re.findall(r'href=["\']([^"\']+)["\']', t)
               if not h.endswith(('.css','.js','.png','.gif','.ico')) and not h.startswith('mailto')))
def allfields(t):
    d={}
    for name,val in re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*name=["\']([^"\']+)["\'][^>]*value=["\']([^"\']*)["\']', t): d[name]=html.unescape(val)
    for val,name in re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*value=["\']([^"\']*)["\'][^>]*name=["\']([^"\']+)["\']', t): d.setdefault(name, html.unescape(val))
    return d
def err(t): return 'ErrorGeneral' in t or 'An error has occurred' in t
def follow(resp):
    while resp.status_code in (301,302,303,307):
        resp=c.get(urljoin(str(resp.url), resp.headers['location']))
    return resp
r=follow(c.get("https://pxweb.nso.gov.vn/pxweb/en/"))
ind=[l for l in cL(r.text,str(r.url)) if '/Industry/?' in l][0]; r=follow(c.get(ind))
tl=[l for l in cL(r.text,str(r.url)) if 'tablelist=true' in l][0]; r=follow(c.get(tl))
tab=[l for l in cL(r.text,str(r.url)) if 'E07.09.px/' in l][0]; r=follow(c.get(tab))
t=r.text; url=str(r.url)
for sa in re.findall(r'name=["\'](ctl00\$[^"\']*ShowAllValuesButton)["\']', t):
    f=allfields(t); f['__EVENTTARGET']=''; f[sa]='ShowAll'; r=follow(c.post(url,data=f)); t=r.text; url=str(r.url)
btn=re.search(r'name=["\'](ctl00\$[^"\']*ButtonViewTable)["\']', t).group(1)
f=allfields(t); f['__EVENTTARGET']=''; f[btn]='Continue'; r=follow(c.post(url,data=f)); t=r.text; url=str(r.url)
print("table view url:", url[:80], "len", len(t))
# now try export WITHOUT following redirects to see Location/CD
of=re.search(r'name=["\'](ctl00\$[^"\']*OutputFormatDropDownList)["\']', t).group(1)
f=allfields(t); f['__EVENTTARGET']=of; f[of]='FileTypeJsonStat'
ex=c.post(url, data=f)  # no follow
print("EXPORT raw:", ex.status_code, "ct", ex.headers.get('content-type','')[:30], "loc", ex.headers.get('location','')[:80], "cd", ex.headers.get('content-disposition','')[:40])
# inspect data table in the view 't'
print("\nview td count:", t.count('<td'), "| numbers like 100.x present:", bool(re.search(r'>\s*\d+[.,]\d+\s*<', t)))
# dump a data-ish slice
m=re.search(r'(<table[^>]*PxWebTable.*?</table>)', t, re.S) or re.search(r'(<table[^>]*class="[^"]*table[^"]*".*?</table>)', t, re.S)
print("found data table:", bool(m), (len(m.group(1)) if m else 0))

print("\n=== hunt data-fetch endpoint in table view ===")
for pat in [r'PxWebQueryData[^"\' ]*', r'GetTable[^"\' ]*', r'asmx[^"\' ]*', r'ashx[^"\' ]*', r'WebService[^"\' ]*',
            r'PageMethod', r'ScriptManager', r'\.aspx/\w+', r'url\s*[:=]\s*["\'][^"\']+["\']',
            r'data-url=["\'][^"\']+', r'PxWeb\w*\.(?:aspx|ashx|asmx)', r'tableData|TableData|jsonData|chartData']:
    h=re.findall(pat, t, re.I)
    if h: print(f"  [{pat[:25]}]:", list(dict.fromkeys(h))[:5])
scripts=re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', t)
print("scripts:", [s for s in scripts if 'jquery' not in s.lower()][:12])
# embedded inline script urls
inline=re.findall(r'["\'](/pxweb/[^"\']*\.(?:aspx|ashx|asmx)[^"\']*)["\']', t)
print("inline pxweb endpoints:", list(dict.fromkeys(inline))[:8])
