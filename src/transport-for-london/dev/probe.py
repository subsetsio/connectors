import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, csv, json
from subsets_utils import get

def head_csv(url, n=2):
    r = get(url, timeout=(10,120))
    r.raise_for_status()
    text = r.content.decode("utf-8", "replace")
    rdr = csv.reader(io.StringIO(text))
    rows = []
    for i, row in enumerate(rdr):
        rows.append(row)
        if i >= n: break
    return rows, len(text)

# usage-stats: oldest-ish and a recent file (discover recent via listing separately)
for url in [
    "https://cycling.data.tfl.gov.uk/usage-stats/01aJourneyDataExtract10Jan16-23Jan16.csv",
]:
    try:
        rows, ln = head_csv(url)
        print("USAGE", url.split("/")[-1])
        print("  header:", rows[0])
        print("  row1:", rows[1] if len(rows)>1 else None)
    except Exception as e:
        print("USAGE ERR", e)

# AccidentStats JSON shape + out of range behavior
import subsets_utils
for yr in [2019, 2020, 2004]:
    try:
        r = get(f"https://api.tfl.gov.uk/AccidentStats/{yr}", timeout=(10,180))
        ct = r.headers.get("content-type")
        print(f"ACCIDENT {yr}: status={r.status_code} ct={ct} len={len(r.content)}")
        if r.status_code==200 and "json" in (ct or ""):
            data = r.json()
            print("  type:", type(data).__name__, "n=", len(data) if isinstance(data,list) else "-")
            if isinstance(data, list) and data:
                rec = data[0]
                print("  keys:", sorted(rec.keys()))
                print("  sample:", {k: rec[k] for k in list(rec)[:8]})
    except Exception as e:
        print(f"ACCIDENT {yr} ERR", type(e).__name__, e)
