from subsets_utils import get
r = get("https://datos.estadisticas.pr/api/3/action/package_show",
        params={"id":"comercio-externo"}, timeout=(10,120))
r.raise_for_status()
print("OK", len(r.json()["result"]["resources"]), "resources")
