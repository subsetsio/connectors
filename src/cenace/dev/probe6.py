from subsets_utils import get
import json
# CKAN API on datos.gob.mx
for ds in ["pnd_mda_sistema_interconectado_nacional_2023","pnd_mda_sistema_interconectado_baja_california_2020"]:
    try:
        r=get(f"https://datos.gob.mx/api/3/action/package_show?id={ds}", timeout=(10,60))
        j=r.json()
        res=j["result"]["resources"]
        print(ds, "->", [(x.get("format"), x.get("url")) for x in res][:4])
    except Exception as e:
        print(ds, "ERR", type(e).__name__, str(e)[:120])
