import json, re
from subsets_utils import get, post
WS="https://afrobarometer-online-analysis.com/odav2/ws/oda/"
CFG="https://afrobarometer-online-analysis.com/odav2/oda.jsp?config=7"

def get_config():
    html=get(CFG,timeout=60).text
    i=html.find("config:"); s=html.find("{",i); depth=0
    for j in range(s,len(html)):
        if html[j]=="{":depth+=1
        elif html[j]=="}":
            depth-=1
            if depth==0:e=j+1;break
    return json.loads(html[s:e])

cfg=get_config()
rounds=cfg["rounds"]; tit=cfg["titrounds"]
print("rounds",rounds); print("titrounds",tit)
sid=post(WS+"stats/session/7",json={},timeout=30).json()["sid"]

# union samples (country->said), and union questions (varcode->latest qid)
country_said={}   # country name -> (round_index, said)
var_rep={}        # variable code -> (round_index, qid, title, grupo)
for ridx,rid in enumerate(rounds):
    # need amids; pass all region valors for this round
    valors=[str(r["valor"]) for r in cfg["regions"] if f"#{rid}#" in (r.get("rounds") or "")]
    amids=",".join(valors) if valors else "2"
    idx=post(WS+f"index/7/{rid}/1",data=f"amids={amids}",headers={"odaSession":str(sid),"Content-Type":"application/x-www-form-urlencoded"},timeout=60).json()
    for s in idx.get("samples",{}).get("rows",[]):
        name=s["data"][1].strip()
        country=re.sub(r"\s*\(.*\)$","",name).strip()
        # keep latest round's said per country
        country_said[country]=(ridx, s["id"])
    for it in idx.get("lista",[]):
        if it.get("formato")=="P" and it.get("variable"):
            vc=it["variable"]
            if vc not in var_rep or ridx> var_rep[vc][0]:
                var_rep[vc]=(ridx, it["id"], it["title"], it["grupo"])
    print(f"round {tit[ridx]}: lista={len(idx.get('lista',[]))} samples={len(idx.get('samples',{}).get('rows',[]))} cum_countries={len(country_said)} cum_vars={len(var_rep)}")

print("\nTOTAL distinct countries:",len(country_said))
print("TOTAL distinct variables:",len(var_rep))
all_saids=",".join(str(v[1]) for v in country_said.values())
# test one question with full country set
qid=var_rep.get("Q22",(0,2549018))[1]
b={"cuid":rounds[-1],"amids":"","saids":all_saids,"idioma":1,"roundEquiv":0,"cross1":-999999,"cross2":0,"showEmpty":True,"timeseries":True,"maps":False,"mapa":0,"trad":-1}
d=post(WS+f"question/7/{qid}",json=b,headers={"odaSession":str(sid)},timeout=120).json()
r=d["resultado"]
print("\nQ22 call: tipo",r.get("tipo_resultado"),"n_country_tables",len(r["tables"]),"rounds_cols",[c['shortLabel'] for c in r['etiqCols']])
print("countries in result:",len(r.get("etiqCols2",[])))
