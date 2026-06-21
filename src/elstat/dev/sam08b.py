import sys, importlib.util
sys.path.insert(0,"src")
spec=importlib.util.spec_from_file_location("m","src/nodes/elstat.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for code in ["SAM08"]:
    files=m._select_excel(m._excel_attachments(code))
    rows=[]
    for fn,c in files: rows.extend(m._melt_workbook(c,fn))
    print(code, "files=", [f for f,_ in files][:4], "rows=", len(rows))
