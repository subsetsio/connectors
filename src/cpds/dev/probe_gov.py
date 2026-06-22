import io
from subsets_utils import get, transient_retry
import openpyxl

@transient_retry(attempts=8, min_wait=5, max_wait=90)
def fetch(url):
    r = get(url, timeout=120); r.raise_for_status(); return r.content

gov = fetch("https://cpds-data.org/wp-content/uploads/2025/06/government_composition_1960-2023_update_2025.xlsx")
wb = openpyxl.load_workbook(io.BytesIO(gov), read_only=True, data_only=True)

def header_rows(ws):
    rows=list(ws.iter_rows(values_only=True))
    # find row index where col A == 'Year'
    hidx=None
    for i,r in enumerate(rows):
        if r and str(r[0]).strip()=="Year":
            hidx=i; break
    return hidx, rows

for cname in ["Australia","Germany","United States"]:
    ws=wb[cname]
    hidx,rows=header_rows(ws)
    print(f"\n=== {cname} header at row {hidx}, total rows {len(rows)}")
    top=rows[hidx]; sub=rows[hidx+1]
    for j in range(len(top)):
        t=top[j]; s=sub[j]
        if t is not None or s is not None:
            print(f"  col{j}: top={t!r} sub={s!r}")
    # last data rows
    data=[r for r in rows[hidx+2:] if r[0] is not None]
    print("  data rows:", len(data), "last year:", data[-1][0] if data else None)
