import sys, os, json; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
from lxml import html as lh
import re
cases = json.load(open("/tmp/probe_cases.json"))
emap = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/pordata/assets/collect/indicators/current.json"))
for eid, slug, idn in cases:
    geo = eid.rsplit("-",1)[0]
    geoseg = {"portugal":"portugal","europe":"europe","municipalities":"municipalities"}[geo]
    url = f"https://www.pordata.pt/en/{geoseg}/{slug}-{idn}"
    try:
        r = get(url, timeout=(10,60))
    except Exception as ex:
        print(eid, "ERR", ex); continue
    h=r.text
    doc=lh.fromstring(h)
    # find a data table: a <table> whose first row header contains 'Years' or has many numeric rows
    best=None; bestrows=0
    for t in doc.xpath("//table"):
        rows=t.xpath(".//tr")
        digits=len(re.findall(r"\d",t.text_content()))
        if len(rows)>=5 and digits>50 and len(rows)>bestrows:
            # ensure not script
            if any(a.tag in ("script","style") for a in t.iterancestors()): continue
            best=t; bestrows=len(rows)
    hdr=""
    if best is not None:
        r0=best.xpath(".//tr")[0]
        hdr=[c.text_content().strip()[:12] for c in r0.xpath("./td|./th")][:6]
    print(f"{eid:22} status={r.status_code} inline_table_rows={bestrows} ValueCell={h.count('ValueCell')} hdr={hdr}")
