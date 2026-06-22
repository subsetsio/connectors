import lxml.html
from subsets_utils import get

def show(label, url):
    print("=" * 70)
    print(f"{label}: {url}")
    r = get(url, timeout=(10.0, 60.0))
    print("status", r.status_code, "len", len(r.text))
    doc = lxml.html.fromstring(r.text)
    # find date-nav links pointing at chart urls
    links = [a.get("href") for a in doc.xpath("//a[@href]") if a.get("href") and "chart" in a.get("href")]
    print("chart links sample:", sorted(set(links))[:8])
    for ti, t in enumerate(doc.xpath("//table")):
        rows = t.xpath(".//tr")
        if len(rows) < 2:
            continue
        headers = [c.text_content().strip() for c in rows[0].xpath("./th|./td")]
        print(f"  table[{ti}] rows={len(rows)} headers={headers}")
        for dr in rows[1:3]:
            print("     data:", [c.text_content().strip() for c in dr.xpath('./td|./th')])
        break

show("weekly-landing", "https://www.the-numbers.com/weekly-box-office-chart")
show("budgets/all/1", "https://www.the-numbers.com/movie/budgets/all/1")
show("budgets/all", "https://www.the-numbers.com/movie/budgets/all")
