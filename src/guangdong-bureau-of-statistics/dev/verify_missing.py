import json
from subsets_utils import get, transient_retry
cat=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/guangdong-bureau-of-statistics/assets/collect/entities/current.json"))
base="http://tjnj.gdstats.gov.cn:8080/tjnj/2025/directory"
OLE2=b'\xd0\xcf'
@transient_retry(attempts=4)
def fetch(url):
    r=get(url,timeout=(10,90)); return r
for eid in ['01-08','11-02','11-03','11-13','01-02','01-03','22-04']:
    parts=cat[eid]["source_metadata"]["parts"]
    for p in parts:
        url=f"{base}/{p[:2]}/excel/{p}.xls"
        try:
            r=fetch(url)
            print(f"{eid:8} {p:10} {r.status_code} bytes={len(r.content)} ole2={r.content[:2]==OLE2}")
        except Exception as e:
            print(f"{eid:8} {p:10} EXC {type(e).__name__}")
