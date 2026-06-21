import httpx, re, html
from urllib.parse import urljoin
H={"User-Agent":"Mozilla/5.0 AppleWebKit/537.36 Chrome/120 Safari/537.36"}
c=httpx.Client(timeout=60, follow_redirects=True, headers=H)
def links(t, base):
    return list(dict.fromkeys(urljoin(base, html.unescape(h)) for h in re.findall(r'href=["\']([^"\']+)["\']', t)
               if not h.endswith(('.css','.js','.png','.gif','.ico')) and not h.startswith('mailto')))
r=c.get("https://pxweb.nso.gov.vn/pxweb/en/")
ind=[l for l in links(r.text,str(r.url)) if '/Industry/?' in l][0]
r=c.get(ind); tl=[l for l in links(r.text,str(r.url)) if 'tablelist=true' in l][0]
r=c.get(tl); tab=[l for l in links(r.text,str(r.url)) if 'E07.09.px/' in l][0]
r=c.get(tab); t=r.text; url=str(r.url)

def hidden(name):
    m=re.search(r'<input[^>]*name=["\']'+re.escape(name)+r'["\'][^>]*value=["\']([^"\']*)["\']', t) or \
      re.search(r'<input[^>]*value=["\']([^"\']*)["\'][^>]*name=["\']'+re.escape(name)+r'["\']', t)
    return html.unescape(m.group(1)) if m else ""
form={}
for h_ in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION','__VIEWSTATEENCRYPTED','__EVENTARGUMENT']:
    form[h_]=hidden(h_)
# language hidden select default
# find all ValuesListBox selects and their option values
listboxes=re.findall(r'<select[^>]*name=["\'](ctl00\$[^"\']*ValuesListBox)["\'][^>]*>(.*?)</select>', t, re.S)
print("num variable listboxes:", len(listboxes))
for name, body in listboxes:
    vals=re.findall(r'<option[^>]*value=["\']([^"\']*)["\']', body)
    form[name]=vals  # all values
    print("  ", name.split('$')[-3], "nvals", len(vals), vals[:3])
# output format dropdown name
ofname=re.search(r'<select[^>]*name=["\'](ctl00\$[^"\']*OutputFormatDropDownList)["\']', t).group(1)
print("OF name:", ofname)
form[ofname]="FileTypeJsonStat"
form['__EVENTTARGET']=ofname
# language combo
lang=re.search(r'<select[^>]*name=["\'](ctl00\$cboSelectLanguages)["\']', t)
if lang: form[lang.group(1)]="en"
# POST
post=c.post(url, data=form)
ct=post.headers.get("content-type","")
cd=post.headers.get("content-disposition","")
print("\nPOST status:", post.status_code, "ct:", ct[:40], "cd:", cd[:60], "len:", len(post.content))
head=post.text[:200]
print("body head:", head)
