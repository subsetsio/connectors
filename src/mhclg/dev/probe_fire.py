import sys, os
sys.path.insert(0, os.path.abspath("src"))
from subsets_utils import get
import io
def content(bp):
    r=get(f"https://www.gov.uk/api/content/{bp}", timeout=(10,120)); r.raise_for_status(); return r.json()
for eid,bp in [("fire","government/statistical-data-sets/fire-statistics-data-tables"),
               ("planning","government/statistical-data-sets/live-tables-on-planning-application-statistics")]:
    d=content(bp); atts=d["details"]["attachments"]
    tab=[a for a in atts if a.get("content_type") in {
        "text/csv","application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.oasis.opendocument.spreadsheet"}]
    print("="*60, eid, "total atts:",len(atts),"tabular:",len(tab))
    # size of largest few by file_size
    sizes=sorted([(a.get("file_size") or 0, a.get("content_type","")[-12:], a.get("filename")) for a in tab], reverse=True)[:6]
    for s in sizes: print(f"  {s[0]:>10} bytes  {s[1]:<12} {s[2]}")
    print("  total tabular bytes:", sum((a.get('file_size') or 0) for a in tab))
