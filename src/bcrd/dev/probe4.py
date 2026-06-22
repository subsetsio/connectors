import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))
from constants import FILES_BY_SPEC
from subsets_utils import get
sid="bcrd-sector-monetario-y-financiero-tasas-diariasbac"
paths=FILES_BY_SPEC.get(sid,[])
print(sid,"->",len(paths),"files")
for p in paths[:3]:
    url="https://cdn.bancentral.gov.do/"+p
    r=get(url, timeout=(10,60))
    print(r.status_code, len(r.content), url)
