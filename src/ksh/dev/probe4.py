import json, re
from subsets_utils import get
coll = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/ksh/assets/collect/entities/current.json"))
sm=coll["0fadb463-4f83-4631-b791-71dc07af9bb3"]["source_metadata"]
did=sm["dataset_id"]; print("dataset",did, sm["dataset_title_en"])
rdf=get(f"https://data.ksh.hu/datasets/{did}/metadata.rdf", timeout=60).text
for m in re.findall(r"/datasets/[^/]+/data/([0-9a-f-]+)\.([a-z]+)", rdf):
    print("dist:", m)
# try xlsx for the resource
for ext in ("csv","xml","xlsx"):
    r=get(f"https://data.ksh.hu/datasets/{did}/data/0fadb463-4f83-4631-b791-71dc07af9bb3.{ext}", timeout=60)
    print(ext, r.status_code, r.headers.get("content-type","")[:25])
