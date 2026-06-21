import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
from lxml import html as lh
import re
from lxml import etree

def data_table(doc):
    best=None;bd=0
    for t in doc.xpath("//table"):
        if any(a.tag in ("script","style") for a in t.iterancestors()): continue
        rows=t.xpath(".//tr")
        d=len(re.findall(r"\d",t.text_content()))
        if len(rows)>=5 and d>bd: best=t;bd=d
    return best

for geo,slug,idn,label in [("portugal","resident+population+total+and+by+age+group",10,"2lvl-header"),
                           ("portugal","gross+domestic+product+(gdp)",130,"1lvl-header"),
                           ("portugal","unemployment+rate+total+and+by+sex+(percentage)",550,"pct")]:
    url=f"https://www.pordata.pt/en/{geo}/{slug}-{idn}"
    r=get(url,timeout=(10,60)); doc=lh.fromstring(r.text)
    t=data_table(doc)
    print(f"\n##### {label} {idn}  url={url}")
    rows=t.xpath("./tr") or t.xpath(".//tr")
    print("total tr:", len(rows))
    for i,row in enumerate(rows[:4]):
        cells=row.xpath("./td|./th")
        desc=[(c.tag, c.get('colspan'), c.text_content().strip()[:14]) for c in cells[:8]]
        print(f"  r{i}:", desc)
    # last data row
    lr=rows[-1]; cells=lr.xpath("./td|./th")
    print("  LAST:", [(c.tag, c.text_content().strip()[:12]) for c in cells[:6]])
