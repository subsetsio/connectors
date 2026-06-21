import sys, glob, os
sys.path.insert(0,"src")
import nodes.banco_de_portugal as m
from subsets_utils import load_raw_ndjson

# small (1 series) and a medium one
small="05e2845d5d567afd88b699a91b0c20b8"
med="6a83b46f5911d1b086a2891746a2fd9a"  # loans for house purchase
for ds in (small, med):
    nid=f"banco-de-portugal-{ds}"
    m.fetch_one(nid)
    rows=load_raw_ndjson(nid)
    print(f"{ds}: {len(rows)} rows; sample={rows[0]}")
    # check distinct series & date format
    print("   distinct series:", len({r['series_id'] for r in rows}),
          "dates:", min(r['reference_date'] for r in rows), "->", max(r['reference_date'] for r in rows))

# now run the transform SQL for med via duckdb directly
import duckdb
from subsets_utils.config import raw_uri
base=raw_uri("__p__","__").rsplit("/",1)[0]
f=glob.glob(base+f"/banco-de-portugal-{med}.ndjson.gz")[0]
spec=[s for s in m.TRANSFORM_SPECS if s.id==f"banco-de-portugal-{med}-transform"][0]
duckdb.sql(f'CREATE TEMP VIEW "banco-de-portugal-{med}" AS SELECT * FROM read_json_auto(\'{f}\')')
res=duckdb.sql(spec.sql).fetchnumpy()
print("transform cols:", list(res.keys()), "nrows:", len(res['value']))
print("transform sample date:", res['reference_date'][0], "value:", res['value'][0])
