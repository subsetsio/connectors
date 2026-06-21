from subsets_utils import get
import json
def fetch(u):
    r = get(u, timeout=(10,120)); r.raise_for_status(); return r.json()
for u in ["https://servicios.ine.es/wstempus/js/EN/DATOS_TABLA/28481",
          "https://servicios.ine.es/wstempus/js/EN/DATOS_TABLA/28481?nult=2"]:
    d = fetch(u)
    print("URL", u)
    print("type:", type(d).__name__)
    if isinstance(d, dict):
        print("keys:", list(d.keys())[:20])
        print(json.dumps(d, ensure_ascii=False)[:800])
    elif isinstance(d, list):
        print("len:", len(d), "first type:", type(d[0]).__name__)
        print(json.dumps(d[0], ensure_ascii=False)[:600])
    print("----")
