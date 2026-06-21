import io, re
from subsets_utils import get

base = "https://eaindustry.nic.in/"
page = get(base+"download_data_1112.asp", timeout=(10,60)).text
mfile = sorted(set(re.findall(r'indx_download_1112/monthly_index_\d{6}\.xls', page)))[-1]
print("monthly file:", mfile)

# --- WPI monthly (.xls -> xlrd) ---
import xlrd
content = get(base+mfile, timeout=(10,120)).content
print("bytes:", len(content))
wb = xlrd.open_workbook(file_contents=content)
sh = wb.sheet_by_index(0)
print("sheets:", wb.sheet_names(), "dims:", sh.nrows, "x", sh.ncols)
for r in range(min(6, sh.nrows)):
    print("ROW", r, [sh.cell_value(r,c) for c in range(min(sh.ncols, 12))])
print("...last data rows...")
for r in range(max(0,sh.nrows-3), sh.nrows):
    print("ROW", r, [sh.cell_value(r,c) for c in range(min(sh.ncols, 12))])
