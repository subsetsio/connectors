import json, re, math
from concurrent.futures import ThreadPoolExecutor
from subsets_utils import get

ROOT = "/Users/nathansnellaert/Documents/hardened"
ents = json.load(open(f"{ROOT}/data/sources/statistics-denmark/assets/collect/entities/current.json"))

def year_of(p):
    m=re.match(r"(\d{4})",p or ""); return int(m.group(1)) if m else None
def gran(latest):
    if not latest: return "a"
    if "M" in latest: return "m"
    if "Q" in latest or "K" in latest: return "q"
    return "a"
FLAG=["population","gross domestic","gdp","consumer price","price index","harmonised","unemploy","labour force","disposable income","national account","balance of payment","export","import","foreign trade","inflation","interest rate","government finance","public finance","gross national","employ"]
SOLID=["income","wage","earnings","price","trade","turnover","sales","production","investment","debt","enterprise","compan","education","health","hospital","crime","energy","emission","tax","benefit","pension","household","family","vehicle","transport","tourism","agricultur","construction","dwelling","house","birth","death","migration","retail","bankrupt","interest","stock","consumption"]
def value(tid,e):
    sm=e["source_metadata"]; text=(sm.get("text") or "").lower()
    fy=year_of(sm.get("firstPeriod")); ly=year_of(sm.get("latestPeriod")); g=gran(sm.get("latestPeriod"))
    v=0.0; v+={"m":14,"q":10,"a":2}[g]
    if fy and ly:
        sp=ly-fy; v+= 14 if sp>=40 else 11 if sp>=25 else 7 if sp>=12 else 3 if sp>=5 else 0
    if ly: v+= 12 if ly>=2026 else 9 if ly==2025 else 4 if ly==2024 else -3 if ly==2023 else -14 if ly==2022 else -30
    if any(k in text for k in FLAG): v+=20
    elif any(k in text for k in SOLID): v+=7
    return v

vals={t:value(t,e) for t,e in ents.items()}
pool=sorted(vals,key=lambda t:-vals[t])[:750]

def info(tid):
    try:
        r=get(f"https://api.statbank.dk/v1/tableinfo/{tid}",params={"format":"JSON","lang":"en"},timeout=60)
        r.raise_for_status()
        vs=r.json().get("variables",[])
        prod=1
        for v in vs: prod*=max(1,len(v.get("values") or []))
        return tid,prod,len(vs)
    except Exception as ex:
        return tid,None,str(ex)[:40]

out={}
with ThreadPoolExecutor(max_workers=16) as ex:
    for tid,prod,nv in ex.map(info,pool):
        out[tid]={"prod":prod,"nv":nv}
json.dump({"vals":{t:vals[t] for t in pool},"info":out},open(f"{ROOT}/data/sources/statistics-denmark/work/sizes.json","w"))
ok=[t for t in pool if out[t]["prod"]]
print("fetched",len(ok),"of",len(pool))
import statistics
prods=sorted(out[t]["prod"] for t in ok)
print("prod percentiles: p50",prods[len(prods)//2],"p90",prods[int(len(prods)*.9)],"max",prods[-1])
for cap in (1_000_000,2_000_000,3_000_000,5_000_000):
    print(f"  cap {cap}: {sum(1 for t in ok if out[t]['prod']<=cap)} tables under cap")
