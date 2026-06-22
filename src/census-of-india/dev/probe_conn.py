from subsets_utils import get
import sys
url="https://censusindia.gov.in/nada/index.php/api/catalog/search?tab_type=table&ps=2&page=1"
try:
    r=get(url, timeout=(10,60))
    print("catalog HTTP", r.status_code, "found=", r.json()["result"]["found"])
except Exception as e:
    print("catalog ERR", type(e).__name__, str(e)[:200])
# test a download URL
durl="https://censusindia.gov.in/nada/index.php/catalog/42526/download/47057/foo"  # may 404 but tests TLS
try:
    r=get("https://censusindia.gov.in/nada/index.php/metadata/export/42526/json", timeout=(10,60))
    print("metadata HTTP", r.status_code, "resources?", "resources" in r.json())
except Exception as e:
    print("metadata ERR", type(e).__name__, str(e)[:200])
