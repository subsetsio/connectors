import httpx, urllib.request, json, ssl
host="ws01.cenace.gob.mx:8082"
tail="/2024/06/01/2024/06/01/JSON"
def zona(txt):
    try:
        j=json.loads(txt); res=j.get("Resultados",[])
        return [(x.get("zona_carga"), len(x.get("Valores",[]))) for x in res]
    except Exception as e: return ("nonjson", txt[:80])

ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
# 1) urllib raw space
for raw in ["CENTRO ORIENTE","CENTRO%20ORIENTE","VALLE DE MEXICO"]:
    url=f"https://{host}/SWPEND/SIM/SIN/MDA/{urllib.parse.quote(raw)}{tail}" if False else f"https://{host}/SWPEND/SIM/SIN/MDA/{raw.replace(' ','%20')}{tail}"
    try:
        req=urllib.request.Request(url)
        t=urllib.request.urlopen(req, context=ctx, timeout=40).read().decode("utf-8","replace")
        print("urllib", repr(raw), "->", zona(t))
    except Exception as e:
        print("urllib", repr(raw), "ERR", type(e).__name__, str(e)[:80])
