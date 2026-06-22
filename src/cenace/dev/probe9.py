from subsets_utils import get
import json
def summarize(u, key):
    r=get(u, timeout=(10,90)); j=r.json(); res=j.get("Resultados",[])
    names=[x.get(key) for x in res]
    nval=sum(len(x.get("Valores",[])) for x in res)
    print(u.split("SIM/")[1][:40], "groups=",len(res),"totvals=",nval)
    print("  names:", names[:40])
# PEND no-zone, all 3 systems
summarize("https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN/MDA/2024/06/01/2024/06/01/JSON","zona_carga")
summarize("https://ws01.cenace.gob.mx:8082/SWPEND/SIM/BCA/MDA/2024/06/01/2024/06/01/JSON","zona_carga")
summarize("https://ws01.cenace.gob.mx:8082/SWPEND/SIM/BCS/MDA/2024/06/01/2024/06/01/JSON","zona_carga")
# Does PML also accept no-node? (would be huge)
r=get("https://ws01.cenace.gob.mx:8082/SWPML/SIM/SIN/MDA/2024/06/01/2024/06/01/JSON", timeout=(10,90))
print("PML no-node:", r.status_code, r.text[:120])
