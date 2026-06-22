import sys; sys.path.insert(0,'src')
import nodes.cbn as c
from datetime import datetime,timezone
end_year=datetime.now(tz=timezone.utc).year+1
for tid in [81,5,12]:
    info=c._indicators_for_table(tid); ids=[i for i,_ in info]; names=[n for _,n in info]
    wide=c._search(tid,ids,f"{c.DATE_FLOOR_YEAR}-01-01",f"{end_year}-12-31",attempts=5)
    cp,body=c._grid(wide.get("TableView") or "")
    print(f"t{tid}: aligned={c._check_alignment(body,ids)} inds={len(ids)} body={len(body)}")
    out={}
    c._emit_non_daily(cp,body,ids,names,out)
    rows=list(out.values())
    print(f"  rows={len(rows)} freqs={set(r['frequency'] for r in rows)}")
    # show a sample for first indicator
    s=[r for r in rows if r['indicator_id']==ids[0]][:3]
    for r in s: print("   ",r['indicator_id'],r['indicator'][:25],r['period'],r['date'],r['value'])
    # date range
    ds=[r['date'] for r in rows if r['date']]
    print("   date range",min(ds),max(ds))
