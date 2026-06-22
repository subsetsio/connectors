from subsets_utils import get
r = get("https://cpds-data.org/data/", timeout=60)
print("status:", r.status_code, "final url:", str(r.url))
print(r.text[:1200])
