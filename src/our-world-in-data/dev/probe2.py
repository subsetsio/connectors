import io
import pyarrow.csv as pacsv
import duckdb
from subsets_utils import get

SLUG = "ai-training-computation-vs-parameters-by-domain"
url = f"https://ourworldindata.org/grapher/{SLUG}.csv"
r = get(url, params={"csvType": "full", "useColumnShortNames": "true"}, timeout=(10.0, 120.0))
print("status", r.status_code, "bytes", len(r.content))
print("---- first 600 bytes ----")
print(r.content[:600].decode("utf-8", "replace"))

print("\n---- pyarrow default ----")
try:
    t = pacsv.read_csv(io.BytesIO(r.content))
    print("ok", t.num_rows, t.column_names)
except Exception as e:
    print("FAIL:", type(e).__name__, str(e)[:200])

print("\n---- pyarrow newlines_in_values=True ----")
try:
    t = pacsv.read_csv(
        io.BytesIO(r.content),
        parse_options=pacsv.ParseOptions(newlines_in_values=True),
    )
    print("ok", t.num_rows, t.column_names)
except Exception as e:
    print("FAIL:", type(e).__name__, str(e)[:200])

print("\n---- duckdb read_csv_auto ----")
try:
    con = duckdb.connect()
    con.execute("CREATE TABLE t AS SELECT * FROM read_csv_auto(?, all_varchar=false)", [_p := "/tmp/owid_probe.csv"]) if False else None
    # write to temp then read
    with open("/tmp/owid_probe.csv", "wb") as f:
        f.write(r.content)
    t = con.execute("SELECT * FROM read_csv_auto('/tmp/owid_probe.csv')").arrow()
    print("ok", t.num_rows, t.column_names)
    print("schema:", t.schema)
except Exception as e:
    print("FAIL:", type(e).__name__, str(e)[:200])
