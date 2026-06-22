import sys
sys.path.insert(0, "src")
from utils import _fetch, _has_rows

# Does BNM serve exchange-rate / kijang history older than 2021? Probe multiple months per year.
for res, path in [("exchange-rate", "exchange-rate/USD/year/{y}/month/{m}"),
                  ("kijang-emas", "kijang-emas/year/{y}/month/{m}")]:
    print(f"\n=== {res} ===")
    for y in [2015, 2018, 2019, 2020, 2021]:
        hits = []
        for m in (1, 3, 6, 9, 12):
            p = _fetch(path.format(y=y, m=m))
            if _has_rows(p):
                hits.append(m)
        print(f"  {y}: months_with_data={hits}")
