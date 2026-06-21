import io
from subsets_utils import get
import xlrd

def show(url):
    print("\n===== ", url)
    r = get(url, timeout=(10,120))
    print("status", r.status_code, "bytes", len(r.content), "ctype", r.headers.get('content-type'))
    try:
        book = xlrd.open_workbook(file_contents=r.content)
    except Exception as e:
        print("xlrd FAIL:", type(e).__name__, e); return
    sh = book.sheet_by_index(0)
    print("sheets", book.sheet_names(), "dims", sh.nrows, "x", sh.ncols)
    for ri in range(min(sh.nrows, 12)):
        row=[]
        for ci in range(min(sh.ncols, 10)):
            v=sh.cell_value(ri,ci)
            if isinstance(v,float): v=round(v,3)
            row.append(str(v)[:18])
        print(f" r{ri:2}:", " | ".join(row))

base="http://tjnj.gdstats.gov.cn:8080/tjnj/2025/directory"
for u in [
    f"{base}/02/excel/02-01.xls",   # GDP main indicators (time series)
    f"{base}/03/excel/03-01.xls",   # population main
    f"{base}/02/excel/02-15-0.xls", # GDP by city part 0
]:
    show(u)
