from subsets_utils import get
MYH="https://myhospitalsapi.aihw.gov.au/api/v1"
H={"Accept":"application/json"}

# measure categories
cats=get(f"{MYH}/measure-categories", headers=H, timeout=(10,60)).json()["result"]
codes=[c["measure_category_code"] for c in cats]
print("categories:", codes)

# flat-data-extract: page sizes per category
import json
total=0
first_row=None
for code in codes:
    skip=0; top=5000; n=0
    while True:
        d=get(f"{MYH}/flat-data-extract/{code}", headers=H, params={"top":top,"skip":skip}, timeout=(10,120)).json()
        rows=d["result"]["data"]
        if first_row is None and rows:
            first_row=rows[0]
        n+=len(rows)
        if len(rows)<top: break
        skip+=top
    print(f"  {code}: {n} rows")
    total+=n
print("TOTAL flat-data-extract rows:", total)
print("first_row keys:", sorted(first_row.keys()))
print("first_row sample:", json.dumps(first_row)[:700])

# measures + reporting-units shape
m=get(f"{MYH}/measures", headers=H, timeout=(10,60)).json()["result"][0]
print("\nMEASURE keys:", sorted(m.keys()))
print(json.dumps(m)[:500])
u=get(f"{MYH}/reporting-units", headers=H, timeout=(10,90)).json()["result"][0]
print("\nUNIT keys:", sorted(u.keys()))
print(json.dumps({k:u[k] for k in u if k!='mapped_reporting_units'})[:500])
