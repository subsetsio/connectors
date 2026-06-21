import json
from subsets_utils import get

for url in [
    "https://climateactiontracker.org/data-portal/api/country-emissions/records/?page_size=3",
    "https://climateactiontracker.org/data-portal/api/records/?page_size=3",
]:
    r = get(url, timeout=(10.0, 120.0))
    r.raise_for_status()
    d = r.json()
    print("=" * 80)
    print("URL:", url)
    print("keys:", list(d.keys()))
    print("count:", d.get("count"))
    print("next:", d.get("next"))
    res = d.get("results", [])
    print("n_results_on_page:", len(res))
    if res:
        print("first record:")
        print(json.dumps(res[0], indent=2, ensure_ascii=False))
        # types
        print("field types:", {k: type(v).__name__ for k, v in res[0].items()})
