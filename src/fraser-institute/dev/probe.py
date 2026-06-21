import json, duckdb, sys
sys.path.insert(0, "src")
from nodes.fraser_institute import TRANSFORM_SPECS, _flatten

files = {
 "fraser-institute-economic-freedom-of-the-world":"/tmp/ftw_get_all_data.json",
 "fraser-institute-economic-freedom-of-north-america-allgov":"/tmp/ftw_get_states_data.json",
 "fraser-institute-economic-freedom-of-north-america-subnational":"/tmp/ftw_get_subnational_data.json",
}
con = duckdb.connect()
for asset, f in files.items():
    rows = _flatten(json.load(open(f)))
    p = f"/tmp/{asset}.ndjson"
    with open(p,"w") as fh:
        for r in rows: fh.write(json.dumps(r)+"\n")
    # register a view named after the asset id
    con.execute(f'CREATE VIEW "{asset}" AS SELECT * FROM read_json_auto(\'{p}\')')

for spec in TRANSFORM_SPECS:
    res = con.execute(spec.sql).fetchall(); ncol = len(con.execute(spec.sql).description)
    name = spec.id.replace("-transform","")
    yr = con.execute(f"SELECT min(year),max(year),count(distinct year) FROM ({spec.sql})").fetchone()
    dup = con.execute(f"SELECT count(*)-count(distinct (CAST(year AS VARCHAR)||'|'||iso_code)) FROM ({spec.sql})").fetchone()[0]
    print(f"{name}: rows={len(res)} cols={ncol} years={yr} dup_year_iso={dup}")
    print("   cols:", [d[0] for d in con.execute(spec.sql).description])
