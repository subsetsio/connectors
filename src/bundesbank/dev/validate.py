import os, glob, duckdb, sys
sys.path.insert(0, "src")
from nodes import bundesbank as B
from subsets_utils import load_raw_parquet
DATA = os.environ["DATA_DIR"]
def rg(pat): return sorted(glob.glob(os.path.join(DATA,"raw",pat)))

B.fetch_one("bundesbank-bbzvs01")
f = rg("bundesbank-bbzvs01.parquet")[0]
con = duckdb.connect()
con.execute(f'CREATE VIEW "bundesbank-bbzvs01" AS SELECT * FROM read_parquet(\'{f}\')')
sql = B._transform_sql("bundesbank-bbzvs01")
n = con.execute(f"SELECT count(*) FROM ({sql})").fetchone()[0]
nd = con.execute(f"SELECT count(*) FROM ({sql}) WHERE date IS NULL").fetchone()[0]
print("BBZVS01 transform rows:", n, "null-date:", nd)
print("BBZVS01 sample:", con.execute(f"SELECT date,frequency,series_id,value FROM ({sql}) ORDER BY date LIMIT 3").fetchall())
print("freqs:", con.execute(f"SELECT DISTINCT frequency FROM ({sql})").fetchall())

B._fetch_bbkrt_year("bundesbank-bbkrt-2026","BBKRT","2026")
con.execute(f'CREATE VIEW "bundesbank-bbkrt" AS SELECT * FROM read_parquet(\'{os.path.join(DATA,"raw","bundesbank-bbkrt-*.parquet")}\')')
sqlk = B._transform_sql("bundesbank-bbkrt")
nk = con.execute(f"SELECT count(*) FROM ({sqlk})").fetchone()[0]
ndk = con.execute(f"SELECT count(*) FROM ({sqlk}) WHERE date IS NULL").fetchone()[0]
print("\nBBKRT(2026) transform rows:", nk, "null-date:", ndk)
print("BBKRT freqs:", con.execute(f"SELECT DISTINCT frequency FROM ({sqlk})").fetchall())
print("BBKRT sample:", con.execute(f"SELECT date,frequency,series_id,value FROM ({sqlk}) ORDER BY date DESC LIMIT 2").fetchall())
