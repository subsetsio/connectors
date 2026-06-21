import httpx, re, html
from urllib.parse import urljoin
H={"User-Agent":"Mozilla/5.0 AppleWebKit/537.36 Chrome/120 Safari/537.36"}
c=httpx.Client(timeout=60, follow_redirects=True, headers=H)
def L(t, base):
    return list(dict.fromkeys(urljoin(base, html.unescape(h)) for h in re.findall(r'href=["\']([^"\']+)["\']', t)
               if not h.endswith(('.css','.js','.png','.gif','.ico')) and not h.startswith('mailto')))
def allfields(t):
    """all input hidden + the current VIEWSTATE etc + selects with their current selected option"""
    d={}
    for name,val in re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*name=["\']([^"\']+)["\'][^>]*value=["\']([^"\']*)["\']', t):
        d[name]=html.unescape(val)
    # also inputs where value precedes name
    for val,name in re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*value=["\']([^"\']*)["\'][^>]*name=["\']([^"\']+)["\']', t):
        d.setdefault(name, html.unescape(val))
    return d
def err(t): return 'ErrorGeneral' in t or 'An error has occurred' in t

r=c.get("https://pxweb.nso.gov.vn/pxweb/en/")
ind=[l for l in L(r.text,str(r.url)) if '/Industry/?' in l][0]
r=c.get(ind); tl=[l for l in L(r.text,str(r.url)) if 'tablelist=true' in l][0]
r=c.get(tl); tab=[l for l in L(r.text,str(r.url)) if 'E07.09.px/' in l][0]
r=c.get(tab); t=r.text; url=str(r.url)

# ShowAll postback for each variable repeater (ctl01, ctl02)
showalls=re.findall(r'name=["\'](ctl00\$[^"\']*VariableValueSelect\$ShowAllValuesButton)["\']', t)
print("showall buttons:", len(showalls))
for sa in showalls:
    f=allfields(t); f['__EVENTTARGET']=''; f['__EVENTARGUMENT']=''; f[sa]='ShowAll'
    rr=c.post(url, data=f); t=rr.text; url=str(rr.url)
    print("  ShowAll", sa.split('$')[-3], "->", rr.status_code, "err=", err(t), "len", len(t))
    if err(t): break

if not err(t):
    btn=re.search(r'name=["\'](ctl00\$[^"\']*ButtonViewTable)["\']', t).group(1)
    f=allfields(t); f['__EVENTTARGET']=''; f['__EVENTARGUMENT']=''; f[btn]='Continue'
    rr=c.post(url, data=f); t=rr.text; url=str(rr.url)
    print("Continue ->", rr.status_code, "err=", err(t), "td count", t.count('<td'), "OF present", 'OutputFormatDropDownList' in t)
    if not err(t) and 'OutputFormatDropDownList' in t:
        of=re.search(r'name=["\'](ctl00\$[^"\']*OutputFormatDropDownList)["\']', t).group(1)
        f=allfields(t); f['__EVENTTARGET']=of; f['__EVENTARGUMENT']=''; f[of]='FileTypeJsonStat'
        rr=c.post(url, data=f)
        print("Export ->", rr.status_code, "ct:", rr.headers.get('content-type','')[:40], "len", len(rr.content))
        print("  head:", rr.text[:200].replace(chr(10),' '))

        et=rr.text
        print("\n=== search export response for download pointers ===")
        for pat in [r'FileDownload[^"\' ]*', r'window\.location[^;]*', r'location\.href[^;]*', r'<iframe[^>]*src=["\']([^"\']+)', r'meta[^>]*http-equiv=["\']refresh["\'][^>]*content=["\']([^"\']+)', r'href=["\']([^"\']*(?:Download|\.json|FileType|getfile|File)[^"\']*)', r'/pxweb/[^"\' ]*\.(?:json|px|csv)', r'__doPostBack\([^)]*Save[^)]*\)']:
            h=re.findall(pat, et, re.I)
            if h: print(f"  [{pat[:30]}]:", list(dict.fromkeys(h))[:5])
        # any new form action or buttons mentioning save/download
        print("  buttons w/ save/download:", re.findall(r'name=["\']([^"\']*(?:[Ss]ave|[Dd]ownload|[Ss]ubmit)[^"\']*)["\']', et)[:8])
