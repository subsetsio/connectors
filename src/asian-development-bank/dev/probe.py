from subsets_utils import get
import io, csv, collections

base = "https://kidb.adb.org/api/v4/sdmx/data/ADB,"
def pull(flow, key):
    url = f"{base}{flow}/{key}?format=sdmx-csv"
    r = get(url, timeout=(10,180))
    return r.status_code, r.text

for flow in ["PPL_POP", "MFP_PR", "GLB_ET"]:
    for key in ["..", "A..", "all"]:
        try:
            sc, txt = pull(flow, key)
            freqs = collections.Counter()
            rdr = csv.DictReader(io.StringIO(txt))
            cols = rdr.fieldnames
            for row in rdr:
                freqs[row.get("FREQ")] += 1
            n = sum(freqs.values())
            print(f"{flow:10s} key={key:5s} status={sc} rows={n:6d} freqs={dict(freqs)}")
        except Exception as e:
            print(f"{flow:10s} key={key:5s} ERROR {type(e).__name__}: {e}")
    print()

sc, txt = pull("PPL_POP", "A..")
rdr = csv.DictReader(io.StringIO(txt))
print("COLUMNS:", rdr.fieldnames)
for i,row in enumerate(rdr):
    if i<2: print(row)
    else: break
