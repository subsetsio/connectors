import re
import lxml.html as LH
from subsets_utils import get

BASE = "https://www.olympedia.org"
html = get(BASE + "/editions", timeout=(10.0, 120.0)).text
doc = LH.fromstring(html)

# Walk body in document order, print headings (any h-tag) and table markers
body = doc.body if doc.body is not None else doc
print("=== document-order headings + tables ===")
for el in body.iter():
    tag = el.tag
    if isinstance(tag, str) and re.fullmatch(r"h[1-6]", tag):
        txt = " ".join(t.strip() for t in el.itertext() if t.strip())
        print(f"  <{tag}> {txt!r}")
    elif tag == "table":
        # first edition id + a couple cells
        ids = [h for h in el.xpath('.//a/@href') if re.search(r"/editions/\d+$", h)]
        print(f"  <table> n_edition_ids={len(set(ids))} first={ids[0] if ids else None}")

# countries: inspect a modern row's 3rd cell for img/checkmark
print("=== countries cell3 inspection ===")
chtml = get(BASE + "/countries", timeout=(10.0, 120.0)).text
cdoc = LH.fromstring(chtml)
tbl = cdoc.xpath("//table")[0]
for tr in tbl.xpath(".//tr")[1:4]:
    tds = tr.xpath("./td")
    if len(tds) >= 3:
        c3 = tds[2]
        print("  abbr=", (tds[0].text_content().strip()),
              "имgs=", len(c3.xpath('.//img')),
              "html=", LH.tostring(c3, encoding="unicode").strip()[:120])
