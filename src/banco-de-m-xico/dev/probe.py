import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import json

# tokenless probe — confirm error semantics + reachability
for path in [
    "series/SF43718",
    "series/SF43718/datos/oportuno",
]:
    url = "https://www.banxico.org.mx/SieAPIRest/service/v1/" + path
    try:
        r = get(url, timeout=(10.0, 60.0), headers={"Accept": "application/json"})
        print(path, "->", r.status_code, "ctype", r.headers.get("content-type"))
        print("  body:", r.text[:400])
    except Exception as e:
        print(path, "ERR", type(e).__name__, e)
