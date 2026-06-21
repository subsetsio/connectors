import io, time, tempfile, os
import pyarrow.csv as pacsv
import duckdb
from subsets_utils import get

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
SLUG = "ai-training-computation-vs-parameters-by-domain"

def fetch(slug, tries=10):
    url = f"https://ourworldindata.org/grapher/{slug}.csv"
    for i in range(tries):
        r = get(url, params={"csvType": "full", "useColumnShortNames": "true"},
                headers={"User-Agent": UA}, timeout=(10.0, 180.0))
        if r.status_code == 200:
            return r.content
        time.sleep(3 * (i + 1))
    return None

c = fetch(SLUG)
print("bytes", len(c))
# show a window around a newline-in-quote
txt = c.decode("utf-8","replace")
print("---- raw head ----")
print(txt[:400])
print("---- does it contain quoted multiline? count of dquotes:", txt.count('"'))

print("\n== pyarrow newlines_in_values=True ==")
try:
    t = pacsv.read_csv(io.BytesIO(c), parse_options=pacsv.ParseOptions(newlines_in_values=True))
    print("OK", t.num_rows, t.column_names)
except Exception as e:
    print("FAIL", str(e)[:160])

print("\n== duckdb explicit delim/quote ==")
fd, path = tempfile.mkstemp(suffix=".csv"); os.write(fd, c); os.close(fd)
try:
    t = duckdb.connect().execute(
        f"SELECT * FROM read_csv('{path}', delim=',', quote='\"', escape='\"', header=true, sample_size=-1)"
    ).to_arrow_table()
    print("OK", t.num_rows, t.column_names)
    print("schema", [(f.name, str(f.type)) for f in t.schema])
finally:
    os.remove(path)
