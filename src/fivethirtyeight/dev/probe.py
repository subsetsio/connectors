import io
import pyarrow.csv as pacsv
from subsets_utils import get

# Probe a couple of representative CSVs (uppercase/underscore path + a normal one)
for path in ["airline-safety/airline-safety.csv", "births/US_births_2000-2014_SSA.csv", "polls/president_polls.csv"]:
    url = f"https://raw.githubusercontent.com/fivethirtyeight/data/master/{path}"
    r = get(url, timeout=(10.0, 120.0))
    print("===", path, r.status_code, len(r.content), "bytes")
    try:
        t = pacsv.read_csv(io.BytesIO(r.content))
        print("  rows", t.num_rows, "cols", t.num_columns)
        print("  schema:", [(f.name, str(f.type)) for f in t.schema][:8])
    except Exception as e:
        print("  PARSE ERROR:", type(e).__name__, e)
