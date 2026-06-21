import httpx, re, html
from urllib.parse import urljoin
H={"User-Agent":"Mozilla/5.0 Chrome/120"}
c=httpx.Client(timeout=60, follow_redirects=True, headers=H)
def cL(t, base):
    return list(dict.fromkeys(urljoin(base, html.unescape(h)) for h in re.findall(r'href=["\']([^"\']+)["\']', t)
               if not h.endswith(('.css','.js','.png','.gif','.ico')) and not h.startswith('mailto')))
def allfields(t):
    d={}
    for n,v in re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*name=["\']([^"\']+)["\'][^>]*value=["\']([^"\']*)["\']', t): d[n]=html.unescape(v)
    for v,n in re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*value=["\']([^"\']*)["\'][^>]*name=["\']([^"\']+)["\']', t): d.setdefault(n, html.unescape(v))
    return d
r=c.get("https://pxweb.nso.gov.vn/pxweb/en/")
ind=[l for l in cL(r.text,str(r.url)) if '/Industry/?' in l][0]; r=c.get(ind)
tl=[l for l in cL(r.text,str(r.url)) if 'tablelist=true' in l][0]; r=c.get(tl)
tab=[l for l in cL(r.text,str(r.url)) if 'E07.09.px/' in l][0]; r=c.get(tab); t=r.text; url=str(r.url)
for sa in re.findall(r'name=["\'](ctl00\$[^"\']*ShowAllValuesButton)["\']', t):
    f=allfields(t); f['__EVENTTARGET']=''; f[sa]='ShowAll'; r=c.post(url,data=f); t=r.text; url=str(r.url)
btn=re.search(r'name=["\'](ctl00\$[^"\']*ButtonViewTable)["\']', t).group(1)
f=allfields(t); f['__EVENTTARGET']=''; f[btn]='Continue'; r=c.post(url,data=f); t=r.text; url=str(r.url)
print("warmed view:", url[:70])
# The div that loads Table.aspx — find its Url and any query the JS appends
mdiv=re.search(r'Url=["\']([^"\']*Table\.aspx[^"\']*)["\']', t)
print("div Url attr:", mdiv.group(1) if mdiv else None)
# find PxWeb 'px_tableid'/ query hints near Table
ctx=t[t.find('Table.aspx')-200:t.find('Table.aspx')+200] if 'Table.aspx' in t else ''
print("ctx:", ctx.replace('\n',' ')[:300])
# GET Table.aspx following redirects, dump final
ta=urljoin(url if url.endswith('/') else url.split('?')[0]+'/', "Table.aspx")
rr=c.get(ta)
print("\nTable.aspx final:", rr.status_code, str(rr.url)[:70], "len", len(rr.text), "td", rr.text.count('<td'), "nums", bool(re.search(r'>\s*-?\d+[.,]\d+\s*<', rr.text)))
# POST to Table.aspx (jQuery .load can POST if data given; PxWeb uses GET though)
