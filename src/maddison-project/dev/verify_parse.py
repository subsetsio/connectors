import sys; sys.argv=['x']
import io, openpyxl, pyarrow as pa
from subsets_utils import get
import nodes.maddison_project as m
wb = m._load_workbook()
# country
ws = wb["Full data"]; it = ws.iter_rows(values_only=True); next(it)
crows=[r for r in it if r[0] is not None]
print("country rows:", len(crows))
# regional via the real parsing path
wb2 = m._load_workbook()
ws2 = wb2["Regional data"]; grid=list(ws2.iter_rows(values_only=True))
label_row=grid[1]; region_names=[str(label_row[c]).strip() for c in range(1,9)]
cols=[(region_names[i],1+i,11+i) for i in range(8)]+[("World",9,19)]
rows=[]
for r in grid[2:]:
    y=m._to_int(r[0])
    if y is None: continue
    for region,gc,pc in cols:
        g=m._to_float(r[gc]) if gc<len(r) else None
        p=m._to_float(r[pc]) if pc<len(r) else None
        if g is None and p is None: continue
        rows.append((region,y,g,p))
print("regional rows:", len(rows))
print("regions:", sorted(set(x[0] for x in rows)))
print("year range:", min(x[1] for x in rows), max(x[1] for x in rows))
print("sample:", rows[:3])
print("World rows:", [x for x in rows if x[0]=='World'][:2], "count", sum(1 for x in rows if x[0]=='World'))
