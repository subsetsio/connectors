from subsets_utils import get
import csv, io

def probe(df):
    url = f"https://kidb.adb.org/api/v4/sdmx/data/ADB,{df}/A..?format=sdmx-csv"
    r = get(url, timeout=(10,120))
    r.raise_for_status()
    text = r.text
    rows = list(csv.DictReader(io.StringIO(text)))
    print(f"\n=== {df}: HTTP {r.status_code}, {len(rows)} rows, {len(text)} bytes")
    if rows:
        print("cols:", list(rows[0].keys()))
        s = rows[0]
        print("sample row:", {k: s[k] for k in s})
        # check OBS_VALUE numeric-ness & TIME range
        tp = sorted({x["TIME_PERIOD"] for x in rows})
        print("TIME_PERIOD range:", tp[0], "..", tp[-1])
        econ = sorted({x["ECONOMY_CODE"] for x in rows})
        print("n economies:", len(econ))
        nonnum = [x["OBS_VALUE"] for x in rows[:2000] if x["OBS_VALUE"] and _nonnum(x["OBS_VALUE"])]
        print("non-numeric OBS_VALUE sample (first 2000):", nonnum[:5])

def _nonnum(v):
    try: float(v); return False
    except: return True

for df in ["PPL_POP", "SDG_14", "MFP_XR"]:
    probe(df)
