import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils as su
from utils import install_ca, excel_to_long
install_ca()
from constants import ENTITY_FILES
for eid, meta in ENTITY_FILES.items():
    url = meta["urls"][0]
    fn = url.rsplit("/",1)[-1]
    out = excel_to_long(su.get(url,timeout=(10,120)).content, fn)
    regions = [r["region"] for r in out]
    distinct = sorted(set(regions))
    print(eid, "rows", len(out), "distinct_regions", len(distinct), "->", distinct[:6])
