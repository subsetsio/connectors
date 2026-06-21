import sys; sys.path.insert(0,"src")
from subsets_utils import get, transient_retry
import pyarrow as pa, duckdb

@transient_retry()
def gj(u):
    r=get(u, timeout=(10,180)); r.raise_for_status(); return r.json()["value"]

BASE="http://www.ipeadata.gov.br/api/odata4"
meta=gj(f"{BASE}/Metadados")[:50]
series_rows=[{k:r.get(k) for k in ["SERCODIGO","SERNOME","SERCOMENTARIO","SERATUALIZACAO","BASNOME","FNTSIGLA","FNTNOME","FNTURL","PERNOME","UNINOME","MULNOME","SERSTATUS","PAICODIGO","TEMCODIGO","SERNUMERICA"]} for r in meta]
sschema=pa.schema([(f,pa.string()) for f in ["SERCODIGO","SERNOME","SERCOMENTARIO","SERATUALIZACAO","BASNOME","FNTSIGLA","FNTNOME","FNTURL","PERNOME","UNINOME","MULNOME","SERSTATUS","PAICODIGO"]]+[("TEMCODIGO",pa.int64()),("SERNUMERICA",pa.bool_())])
st=pa.Table.from_pylist(series_rows, schema=sschema)

vals=[]
for c in [r["SERCODIGO"] for r in meta[:3]]:
    vals+=gj(f"{BASE}/ValoresSerie(SERCODIGO='{c}')")
vschema=pa.schema([("SERCODIGO",pa.string()),("VALDATA",pa.string()),("VALVALOR",pa.float64()),("NIVNOME",pa.string()),("TERCODIGO",pa.string())])
vt=pa.Table.from_pylist([{k:v.get(k) for k in ["SERCODIGO","VALDATA","VALVALOR","NIVNOME","TERCODIGO"]} for v in vals], schema=vschema)

con=duckdb.connect()
con.register("ipea-series", st)
con.register("ipea-values", vt)
s=con.execute('''SELECT SERCODIGO AS series_code, SERNOME AS name, BASNOME AS database, TEMCODIGO AS theme_code, CAST(SERATUALIZACAO AS TIMESTAMP) AS last_updated, SERNUMERICA AS is_numeric FROM "ipea-series" WHERE SERCODIGO IS NOT NULL''').arrow().read_all()
print("series transform rows:", s.num_rows, "cols:", s.column_names)
print(s.slice(0,2).to_pydict())
v=con.execute('''SELECT SERCODIGO AS series_code, CAST(substr(VALDATA,1,10) AS DATE) AS date, CAST(VALVALOR AS DOUBLE) AS value, NULLIF(NIVNOME,'') AS geo_level, NULLIF(TERCODIGO,'') AS territory_code FROM "ipea-values" WHERE VALVALOR IS NOT NULL AND VALDATA IS NOT NULL''').arrow().read_all()
print("values transform rows:", v.num_rows, "cols:", v.column_names)
print({k:v.column(k)[0].as_py() for k in v.column_names})
