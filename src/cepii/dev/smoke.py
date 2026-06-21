"""Local smoke test of fetch + transform for SMALL entities only.
Writes raw to the local data dir (CI unset). Run from connector dir."""
import sys
sys.path.insert(0, "src")

import duckdb
import nodes.cepii as M
from subsets_utils import list_raw_files
from subsets_utils.config import raw_uri

SMALL = [
    "cepii-trade-volume",
    "cepii-product-level-trade-elasticities",
    "cepii-language",
    "cepii-eqchange",
    "cepii-geodist",
    "cepii-econmap",
    "cepii-intense",
    "cepii-macmap-hs6",
]

READERS = {".parquet": "read_parquet", ".csv": "read_csv_auto", ".tsv": "read_csv_auto"}

def reader_for(p):
    n = p.lower()
    for suf in (".gz",):
        if n.endswith(suf):
            n = n[:-len(suf)]
    for ext, rd in READERS.items():
        if n.endswith(ext):
            return rd
    return None

base = raw_uri("__probe__", "__").rsplit("/", 1)[0]
sql_by_id = {s.id: s.sql for s in M.TRANSFORM_SPECS}

for did in SMALL:
    print(f"\n===== {did}")
    try:
        M.fetch_one(did)
    except Exception as e:
        print(f"  FETCH FAILED: {type(e).__name__}: {e}")
        continue
    rels = list_raw_files(f"{did}.*") or list_raw_files(f"{did}-*")
    print(f"  raw files: {rels[:3]}{'...' if len(rels)>3 else ''} (n={len(rels)})")
    rd = reader_for(rels[0])
    paths = [f"{base}/{r}" for r in rels]
    con = duckdb.connect()
    con.sql(f'CREATE OR REPLACE TEMP VIEW "{did}" AS SELECT * FROM {rd}({paths})')
    cols = [c[0] for c in con.sql(f'SELECT * FROM "{did}" LIMIT 0').description]
    print(f"  raw columns ({len(cols)}): {cols[:12]}")
    sql = sql_by_id[f"{did}-transform"]
    try:
        n = con.sql(f"SELECT count(*) FROM ({sql})").fetchone()[0]
        out_cols = [c[0] for c in con.sql(f"SELECT * FROM ({sql}) LIMIT 0").description]
        print(f"  TRANSFORM rows={n:,} cols={out_cols[:12]}")
        print(con.sql(f"SELECT * FROM ({sql}) LIMIT 2"))
    except Exception as e:
        print(f"  TRANSFORM FAILED: {type(e).__name__}: {e}")
