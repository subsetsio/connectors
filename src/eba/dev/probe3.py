import io, re
from subsets_utils import get
import openpyxl, pyarrow.csv as pacsv

def latest_te_csv_url(filename):
    main = get("https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise", timeout=(10,60)).text
    years = {}
    for href in re.findall(r'href="([^"]*transparency[^"]*)"', main):
        m = re.search(r'/(20\d\d)-eu-wide-transparency', href)
        if m: years[int(m.group(1))] = href
    y = max(years)
    page = href = years[y]
    if href.startswith('/'): href = "https://www.eba.europa.eu"+href
    html = get(href, timeout=(10,60)).text
    m = re.search(r'(https://www\.eba\.europa\.eu/assets/TE\d+/Full_database/\d+/'+re.escape(filename)+r')', html)
    return y, (m.group(1) if m else None)

print("TE discovery:")
for f in ["tr_cre.csv","tr_mrk.csv","tr_sov.csv","tr_oth.csv"]:
    print(" ", f, latest_te_csv_url(f))

# Risk dashboard KRI discovery + parse
rd = get("https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/risk-monitoring/risk-dashboard", timeout=(10,60)).text
m = re.findall(r'href="([^"]*Data%20Annex%20InteractiveRiskDashboard[^"]*\.xlsx)"', rd)
print("\nRD annex candidates:", len(m), m[0] if m else None)
url = m[0]
if url.startswith('/'): url = "https://www.eba.europa.eu"+url
r = get(url, timeout=(10,180))
wb = openpyxl.load_workbook(io.BytesIO(r.content), read_only=True, data_only=True)
ws = wb["KRIs by country and EU"]
rows=list(ws.iter_rows(values_only=True))
print("KRI header:", rows[0], "nrows:", len(rows))
periods = sorted({rw[0] for rw in rows[1:] if rw[0] is not None})
inds = sorted({rw[2] for rw in rows[1:] if rw[2] is not None})
print("period range:", periods[0], periods[-1], "n_periods", len(periods))
print("n_indicators", len(inds), "sample", inds[:8])
