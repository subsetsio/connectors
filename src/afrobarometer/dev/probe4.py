import json, re
from subsets_utils import get, post
WS="https://afrobarometer-online-analysis.com/odav2/ws/oda/"
sid=post(WS+"stats/session/7",json={},timeout=30).json()["sid"]
idx=post(WS+"index/7/1686/1",data="amids=2",headers={"odaSession":str(sid),"Content-Type":"application/x-www-form-urlencoded"},timeout=60).json()
saids=",".join(str(s["id"]) for s in idx["samples"]["rows"])

def parse(qid):
    b={"cuid":1686,"amids":"","saids":saids,"idioma":1,"roundEquiv":0,"cross1":-999999,"cross2":0,"showEmpty":True,"timeseries":True,"maps":False,"mapa":0,"trad":-1}
    d=post(WS+f"question/7/{qid}",json=b,headers={"odaSession":str(sid)},timeout=120).json()
    if not d.get("success"): return None,d
    r=d["resultado"]; ficha=d.get("ficha",{})
    rounds=[(c.get("shortLabel","").strip(),c.get("total")) for c in r["etiqCols"]]
    countries=[c.get("shortLabel","").strip() for c in r.get("etiqCols2",[])]
    rows=[]
    for ci,t in enumerate(r["tables"]):
        country=countries[ci] if ci<len(countries) else f"col{ci}"
        if country=="(N)": continue
        for ans in t["rows"]:
            if ans.get("total"): continue
            fr=ans.get("frecuenciasN",[]); pv=ans.get("porcentajeV",[])
            for ri,(rlbl,rtot) in enumerate(rounds):
                if rtot or rlbl=="(N)": continue
                n=fr[ri] if ri<len(fr) else 0
                p=pv[ri] if ri<len(pv) else None
                if (n in (0,None)) and (p in (0,0.0,None)): continue
                rows.append((ficha.get("MAVARIABLE"),country,rlbl,ans.get("valorCat"),(ans.get("longLabel") or "")[:40],ans.get("missing"),n,round(p,2) if p is not None else None))
    return rows, ficha

rows,ficha=parse(2549018)  # Q22 recurring
print("Q22 rows:",len(rows)); 
for x in rows[:4]: print("  ",x)
print("ficha MAUNIT/MATIPOINDICADOR/MACATEGORIAS:",ficha.get("MAUNIT"),ficha.get("MATIPOINDICADOR"),"|",str(ficha.get("MACATEGORIAS"))[:120])
# a single round question: pick one from R8 only. find a var present only in R8
print("\n--- distinct countries seen in Q22:",len(set(r[1] for r in rows)))
print("--- distinct rounds seen:",sorted(set(r[2] for r in rows)))
