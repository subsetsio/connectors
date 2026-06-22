import lxml.html
from subsets_utils import get

# Inspect homepage nav for budget/finance links
r = get("https://www.the-numbers.com/", timeout=(10.0, 60.0))
doc = lxml.html.fromstring(r.text)
links = sorted(set(a.get("href") for a in doc.xpath("//a[@href]") if a.get("href")))
for l in links:
    if any(k in l.lower() for k in ("budget", "financ", "market", "record", "gross", "chart")):
        print("NAV:", l)

print("-" * 60)
for cand in [
    "https://www.the-numbers.com/movie/budgets",
    "https://www.the-numbers.com/movie/production-budgets",
    "https://www.the-numbers.com/movies/production-budgets",
    "https://www.the-numbers.com/movie/budgets/all-time",
    "https://www.the-numbers.com/box-office-records/worldwide/all-movies/production-budgets",
    "https://www.the-numbers.com/financials/most-expensive-movies",
    "https://www.the-numbers.com/movie/budgets/most-expensive",
]:
    try:
        rr = get(cand, timeout=(10.0, 60.0))
        d = lxml.html.fromstring(rr.text)
        hdrs = []
        for t in d.xpath("//table"):
            rows = t.xpath(".//tr")
            if len(rows) > 5:
                hdrs = [c.text_content().strip() for c in rows[0].xpath("./th|./td")]
                nrows = len(rows)
                break
        print(rr.status_code, cand, "->", hdrs, f"({nrows if hdrs else 0} rows)")
    except Exception as e:
        print("ERR", cand, type(e).__name__, e)
