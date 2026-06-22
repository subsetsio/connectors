import io
import pandas as pd
from subsets_utils import get

DIRECT = "https://www.aaii.com/files/surveys/sentiment.xls"
WB_API = "http://archive.org/wayback/available?url=aaii.com/files/surveys/sentiment.xls"


def try_direct():
    try:
        r = get(DIRECT, timeout=(10.0, 60.0))
        print("DIRECT status", r.status_code, "len", len(r.content), "ctype", r.headers.get("content-type"))
        if r.status_code == 200 and b"Incapsula" not in r.content[:2000]:
            return r.content
    except Exception as e:
        print("DIRECT err", type(e).__name__, e)
    return None


def try_wayback():
    r = get(WB_API, timeout=(10.0, 60.0))
    j = r.json()
    snap = j["archived_snapshots"]["closest"]
    print("WB snapshot", snap["timestamp"], snap["status"], snap["url"])
    ts = snap["timestamp"]
    raw_url = f"https://web.archive.org/web/{ts}id_/https://www.aaii.com/files/surveys/sentiment.xls"
    r2 = get(raw_url, timeout=(10.0, 120.0))
    print("WB raw status", r2.status_code, "len", len(r2.content), "ctype", r2.headers.get("content-type"))
    return r2.content


content = try_direct() or try_wayback()
print("got bytes:", len(content), "magic:", content[:8])

df = pd.read_excel(io.BytesIO(content), sheet_name="SENTIMENT", header=3, skiprows=[4], engine="xlrd")
print("raw cols:", list(df.columns))
d = pd.to_datetime(df.iloc[:, 0], errors="coerce")
valid = df[d.notna()].copy()
print("valid weekly rows:", len(valid))
print("date span:", d.dropna().min(), "->", d.dropna().max())
print(valid.head(3).iloc[:, :8].to_string())
print(valid.tail(2).iloc[:, :8].to_string())
print("dtypes:", list(zip(df.columns[:14], [str(t) for t in df.dtypes[:14]])))
