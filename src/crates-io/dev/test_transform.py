"""Validate the CSV->parquet->DuckDB-SQL path on categories (first member)."""
import os, tarfile, tempfile, shutil
import httpx, duckdb, pyarrow as pa, pyarrow.csv as pcsv


class _IterReader:
    def __init__(self, it): self._it, self._buf = it, b""
    def read(self, n=-1):
        if n is None or n < 0:
            c=[self._buf]; self._buf=b""; c.extend(self._it); return b"".join(c)
        while len(self._buf) < n:
            try: self._buf += next(self._it)
            except StopIteration: break
        out, self._buf = self._buf[:n], self._buf[n:]; return out


COLS = ["id","slug","category","description","crates_cnt","path","created_at"]
URL = "https://static.crates.io/db-dump.tar.gz"
tmp = tempfile.mkdtemp()
csv_path = os.path.join(tmp, "categories.csv")
with httpx.stream("GET", URL, follow_redirects=True, timeout=120.0) as r:
    r.raise_for_status()
    tar = tarfile.open(fileobj=_IterReader(r.iter_bytes(1<<16)), mode="r|gz")
    for m in tar:
        if m.name.endswith("/data/categories.csv"):
            with open(csv_path,"wb") as f: shutil.copyfileobj(tar.extractfile(m), f)
            break

convert = pcsv.ConvertOptions(include_columns=COLS, column_types={c: pa.string() for c in COLS})
parse = pcsv.ParseOptions(newlines_in_values=True)
reader = pcsv.open_csv(csv_path, parse_options=parse, convert_options=convert)
pq = os.path.join(tmp, "categories.parquet")
import pyarrow.parquet as pqw
schema = reader.schema
print("raw schema:", schema)
with pqw.ParquetWriter(pq, schema) as w:
    for b in reader:
        w.write_table(pa.Table.from_batches([b], schema=schema))

con = duckdb.connect()
con.execute(f'CREATE VIEW "crates-io-categories" AS SELECT * FROM read_parquet(\'{pq}\')')
sql = '''
    SELECT CAST(id AS BIGINT) AS id, slug, category, description,
           CAST(COALESCE(crates_cnt,'0') AS BIGINT) AS crates_cnt, path,
           CAST(created_at AS TIMESTAMP) AS created_at
    FROM "crates-io-categories"
    WHERE id IS NOT NULL AND slug IS NOT NULL AND category IS NOT NULL
'''
res = con.sql(sql)
print("transform schema:", res.types, res.columns)
rows = con.sql(f"SELECT count(*) FROM ({sql})").fetchone()[0]
print("rows:", rows)
print(con.sql(sql + " LIMIT 3").fetchall())
assert rows > 50, rows
print("OK")
