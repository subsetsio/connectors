import json, csv, io
import xml.etree.ElementTree as ET
from subsets_utils import get
coll = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/ksh/assets/collect/entities/current.json"))

# 1. Show CSV headers across several csv resources (check delimiter/layout variety)
print("=== CSV headers ===")
n=0
for rid,e in coll.items():
    sm=e["source_metadata"]
    if sm["data_format"]!="csv": continue
    r=get(f"https://data.ksh.hu/datasets/{sm['dataset_id']}/data/{rid}.csv", timeout=60)
    first=r.text.splitlines()[0]
    print(rid[:8], "|", first[:130])
    n+=1
    if n>=6: break

# 2. XML obs structure for one resource
print("\n=== XML Series/Obs ===")
for rid,e in coll.items():
    sm=e["source_metadata"]
    if sm["data_format"]!="xml": continue
    r=get(f"https://data.ksh.hu/datasets/{sm['dataset_id']}/data/{rid}.xml", timeout=60)
    root=ET.fromstring(r.text.encode("utf-8"))
    # find DataSet then Series then Obs (namespace-agnostic by localname)
    def ln(t): return t.rsplit('}',1)[-1]
    series=[el for el in root.iter() if ln(el.tag)=="Series"]
    obs=[el for el in root.iter() if ln(el.tag)=="Obs"]
    print("rid",rid[:8],"series",len(series),"obs",len(obs))
    print("series attrib:", dict(series[0].attrib))
    print("obs attrib:", dict(obs[0].attrib))
    break
