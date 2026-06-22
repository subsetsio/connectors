import io, json, duckdb
from utils import build_groups, csv_rows
groups = build_groups()
ENTS=[
 "taxation-statistics--financialratios4trusts1c-csv",
 "taxation-statistics--actitivitystatementratios1individuals1a-csv",
 "taxation-statistics--snapshottable2bcompanytaxratesince2001-02-csv",  # may not exist; will error -> shows missing handling
]
import json as J
u=J.load(open('/Users/nathansnellaert/Documents/hardened/data/sources/ato/work/entity_union.json'))
ENTS=[e for e in ENTS if e in u][:2] + [u[10], u[60], u[120]]
for ent in ENTS:
    res=groups.get(ent)
    rows=[]; keys={}
    for r in res:
        if r["format"]!="CSV" or not r.get("url"): continue
        for row in csv_rows(r["url"], r["income_year"]):
            rows.append(row); [keys.setdefault(k,None) for k in row]
    cols=list(keys)
    norm=[{k:row.get(k) for k in cols} for row in rows]
    p="/tmp/_v.ndjson"
    with open(p,"w") as f:
        for row in norm: f.write(json.dumps(row,separators=(",",":"))+"\n")
    cnt=duckdb.sql(f"SELECT count(*) FROM read_json_auto('{p}')").fetchone()[0]
    sch=duckdb.sql(f"DESCRIBE SELECT * FROM read_json_auto('{p}')").fetchall()
    print(f"\n{ent}\n  rows={len(norm)} duckdb_count={cnt} ncols={len(cols)}")
    print("  schema:", [(c[0][:30],c[1]) for c in sch][:8])
