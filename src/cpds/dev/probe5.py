from subsets_utils import get
for i in range(5):
    r = get("https://cpds-data.org/data/", timeout=60)
    print(i, r.status_code, len(r.text))
    if len(r.text) < 2000:
        print("  BODY:", repr(r.text[:960]))
