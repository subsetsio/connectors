from subsets_utils import get, configure_http
URL = "https://www.ghsindex.org/wp-content/uploads/2022/04/2021-GHS-Index-April-2022.csv"
configure_http(headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/csv,application/csv,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://ghsindex.org/report-model/",
})
r = get(URL, timeout=(10.0,120.0))
print("status:", r.status_code, "len:", len(r.content))
