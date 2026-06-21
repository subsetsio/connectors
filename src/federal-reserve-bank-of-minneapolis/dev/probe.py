import io, csv
from subsets_utils import get

BASE = "https://www.minneapolisfed.org/-/media/assets/institute/census/data-center"
mods = ["pctl_of_inc", "inc_share", "prop_share", "inc_change_distributions", "transition_matrix"]

for m in mods:
    for variant in (f"{m}_all_data", f"na_{m}_all_data"):
        url = f"{BASE}/{variant}.csv"
        r = get(url, timeout=(10.0, 180.0))
        r.raise_for_status()
        b = r.content
        text = b.decode("utf-8-sig")
        rdr = csv.reader(io.StringIO(text))
        header = next(rdr)
        nrows = sum(1 for _ in rdr)
        print(f"{variant:42s} bytes={len(b):>10,} rows={nrows:>8,} cols={len(header)}")
    print()
