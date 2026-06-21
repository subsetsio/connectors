import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import re
import lxml.html
from subsets_utils import get


def fetch(url):
    r = get(url, timeout=(10.0, 120.0))
    r.raise_for_status()
    r.encoding = "utf-8"
    return r.text


_NUM_RE = re.compile(r"^-?[\d,]+(?:\.\d+)?$")


def _clean(s):
    return re.sub(r"\s+", " ", (s or "").replace("\xa0", " ")).strip()


def _is_num(s):
    s = s.replace(",", "").replace(" ", "")
    return bool(_NUM_RE.match(s.replace(",", ""))) and bool(re.search(r"\d", s))


def grid_from_table(tbl):
    """Expand rowspan/colspan into a dense grid of cell texts."""
    rows = tbl.xpath(".//tr")
    grid = []
    occupied = {}  # (r,c) -> text already placed by a span
    for r, tr in enumerate(rows):
        while len(grid) <= r:
            grid.append({})
        c = 0
        for cell in tr.xpath("./td|./th"):
            while (r, c) in occupied:
                c += 1
            txt = _clean(cell.text_content())
            try:
                rs = int(cell.get("rowspan", 1))
            except ValueError:
                rs = 1
            try:
                cs = int(cell.get("colspan", 1))
            except ValueError:
                cs = 1
            for dr in range(rs):
                for dc in range(cs):
                    occupied[(r + dr, c + dc)] = txt
            c += cs
    ncols = (max((cc for (rr, cc) in occupied), default=-1) + 1)
    nrows = len(rows)
    mat = [["" for _ in range(ncols)] for _ in range(nrows)]
    for (rr, cc), t in occupied.items():
        if rr < nrows and cc < ncols:
            mat[rr][cc] = t
    return mat


def melt(mat):
    if not mat or not mat[0]:
        return [], 0, 0
    nrows, ncols = len(mat), len(mat[0])
    # header rows: leading rows with no numeric cell
    H = 0
    for row in mat:
        if any(_is_num(x) for x in row):
            break
        H += 1
    H = max(H, 1)
    # label cols: leading cols with no numeric cell in body rows
    L = 0
    for c in range(ncols):
        if any(_is_num(mat[r][c]) for r in range(H, nrows)):
            break
        L += 1
    L = max(L, 1)
    records = []
    for r in range(H, nrows):
        row_label = " / ".join(x for x in (mat[r][c] for c in range(L)) if x)
        for c in range(L, ncols):
            val = mat[r][c]
            if not _is_num(val):
                continue
            col_label = " / ".join(x for x in (mat[h][c] for h in range(H)) if x)
            records.append((row_label, col_label, val))
    return records, H, L


for url in [
    "http://www.moe.gov.cn/jyb_sjzl/moe_560/2023/quanguo/202501/t20250120_1176410.html",
]:
    html = fetch(url)
    doc = lxml.html.fromstring(html)
    tables = doc.xpath("//table")
    print(f"URL {url}: {len(tables)} <table>")
    # pick the data table = the one with most numeric cells
    best, bestn = None, -1
    for t in tables:
        m = grid_from_table(t)
        n = sum(_is_num(x) for row in m for x in row)
        if n > bestn:
            best, bestn = m, n
    recs, H, L = melt(best)
    print(f"  grid {len(best)}x{len(best[0])}, H={H} L={L}, numeric cells={bestn}, records={len(recs)}")
    for rec in recs[:6]:
        print("   ", rec)
