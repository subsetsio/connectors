import io, openpyxl
from subsets_utils import get
url = "https://www.macrohistory.net/app/download/9834512569/JSTdatasetR6.xlsx?t=1763503850"
r = get(url, timeout=(10,120))
r.raise_for_status()
print("bytes", len(r.content), "ctype", r.headers.get("content-type"))
wb = openpyxl.load_workbook(io.BytesIO(r.content), read_only=True, data_only=True)
ws = wb[wb.sheetnames[0]]
rows = ws.iter_rows(values_only=True)
hdr = list(next(rows))
print("ncols", len(hdr))
# scan column python types
from collections import defaultdict
types = defaultdict(set)
n=0
samples = {}
for row in rows:
    n+=1
    for h,v in zip(hdr,row):
        if v is not None:
            types[h].add(type(v).__name__)
            samples.setdefault(h, v)
print("nrows", n)
for h in hdr:
    print(f"{h:30s} types={sorted(types[h])} sample={samples.get(h)!r}")
