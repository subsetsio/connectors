from subsets_utils import get
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
base = "https://www.epo.org/sites/default/files/stc_centre/statistic_centre_data/json-data"
for f in ["fields-metadata.json", "countries.json"]:
    r = get(f"{base}/{f}", headers={"User-Agent": UA}, timeout=(10.0, 120.0))
    print(f, r.status_code, "bytes", len(r.content))
    if f == "fields-metadata.json":
        d = r.json(); print("  type", type(d).__name__, "len", len(d), "item0", d[0])
