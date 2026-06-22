import io, zipfile, csv, json, sys
sys.path.insert(0, "src")
from subsets_utils import get
import duckdb

def fetch(params):
    r = get("https://oasis.caiso.com/oasisapi/SingleZip", params=params, timeout=(10,180))
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    name = zf.namelist()[0]
    txt = zf.read(name).decode("utf-8","replace")
    if name.endswith(".xml"):
        print("ERR", txt[:200]); return []
    return list(csv.DictReader(io.StringIO(txt)))

cases = {
 "prc_lmp": dict(queryname="PRC_LMP",version=12,market_run_id="DAM",node="TH_SP15_GEN-APND",
   startdatetime="20240601T08:00-0000",enddatetime="20240603T08:00-0000",resultformat=6),
 "prc_intvl_lmp": dict(queryname="PRC_INTVL_LMP",version=3,market_run_id="RTM",node="TH_SP15_GEN-APND",
   startdatetime="20240601T08:00-0000",enddatetime="20240602T08:00-0000",resultformat=6),
 "prc_fuel": dict(queryname="PRC_FUEL",version=1,fuel_region_id="ALL",
   startdatetime="20240601T08:00-0000",enddatetime="20240603T08:00-0000",resultformat=6),
 "as_results": dict(queryname="AS_RESULTS",version=1,market_run_id="DAM",anc_type="ALL",anc_region="ALL",
   startdatetime="20240601T08:00-0000",enddatetime="20240603T08:00-0000",resultformat=6),
}
con = duckdb.connect()
for k,p in cases.items():
    rows = fetch(p)
    print(f"\n### {k}: {len(rows)} raw rows; cols={list(rows[0].keys()) if rows else []}")
    con.register("t", duckdb.from_pylist if False else None) if False else None
    # write ndjson temp and read
    with open(f"dev/{k}.ndjson","w") as f:
        for r in rows: f.write(json.dumps(r)+"\n")
