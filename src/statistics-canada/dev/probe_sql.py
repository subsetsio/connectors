import io, zipfile, tempfile, os
import duckdb
from subsets_utils import get

pid="10100002"
j=get(f"https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{pid}/en", timeout=(10,120)).json()
url=j["object"]
rz=get(url, timeout=(10,300))
zf=zipfile.ZipFile(io.BytesIO(rz.content))
tmp=tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
with zf.open(f"{pid}.csv") as f:
    while True:
        c=f.read(1<<20)
        if not c: break
        tmp.write(c)
tmp.close()
con=duckdb.connect()
con.execute(f"CREATE VIEW dep AS SELECT * FROM read_csv_auto('{tmp.name}')")
print("columns/types:")
for row in con.execute("DESCRIBE dep").fetchall(): print("  ", row[0], row[1])
sql='''
SELECT * REPLACE (TRY_CAST("VALUE" AS DOUBLE) AS "VALUE")
FROM dep
'''
res=con.execute(sql)
import pyarrow as pa
t=res.fetch_arrow_table()
print("rows:", t.num_rows)
print("VALUE type:", t.schema.field("VALUE").type)
print("non-null VALUE:", t.column("VALUE").null_count, "nulls of", t.num_rows)
os.unlink(tmp.name)
