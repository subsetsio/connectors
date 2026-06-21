import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
url="https://statisticsmaldives.gov.mv/yearbook/statisticalarchive/wp-content/uploads/sites/3/2025/06/1.10.xlsx"
# default subsets_utils UA
r=get(url, timeout=(10,60))
print("default get:", r.status_code, r.headers.get("content-type"), len(r.content))
print("req UA sent:", r.request.headers.get("user-agent"))
# browser UA + accept
r2=get(url, timeout=(10,60), headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36","Accept":"*/*"})
print("browser get:", r2.status_code, r2.headers.get("content-type"), len(r2.content))
