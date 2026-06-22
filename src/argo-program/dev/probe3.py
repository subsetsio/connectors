import sys
from subsets_utils import get
EBASE = "https://erddap.ifremer.fr/erddap"

def size(url, label, show=2):
    try:
        r = get(url, timeout=(10.0, 240.0))
        n = r.text.count("\n")
        print(f"{label}: HTTP {r.status_code}, {len(r.content)} bytes, ~{n} lines", flush=True)
        for line in r.text.splitlines()[:show]:
            print("   ", line[:240], flush=True)
    except Exception as e:
        print(f"{label}: ERROR {type(e).__name__}: {str(e)[:300]}", flush=True)

# time ranges
for did in ["ArgoFloats", "ArgoFloats-synthetic-BGC", "ArgoFloats-reference"]:
    try:
        r = get(f"{EBASE}/info/{did}/index.json", timeout=(10.0, 60.0)); t = r.json()["table"]; cols = t["columnNames"]
        an, val = cols.index("Attribute Name"), cols.index("Value")
        d = {row[an]: row[val] for row in t["rows"] if row[an] in ("time_coverage_start","time_coverage_end")}
        print(f"{did}: {d}", flush=True)
    except Exception as e:
        print(f"{did}: info ERROR {e}", flush=True)

# reference: one year, lean cols -> gauge annual volume
size(f"{EBASE}/tabledap/ArgoFloats-reference.csv?platform_number,time,pres&time%3E=2010-01-01T00:00:00Z&time%3C=2011-01-01T00:00:00Z",
     "reference year 2010 (3 cols)")

# OACP-Argo-Global griddap
try:
    r = get(f"{EBASE}/info/OACP-Argo-Global/index.json", timeout=(10.0, 60.0)); t = r.json()["table"]; cols = t["columnNames"]
    rt, vn = cols.index("Row Type"), cols.index("Variable Name")
    dims = [row[vn] for row in t["rows"] if row[rt] == "dimension"]
    vars_ = [row[vn] for row in t["rows"] if row[rt] == "variable"]
    print("OACP dims:", dims, "| nvars:", len(vars_), "| first:", vars_[:6], flush=True)
except Exception as e:
    print("OACP info ERROR", e, flush=True)

size(f"{EBASE}/griddap/OACP-Argo-Global.csv?GLOBAL_PPD", "OACP griddap GLOBAL_PPD", show=4)
