import sys; sys.path.insert(0,'src')
import nodes.cbn as c
tid=48
info=c._indicators_for_table(tid); ids=[i for i,_ in info]; names=[n for _,n in info]
far="2028-12-31"; out={}; active=[]
for y in range(2010,2025):
    for m in range(1,13):
        j=c._search(tid,ids,f"{y}-{m:02d}-01",far,attempts=1)
        if c._no_data(j): continue
        cp,bd=c._grid(j.get("TableView") or "")
        if not c._check_alignment(bd,ids): continue
        if not active: print("first daily:",y,m,"is_daily=",c._looks_daily(cp))
        active.append((y,m))
        c._emit_daily_month(cp,bd,ids,names,y,m,out)
print("active months:",len(active),"first",active[0] if active else None,"last",active[-1] if active else None)
rows=list(out.values())
print("total daily rows:",len(rows))
ds=[r['date'] for r in rows]
print("date range",min(ds),max(ds))
# verify positional dates valid (no 31-Jun etc): all dates are real -> date() already validates
import collections
print("freq set",set(r['frequency'] for r in rows))
s=sorted([r for r in rows if r['indicator_id']==ids[0]],key=lambda x:x['date'])
print("ind0",names[0],"first",s[0]['period'],s[0]['value'],"last",s[-1]['period'],s[-1]['value'])
