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


_NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")


def _clean(s):
    return re.sub(r"\s+", " ", (s or "").replace("\xa0", " ")).strip()


def _is_num(s):
    s = s.replace(",", "").replace(" ", "")
    return bool(_NUM_RE.match(s)) and bool(re.search(r"\d", s))


def grid_from_table(tbl):
    rows = tbl.xpath(".//tr")
    occupied = {}
    for r, tr in enumerate(rows):
        c = 0
        for cell in tr.xpath("./td|./th"):
            while (r, c) in occupied:
                c += 1
            txt = _clean(cell.text_content())
            try:
                rs = max(1, int(cell.get("rowspan", 1)))
            except ValueError:
                rs = 1
            try:
                cs = max(1, int(cell.get("colspan", 1)))
            except ValueError:
                cs = 1
            for dr in range(rs):
                for dc in range(cs):
                    occupied[(r + dr, c + dc)] = txt
            c += cs
    nrows = len(rows)
    ncols = max((cc for (rr, cc) in occupied), default=-1) + 1
    mat = [["" for _ in range(ncols)] for _ in range(nrows)]
    for (rr, cc), t in occupied.items():
        if rr < nrows and cc < ncols:
            mat[rr][cc] = t
    return mat


def melt(mat):
    if not mat or not mat[0]:
        return []
    nrows, ncols = len(mat), len(mat[0])
    H = 0
    for row in mat:
        if any(_is_num(x) for x in row):
            break
        H += 1
    if H == 0 or H >= nrows:
        return []
    L = 0
    for c in range(ncols):
        if any(_is_num(mat[r][c]) for r in range(H, nrows)):
            break
        L += 1
    L = max(L, 1)
    out = []
    for r in range(H, nrows):
        row_label = " / ".join(x for x in (mat[r][c] for c in range(L)) if x)
        for c in range(L, ncols):
            val = mat[r][c]
            if not _is_num(val):
                continue
            col_label = " / ".join(dict.fromkeys(x for x in (mat[h][c] for h in range(H)) if x))
            out.append((row_label, col_label, float(val.replace(",", ""))))
    return out


def parse_article(html):
    doc = lxml.html.fromstring(html)
    for bad in doc.xpath("//style|//script"):
        bad.getparent().remove(bad)
    leaves = [t for t in doc.xpath("//table") if not t.xpath(".//table")]
    recs = []
    for ti, t in enumerate(leaves):
        m = grid_from_table(t)
        n = sum(_is_num(x) for row in m for x in row)
        if n < 3:
            continue
        for (rl, cl, v) in melt(m):
            recs.append((ti, rl, cl, v))
    return recs


for url in [
    "http://www.moe.gov.cn/jyb_sjzl/moe_560/2023/quanguo/202501/t20250120_1176410.html",
    "http://www.moe.gov.cn/jyb_sjzl/moe_560/jytjsj_2015/2015_qg/",  # find an article below
]:
    if url.endswith("/"):
        # discover one article from this index
        ih = fetch(url)
        d = lxml.html.fromstring(ih)
        d.make_links_absolute(url)
        art = None
        for a in d.xpath("//a[@href]"):
            if (a.get("title") or "").strip() == "各级各类学历教育学生情况" and re.search(r"/t\d{8}_\d+\.html$", a.get("href")):
                art = a.get("href")
                break
        print("2015 article:", art)
        url = art
    recs = parse_article(fetch(url))
    print(f"  {url}: {len(recs)} records")
    for rec in recs[:5]:
        print("   ", rec)
    print("   ...tail:", recs[-1] if recs else None)
