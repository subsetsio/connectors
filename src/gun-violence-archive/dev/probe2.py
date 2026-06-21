import io
import re
import pandas as pd
from subsets_utils import get

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
BASE = "https://www.gunviolencearchive.org"
H = {"User-Agent": UA}

slug = "accidental-child-deaths"
html = get(f"{BASE}/{slug}", headers=H, timeout=30).text
uuid = re.search(r"query/([a-f0-9-]{36})", html).group(1)

def rows(n):
    r = get(f"{BASE}/query/{uuid}/export-api", params={"page": n}, headers=H, timeout=30)
    tables = pd.read_html(io.StringIO(r.text))
    for t in tables:
        if any("Incident ID" in str(c) for c in t.columns):
            return t
    return None

for n in [199, 200, 201, 202, 205, 300]:
    t = rows(n)
    if t is None or len(t) == 0:
        print(f"page {n}: 0 rows")
    else:
        ids = list(t["Incident ID"])
        print(f"page {n}: {len(t)} rows, first_id={ids[0]}, last_id={ids[-1]}")
