import json, tempfile, os
import duckdb
from subsets_utils import get
import sys
sys.path.insert(0, "src/nodes")
import data_gov as M

BASE = M.BASE
def action(a, **p):
    r = get(f"{BASE}/action/{a}", params=p, timeout=(10.0,180.0)); r.raise_for_status()
    return r.json()["result"]

res = action("package_search", rows=300, start=0, sort=M.SORT)["results"]
ds_rows = [M._dataset_row(p) for p in res]
rs_rows = []
for p in res: rs_rows.extend(M._resource_rows(p))
orgs = action("organization_list", all_fields="true", limit=25, offset=0)
org_rows = [{
 "id":o.get("id"),"name":o.get("name"),"title":o.get("title"),"display_name":o.get("display_name"),
 "description":o.get("description"),"package_count":o.get("package_count"),
 "organization_type":o.get("organization_type"),"type":o.get("type"),"state":o.get("state"),
 "created":o.get("created"),"num_followers":o.get("num_followers"),
 "is_organization":o.get("is_organization"),"approval_status":o.get("approval_status")} for o in orgs]

def run(name, rows, sql, view):
    d=tempfile.mkdtemp()
    fp=os.path.join(d,"x.ndjson")
    with open(fp,"w") as f:
        for r in rows: f.write(json.dumps(r)+"\n")
    con=duckdb.connect()
    con.execute(f'CREATE VIEW "{view}" AS SELECT * FROM read_json_auto(\'{fp}\')')
    sql2 = sql  # SQL already references view by name
    out=con.execute(sql2).fetch_arrow_table()
    print(f"\n=== {name}: {out.num_rows} rows, {out.num_columns} cols ===")
    print("cols:", out.schema.names)
    print("types:", [str(out.schema.field(i).type) for i in range(out.num_columns)])
    print("sample:", out.slice(0,1).to_pylist())

specs = {s.id: s for s in M.TRANSFORM_SPECS}
run("datasets", ds_rows, specs["data-gov-datasets-transform"].sql, "data-gov-datasets")
run("resources", rs_rows, specs["data-gov-resources-transform"].sql, "data-gov-resources")
run("organizations", org_rows, specs["data-gov-organizations-transform"].sql, "data-gov-organizations")
print("\nrow counts: datasets",len(ds_rows),"resources",len(rs_rows),"orgs",len(org_rows))
