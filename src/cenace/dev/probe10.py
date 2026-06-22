from subsets_utils import get
def info(label,u):
    r=get(u,timeout=(10,120))
    try:
        j=r.json(); res=j.get("Resultados",[]); n=sum(len(x.get("Valores",[])) for x in res)
        print(label, r.status_code, "groups",len(res),"vals",n, "| status:",j.get("status"))
    except Exception:
        print(label, r.status_code, "TEXT:", r.text[:90])
info("PEND 7d nolist","https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN/MDA/2024/06/01/2024/06/07/JSON")
info("PSC 7d nolist","https://ws01.cenace.gob.mx:8082/SWPSC/SIM/SIN/MDA/2024/06/01/2024/06/07/JSON")
info("PML 20-node 7d","https://ws01.cenace.gob.mx:8082/SWPML/SIM/SIN/MDA/" + ",".join(["01PLO-115"]*1+["01AHU-115"]) + "/2024/06/01/2024/06/07/JSON")
info("MTR old ok","https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN/MTR/2024/06/01/2024/06/01/JSON")
info("MTR recent (unpub)","https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN/MTR/2026/06/20/2026/06/20/JSON")
info("MDA future+2","https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN/MDA/2026/06/30/2026/06/30/JSON")
