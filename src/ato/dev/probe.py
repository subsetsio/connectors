import re, json
from subsets_utils import get

BASE="https://data.gov.au/data"
ORG="australiantaxationoffice"

def fetch_catalog():
    out=[]; start=0
    while True:
        r=get(f"{BASE}/api/3/action/package_search",
              params={"fq":f"organization:{ORG}","rows":50,"start":start}, timeout=(10,120))
        r.raise_for_status()
        res=r.json()["result"]; batch=res["results"]; out.extend(batch); start+=len(batch)
        if not batch or start>=res["count"]: break
    return out

YEARLY=[(re.compile(r"^taxation-statistics-(\d{4}-\d{2})$"),"taxation-statistics"),
        (re.compile(r"^international-related-party-dealings-(\d{4}-\d{2})$"),"international-related-party-dealings")]
YEAR_TOKEN=re.compile(r"\b(19|20)\d{2}[-–]\d{2}\b|\bts\d{2}\b|\b(19|20)\d{2}\b",re.I)
def fam_year(n):
    for p,f in YEARLY:
        m=p.match(n)
        if m: return f,m.group(1)
    return n,None
def norm(name):
    s=(name or "").lower(); s=YEAR_TOKEN.sub(" ",s); s=re.sub(r"[^a-z0-9]+","-",s).strip("-"); return s or "unnamed"

pkgs=fetch_catalog()
print("packages",len(pkgs))
groups={}
for pkg in pkgs:
    fam,py=fam_year(pkg["name"])
    for res in pkg.get("resources",[]):
        fmt=(res.get("format") or "")
        if "pdf" in fmt.lower(): continue
        key=f"{fam}--{norm(res.get('name') or res.get('id'))}".lower().replace("_","-")
        groups.setdefault(key,[]).append((py,res["id"],fmt,bool(res.get("datastore_active")),res.get("name")))
print("groups",len(groups))

union=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/ato/work/entity_union.json"))
missing=[u for u in union if u not in groups]
print("union",len(union),"missing from reconstruction:",len(missing))
for m in missing[:10]: print("  MISSING",m)

# probe one entity's datastore
sample="taxation-statistics/financialratios4trusts1c-csv"
print("=== sample",sample,"===")
for py,rid,fmt,ds,nm in groups[sample]:
    print(py,rid,fmt,"datastore=",ds,"|",nm)
    rr=get(f"{BASE}/api/3/action/datastore_search",params={"resource_id":rid,"limit":3},timeout=(10,120))
    rr.raise_for_status(); d=rr.json()["result"]
    print("   total",d["total"],"fields",[f['id'] for f in d['fields']])
    print("   rec0",d['records'][0] if d['records'] else None)
