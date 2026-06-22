import json, io, gzip, tempfile, os
import duckdb
from subsets_utils import get, get_client

API = "https://api.statbank.dk/v1"

def tableinfo(tid):
    r = get(f"{API}/tableinfo/{tid}", params={"format": "JSON"}, timeout=(10, 120))
    r.raise_for_status(); return r.json()

def run(tid):
    info = tableinfo(tid)
    varcodes = [v["id"] for v in info["variables"]]
    time_codes = {v["id"].upper() for v in info["variables"] if v.get("time")}
    body = {"table": tid, "lang": "en", "format": "BULK",
            "variables": [{"code": c, "values": ["*"]} for c in varcodes]}
    tmp = tempfile.NamedTemporaryFile(suffix=".ndjson.gz", delete=False).name
    written = 0
    with get_client().stream("POST", f"{API}/data", json=body, timeout=(10, 600)) as r:
        r.raise_for_status()
        lines = r.iter_lines()
        cols = [c.strip() for c in next(lines).split(";")]
        keys = []
        for c in cols:
            cu = c.upper()
            keys.append("value" if cu == "INDHOLD" else "time" if cu in time_codes else c.lower())
        ncols = len(keys)
        with gzip.open(tmp, "wt", encoding="utf-8") as f:
            for line in lines:
                if not line: continue
                parts = line.split(";")
                if len(parts) != ncols: continue
                f.write(json.dumps({keys[i]: parts[i] for i in range(ncols)}, separators=(",",":")) + "\n")
                written += 1
    con = duckdb.connect()
    con.execute(f"CREATE VIEW src AS SELECT * FROM read_json_auto('{tmp}')")
    schema = con.execute("DESCRIBE src").fetchall()
    sql = '''SELECT * EXCLUDE (value), TRY_CAST(value AS DOUBLE) AS value
             FROM src WHERE value <> '..' AND TRY_CAST(value AS DOUBLE) IS NOT NULL'''
    res = con.execute(sql).fetchall()
    desc = [d[0] for d in con.execute("DESCRIBE ("+sql+")").fetchall()]  # noqa
    print(f"\n=== {tid}: raw rows={written}")
    print("  view schema:", [(c[0],c[1]) for c in schema])
    print("  transform out cols:", [d[0] for d in con.execute(f"DESCRIBE {sql.__class__ and 'src'}").fetchall()] if False else "")
    print("  transform rows:", len(res))
    print("  sample out:", res[0] if res else None)
    os.unlink(tmp)

for tid in ["DNMNOGL", "DNVPU", "DNRENTD"]:
    run(tid)
