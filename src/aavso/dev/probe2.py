from subsets_utils import get
import io
import pyarrow as pa
import pyarrow.csv as pacsv

BASE = "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync"
COLS = ["recno","OID","Name","V","RAJ2000","DEJ2000","Type","l_max","max","u_max","n_max","f_min","l_min","min","u_min","n_min","Epoch","u_Epoch","l_Period","Period","u_Period","Sp","n_OID"]
TYPES = {"recno":pa.int64(),"OID":pa.int64(),"Name":pa.string(),"V":pa.int64(),
 "RAJ2000":pa.float64(),"DEJ2000":pa.float64(),"Type":pa.string(),"l_max":pa.string(),
 "max":pa.float64(),"u_max":pa.string(),"n_max":pa.string(),"f_min":pa.string(),
 "l_min":pa.string(),"min":pa.float64(),"u_min":pa.string(),"n_min":pa.string(),
 "Epoch":pa.float64(),"u_Epoch":pa.string(),"l_Period":pa.string(),"Period":pa.float64(),
 "u_Period":pa.string(),"Sp":pa.string(),"n_OID":pa.string()}

q = f'SELECT TOP 1000 {",".join(COLS)} FROM "B/vsx/vsx" WHERE recno > 0 ORDER BY recno'
r = get(BASE, params={"REQUEST":"doQuery","LANG":"ADQL","FORMAT":"csv","QUERY":q}, timeout=(10,180))
r.raise_for_status()
tbl = pacsv.read_csv(io.BytesIO(r.content),
    convert_options=pacsv.ConvertOptions(column_types=TYPES, strings_can_be_null=True))
print("schema:")
print(tbl.schema)
print("rows", tbl.num_rows)
import pyarrow.compute as pc
for c in ["max","min","Epoch","Period","V","RAJ2000"]:
    col=tbl[c]
    print(c, "nulls=", col.null_count)
print("sample names:", [tbl["Name"][i].as_py() for i in range(3)])
print("max range:", pc.min(tbl["max"]).as_py(), pc.max(tbl["max"]).as_py())
