from subsets_utils import get
import io
import pyarrow.csv as pacsv

BASE = "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync"
COLS = "recno,OID,Name,V,RAJ2000,DEJ2000,Type,l_max,max,u_max,n_max,f_min,l_min,min,u_min,n_min,Epoch,u_Epoch,l_Period,Period,u_Period,Sp,n_OID"

def run(q):
    r = get(BASE, params={"REQUEST":"doQuery","LANG":"ADQL","FORMAT":"csv","QUERY":q}, timeout=(10,180))
    r.raise_for_status()
    return r.text

# 1) paged query by recno watermark
q = f'SELECT TOP 5 {COLS} FROM "B/vsx/vsx" WHERE recno > 100000 ORDER BY recno'
t = run(q)
print("=== page sample (recno>100000) ===")
print(t[:1200])
lines = t.strip().splitlines()
print("rows returned:", len(lines)-1)

# 2) how big a TOP does sync honor? request 200000
q2 = f'SELECT TOP 200000 recno FROM "B/vsx/vsx" WHERE recno > 0 ORDER BY recno'
t2 = run(q2)
n = len(t2.strip().splitlines())-1
print("=== TOP 200000 returned rows:", n, "===")

# 3) parse a page all-string with pyarrow
tbl = pacsv.read_csv(io.BytesIO(t.encode()),
    convert_options=pacsv.ConvertOptions(column_types={c: __import__("pyarrow").string() for c in COLS.split(",")}))
print("parsed schema:", tbl.schema.names, "rows", tbl.num_rows)
