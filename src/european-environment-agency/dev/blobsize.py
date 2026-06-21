from subsets_utils import get
import urllib.request, json
md=json.loads(urllib.request.urlopen(urllib.request.Request("https://discodata.eea.europa.eu/md",headers={"User-Agent":"x"}),timeout=180).read())
# find AirQualityStatistics blob + a few big ones via HEAD
urls=[]
for db in md:
    for sch in db.get("Schemas",[]):
        if sch["name"]!="latest": continue
        for t in sch.get("Tables",[]):
            u=t.get("datalakeUrl")
            if u: urls.append((f"{db['name']}.{t['name']}", u))
print("total blob urls:", len(urls))
import subsets_utils
for name in ["AirQualityDataFlows.AirQualityStatistics","AirQualityDataFlows.Measurements"]:
    for n,u in urls:
        if n==name:
            r=get(u, headers={"Range":"bytes=0-0"}, timeout=(10,60))
            print(name, "status", r.status_code, "content-range", r.headers.get("content-range"), "full-len", r.headers.get("content-length"))
