import sys, time, importlib.util
sys.path.insert(0,"src")
spec=importlib.util.spec_from_file_location("elstat_node","src/nodes/elstat.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
# single-threaded, polite
for code in ["SAM08","SEL84","SPO18","SFA10","SIN06","SMA27","SME12","SME16"]:
    try:
        files=mod._select_excel(mod._excel_attachments(code))
        rows=[]
        for fn,content in files: rows.extend(mod._melt_workbook(content,fn))
        print(f"{code}: files={[fn for fn,_ in files]} rows={len(rows)}")
    except Exception as e:
        print(f"{code}: ERR {type(e).__name__}: {str(e)[:120]}")
    time.sleep(1)
