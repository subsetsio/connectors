from utils import build_groups, _download
import csv, io
groups=build_groups()
for ent in ["taxation-statistics--individuals-table-20-average-taxable-income-income-year",
            "taxation-statistics--individuals-table-27-maps",
            "taxation-statistics--individuals-table-28"]:
    print("\n====",ent)
    for r in groups.get(ent,[]):
        print("  fmt",r["format"],"yr",r["income_year"],"url",(r["url"] or "")[-70:])
        if r["format"]=="CSV" and r.get("url"):
            try:
                txt=_download(r["url"]).decode("utf-8-sig",errors="replace")
                rdr=csv.reader(io.StringIO(txt))
                head=[next(rdr,None) for _ in range(3)]
                print("    first rows:", [h[:6] if h else None for h in head])
                print("    total_len_chars", len(txt))
            except Exception as e:
                print("    ERR",type(e).__name__,str(e)[:80])
