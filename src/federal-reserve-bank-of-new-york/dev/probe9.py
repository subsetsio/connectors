from subsets_utils import get
# default UA, no custom header
r=get("https://markets.newyorkfed.org/api/rates/all/latest.json", timeout=(10,60))
print("default UA status:", r.status_code, "len", len(r.text))
print(r.text[:120])
