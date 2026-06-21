import sys; sys.path.insert(0,"src")
import io, openpyxl
from subsets_utils import get

def probe(fid, name):
    print(f"\n########## {name} (file {fid}) ##########")
    r=get(f"https://dataverse.nl/api/access/datafile/{fid}", timeout=600)
    r.raise_for_status()
    wb=openpyxl.load_workbook(io.BytesIO(r.content), read_only=True, data_only=True)
    print("SHEETS:", wb.sheetnames)
    for sn in wb.sheetnames[:6]:
        ws=wb[sn]; rows=[]
        for i,row in enumerate(ws.iter_rows(values_only=True)):
            rows.append(row)
            if i>=3: break
        print(f"  --- '{sn}' ~{ws.max_row}x{ws.max_column} ---")
        for row in rows:
            print("    ", [ (str(c)[:16] if c is not None else None) for c in row[:16] ])

for fid,name in [
  (268662,"WIODlr SEA lr_wiod_sea_final.xlsx"),
  (199095,"WIOD2016 Socio_Economic_Accounts.xlsx"),
  (199111,"WIOD2013 Socio_Economic_Accounts_July14.xlsx"),
  (410572,"ASUT xlsx"),
]:
    try: probe(fid,name)
    except Exception as e: print("ERR",name,repr(e))
