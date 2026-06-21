import json
from subsets_utils import get

coll = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/ksh/assets/collect/entities/current.json"))
# pick one csv and one xml resource
csv_r=xml_r=None
for rid,e in coll.items():
    sm=e["source_metadata"]
    if sm["data_format"]=="csv" and not csv_r: csv_r=(rid,sm["dataset_id"])
    if sm["data_format"]=="xml" and not xml_r: xml_r=(rid,sm["dataset_id"])
print("csv:",csv_r,"\nxml:",xml_r)

rid,did=csv_r
r=get(f"https://data.ksh.hu/datasets/{did}/data/{rid}.csv", timeout=60)
print("\n=== CSV status",r.status_code, "len",len(r.text))
print(r.text.splitlines()[0])
print(r.text.splitlines()[1])

rid,did=xml_r
r=get(f"https://data.ksh.hu/datasets/{did}/data/{rid}.xml", timeout=60)
print("\n=== XML status",r.status_code,"len",len(r.text))
print(r.text[:1500])
# does csv work for the xml resource?
r2=get(f"https://data.ksh.hu/datasets/{did}/data/{rid}.csv", timeout=60)
print("\n=== xml-resource as .csv status", r2.status_code, "len", len(r2.text), "ctype", r2.headers.get("content-type"))
