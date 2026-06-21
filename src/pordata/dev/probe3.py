import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
from lxml import html as lh
import re

for geo, slug, idn in [("europe","resident+population",1951), ("municipalities","crude+marriage+rate",360)]:
    url = f"https://www.pordata.pt/en/{geo}/{slug}-{idn}"
    r = get(url, timeout=(10,60))
    doc = lh.fromstring(r.text)
    print(f"\n##### {geo}/{idn} len={len(r.text)}")
    tables = doc.xpath("//table")
    print("total <table>:", len(tables))
    for ti,t in enumerate(tables):
        rows = t.xpath(".//tr")
        if len(rows)<3: continue
        # is this inside a script/style?
        anc = {a.tag for a in t.iterancestors()}
        ncol = max((len(rr.xpath('./td|./th')) for rr in rows), default=0)
        digits = len(re.findall(r'\d', t.text_content()))
        hdr = [c.text_content().strip()[:14] for c in rows[0].xpath('./td|./th')][:8]
        print(f"  t[{ti}] rows={len(rows)} cols={ncol} digits={digits} hdr={hdr}")
    # search raw for a country name + number to see if data present
    print("  'Germany' occurrences:", r.text.count("Germany"))
    print("  year 2023 occurrences:", r.text.count("2023"))
