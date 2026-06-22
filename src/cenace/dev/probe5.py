from subsets_utils import get
# Try PEND "all zones" style and check if single-token works broadly
for z in ["VDM","VALLEDEMEXICO","MEXICO","CENTRO","MONTERREY","GUADALAJARA","TIJUANA","MEXICALI","CULIACAN","HERMOSILLO","LAGUNA","MERIDA","QUERETARO","TOLUCA","PUEBLA"]:
    r = get(f"https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN/MDA/{z}/2024/06/01/2024/06/01/JSON", timeout=(10,40))
    try:
        res=r.json().get("Resultados",[])
        n=sum(len(x.get("Valores",[])) for x in res)
        print(z, r.status_code, "vals", n)
    except Exception as e:
        print(z, r.status_code, "err")
