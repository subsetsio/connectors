import time
from subsets_utils import get, configure_http, transient_retry
from lxml import html as lh

configure_http(headers={"User-Agent": "subsets.io-connector/1.0 (+https://subsets.io)"})


@transient_retry(attempts=6, min_wait=2, max_wait=30)
def fetch(url):
    r = get(url, timeout=(30.0, 120.0))
    r.raise_for_status()
    return r.text


for cat in ["content_management", "server_location", "ssl_certificate"]:
    url = f"https://w3techs.com/technologies/history_overview/{cat}/ms/y"
    text = fetch(url)
    doc = lh.fromstring(text)
    tables = doc.xpath("//table")
    print(f"\n##### {cat}: {len(tables)} tables")
    for t in tables:
        rows = t.xpath("./tr") or t.xpath("./tbody/tr")
        if not rows:
            continue
        first = rows[0]
        head_cells = [c.text_content().strip() for c in first.xpath("./td|./th")]
        datarows = [row for row in rows if row.xpath("./th") and row.xpath("./td")]
        if len(datarows) >= 3 and len(head_cells) >= 5:
            print("  HEADER cells:", head_cells)
            for row in datarows[:4]:
                th = row.xpath("./th")[0].text_content().strip()
                tds = [c.text_content().strip() for c in row.xpath("./td")]
                print(f"   ROW {th!r}: {tds}")
            print("  total datarows:", len(datarows))
            break
    time.sleep(2)
