import json
from subsets_utils import post
WS="https://afrobarometer-online-analysis.com/odav2/ws/oda/"
sid=post(WS+"stats/session/7",json={},timeout=30).json()["sid"]
idx=post(WS+"index/7/1686/1",data="amids=2",headers={"odaSession":str(sid),"Content-Type":"application/x-www-form-urlencoded"},timeout=60).json()
all_saids=",".join(str(s["id"]) for s in idx["samples"]["rows"])
qid=2549018  # Support for democracy
b={"cuid":1686,"amids":"","saids":all_saids,"idioma":1,"roundEquiv":0,"cross1":-999999,"cross2":0,"showEmpty":True,"timeseries":True,"maps":False,"mapa":0,"trad":-1}
d=post(WS+f"question/7/{qid}",json=b,headers={"odaSession":str(sid)},timeout=90).json()
r=d["resultado"]
print("tipo",r.get("tipo_resultado"))
print("N tables:",len(r["tables"]))
print("etiqCols (rounds):",[c["shortLabel"] for c in r["etiqCols"]])
print("etiqCols2 (countries):",len(r.get("etiqCols2",[])),"->",[c["shortLabel"] for c in r.get("etiqCols2",[])][:5])
for ti,t in enumerate(r["tables"][:2]):
    print(f"--- table {ti} keys:",list(t.keys()))
    print("   table-level fields:",{k:t[k] for k in t if k!='rows'})
    print("   n rows:",len(t["rows"]))
    print("   row0:",json.dumps({k:t['rows'][0].get(k) for k in ('longLabel','frecuenciasN','porcentajeV')}))
# Also check ficha (question metadata)
print("ficha keys:",list(d.get("ficha",{}).keys()))
print("ficha:",json.dumps(d.get("ficha",{}))[:400])
print("samplestext:",json.dumps(d.get("samples"))[:200] if d.get("samples") else None)
