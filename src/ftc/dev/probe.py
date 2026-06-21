import csv, io, re
from subsets_utils import get

BASE = "https://www.ftc.gov"
DATASETS_PAGE = BASE + "/policy-notices/open-government/data-sets"
DNC_PAGE = BASE + "/policy-notices/open-government/data-sets/do-not-call-data"

html = get(DATASETS_PAGE, timeout=(10, 120)).content.decode("utf-8", "replace")
hrefs = re.findall(r'href="([^"]*attachments/data-sets/[^"]+\.csv)"', html)
print("data-set CSV links found:", len(hrefs))
for slug in ["ftc_civil_penalty_actions", "hsr_transactions_filings_second_requests_by_fy"]:
    pat = re.compile(rf'/{re.escape(slug)}(?:_\d+)?\.csv$')
    matches = [h for h in hrefs if "dictionary" not in h and pat.search(h)]
    print(slug, "->", matches)

# probe one CSV parse with cp1252
url = BASE + [h for h in hrefs if "ftc_merger_enforcement_actions" in h and "dictionary" not in h][0]
raw = get(url, timeout=(10, 120)).content
rows = list(csv.DictReader(io.StringIO(raw.decode("cp1252", errors="replace"))))
print("merger rows:", len(rows), "keys:", list(rows[0].keys()))
print("sample industry:", rows[0].get("MatterIndustry"))

# DNC daily files
dnc_html = get(DNC_PAGE, timeout=(10, 120)).content.decode("utf-8", "replace")
dnc = re.findall(r'href="([^"]*DNC_Complaint_Numbers_\d{4}-\d{2}-\d{2}\.csv)"', dnc_html)
dnc = list(dict.fromkeys(dnc))
print("DNC daily files listed:", len(dnc), "first:", dnc[0] if dnc else None)
draw = get(BASE + dnc[0], timeout=(10, 120)).content
drows = list(csv.DictReader(io.StringIO(draw.decode("cp1252", errors="replace"))))
print("one DNC file rows:", len(drows), "keys:", list(drows[0].keys()))
