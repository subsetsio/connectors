import io, time, tempfile, os
import pyarrow.csv as pacsv
import duckdb
from subsets_utils import get

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def fetch(slug, tries=10):
    url = f"https://ourworldindata.org/grapher/{slug}.csv"
    for i in range(tries):
        r = get(url, params={"csvType": "full", "useColumnShortNames": "true"},
                headers={"User-Agent": UA}, timeout=(10.0, 180.0))
        if r.status_code == 200:
            return r.content
        time.sleep(3 * (i + 1))
    return None

# problem chart + a couple normal ones to make sure the robust path doesn't regress
SLUGS = ["ai-training-computation-vs-parameters-by-domain", "life-expectancy", "political-regime-polity"]

def pyarrow_robust(content):
    def skip(row):
        return "skip"
    opts = pacsv.ParseOptions(newlines_in_values=True, invalid_row_handler=skip)
    return pacsv.read_csv(io.BytesIO(content), parse_options=opts)

def duckdb_robust(content):
    fd, path = tempfile.mkstemp(suffix=".csv"); os.write(fd, content); os.close(fd)
    try:
        return duckdb.connect().execute(
            f"SELECT * FROM read_csv('{path}', auto_detect=true, header=true, "
            f"ignore_errors=true, strict_mode=false, sample_size=-1)"
        ).to_arrow_table()
    finally:
        os.remove(path)

for slug in SLUGS:
    print("==", slug)
    c = fetch(slug)
    if not c:
        print("  fetch failed"); continue
    try:
        t = pyarrow_robust(c)
        print("  pyarrow_robust OK", t.num_rows, t.column_names)
    except Exception as e:
        print("  pyarrow_robust FAIL", str(e)[:140])
    try:
        t = duckdb_robust(c)
        print("  duckdb_robust  OK", t.num_rows, t.column_names[:6])
    except Exception as e:
        print("  duckdb_robust  FAIL", type(e).__name__, str(e)[:140])
