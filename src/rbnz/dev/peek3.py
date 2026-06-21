import openpyxl, io
for label,path in {"B1m":"dev/wb_26c35d.xlsx","M5":"dev/wb_a35c9a.xlsx"}.items():
    content=open(path,'rb').read()
    wb=openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    for sh in ["Data","Series Definitions"]:
        ws=wb[sh]; ws.reset_dimensions()
        grid=[list(r) for r in ws.iter_rows(values_only=True)]
        print(f"\n##### {label}/{sh} rows={len(grid)}")
        for i,r in enumerate(grid[:6]):
            print(" ",i,[(f"{type(c).__name__}:{str(c)[:14]}" if c is not None else None) for c in r[:5]])
    wb.close()
