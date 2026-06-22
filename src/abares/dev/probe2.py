import io
from subsets_utils import get, transient_retry, is_transient
import httpx, pandas as pd

@transient_retry(attempts=5)
def dl(url):
    r = get(url, timeout=(15,180))
    r.raise_for_status()
    return r.content

urls = {
 "forests_csv":"https://data.gov.au/data/dataset/c426860e-9b55-404e-9892-e975794018d5/resource/849a0d00-577a-4eb2-b77f-4d63264201ae/download/aus_for23_attributes.csv",
}
print("ReadError transient?", is_transient(httpx.ReadError("x")))
for k,u in urls.items():
    try:
        c = dl(u)
        print(k, "OK bytes", len(c))
        df=pd.read_csv(io.BytesIO(c), dtype=str, nrows=3)
        print("  cols:", list(df.columns)[:6])
    except Exception as e:
        print(k, "FAIL", type(e).__name__, str(e)[:100])
