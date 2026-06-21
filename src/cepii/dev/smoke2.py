import sys
sys.path.insert(0, "src")
import duckdb
import nodes.cepii as M
from subsets_utils import list_raw_files
from subsets_utils.config import raw_uri

TARGETS = ["cepii-trade-volume", "cepii-product-level-trade-elasticities", "cepii-rprod", "cepii-eqchange"]
READERS = {".parquet": "read_parquet", ".csv": "read_csv_auto", ".tsv": "read_csv_auto"}

def reader_for(p):
    n = p.lower()
    if n.endswith(".gz"):
        n = n[:-3]
    for ext, rd in READERS.items():
        if n.endswith(ext):
            return rd

base = raw_uri("__probe__", "__").rsplit("/", 1)[0]
sql_by_id = {s.id: s.sql for s in M.TRANSFORM_SPECS}
for did in TARGETS:
    print(f"\n===== {did}")
    try:
        M.fetch_one(did)
    except Exception as e:
        print(f"  FETCH FAILED: {type(e).__name__}: {e}"); continue
    rels = list_raw_files(f"{did}.*") or list_raw_files(f"{did}-*")
    rd = reader_for(rels[0])
    paths = [f"{base}/{r}" for r in rels]
    con = duckdb.connect()
    con.sql(f'CREATE OR REPLACE TEMP VIEW "{did}" AS SELECT * FROM {rd}({paths})')
    cols = [c[0] for c in con.sql(f'SELECT * FROM "{did}" LIMIT 0').description]
    print(f"  raw cols ({len(cols)}): {cols[:10]}")
    sql = sql_by_id[f"{did}-transform"]
    try:
        n = con.sql(f"SELECT count(*) FROM ({sql})").fetchone()[0]
        oc = [c[0] for c in con.sql(f"SELECT * FROM ({sql}) LIMIT 0").description]
        print(f"  TRANSFORM rows={n:,} cols={oc[:10]}")
        print(con.sql(f"SELECT * FROM ({sql}) LIMIT 3"))
    except Exception as e:
        print(f"  TRANSFORM FAILED: {type(e).__name__}: {e}")
