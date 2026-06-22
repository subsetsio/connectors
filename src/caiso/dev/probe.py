import io, zipfile, csv, time
import xml.etree.ElementTree as ET
from subsets_utils import get

BASE = "https://oasis.caiso.com/oasisapi/SingleZip"

# (queryname, extra params, market_run_id)
PROBES = [
    ("PRC_LMP", {"node": "TH_NP15_GEN-APND"}, "DAM"),
    ("SLD_FCST", {}, "DAM"),
    ("AS_RESULTS", {"anc_type": "ALL", "anc_region": "ALL"}, "DAM"),
    ("PRC_FUEL", {"fuel_region_id": "ALL"}, None),
    ("ENE_SLRS", {"tac_zone_name": "ALL", "schedule": "ALL"}, "DAM"),
    ("TRNS_USAGE", {"ti_id": "ALL", "ti_direction": "ALL"}, "DAM"),
]

def fetch(qn, extra, mrid):
    params = {"queryname": qn, "version": "1", "resultformat": "6",
              "startdatetime": "20240115T08:00-0000", "enddatetime": "20240117T08:00-0000"}
    params.update(extra)
    if mrid: params["market_run_id"] = mrid
    r = get(BASE, params=params, timeout=(10,90))
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    name = zf.namelist()[0]
    raw = zf.read(name)
    if name.lower().endswith(".csv"):
        rdr = csv.reader(io.StringIO(raw.decode("utf-8-sig")))
        rows = list(rdr)
        hdr = rows[0]
        print(f"\n=== {qn} ({mrid}) -> {name}  rows={len(rows)-1}")
        print("COLS:", hdr)
        if len(rows) > 1:
            print("SAMPLE:", dict(zip(hdr, rows[1])))
    else:
        print(f"\n=== {qn} ({mrid}) -> {name} (XML)")
        print(raw.decode("utf-8","replace")[:400])

for qn, extra, mrid in PROBES:
    try:
        fetch(qn, extra, mrid)
    except Exception as e:
        print(f"\n=== {qn} ({mrid}) ERROR {type(e).__name__}: {e}")
    time.sleep(5)
