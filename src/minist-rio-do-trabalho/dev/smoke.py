import os, sys
sys.path.insert(0, "src")
sys.path.insert(0, "src/nodes")
os.environ.pop("CI", None)  # local dev mode -> writes under data/dev
import duckdb
import nodes.minist_rio_do_trabalho as M
from subsets_utils import list_raw_files, load_raw_ndjson

# one tiny novo-caged EXC archive
url = M.FTP_ROOT + "NOVO%20CAGED/2026/202604/CAGEDEXC202604.7z"
asset = "minist-rio-do-trabalho-novo-caged-exclusoes-202604"
n = M._process_archive(url, asset, {"competencia": 202604, "arquivo_fonte": "CAGEDEXC202604"})
print("rows written:", n)
files = list_raw_files(f"minist-rio-do-trabalho-novo-caged-exclusoes-*")
print("raw files:", files)
rows = load_raw_ndjson(asset)
print("rows back:", len(rows), "| sample keys:", sorted(rows[0].keys())[:12], "...total", len(rows[0]))
print("sample row competencia/arquivo:", rows[0].get("competencia"), rows[0].get("arquivo_fonte"))

# now exercise the transform SQL via duckdb over the local file
base = files[0].rsplit("/",1)[0] if "/" in files[0] else "."
# find the actual local path
import glob
cands = glob.glob(f"data/dev/**/{asset}.ndjson.gz", recursive=True) or glob.glob(f"**/{asset}.ndjson.gz", recursive=True)
print("local path:", cands)
p = cands[0]
sql = M._CAGED_SQL.format(dep="t")
duckdb.sql(f"CREATE VIEW t AS SELECT * FROM read_json_auto(['{p}'])")
res = duckdb.sql(sql)
print("transform cols:", res.columns[:8], "...n=", len(res.columns))
print("transform sample:", duckdb.sql(sql + " LIMIT 2").fetchall()[0][:5])
print("transform rowcount:", duckdb.sql(f"SELECT count(*) FROM ({sql})").fetchone()[0])
