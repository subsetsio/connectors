import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
from lxml import html as lh
import re

CASES = [
    ("europe", "resident+population", 1951),
    ("municipalities", "crude+marriage+rate", 360),
    ("portugal", "gross+domestic+product+(gdp)", 130),
]
def biggest_table(doc):
    tables = doc.xpath("//table")
    cand = [t for t in tables if len(t.xpath('.//tr'))>=2]
    return max(cand, key=lambda t: len(re.findall(r'\d', t.text_content())), default=None)

for geo, slug, idn in CASES:
    url = f"https://www.pordata.pt/en/{geo}/{slug}-{idn}"
    r = get(url, timeout=(10,60))
    doc = lh.fromstring(r.text)
    t = biggest_table(doc)
    print(f"\n=== {geo}/{idn} {url} status={r.status_code}")
    if t is None: 
        print("  no table"); continue
    rows = t.xpath(".//tr")
    print(f"  rows={len(rows)}")
    for r2 in rows[:5]:
        cells = [c.text_content().strip()[:16] for c in r2.xpath("./td|./th")]
        print("   ", cells[:10])
