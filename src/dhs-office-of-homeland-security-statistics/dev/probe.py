import io, re
from subsets_utils import get
import openpyxl

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def fetch(url):
    r=get(url, headers={"User-Agent":UA}, timeout=(10,120))
    r.raise_for_status()
    return r.content

def grid(content, sheet):
    wb=openpyxl.load_workbook(io.BytesIO(content), data_only=True, read_only=True)
    ws=wb[sheet]
    rows=[[c for c in row] for row in ws.iter_rows(values_only=True)]
    wb.close()
    return rows

for url, sheet in [
    ("https://ohss.dhs.gov/system/files/2026-06/2026_0604_ohss_yearbook_lawful_permanent_residents_fy2024.xlsx","Table 1"),
    ("https://ohss.dhs.gov/system/files/2026-06/2026_0604_ohss_yearbook_lawful_permanent_residents_fy2024.xlsx","Table 2"),
    ("https://ohss.dhs.gov/sites/default/files/2024-10/24-1011_ohss_immigration-enforcement-and-legal-processes-tables-june-2024_2.xlsx","ERO Arrests by Citizenship"),
]:
    print("\n##### ", sheet)
    try:
        g=grid(fetch(url), sheet)
    except Exception as e:
        print("ERR", type(e).__name__, e); continue
    print("nrows", len(g))
    for i,r in enumerate(g[:14]):
        cells=[("" if c is None else str(c))[:22] for c in r[:8]]
        print(i, "|".join(cells))
