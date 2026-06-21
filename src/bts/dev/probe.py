import sys, os, io, zipfile, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get, post
import re, html as htmlmod
def page(code):
    return get(f"https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ={code}&QO_fu146_anzr=b0-gvzr",timeout=(10,60)).text
def hidden(html,n):
    m=re.search(r'name="'+n+r'"[^>]*value="([^"]*)"',html);return htmlmod.unescape(m.group(1)) if m else ""
def custom(code, yr, per=None):
    html=page(code)
    has_period = "cboPeriod" in html
    data={"__VIEWSTATE":hidden(html,"__VIEWSTATE"),"__VIEWSTATEGENERATOR":hidden(html,"__VIEWSTATEGENERATOR"),"__EVENTVALIDATION":hidden(html,"__EVENTVALIDATION"),"cboGeography":"All","cboYear":yr,"chkAllVars":"on","btnDownload":"Download"}
    if has_period and per: data["cboPeriod"]=per
    r=post(f"https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ={code}&QO_fu146_anzr=b0-gvzr",data=data,timeout=(10,180),follow_redirects=False)
    print(f"--- {code} y={yr} p={per} has_period={has_period} status={r.status_code} ct={r.headers.get('content-type')} len={len(r.content)}")
    if r.headers.get('content-type','').startswith('application/zip'):
        z=zipfile.ZipFile(io.BytesIO(r.content))
        members={n:z.getinfo(n).file_size for n in z.namelist()}
        print("   members:",members)
        datamem=[n for n in z.namelist() if n.lower() not in ("term.csv","documentation.csv")]
        if datamem:
            with z.open(datamem[0]) as f:
                rr=csv.reader(io.TextIOWrapper(f,encoding="utf-8",errors="replace"))
                h=next(rr); nrows=sum(1 for _ in rr)
                print(f"   DATA {datamem[0]} ncols={len(h)} datarows={nrows} head={h[:6]}")
custom("FJH","2024","1")   # monthly
custom("FIH","2024","1")   # quarterly
custom("FLF","2023")       # annual (nper=0)
custom("FMG","2024","1")   # T-100 segment monthly (big-ish)
