import io, time, re
import pandas as pd
import lxml.html as LH
from subsets_utils import get

BASE = "https://www.olympedia.org"

def fetch(path):
    r = get(BASE + path, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.text

def show_tables(path, label):
    print("=" * 70); print(label, path)
    html = fetch(path)
    tables = pd.read_html(io.StringIO(html))
    print(f"  #tables={len(tables)}")
    for i, t in enumerate(tables):
        print(f"  table[{i}] shape={t.shape} cols={list(t.columns)}")
        print("   ", t.head(2).to_dict("records"))
    return html

# editions: headings + per-table first-row edition id + country flag
html = fetch("/editions")
doc = LH.fromstring(html)
print("=== EDITIONS structure ===")
for tbl in doc.xpath("//table"):
    # nearest preceding heading
    hs = tbl.xpath("preceding::h1[1]/text() | preceding::h2[1]/text() | preceding::h3[1]/text()")
    rows = tbl.xpath(".//tr")
    first_data = None
    for tr in rows:
        ed = tr.xpath('.//a[contains(@href,"/editions/")]/@href')
        ed = [h for h in ed if re.search(r"/editions/\d+$", h)]
        if ed:
            noc = tr.xpath('.//a[contains(@href,"/countries/")]/@href')
            cells = [c.strip() for c in tr.xpath(".//td//text()") if c.strip()]
            first_data = (ed[0], noc[:2], cells[:6])
            break
    nids = len(set(h for tr in rows for h in tr.xpath('.//a[contains(@href,"/editions/")]/@href') if re.search(r"/editions/\d+$", h)))
    print(f"  heading={hs[-1:] if hs else '?'} rows={len(rows)} uniq_edition_ids={nids} first={first_data}")

time.sleep(3)
show_tables("/statistics/medal/athlete", "MEDALS_BY_ATHLETE")
time.sleep(3)
show_tables("/statistics/participation", "PARTICIPATIONS")
time.sleep(3)
show_tables("/statistics/age", "AGE")
time.sleep(3)
show_tables("/countries", "COUNTRIES")
time.sleep(3)
show_tables("/sports", "SPORTS")
time.sleep(3)
show_tables("/records/sport/ARC", "RECORDS ARCHERY")
