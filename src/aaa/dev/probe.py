import re
from datetime import date, datetime, timezone
from subsets_utils import get

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")

GRADE_MAP = {"regular": "Regular", "mid-grade": "Mid-Grade", "mid": "Mid-Grade",
             "premium": "Premium", "diesel": "Diesel", "e85": "E85"}


def _txt(s):
    return re.sub(r"<[^>]+>", "", s).replace("&nbsp;", " ").strip()


def _as_of(html):
    m = re.search(r"as of\s+(\d{1,2})/(\d{1,2})/(\d{2,4})", html)
    if not m:
        return datetime.now(timezone.utc).date()
    mo, da, yr = (int(x) for x in m.groups())
    if yr < 100:
        yr += 2000
    return date(yr, mo, da)


def _price(cell):
    t = _txt(cell).replace("$", "").replace(",", "")
    try:
        return float(t)
    except ValueError:
        return None


def parse_table(tbl):
    """table-mob -> {time_label: {grade: price}}. Returns grades + 'Current Avg.' row."""
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", tbl, re.S)
    if not rows:
        return None, {}
    hdr = [_txt(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", rows[0], re.S)]
    grades = [GRADE_MAP.get(g.lower()) for g in hdr[1:]]
    out = {}
    for r in rows[1:]:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)
        if not cells:
            continue
        label = _txt(cells[0])
        prices = {}
        for g, c in zip(grades, cells[1:]):
            if g:
                prices[g] = _price(c)
        out[label] = prices
    return grades, out


def main():
    # national
    r = get("https://gasprices.aaa.com/", headers={"User-Agent": UA}, timeout=(10, 60))
    print("national HTTP", r.status_code, "as_of", _as_of(r.text))
    m = re.search(r'<table class="table-mob">(.*?)</table>', r.text, re.S)
    grades, parsed = parse_table(m.group(1))
    print("  grades:", grades)
    print("  Current Avg.:", parsed.get("Current Avg."))
    print("  rows:", list(parsed))

    # state page CA
    r = get("https://gasprices.aaa.com/?state=CA", headers={"User-Agent": UA}, timeout=(10, 60))
    print("\nstate CA HTTP", r.status_code, "as_of", _as_of(r.text))
    tables = re.findall(r'<table class="table-mob">(.*?)</table>', r.text, re.S)
    print("  n table-mob:", len(tables))
    g0, state_tbl = parse_table(tables[0])
    print("  statewide grades:", g0, "Current:", state_tbl.get("Current Avg."))
    # metros: h3 data-title then following table
    metros = re.findall(r'<h3[^>]*data-title[^>]*>(.*?)</h3>\s*<div>.*?(<table class="table-mob">.*?</table>)', r.text, re.S)
    print("  n metros matched:", len(metros))
    for name, tbl in metros[:3]:
        gg, pt = parse_table(re.search(r'<table class="table-mob">(.*?)</table>', tbl, re.S).group(1))
        print("   ", _txt(name), "->", pt.get("Current Avg."))


main()
