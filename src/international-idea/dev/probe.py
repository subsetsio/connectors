from subsets_utils import get
import io, openpyxl

# 1. GSoD labels shape
labels = get("https://www.idea.int/gsod-indices/api/labels", timeout=60).json()
print("LABELS:", len(labels), "first:", labels[0])

# 2. GSoD data one row
d = get("https://www.idea.int/gsod-indices/api/data?year1=2020&year2=2020", timeout=120).json()
print("DATA rows:", len(d), "ncols:", len(d[0]))
print("DATA keys:", list(d[0].keys()))
print("sample vals:", {k: d[0][k] for k in list(d[0])[:12]})

# 3. Voter turnout xlsx export
r = get("https://www.idea.int/data-tools/export?type=region_only&themeId=293&world=all&loc=home", timeout=120)
print("VT status", r.status_code, "ctype", r.headers.get("content-type"), "bytes", len(r.content))
wb = openpyxl.load_workbook(io.BytesIO(r.content), read_only=True, data_only=True)
print("VT sheets:", wb.sheetnames)
for sn in wb.sheetnames[:3]:
    ws = wb[sn]
    print(f"--- sheet '{sn}' dims={ws.max_row}x{ws.max_column} ---")
    for i,row in enumerate(ws.iter_rows(values_only=True)):
        print(i, row)
        if i>=8: break
