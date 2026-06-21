import pandas as pd
from io import StringIO
from subsets_utils import get

# parks.json shape
r = get("https://queue-times.com/parks.json", timeout=30)
groups = r.json()
parks = [p for g in groups for p in g.get("parks", [])]
print("companies:", len(groups), "parks:", len(parks))
print("sample park:", parks[0])

# attendance page for Disneyland (id 16)
for pid in [16, 57, 999]:
    resp = get(f"https://queue-times.com/parks/{pid}/attendances", timeout=30)
    print(f"\n--- park {pid}: HTTP {resp.status_code} ---")
    if resp.status_code != 200:
        continue
    tables = pd.read_html(StringIO(resp.text))
    print("num tables:", len(tables))
    df = tables[0]
    print("cols:", list(df.columns))
    print(df.head(4).to_string())
    print("dtypes:", dict(df.dtypes.astype(str)))
