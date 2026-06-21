from subsets_utils import get
import csv, io

def mdt(theme, tb, sv, sp):
    fn_sp = sp.replace('%','percent')
    url = f"https://www.censtatd.gov.hk/data/MDT_{theme}_{tb}_{sv}_{fn_sp}.csv"
    r = get(url, timeout=(10,60))
    rows = list(csv.reader(io.StringIO(r.text))) if r.status_code==200 else []
    print(f"  {sv}/{sp} -> {fn_sp}  http={r.status_code} nrows={len(rows)-1 if rows else 0} cols={rows[0] if rows else None}")

print("110-01001A POP_XFDH/Prop_1dp_%_n:")
mdt("76","110-01001A","POP_XFDH","Prop_1dp_%_n")
print("310-31001 CUR/YoY_1dp_%_s:")
mdt("69","310-31001","CUR","YoY_1dp_%_s")
print("310-31001 CUR/Raw_M_hkd_d (control):")
mdt("69","310-31001","CUR","Raw_M_hkd_d")
