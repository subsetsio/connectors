import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
from lxml import html as lh
import re

CASES = [
    ("portugal", "resident+population+total+and+by+age+group", 10),
    ("europe", "resident+population-1951", None),  # slug already has id? handle below
    ("municipalities", "nights+spent+in+tourist+accommodations+total+and+by+type+of+establishment", 748),
]

def fetch(geo, slug, idn):
    url = f"https://www.pordata.pt/en/{geo}/{slug}-{idn}"
    r = get(url, timeout=(10,60))
    print("URL", url, "->", r.status_code, "len", len(r.text))
    doc = lh.fromstring(r.text)
    tables = doc.xpath("//table")
    print("  #tables:", len(tables))
    for ti, t in enumerate(tables):
        rows = t.xpath(".//tr")
        if len(rows) < 2: continue
        ncol = max((len(r.xpath("./td|./th")) for r in rows), default=0)
        # heuristic: data table has many rows & numeric cells
        txt = t.text_content()
        nums = len(re.findall(r"\d", txt))
        print(f"  table[{ti}] rows={len(rows)} maxcols={ncol} digits={nums}")
    return doc

for geo, slug, idn in CASES[:1]:
    doc = fetch(geo, slug, idn)
    # dump biggest table header + first rows
    tables = doc.xpath("//table")
    best = max(tables, key=lambda t: len(t.text_content()))
    rows = best.xpath(".//tr")
    print("=== BEST TABLE first 4 rows ===")
    for r in rows[:4]:
        cells = [c.text_content().strip()[:20] for c in r.xpath("./td|./th")]
        print("  ", cells[:12])
