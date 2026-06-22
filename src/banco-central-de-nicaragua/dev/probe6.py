import lxml.html as LH
from subsets_utils import get
BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
for ext in ["htm","xls"]:
  for code in ["4.IMAE"]:
    r=get(f"{BASE}{code}.{ext}", timeout=(10,60))
    h=r.content.decode("iso-8859-1","replace")
    print("="*50,code,ext,"len",len(h),"yrs:",[y for y in ["1994","1995","2010","2020","2024"] if y in h])
    doc=LH.fromstring(h)
    rows=doc.xpath("//table//tr")
    data=[[ (c.text_content() or '').strip() for c in tr.xpath('./td|./th')] for tr in rows]
    data=[r for r in data if any(c for c in r)]
    print("datarows",len(data))
    for row in data[:20]:
        print("  ",[c for c in row if c][:16])
