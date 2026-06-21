import json
from subsets_utils import post, get

# size of the failed table + a few accepted ones
for pid in [10100005, 10100002, 10100004, 10100006]:
    r = post("https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata",
             json=[{"productId": pid}], timeout=(10,60))
    j = r.json()[0]
    o = j.get("object", {})
    print(pid, "status", j.get("status"),
          "nbSeries", o.get("nbSeriesCube"), "nbDatapoints", o.get("nbDatapointsCube"),
          "| title:", (o.get("cubeTitleEn") or "")[:50])
