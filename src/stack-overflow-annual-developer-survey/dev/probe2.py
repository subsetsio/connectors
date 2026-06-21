import io
import pandas as pd
from subsets_utils import get
RAW = "https://github.com/StackExchange/Survey/raw/refs/heads/main/packages/archive"
for year in ("2016","2017","2019","2020","2022","2025"):
    r = get(f"{RAW}/{year}/schema.csv", timeout=(10.0,60.0)); r.raise_for_status()
    df = pd.read_csv(io.BytesIO(r.content), dtype=str, encoding="utf-8-sig", nrows=2)
    print(year, "->", list(df.columns))
