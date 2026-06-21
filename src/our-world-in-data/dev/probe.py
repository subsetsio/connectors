import io
import pyarrow as pa
import pyarrow.csv as pacsv
from subsets_utils import get

for slug in ["life-expectancy", "academic-freedom-index", "political-regime-polity"]:
    url = f"https://ourworldindata.org/grapher/{slug}.csv"
    r = get(url, params={"csvType": "full", "useColumnShortNames": "true"}, timeout=(10.0, 120.0))
    print("==", slug, r.status_code, "bytes", len(r.content))
    tbl = pacsv.read_csv(io.BytesIO(r.content))
    print("cols:", tbl.column_names)
    print("schema:", tbl.schema)
    print("rows:", tbl.num_rows)
    print("first row:", {c: tbl.column(c)[0].as_py() for c in tbl.column_names})
    print()

# 404 behavior
r = get("https://ourworldindata.org/grapher/this-slug-does-not-exist-xyz.csv",
        params={"csvType": "full"}, timeout=(10.0, 60.0))
print("404 probe status:", r.status_code, "body head:", r.content[:200])
