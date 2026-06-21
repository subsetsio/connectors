import httpx, re, html
from urllib.parse import urljoin
H={"User-Agent":"Mozilla/5.0 AppleWebKit/537.36 Chrome/120 Safari/537.36"}
c=httpx.Client(timeout=60, follow_redirects=True, headers=H)
def L(t, base):
    return list(dict.fromkeys(urljoin(base, html.unescape(h)) for h in re.findall(r'href=["\']([^"\']+)["\']', t)
               if not h.endswith(('.css','.js','.png','.gif','.ico')) and not h.startswith('mailto')))
def hid(t, name):
    m=re.search(r'name=["\']'+re.escape(name)+r'["\'][^>]*value=["\']([^"\']*)["\']', t) or \
      re.search(r'value=["\']([^"\']*)["\'][^>]*name=["\']'+re.escape(name)+r'["\']', t)
    return html.unescape(m.group(1)) if m else ""
def hiddens(t):
    d={}
    for n in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION','__VIEWSTATEENCRYPTED']:
        d[n]=hid(t,n)
    return d
def listboxes(t):
    out={}
    for name, body in re.findall(r'<select[^>]*name=["\'](ctl00\$[^"\']*ValuesListBox)["\'][^>]*>(.*?)</select>', t, re.S):
        out[name]=re.findall(r'<option[^>]*value=["\']([^"\']*)["\']', body)
    return out

r=c.get("https://pxweb.nso.gov.vn/pxweb/en/")
ind=[l for l in L(r.text,str(r.url)) if '/Industry/?' in l][0]
r=c.get(ind); tl=[l for l in L(r.text,str(r.url)) if 'tablelist=true' in l][0]
r=c.get(tl); tab=[l for l in L(r.text,str(r.url)) if 'E07.09.px/' in l][0]
r=c.get(tab); t=r.text; url=str(r.url)

# STEP 1: select all values + Continue
form=hiddens(t); form['__EVENTTARGET']=''; form['__EVENTARGUMENT']=''
for name,vals in listboxes(t).items(): form[name]=vals
btn=re.search(r'name=["\'](ctl00\$[^"\']*ButtonViewTable)["\']', t).group(1)
form[btn]='Continue'
r2=c.post(url, data=form); t2=r2.text
print("STEP1:", r2.status_code, "err=", 'ErrorGeneral' in t2 or 'error has occurred' in t2, "len", len(t2))
print("  table rendered? td count:", t2.count('<td'), "OF present:", 'OutputFormatDropDownList' in t2)

# STEP 2: pick JSON-stat output format
of=re.search(r'name=["\'](ctl00\$[^"\']*OutputFormatDropDownList)["\']', t2)
if of:
    of=of.group(1)
    form2=hiddens(t2); form2['__EVENTTARGET']=of; form2['__EVENTARGUMENT']=''
    form2[of]='FileTypeJsonStat'
    r3=c.post(str(r2.url), data=form2)
    print("STEP2:", r3.status_code, "ct:", r3.headers.get('content-type','')[:40], "cd:", r3.headers.get('content-disposition','')[:50], "len:", len(r3.content))
    body=r3.text[:300]
    print("  head:", body.replace(chr(10),' '))
