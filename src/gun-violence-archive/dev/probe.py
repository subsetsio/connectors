import re
import pandas as pd
from subsets_utils import get

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
BASE = "https://www.gunviolencearchive.org"
H = {"User-Agent": UA}

slug = "accidental-child-deaths"  # small report
html = get(f"{BASE}/{slug}", headers=H, timeout=30).text
uuid = re.search(r"query/([a-f0-9-]{36})", html).group(1)
print("uuid:", uuid)

def page(n):
    r = get(f"{BASE}/query/{uuid}/export-api", params={"page": n}, headers=H, timeout=30)
    return r

for n in [0, 1, 200]:
    r = page(n)
    tables = pd.read_html(r.text)
    # find the data table (has 'Incident ID' col)
    dt = None
    for t in tables:
        cols = [str(c) for c in t.columns]
        if any("Incident ID" in c for c in cols):
            dt = t
            break
    print(f"--- page {n}: status={r.status_code}, #tables={len(tables)}, datatable_rows={0 if dt is None else len(dt)}")
    if n == 0 and dt is not None:
        print("cols:", list(dt.columns))
        print(dt.head(3).to_dict("records"))
