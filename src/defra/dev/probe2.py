import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
r = get("https://environment.data.gov.uk/flood-monitoring/id/stations.json", params={"_limit":1}, timeout=(10,60))
print("status", r.status_code, "ctype", r.headers.get("content-type"))
print("item0 keys", sorted(r.json()["items"][0].keys()))
r2 = get("https://environment.data.gov.uk/flood-monitoring/data/readings.json?latest", timeout=(10,90))
js = r2.json(); print("latest n", len(js["items"]), "sample", js["items"][0])
