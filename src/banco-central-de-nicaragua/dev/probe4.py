import lxml.html as LH
from subsets_utils import get
BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
r=get(BASE+"4.IMAE.xls", timeout=(10,60))
h=r.content.decode("iso-8859-1","replace")
doc=LH.fromstring(h)
for i,tr in enumerate(doc.xpath("//table//tr")):
    cells=[(c.text_content() or "").strip() for c in tr.xpath("./td|./th")]
    print(i, "ncells=",len(cells), "nonempty=",sum(1 for c in cells if c))
    print("   ", [c for c in cells if c][:20])
