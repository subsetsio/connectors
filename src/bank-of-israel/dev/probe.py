import io, csv
from subsets_utils import get

BASE = "https://edge.boi.org.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS"

def probe(flow, version="1.0"):
    url = f"{BASE}/{flow}/{version}?format=csv"
    r = get(url, timeout=(10.0, 180.0))
    print(f"\n===== {flow} status={r.status_code} bytes={len(r.content)} ct={r.headers.get('content-type')}")
    if r.status_code != 200:
        print(r.text[:500]); return
    text = r.text
    rdr = csv.reader(io.StringIO(text))
    header = next(rdr, None)
    print("HEADER:", header)
    rows = list(rdr)
    print("nrows:", len(rows))
    for row in rows[:3]:
        print("ROW:", row)

# small flow
probe("BR")
# exchange rates
probe("EXR")
