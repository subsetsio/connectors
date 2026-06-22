import httpx
c = httpx.Client(timeout=40, follow_redirects=True, headers={"User-Agent":"subsets-bot/1.0"})
tail="/2024/06/01/2024/06/01/JSON"
for raw in ["CENTRO ORIENTE","VALLE DE MEXICO"]:
    u=httpx.URL(f"https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN/MDA/{raw}{tail}")
    r=c.get(u)
    print("SENT:", str(r.request.url))
    try:
        res=r.json().get("Resultados",[]); print("  ->", [(x.get("zona_carga"),len(x.get("Valores",[]))) for x in res])
    except Exception as e: print("  nonjson", r.status_code, r.text[:80])
# Also: does PEND accept a system-wide call with NO zone segment (like PSC)?
for u in ["https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN/MDA/2024/06/01/2024/06/01/JSON"]:
    r=c.get(u); print("NO-ZONE:", r.status_code, r.text[:120])
