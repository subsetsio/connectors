from subsets_utils import get
import xml.etree.ElementTree as ET
NS={"s":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure"}
r=get("https://api.statistiken.bundesbank.de/rest/metadata/datastructure/BBK/BBK_RTD1?references=children", timeout=(15,120))
print("status", r.status_code, "len", len(r.content))
root=ET.fromstring(r.content)
print("=== Dimensions (in order) ===")
for dim in root.iterfind(".//s:DimensionList/s:Dimension", NS):
    rid=dim.get("id"); pos=dim.get("position")
    ref=dim.find("s:LocalRepresentation/s:Enumeration/Ref", NS)
    cl=ref.get("id") if ref is not None else None
    print(f"  pos={pos} id={rid} codelist={cl}")
print("=== Codelists & sizes ===")
for cl in root.iterfind(".//s:Codelist", NS):
    codes=cl.findall("s:Code", NS)
    print(f"  {cl.get('id')}: {len(codes)} codes; sample={[c.get('id') for c in codes[:8]]}")
