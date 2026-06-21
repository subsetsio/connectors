"""Dataset 2: eu-labour-market-outlook-dashboard — TESTED recipe.

Flow: scrape page -> resolve /sites/default/files/...zip -> download -> unzip
-> extract inner .7z (py7zr) -> parse '...Timeseries- All.xlsx' to tidy long rows.
The filename is DATE-STAMPED ("Download data 21.02.25.zip" / inner ".7z" / inner
xlsx prefixed "13.02.25"), so we rediscover the URL from the page each run.
"""
import io, re, zipfile, tempfile, os
import httpx, py7zr, openpyxl

PAGE = "https://www.bruegel.org/dataset/eu-labour-market-outlook-dashboard"
HEADERS = {"User-Agent": "Mozilla/5.0"}
LINK_RE = re.compile(
    r'href="((?:https?://[^"]+)?/(?:sites/default|system)/files/[^"]+\.(?:xlsx|xls|csv|zip|7z))"'
)

def resolve_zip_url():
    html = httpx.get(PAGE, headers=HEADERS, timeout=60, follow_redirects=True).text
    for m in LINK_RE.finditer(html):
        href = m.group(1)
        if href.lower().endswith(".zip"):
            return href if href.startswith("http") else "https://www.bruegel.org" + href
    raise RuntimeError("zip link not found on page")

def load_labour():
    url = resolve_zip_url()
    zbytes = httpx.get(url, headers=HEADERS, timeout=120, follow_redirects=True).content
    # outer .zip -> inner .7z
    with zipfile.ZipFile(io.BytesIO(zbytes)) as zf:
        inner_name = next(n for n in zf.namelist() if n.lower().endswith(".7z"))
        seven = zf.read(inner_name)
    # inner .7z -> extract the Timeseries-All workbook
    rows = []
    with tempfile.TemporaryDirectory() as td:
        with py7zr.SevenZipFile(io.BytesIO(seven), "r") as z:
            names = z.getnames()
            target = next(n for n in names if n.lower().endswith(".xlsx")
                          and "timeseries- all" in n.lower())
            z.extract(path=td, targets=[target])
        wb = openpyxl.load_workbook(os.path.join(td, target), read_only=True, data_only=True)
        ws = wb["Sheet1"]
        it = ws.iter_rows(values_only=True)
        next(it)  # header: Year, Country, Breakdown, Variable, Value, Variable2, sort_by, sort_by2
        for r in it:
            year, country, indicator, group_code, value, group_label = r[0], r[1], r[2], r[3], r[4], r[5]
            if year is None or value is None:   # ~15k cells are blank (no data)
                continue
            rows.append({
                "year": int(year),
                "country": country,            # ISO-ish 2-letter (EL=Greece, EU=aggregate)
                "indicator": indicator,        # e.g. "Employment rate (%)"
                "breakdown": group_label,      # demographic cut: Total / Men / Women / Low educated ...
                "value": float(value),
            })
    return names, rows

if __name__ == "__main__":
    files, rows = load_labour()
    print("FILES IN .7z:")
    for f in files:
        print("  ", f)
    print("TOTAL ROWS:", len(rows))
    for r in rows[:5]:
        print(r)
