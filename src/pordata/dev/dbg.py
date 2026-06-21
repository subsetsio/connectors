import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src")); sys.path.insert(0, os.path.dirname(__file__))
from subsets_utils import get
from lxml import html as lh
from parser import _find_data_table, NUM_RE
r = get("https://www.pordata.pt/en/portugal/gross+domestic+product+(gdp)-130", timeout=(10,60))
doc = lh.fromstring(r.text)
t = _find_data_table(doc)
print("table found:", t is not None)
if t is not None:
    print("./tr:", len(t.xpath('./tr')), " ./tbody/tr:", len(t.xpath('./tbody/tr')), " .//tr:", len(t.xpath('.//tr')))
    rows = t.xpath('.//tr')
    for r2 in rows[:3]:
        cells=r2.xpath('./td|./th')
        print("  tags:", [c.tag for c in cells][:6], "txt:", [c.text_content().strip()[:8] for c in cells][:6])
