import json
from subsets_utils import get
d = get("https://data.financialresearch.gov/v1/series/dataset/?dataset=FNYR", timeout=(10,120)).json()
m = d["timeseries"]["FNYR-BGCR-A"]["metadata"]
print("description:", json.dumps(m.get("description"), default=str))
print("schedule:", json.dumps(m.get("schedule"), default=str))
print("unit:", json.dumps(m.get("unit"), default=str))
print("release:", json.dumps(m.get("release"), default=str)[:300])
