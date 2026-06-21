import gzip
import json
import tempfile
import os
import duckdb
from subsets_utils import get

# Mimic fetch_one for one small dataset, then run the transform SQL over the
# ndjson.gz via read_json_auto exactly as the runtime does.
from nodes.insee import _flatten, BASE_URL, PAGE_SIZE

ENTITY = "DS_TICE"
path = os.path.join(tempfile.gettempdir(), "insee_smoke.ndjson.gz")

url = f"{BASE_URL}/data/{ENTITY}"
params = {"maxResult": PAGE_SIZE, "page": 1}
n = 0
with gzip.open(path, "wt", encoding="utf-8") as fh:
    while True:
        doc = get(url, params=params, headers={"Accept": "application/json"}, timeout=(10, 180)).json()
        for obs in doc.get("observations") or []:
            fh.write(json.dumps(_flatten(obs), ensure_ascii=False) + "\n")
            n += 1
        paging = doc.get("paging") or {}
        nxt = paging.get("next")
        if not nxt or paging.get("isLast"):
            break
        url, params = nxt, None
print("wrote", n, "rows ->", path)

con = duckdb.connect()
con.sql(f"CREATE TEMP VIEW v AS SELECT * FROM read_json_auto('{path}')")
print("\n-- inferred schema --")
print(con.sql("DESCRIBE v").df().to_string())
res = con.sql('SELECT * FROM v WHERE OBS_VALUE IS NOT NULL').df()
print("\ntransform rows:", len(res))
print("OBS_VALUE dtype:", res["OBS_VALUE"].dtype)
print(res.head(3).to_string())
