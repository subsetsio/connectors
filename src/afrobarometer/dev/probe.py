import json
from subsets_utils import get, post

WS = "https://afrobarometer-online-analysis.com/odav2/ws/oda/"

def sess():
    r = post(WS+"stats/session/7", json={}, timeout=30)
    return r.json()["sid"]

def index(sid, rid, amids):
    r = post(WS+f"index/7/{rid}/1", data=f"amids={amids}",
             headers={"odaSession":str(sid),"Content-Type":"application/x-www-form-urlencoded"}, timeout=60)
    return r.json()

def question(sid, qid, body):
    r = post(WS+f"question/7/{qid}", json=body, headers={"odaSession":str(sid)}, timeout=90)
    return r.json()

sid = sess()
# R10=1686. Get a real opinion question id. Use Q40-ish (Q40 trust president etc). Let's grab index.
idx = index(sid, 1686, "2")  # Algeria valor
qs = [it for it in idx["lista"] if it["formato"]=="P"]
print("R10 questions:", len(qs))
# pick a substantive one with multiple categories - find 'trust' or 'democracy'
cand = [it for it in qs if any(w in it["title"].lower() for w in ("trust","democracy","economic condition","corrupt"))][:3]
for c in cand: print(" cand", c["id"], c["title"])
q = cand[0] if cand else qs[50]
qid = q["id"]; print("Using qid", qid, q["title"])

# samples for R10
samps = idx["samples"]["rows"]
print("R10 samples:", len(samps), "example", samps[0])
all_saids = ",".join(str(s["id"]) for s in samps)

print("\n=== A) cross1=COUNTRY_CROSS, timeseries=false, single round 1686 (per-country within round?) ===")
b = {"cuid":1686,"amids":"","saids":all_saids,"idioma":1,"roundEquiv":1686,"cross1":-999999,"cross2":0,"showEmpty":True,"timeseries":False,"maps":False,"mapa":0,"trad":-1}
d = question(sid, qid, b)
r = d.get("resultado",{})
print("success",d.get("success"),"tipo",r.get("tipo_resultado"))
print("etiqCols:", [c.get("shortLabel") for c in r.get("etiqCols",[])][:50])
rows=r.get("tables",[{}])[0].get("rows",[])
print("n answer rows", len(rows))
if rows: print("row0:", {k:rows[0][k] for k in ("longLabel","frecuenciasN","porcentaje","porcentajeV") if k in rows[0]})

print("\n=== B) cross1=COUNTRY_CROSS, timeseries=true, roundEquiv=0 (country x round?) ===")
b2 = dict(b); b2["timeseries"]=True; b2["roundEquiv"]=0
d2 = question(sid, qid, b2)
r2 = d2.get("resultado",{})
print("success",d2.get("success"),"tipo",r2.get("tipo_resultado"))
print("etiqCols:", [c.get("shortLabel") for c in r2.get("etiqCols",[])][:60])
print("etiqCols2:", [c.get("shortLabel") for c in r2.get("etiqCols2",[])][:60])
rows2=r2.get("tables",[{}])[0].get("rows",[])
print("n rows", len(rows2))
if rows2: print("row0 keys", list(rows2[0].keys())); print("row0", json.dumps(rows2[0])[:500])
