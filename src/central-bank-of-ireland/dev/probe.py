import io, time, json
from subsets_utils import get
import pyarrow.csv as pacsv

BASE = "https://opendata.centralbank.ie"

def show(pid):
    for a in range(8):
        r = get(f"{BASE}/api/3/action/package_show?id={pid}&_={a}", timeout=(10,120))
        rec = json.loads(r.content.decode("utf-8","replace"))["result"]
        if rec.get("name") == pid:
            return rec
        time.sleep(0.4)
    raise RuntimeError("stale")

# Survey resource counts/formats for a few including multi-resource ones
for pid in ["money-and-banking-statistics","gross-national-debt","official-external-reserves",
            "ncid-private-motor-data","retail-interest-rates-mortgage-rates"]:
    rec = show(pid)
    res = rec.get("resources", [])
    print(f"\n=== {pid} | num_resources={len(res)} | freq={rec.get('frequency')}")
    for r in res:
        print(f"   fmt={r.get('format')!r} name={r.get('name')!r} url=...{r.get('url','')[-40:]}")
