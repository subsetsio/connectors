import sys; sys.path.insert(0,'src')
import nodes.cbn as c
tid=48
info=c._indicators_for_table(tid); ids=[i for i,_ in info]; names=[n for _,n in info]
probe=c._search(tid,ids,"2023-01-01","2027-12-31",attempts=4)
print("probe ok",probe.get("IsSuccessful"),"tvlen",len(probe.get("TableView") or ""))
cp,_=c._grid(probe.get("TableView") or "")
print("is_daily:",None if cp is None else c._looks_daily(cp))
out={}
for y,m in [(2024,2),(2024,3)]:
    mj=c._search(tid,ids,f"{y}-{m:02d}-01","2027-12-31",attempts=2)
    g_cp,g_body=c._grid(mj.get("TableView") or "")
    print(f"{y}-{m}: ok={mj.get('IsSuccessful')} aligned={c._check_alignment(g_body,ids)} bodyrows={len(g_body)}")
    c._emit_daily_month(g_cp,g_body,ids,names,y,m,out)
rows=list(out.values())
import collections
print("daily rows:",len(rows),"months:",dict(collections.Counter(r['date'].strftime('%Y-%m') for r in rows)))
febdays=[r['date'].day for r in rows if r['date'].month==2]
print("feb max day:",max(febdays) if febdays else None,"(2024 feb=29)")
s=sorted([r for r in rows if r['indicator_id']==ids[0]],key=lambda x:x['date'])
print("ind0",names[0]); 
for r in s[:2]+s[-2:]: print("  ",r['period'],r['date'],r['value'])
