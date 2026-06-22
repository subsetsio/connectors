import sys, csv, glob
sys.path.insert(0,"src")
# import the pure-python helpers (avoid subsets_utils http)
import importlib.util
spec=importlib.util.spec_from_file_location("m","src/nodes/canada_mortgage_and_housing_corporation.py")
# can't import (needs subsets_utils); instead inline-copy the funcs via exec of needed parts
import re
STD_COLS={"ref_date","geo","dguid","uom","uom_id","scalar_factor","scalar_id","vector","coordinate","value","status","symbol","terminated","decimals"}
exec(open("src/nodes/canada_mortgage_and_housing_corporation.py").read().split("import pyarrow")[0])  # nothing useful
# Just reimplement quickly by importing functions textually is messy; instead test schema build with pyarrow
import pyarrow as pa
SCHEMA = pa.schema([("product_id",pa.string()),("ref_date",pa.string()),("geo",pa.string()),("dguid",pa.string()),("dimensions",pa.string()),("uom",pa.string()),("scalar_factor",pa.string()),("vector",pa.string()),("coordinate",pa.string()),("value",pa.float64()),("status",pa.string()),("decimals",pa.int64())])

def _to_float(raw):
    raw=(raw or "").strip()
    if raw in ("",".","..","...","F","x","E"): return None
    try: return float(raw)
    except ValueError: return None
def _to_int(raw):
    raw=(raw or "").strip()
    if raw=="": return None
    try: return int(raw)
    except ValueError: return None
def normalise(pid,header,rows):
    lower=[h.strip().lower() for h in header]
    idx={n:lower.index(n) for n in STD_COLS if n in lower}
    dimpos=[i for i,n in enumerate(lower) if n not in STD_COLS]
    def cell(row,name):
        i=idx.get(name); return row[i] if i is not None and i<len(row) else ""
    out=[]
    for row in rows:
        if not row: continue
        dims=" | ".join(f"{header[i].strip()}={row[i].strip()}" for i in dimpos if i<len(row) and row[i].strip())
        out.append({"product_id":pid,"ref_date":cell(row,"ref_date").strip() or None,"geo":cell(row,"geo").strip() or None,"dguid":cell(row,"dguid").strip() or None,"dimensions":dims or None,"uom":cell(row,"uom").strip() or None,"scalar_factor":cell(row,"scalar_factor").strip() or None,"vector":cell(row,"vector").strip() or None,"coordinate":cell(row,"coordinate").strip() or None,"value":_to_float(cell(row,"value")),"status":cell(row,"status").strip() or None,"decimals":_to_int(cell(row,"decimals"))})
    return out

for f in ["/tmp/scx/34100097.csv","/tmp/scx_34100133/34100133.csv","/tmp/scx_34100135/34100135.csv"]:
    with open(f,encoding="utf-8-sig") as fh:
        r=csv.reader(fh); h=next(r); rows=list(r)
    pid=f.split("/")[-1].replace(".csv","")
    norm=normalise(pid,h,rows)
    t=pa.Table.from_pylist(norm,schema=SCHEMA)
    print(pid,"rows",len(t),"| sample dims:",norm[0]["dimensions"],"| val",norm[0]["value"],"| vector",norm[0]["vector"])
    # uniqueness check vector+ref_date
    keys=[(r["vector"],r["ref_date"]) for r in norm]
    print("   unique(vector,ref_date):",len(keys)==len(set(keys)),"dupes:",len(keys)-len(set(keys)))
