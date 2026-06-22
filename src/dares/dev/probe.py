import io
import pyarrow.parquet as pq
from subsets_utils import get

BASE = "https://data.dares.travail-emploi.gouv.fr/api/explore/v2.1"

for dsid in ["dares_tempspartiel_detail_annuelles", "dares_defm_communales-brutes", "dares_nomenclature_fap2021"]:
    url = f"{BASE}/catalog/datasets/{dsid}/exports/parquet"
    r = get(url, timeout=(10, 180))
    print("===", dsid, "http", r.status_code, "bytes", len(r.content))
    t = pq.read_table(io.BytesIO(r.content))
    print("  rows", t.num_rows, "cols", t.num_columns)
    print("  schema:", [(f.name, str(f.type)) for f in t.schema][:12])
