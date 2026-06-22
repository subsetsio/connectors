import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import json
# LAUS data_type distinct
r=get("https://data.ct.gov/resource/nfe2-aprv.json", params={"$select":"distinct data_type"}, timeout=(10,120))
print("LAUS data_type:", r.json())
# QCEW sample with possible commas, and ordering
r=get("https://data.ct.gov/resource/7zu6-8dcr.json", params={"$limit":"3","$order":":id"}, timeout=(10,120))
print("QCEW ordered:", [row.get('anntotalwages') for row in r.json()], "n=",len(r.json()))
# OES check a high-employment area to confirm commas present
r=get("https://data.ct.gov/resource/tids-7w95.json", params={"$limit":"1"}, timeout=(10,120))
print("OES emp sample:", r.json()[0]['employment'], r.json()[0]['meanannualwage'])
# CES current data_type distinct & area count
r=get("https://data.ct.gov/resource/h44w-mqs3.json", params={"$select":"distinct month"}, timeout=(10,120))
print("CES current months:", r.json())
