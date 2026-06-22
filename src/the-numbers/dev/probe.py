import lxml.html
from subsets_utils import get

PAGES = {
    "daily": "https://www.the-numbers.com/box-office-chart/daily/2026/06/19",
    "weekend": "https://www.the-numbers.com/box-office-chart/weekend/2026/06/12",
    "weekly": "https://www.the-numbers.com/box-office-chart/weekly/2026/06/08",
    "annual": "https://www.the-numbers.com/market/2025/top-grossing-movies",
    "budgets": "https://www.the-numbers.com/movie/budgets/all",
}

for label, url in PAGES.items():
    print("=" * 70)
    print(f"{label}: {url}")
    try:
        r = get(url, timeout=(10.0, 60.0))
        print("status", r.status_code, "len", len(r.text))
        if r.status_code != 200:
            continue
        doc = lxml.html.fromstring(r.text)
        tables = doc.xpath("//table")
        print(f"# tables: {len(tables)}")
        for ti, t in enumerate(tables):
            rows = t.xpath(".//tr")
            if len(rows) < 2:
                continue
            # header
            head = rows[0]
            headers = [c.text_content().strip() for c in head.xpath("./th|./td")]
            print(f"  table[{ti}] rows={len(rows)} headers={headers}")
            # first 2 data rows
            for dr in rows[1:3]:
                cells = [c.text_content().strip() for c in dr.xpath("./td|./th")]
                print(f"     data: {cells}")
            break  # only first meaningful table per page
    except Exception as e:
        print("ERR", type(e).__name__, e)
