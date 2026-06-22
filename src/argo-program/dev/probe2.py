from subsets_utils import get
import json

EBASE = "https://erddap.ifremer.fr/erddap"

def size(url, label, show=2):
    try:
        r = get(url, timeout=(10.0, 240.0))
        n = r.text.count("\n")
        print(f"{label}: HTTP {r.status_code}, {len(r.content)} bytes, ~{n} lines")
        for line in r.text.splitlines()[:show]:
            print("   ", line[:240])
    except Exception as e:
        print(f"{label}: ERROR {type(e).__name__}: {str(e)[:300]}")

# time actual_range per dataset (from info json attribute NC_GLOBAL/time)
for did in ["ArgoFloats", "ArgoFloats-synthetic-BGC", "ArgoFloats-reference", "ArgoFloats-index"]:
    try:
        r = get(f"{EBASE}/info/{did}/index.json", timeout=(10.0, 60.0))
        t = r.json()["table"]; cols = t["columnNames"]
        rt, vn, an, val = (cols.index("Row Type"), cols.index("Variable Name"),
                           cols.index("Attribute Name"), cols.index("Value"))
        rng = ts = None
        for row in t["rows"]:
            if row[vn] == "time" and row[an] == "actual_range":
                rng = row[val]
            if row[vn] == "time" and row[an] == "time_coverage_end":
                ts = row[val]
        # also global time_coverage
        tc_start = tc_end = None
        for row in t["rows"]:
            if row[an] == "time_coverage_start": tc_start = row[val]
            if row[an] == "time_coverage_end": tc_end = row[val]
        print(f"{did}: time actual_range={rng}  coverage={tc_start}..{tc_end}")
    except Exception as e:
        print(f"{did}: info ERROR {type(e).__name__}: {str(e)[:200]}")

# reference full size (lean cols)
size(f"{EBASE}/tabledap/ArgoFloats-reference.csv?platform_number,time,pres",
     "reference FULL (3 cols)")

# OACP-Argo-Global via griddap: list variables + dims first
try:
    r = get(f"{EBASE}/info/OACP-Argo-Global/index.json", timeout=(10.0, 60.0))
    t = r.json()["table"]; cols = t["columnNames"]
    rt, vn = cols.index("Row Type"), cols.index("Variable Name")
    dims = [row[vn] for row in t["rows"] if row[rt] == "dimension"]
    vars_ = [row[vn] for row in t["rows"] if row[rt] == "variable"]
    print("OACP-Argo-Global dims:", dims)
    print("OACP-Argo-Global vars:", vars_[:8], "...", len(vars_), "total")
except Exception as e:
    print("OACP info ERROR", e)

# griddap small slice for OACP-Argo-Global (all lat/lon, one var)
size(f"{EBASE}/griddap/OACP-Argo-Global.csv?GLOBAL_PPD",
     "OACP-Argo-Global griddap GLOBAL_PPD full", show=4)
