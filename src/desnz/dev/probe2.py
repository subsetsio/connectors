import io, pandas as pd
from subsets_utils import get
BASE="https://ckan.publishing.service.gov.uk/api/3/action"
p=get(f"{BASE}/package_show",params={"id":"21db6396-3daf-4d90-8b3f-054995256018"},timeout=(10,120)).json()["result"]
url=[r for r in p["resources"] if (r.get("format") or "").lower().lstrip(".")=="xlsx"][0]["url"]
b=get(url,timeout=(10,180)).content
df=pd.read_excel(io.BytesIO(b),sheet_name="Data",header=None,nrows=10)
print("Data sheet head:"); print(df.to_string(max_cols=10))
print("full Data shape:", pd.read_excel(io.BytesIO(b),sheet_name="Data",header=None).shape)
# a csv
import csv
cb=get("https://assets.publishing.service.gov.uk/media/6448e77a529eda00123b049a/ambient-gamma-dose-rates-mobile-rrems-monitors-jan-2023.csv",timeout=(10,120)).content
print("csv head:"); print(cb[:400])
