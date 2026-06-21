import io, time, tempfile, os
import pyarrow.csv as pacsv
import duckdb
from subsets_utils import get

SLUGS = [
    "ai-training-computation-vs-parameters-by-domain",
    "life-expectancy",
]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def fetch(slug, tries=8):
    url = f"https://ourworldindata.org/grapher/{slug}.csv"
    for i in range(tries):
        r = get(url, params={"csvType": "full", "useColumnShortNames": "true"},
                headers={"User-Agent": UA}, timeout=(10.0, 180.0))
        if r.status_code == 200:
            return r.content
        print(f"  try {i}: {r.status_code} ({len(r.content)}b)")
        time.sleep(3 * (i + 1))
    return None

def parse_duckdb(content):
    con = duckdb.connect()
    fd, path = tempfile.mkstemp(suffix=".csv"); os.write(fd, content); os.close(fd)
    try:
        t = con.execute(f"SELECT * FROM read_csv_auto('{path}', sample_size=-1)").fetch_arrow_table()
        return t
    finally:
        os.remove(path)

for slug in SLUGS:
    print("==", slug)
    c = fetch(slug)
    if not c:
        print("  could not fetch 200"); continue
    print("  bytes", len(c))
    try:
        t = pacsv.read_csv(io.BytesIO(c))
        print("  pyarrow OK", t.num_rows, t.column_names)
    except Exception as e:
        print("  pyarrow FAIL:", str(e)[:160])
    try:
        t = parse_duckdb(c)
        print("  duckdb OK", t.num_rows, t.column_names)
        print("  duckdb schema:", [(f.name, str(f.type)) for f in t.schema])
    except Exception as e:
        print("  duckdb FAIL:", type(e).__name__, str(e)[:160])
