import io
import pandas as pd
from subsets_utils import get

RAW = "https://github.com/StackExchange/Survey/raw/refs/heads/main/packages/archive"

# results.csv for a recent and an old year
for year in ("2011", "2024"):
    r = get(f"{RAW}/{year}/results.csv", timeout=(10.0, 180.0))
    r.raise_for_status()
    content = r.content
    df = pd.read_csv(io.BytesIO(content), dtype=str, encoding="utf-8-sig", nrows=5)
    print(f"=== results {year}: {len(content)} bytes, {df.shape[1]} cols ===")
    print("first cols:", list(df.columns[:8]))
    print("sample row0 (first 4 cols):", {c: df.iloc[0][c] for c in df.columns[:4]})

# schema.csv structure
r = get(f"{RAW}/2024/schema.csv", timeout=(10.0, 60.0))
r.raise_for_status()
sdf = pd.read_csv(io.BytesIO(r.content), dtype=str, encoding="utf-8-sig")
print("=== schema 2024 ===")
print("cols:", list(sdf.columns))
print("nrows:", len(sdf))
print(sdf.head(3).to_dict("records"))
