import sys; sys.path.insert(0,"src")
import io, openpyxl
from subsets_utils import get

def probe(fid, name):
    print(f"\n########## {name} (file {fid}) ##########")
    r=get(f"https://dataverse.nl/api/access/datafile/{fid}", timeout=300)
    r.raise_for_status()
    wb=openpyxl.load_workbook(io.BytesIO(r.content), read_only=True, data_only=True)
    print("SHEETS:", wb.sheetnames)
    for sn in wb.sheetnames:
        ws=wb[sn]
        rows=[]
        for i,row in enumerate(ws.iter_rows(values_only=True)):
            rows.append(row)
            if i>=4: break
        print(f"  --- sheet '{sn}'  dims~{ws.max_row}x{ws.max_column} ---")
        for row in rows:
            print("    ", [ (str(c)[:18] if c is not None else None) for c in row[:14] ])

for fid,name in [
  (554105,"PWT11.0 pwt110.xlsx"),
  (354095,"PWT10.01 pwt1001.xlsx"),
  (421302,"Maddison2023 mpd2023_web.xlsx"),
  (383800,"PLD2023 pld2023_dataset.xlsx"),
  (382704,"ETD ETD_230918.xlsx"),
  (390044,"ETDTE ETDTE.xlsx"),
]:
    try: probe(fid,name)
    except Exception as e: print("ERR",name,e)
