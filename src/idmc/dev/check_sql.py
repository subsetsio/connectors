"""Validate each transform SQL against a tiny live sample of each feed, so we
catch column/cast errors before paying for a full cloud run."""
import sys
import duckdb

sys.path.insert(0, "src")
from nodes import idmc  # noqa: E402
from subsets_utils import get  # noqa: E402

CID = idmc.CLIENT_ID
BASE = idmc.BASE


def gidd_sample(path):
    j = get(f"{BASE}/gidd/{path}/", params={"client_id": CID, "limit": 5}).json()
    return j["results"]


def run(name, rows, view, sql, transform):
    con = duckdb.connect()
    con.register("rows", {"r": rows}) if False else None
    import pyarrow as pa
    # Build a duckdb view from the list of dicts via json
    import json as _json
    tmp = con.from_arrow(pa.Table.from_pylist(
        [{"j": _json.dumps(r)} for r in rows]))
    con.register("raw_json", tmp)
    con.execute(f'CREATE VIEW "{view}" AS SELECT unnest(from_json(j, \'JSON\')) FROM raw_json') if False else None
    # Simpler: register the rows directly as a struct table
    con.register(view, pa.Table.from_pylist(rows))
    out = con.execute(sql).fetch_arrow_table()
    print(f"\n=== {name}: {out.num_rows} rows, {out.num_columns} cols")
    print(out.schema)


# conflicts / displacements / disasters via GIDD sample
conf = gidd_sample("conflicts")
disp = gidd_sample("displacements")
dis = gidd_sample("disasters")
for r in dis:
    r["event_codes"] = idmc._join(r.get("event_codes"))
    r["event_codes_type"] = idmc._join(r.get("event_codes_type"))

run("conflicts", conf, "idmc-conflicts", idmc._SQL_CONFLICTS, None)
run("displacements", disp, "idmc-displacements", idmc._SQL_DISPLACEMENTS, None)
run("disasters", dis, "idmc-disasters", idmc._SQL_DISASTERS, None)

# idu sample (fetch all then slice — endpoint has no limit param; take first 5)
idu_all = get(f"{BASE}/idus/all/", params={"client_id": CID}).json()
run("idu", idu_all[:5], "idmc-idu", idmc._SQL_IDU, None)

# disaggregations sample
gj = get(f"{BASE}/gidd/disaggregations/disaggregation-geojson/", params={"client_id": CID}).json()
feats = gj["features"][:5]
rows = []
for feat in feats:
    props = feat.get("properties", {}) or {}
    row = {}
    for s, d in idmc._DISAGG_RENAME.items():
        v = props.get(s)
        row[d] = idmc._join(v) if d in idmc._DISAGG_ARRAY_FIELDS else v
    geom = feat.get("geometry") or {}
    lon, lat = idmc._first_coord(geom)
    row["longitude"], row["latitude"], row["geometry_type"] = lon, lat, geom.get("type")
    rows.append(row)
run("disaggregations", rows, "idmc-disaggregations", idmc._SQL_DISAGG, None)

print("\nALL SQL OK")
