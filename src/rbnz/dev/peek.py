import openpyxl, io, datetime
for label,path in {"M5":"dev/wb_a35c9a.xlsx","S10":"dev/wb_9b2be0.xlsx"}.items():
    wb=openpyxl.load_workbook(io.BytesIO(open(path,'rb').read()), read_only=True, data_only=True)
    for sh in ["Data","Series Definitions"]:
        ws=wb[sh]
        grid=[list(r) for r in ws.iter_rows(values_only=True)]
        print(f"\n##### {label} / {sh}  rows={len(grid)}")
        for i,r in enumerate(grid[:8]):
            print(i, [ (str(c)[:18] if c is not None else None) for c in r[:8]])
    wb.close()
