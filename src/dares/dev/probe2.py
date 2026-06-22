import io
import pyarrow.parquet as pq
from subsets_utils import get
BASE = "https://data.dares.travail-emploi.gouv.fr/api/explore/v2.1"
for dsid in ["dares_jint_depuis2005","dares_jint_1975-2004"]:
    r = get(f"{BASE}/catalog/datasets/{dsid}/exports/parquet", timeout=(10,120))
    t = pq.read_table(io.BytesIO(r.content))
    print("===",dsid,"rows",t.num_rows,"cols",t.num_columns)
    print("  schema:",[(f.name,str(f.type)) for f in t.schema])
    print("  head:",t.slice(0,3).to_pylist())
