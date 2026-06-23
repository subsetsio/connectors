import io, ssl, httpx, re
import subsets_utils.http_client as hc
from subsets_utils import get
import openpyxl
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
BC=("ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:"
 "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DEFAULT")
ctx=ssl.create_default_context(); ctx.set_ciphers(BC)
hc._client=httpx.Client(timeout=120, headers={"User-Agent":UA}, follow_redirects=True, verify=ctx)

def sheets(url, names):
    wb=openpyxl.load_workbook(io.BytesIO(get(url).content), data_only=True, read_only=True)
    for nm in names:
        ws=wb[nm]; rows=[list(r) for r in ws.iter_rows(values_only=True)]
        print(f"\n### {nm}  nrows={len(rows)}")
        for i,r in enumerate(rows[:11]):
            print(i,"|".join(("" if c is None else str(c))[:16] for c in r[:7]))
    wb.close()

# need current enforcement workbook
mt=get("https://ohss.dhs.gov/topics/immigration/immigration-enforcement/monthly-tables").text
links=[h if h.startswith("http") else "https://ohss.dhs.gov"+h for h in re.findall(r'href="([^"]+\.xlsx)"',mt)]
months={m:i for i,m in enumerate(["january","february","march","april","may","june","july","august","september","october","november","december"],1)}
def mk(u):
    m=re.search(r"tables-([a-z]+)-(\d{4})",u.lower()); 
    return (int(m.group(2)),months[m.group(1)]) if m and m.group(1) in months else (0,0)
latest=max(links,key=mk); print("latest enforcement:",latest)
sheets(latest, ["ERO Arrests by Citizenship","DHS Repats by Type"])
sheets("https://ohss.dhs.gov/system/files/2026-06/2026_0604_ohss_yearbook_lawful_permanent_residents_fy2024.xlsx", ["Table 1"])
