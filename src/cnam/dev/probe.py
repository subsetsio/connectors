import io
import pyarrow.parquet as pq
from subsets_utils import get

base = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"

# small dataset, parquet export
for ds in ["couverture-sas", "demographie-ages-moyens-part-des-femmes-part-des-plus-de-60-ans"]:
    url = f"{base}/{ds}/exports/parquet"
    r = get(url, timeout=(10, 120))
    print(ds, "status", r.status_code, "bytes", len(r.content), "ctype", r.headers.get("content-type"))
    t = pq.read_table(io.BytesIO(r.content))
    print("  rows", t.num_rows)
    print("  schema:")
    for f in t.schema:
        print("    ", f.name, f.type)
    print("  sample row:", {k: v[0] for k, v in t.slice(0,1).to_pydict().items()})
    print()
