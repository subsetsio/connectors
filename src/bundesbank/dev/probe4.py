import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get, get_client
import xml.etree.ElementTree as ET
NS={"s":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure"}
SDMX_CSV="application/vnd.sdmx.data+csv;version=1.0.0"

r=get("https://api.statistiken.bundesbank.de/rest/metadata/datastructure/BBK/BBK_BSBBK7?references=children",
      headers={"Accept":"application/xml"}, timeout=(15,120))
print("dsd status",r.status_code,"len",len(r.content))
root=ET.fromstring(r.content)
# count codes per codelist
clsizes={}
for cl in root.iterfind(".//s:Codelist", NS):
    clsizes[cl.get("id")]=sum(1 for _ in cl.iterfind("s:Code",NS))
dims=[]
for d in root.iterfind(".//s:DimensionList/s:Dimension", NS):
    cl=d.find(".//s:Enumeration/Ref", NS)
    clid=cl.get("id") if cl is not None else None
    dims.append((int(d.get("position")), d.get("id"), clid, clsizes.get(clid)))
for p,did,clid,n in sorted(dims):
    print(f"pos={p} id={did} codelist={clid} ncodes={n}")

# try splitting by first dimension code: key = CODE.... (pos1)
first=sorted(dims)[0]
print("\nfirst dim:",first)
# get its codes
codes=[]
for cl in root.iterfind(".//s:Codelist", NS):
    if cl.get("id")==first[2]:
        codes=[c.get("id") for c in cl.iterfind("s:Code",NS)]
print("first dim codes:",codes[:20], "..." if len(codes)>20 else "")
ndim=len(dims)
# probe one code, lastNObs=1
if codes:
    key=".".join([codes[0]]+[""]*(ndim-1))
    client=get_client()
    url=f"https://api.statistiken.bundesbank.de/rest/data/BBBK7/{key}?lastNObservations=1"
    with client.stream("GET",url,headers={"Accept":SDMX_CSV},timeout=(15,300)) as resp:
        print(f"\nsplit-by-pos1 code={codes[0]} key={key} status={resp.status_code}")
        if resp.status_code==200:
            n=sum(1 for _ in resp.iter_lines())-1
            print("  rows",n)
