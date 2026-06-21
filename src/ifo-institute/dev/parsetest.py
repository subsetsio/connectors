import os, sys, time, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import configure_http
import nodes.ifo_institute as m

m.configure_http(headers=m._HTTP_HEADERS)

# ---- standard files ----
for entity, token in m._TOKENS.items():
    url = m._resolve_one(token)
    time.sleep(3)
    content = m._fetch_bytes(url, kind="xlsx")
    recs = m._parse_standard(content)
    series = collections.Counter(r[1] for r in recs)
    dmin = min(r[0] for r in recs); dmax = max(r[0] for r in recs)
    print(f"\n## {entity}  ({url.rsplit('/',1)[-1]})  rows={len(recs)}  span={dmin}..{dmax}  nseries={len(series)}")
    for s, n in list(series.items())[:8]:
        print(f"     [{n:4d}] {s}")
    time.sleep(3)

# ---- vintage (just 2 sectors to keep it quick) ----
hrefs = sorted({h for h in m._discover_hrefs() if "-ifo-vintage.xlsx" in h})
print(f"\n## vintage files discovered: {len(hrefs)}")
for href in hrefs[:2]:
    url = m.BASE + href
    fname = href.rsplit("/",1)[-1]
    sector = fname.replace("-ifo-vintage.xlsx","").replace("_"," ").strip()
    time.sleep(3)
    content = m._fetch_bytes(url, kind="xlsx")
    recs = m._parse_vintage(content, sector)
    inds = collections.Counter(r[2] for r in recs)
    vints = set(r[3] for r in recs)
    dmin = min(r[0] for r in recs); dmax = max(r[0] for r in recs)
    print(f"   sector={sector!r} rows={len(recs)} span={dmin}..{dmax} indicators={dict(inds)} nvintages={len(vints)}")
    print(f"     sample: {recs[0]}  ...  {recs[-1]}")
