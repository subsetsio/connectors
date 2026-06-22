import io, time, json
from subsets_utils import get
import pyarrow.csv as pacsv

BASE = "https://opendata.centralbank.ie"
UNION = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/central-bank-of-ireland/work/entity_union.json"))

def show(pid):
    for a in range(10):
        r = get(f"{BASE}/api/3/action/package_show?id={pid}&_={a}", timeout=(10,120))
        rec = json.loads(r.content.decode("utf-8","replace"))["result"]
        if rec.get("name") == pid:
            return rec
        time.sleep(0.4)
    raise RuntimeError(f"stale {pid}")

for pid in UNION:
    rec = show(pid)
    res = rec.get("resources", [])
    csvs = [r for r in res if (r.get("format") or "").upper()=="CSV"]
    fmts = [ (r.get("format") or "?") for r in res ]
    print(f"{pid:60s} nres={len(res)} csvs={len(csvs)} fmts={fmts}")
