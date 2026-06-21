from subsets_utils import get, configure_http

mm_url = "https://missingmigrants.iom.int/sites/g/files/tmzbdl601/files/report-migrant-incident/Missing_Migrants_Global_Figures_allData.csv"

# 1) default UA
r = get(mm_url, timeout=(10.0, 60.0))
print("default UA:", r.status_code, "len", len(r.content), repr(r.content[:80]))

# 2) browser-like UA
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
r2 = get(mm_url, headers={"User-Agent": ua}, timeout=(10.0, 60.0))
print("browser UA:", r2.status_code, "len", len(r2.content), repr(r2.content[:80]))

# 3) simple curl-like UA
r3 = get(mm_url, headers={"User-Agent": "subsets-bot/1.0"}, timeout=(10.0, 60.0))
print("custom UA:", r3.status_code, "len", len(r3.content), repr(r3.content[:80]))
