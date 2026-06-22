import lxml.html as LH
from subsets_utils import get
BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
for code in ["1.23.1","Mon_3_60_5_1","4.V.01.01.02","4.ipcn.1","4.IPCM.1","4.E.9","3.8.2"]:
    r=get(BASE+code+".xls", timeout=(10,60))
    h=r.content.decode("iso-8859-1","replace")
    doc=LH.fromstring(h)
    rows=doc.xpath("//table//tr")
    data=[]
    for tr in rows:
        cells=[(c.text_content() or "").strip() for c in tr.xpath("./td|./th")]
        ne=[c for c in cells if c]
        if ne: data.append(cells)
    print("="*50,code,"datarows",len(data))
    for row in data:
        print("   ",[c for c in row if c][:16])
