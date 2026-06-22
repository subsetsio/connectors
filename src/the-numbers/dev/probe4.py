import lxml.html
from subsets_utils import get

def check(cand):
    try:
        rr = get(cand, timeout=(10.0, 60.0))
        d = lxml.html.fromstring(rr.text)
        hdrs, nrows = [], 0
        for t in d.xpath("//table"):
            rows = t.xpath(".//tr")
            if len(rows) > 5:
                hdrs = [c.text_content().strip() for c in rows[0].xpath("./th|./td")]
                nrows = len(rows); break
        print(rr.status_code, cand, "->", hdrs, f"({nrows} rows)")
    except Exception as e:
        print("ERR", cand, type(e).__name__, str(e)[:40])

for c in [
    "https://www.the-numbers.com/movie/budgets/all/1",
    "https://www.the-numbers.com/sitemap.xml",
    "https://www.the-numbers.com/finances",
    "https://www.the-numbers.com/market/2025/summary",
    "https://www.the-numbers.com/box-office-records",
]:
    check(c)

# confirm a movie detail page DOES carry budget (per-movie, not a listing)
r = get("https://www.the-numbers.com/movie/Toy-Story-5", timeout=(10.0, 60.0))
print("toy story 5 detail status", r.status_code, "has 'Production Budget':",
      "Production Budget" in r.text)
