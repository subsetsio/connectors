import io, openpyxl
from subsets_utils import get

XLSX="https://docs.google.com/spreadsheets/d/1k6Q7_i6GFGeiHwIl-ai7ghS4_K8-7kQ1/export?format=xlsx"
GAS="https://script.google.com/macros/s/AKfycbyZPqzls-14RINmRDddhRwoSW4DylOPrVybRky82qxL5fm7p_QVmZKuQFbBwN6oBdF9aw/exec?path=Sheet1&action=read"

r=get(XLSX, timeout=60)
print("xlsx", r.status_code, len(r.content))
wb=openpyxl.load_workbook(io.BytesIO(r.content), read_only=True, data_only=True)
ws=wb["Data"]
it=ws.iter_rows(values_only=True)
hdr=next(it)
print("hdr", hdr)
rows=[x for x in it if x[4] is not None]
print("n data rows", len(rows))
print("row0", rows[0])
print("types", [type(v).__name__ for v in rows[0]])

g=get(GAS, timeout=60)
print("gas", g.status_code, g.headers.get("content-type"))
j=g.json()
data=j["data"]
print("gas n", len(data))
# field type survey
from collections import Counter
keys=set()
for d in data: keys.update(d.keys())
print("keys", sorted(keys))
for k in ["acc_id","Rscale","Dscale","elevation","slope","acc_no_killed","aspect","acc_date"]:
    vals=Counter(type(d.get(k)).__name__ for d in data)
    print(k, dict(vals))
