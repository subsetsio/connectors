import json, duckdb, pyarrow as pa, pyarrow.parquet as pq
from utils import build_groups, csv_rows, safe_columns
groups=build_groups()
u=json.load(open('/Users/nathansnellaert/Documents/hardened/data/sources/ato/work/entity_union.json'))
ENTS=["taxation-statistics--individuals-table-6b-csv",  # 281 cols
      "taxation-statistics--company-table-5-csv",
      u[0], u[70]]
for ent in ENTS:
    res=groups.get(ent)
    rows=[]; rk={}
    for r in res:
        if r["format"]!="CSV" or not r.get("url"): continue
        for row in csv_rows(r["url"], r["income_year"]):
            rows.append(row); [rk.setdefault(k,None) for k in row]
    cm=safe_columns(rk)
    schema=pa.schema([(cm[k],pa.string()) for k in rk])
    recs=[{cm[k]:(None if row.get(k) is None else str(row.get(k))) for k in rk} for row in rows]
    t=pa.Table.from_pylist(recs, schema=schema)
    pq.write_table(t,"/tmp/_v.parquet")
    cnt=duckdb.sql("SELECT count(*) FROM read_parquet('/tmp/_v.parquet')").fetchone()[0]
    desc=duckdb.sql("DESCRIBE SELECT * FROM read_parquet('/tmp/_v.parquet')").fetchall()
    # check delta-safe names
    bad=[c[0] for c in desc if any(ch in c[0] for ch in ' ,;{}()\n\t=')]
    print(f"{ent}\n  rows={len(recs)} cnt={cnt} ncols={len(schema.names)} unsafe_names={bad[:3]}")
    print("  sample cols:", schema.names[:6])
