import lxml.html as LH
from subsets_utils import get
BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
for code in ["4.IMAE","1.1","1a.2.1.04"]:
    r=get(BASE+code+".xls", timeout=(10,60))
    html=r.content.decode("iso-8859-1","replace")
    doc=LH.fromstring(html)
    rows=doc.xpath("//table//tr")
    print("="*60, code, "rows:", len(rows))
    grid=[]
    for tr in rows:
        cells=[ (c.text_content() or "").strip() for c in tr.xpath("./td|./th")]
        grid.append(cells)
    for i,row in enumerate(grid):
        # compress
        nonempty=[c for c in row if c]
        if nonempty:
            print(i, "|".join(row)[:160])
