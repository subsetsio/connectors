from subsets_utils import get, configure_http
from lxml import html as lh

configure_http(headers={"User-Agent": "subsets.io-connector/1.0 (+https://subsets.io)"})

for cat in ["content_management", "server_location", "ssl_certificate"]:
    url = f"https://w3techs.com/technologies/history_overview/{cat}/ms/y"
    r = get(url, timeout=(10.0, 120.0))
    doc = lh.fromstring(r.text)
    # The data table: find table whose first row has many <td> year headers.
    tables = doc.xpath("//table")
    print(f"\n##### {cat}: {len(tables)} tables, status {r.status_code}")
    # Heuristic: the data table rows start with <th> tech name then <td> percents.
    for t in tables:
        rows = t.xpath("./tr") or t.xpath("./tbody/tr")
        if not rows:
            continue
        # header row: first row, collect <td> text
        first = rows[0]
        head_cells = [c.text_content().strip() for c in first.xpath("./td|./th")]
        # data rows: rows with a leading <th>
        datarows = [row for row in rows if row.xpath("./th") and row.xpath("./td")]
        if len(datarows) >= 3 and len(head_cells) >= 5:
            print("  HEADER cells:", head_cells)
            for row in datarows[:3]:
                th = row.xpath("./th")[0].text_content().strip()
                tds = [c.text_content().strip() for c in row.xpath("./td")]
                print(f"   ROW {th!r}: {tds}")
            print("  total datarows:", len(datarows))
            break
