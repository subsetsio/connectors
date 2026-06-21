import re, json, sys, time
from concurrent.futures import ThreadPoolExecutor
import httpx
from subsets_utils import get

union = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/elstat/work/entity_union.json"))
codes = union if isinstance(union, list) else list(union)

PUB = "https://www.statistics.gr/en/statistics/-/publication/{code}/-"
LINK_RE = re.compile(r'(https?://www\.statistics\.gr[^"]*?documents_WAR_publicationsportlet_INSTANCE_[A-Za-z0-9]+[^"]*?documentID=\d+[^"]*?)"')
DID_RE = re.compile(r'documentID=(\d+)')

client = httpx.Client(follow_redirects=True, timeout=40)

def page(code):
    for attempt in range(4):
        try:
            return get(PUB.format(code=code), timeout=(10,60)).text
        except Exception:
            time.sleep(1.5*(attempt+1))
    return ""

def classify(url):
    url = url.replace("&amp;","&")
    try:
        r = client.head(url)
        cd = r.headers.get("content-disposition",""); ct = r.headers.get("content-type","")
    except Exception:
        return None
    fn = re.search(r'filename="?([^";]+)', cd)
    fn = fn.group(1).strip() if fn else ""
    return ct.split(";")[0], fn

def scan(code):
    html = page(code)
    if not html: return code, None
    links, seen = [], set()
    for m in LINK_RE.finditer(html):
        u = m.group(1); did = DID_RE.search(u).group(1)
        if did in seen: continue
        seen.add(did); links.append(u)
    docs=[]
    for u in links:
        c = classify(u)
        if c: docs.append(c)
    return code, docs

res={}
with ThreadPoolExecutor(max_workers=4) as ex:
    for code, docs in ex.map(scan, codes):
        res[code]=docs

XL = ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet","application/vnd.ms-excel")
def excel_files(docs):
    return [(ct,fn) for ct,fn in docs if ct in XL]
def ts_files(docs):
    return [(ct,fn) for ct,fn in excel_files(docs) if "_TS_" in fn.upper()]

no_excel=[c for c,d in res.items() if d is not None and not excel_files(d)]
no_ts=[c for c,d in res.items() if d is not None and excel_files(d) and not ts_files(d)]
pageerr=[c for c,d in res.items() if d is None]
print("codes:",len(codes))
print("with Excel data file:", sum(1 for c,d in res.items() if d and excel_files(d)))
print("with _TS_ Excel:", sum(1 for c,d in res.items() if d and ts_files(d)))
print("NO Excel at all:", len(no_excel), no_excel)
print("Excel but NO _TS_:", len(no_ts), no_ts)
print("PAGE ERRORS:", len(pageerr), pageerr)
json.dump(res, open("dev/doc_map.json","w"), indent=0)
