import csv, io
from subsets_utils import get
url = "https://kidb.adb.org/api/v4/sdmx/data/ADB,PPL_LE/A.."
r = get(url, params={"format":"sdmx-csv","startPeriod":"2020","endPeriod":"2021"}, timeout=(10,180))
print("status", r.status_code)
txt = r.text
rows = list(csv.DictReader(io.StringIO(txt)))
print("nrows", len(rows))
if rows:
    print("cols", list(rows[0].keys()))
    for rr in rows[:3]:
        print({k:rr[k] for k in rows[0].keys()})
    # distinct FREQ, sample TIME_PERIOD, DATAFLOW
    print("FREQ set", set(r.get("FREQ") for r in rows))
    print("TIME sample", sorted(set(r.get("TIME_PERIOD") for r in rows))[:10])
    print("DATAFLOW sample", list(set(r.get("DATAFLOW") for r in rows))[:3])
