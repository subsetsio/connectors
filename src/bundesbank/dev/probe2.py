import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import xml.etree.ElementTree as ET

NS = {
  "s":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
}
# datastructure for BBBK7
r = get("https://api.statistiken.bundesbank.de/rest/metadata/datastructure/BBK/BBBK7",
        headers={"Accept":"application/xml"}, timeout=(15,120))
print("dsd status", r.status_code, "len", len(r.content))
root = ET.fromstring(r.content)
dims = root.iterfind(".//s:DimensionList/s:Dimension", NS)
print("DIMENSIONS (in order):")
for d in root.iterfind(".//s:DimensionList/s:Dimension", NS):
    did = d.get("id"); pos = d.get("position")
    cl = d.find(".//s:Enumeration/Ref", NS) or d.find(".//s:LocalRepresentation/s:Enumeration/Ref", NS)
    clid = cl.get("id") if cl is not None else None
    print(f"  pos={pos} id={did} codelist={clid}")
