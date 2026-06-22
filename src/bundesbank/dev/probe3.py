import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get, get_client
import xml.etree.ElementTree as ET
NS={"s":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure"}

# 1) dataflow def for BBBK7 -> structure ref
r=get("https://api.statistiken.bundesbank.de/rest/metadata/dataflow/BBK/BBBK7?references=all",
      headers={"Accept":"application/xml"}, timeout=(15,120))
print("dataflow status", r.status_code, "len", len(r.content))
if r.status_code==200:
    root=ET.fromstring(r.content)
    for df in root.iterfind(".//s:Dataflow", NS):
        print("dataflow id", df.get("id"))
        ref=df.find(".//s:Structure/Ref", NS)
        if ref is not None: print("  structure ref id=",ref.get("id"))
    print("DIMENSIONS:")
    for d in root.iterfind(".//s:DataStructure//s:DimensionList/s:Dimension", NS):
        cl=d.find(".//s:Enumeration/Ref", NS)
        print("  pos",d.get("position"),"id",d.get("id"),"codelist",cl.get("id") if cl is not None else None)

# 2) try a tiny slice: lastNObservations=1 to see headers / size and the BBK_ID keys
print("\n--- lastNObservations=1 probe ---")
client=get_client()
SDMX_CSV="application/vnd.sdmx.data+csv;version=1.0.0"
with client.stream("GET","https://api.statistiken.bundesbank.de/rest/data/BBBK7?lastNObservations=1",
                   headers={"Accept":SDMX_CSV}, timeout=(15,300)) as resp:
    print("status",resp.status_code)
    n=0; keys=set(); freqs=set()
    hdr=None
    for line in resp.iter_lines():
        if hdr is None:
            hdr=line.lstrip("﻿").split(";"); 
            idx={c:i for i,c in enumerate(hdr)}
            continue
        f=line.split(";"); n+=1
        keys.add(f[idx["BBK_ID"]].split(".")[0])
        if "BBK_STD_FREQ" in idx: freqs.add(f[idx["BBK_STD_FREQ"]])
    print("rows(series count approx)",n,"flow-prefixes",keys,"freqs",freqs)
