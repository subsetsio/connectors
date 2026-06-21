"""Health invariants for the Robert Shiller raw downloads.

These run post-DAG, in-connector, and load raw through subsets_utils so they
behave identically locally and in the cloud. They catch silent degradation the
file-existence check misses: a workbook that changed sheet layout, a header/
footnote row leaking into the data, or a series quietly dropping out.
"""

from subsets_utils import load_raw_parquet

STOCK = "robert-shiller-us-stock-market"
HOME = "robert-shiller-us-home-price-index"


def test_stock_shape():
    t = load_raw_parquet(STOCK)
    assert len(t) >= 1800, f"{STOCK}: expected >=1800 monthly rows, got {len(t)}"
    cols = set(t.column_names)
    for required in ("date", "sp500_price", "cape", "long_interest_rate"):
        assert required in cols, f"{STOCK}: missing column {required!r}"
    dates = t.column("date").to_pylist()
    assert len(set(dates)) == len(dates), f"{STOCK}: duplicate dates present"
    assert dates[0].startswith("1871"), f"{STOCK}: series should start 1871, got {dates[0]}"
    capes = [c for c in t.column("cape").to_pylist() if c is not None]
    assert capes and 0 < min(capes) and max(capes) < 100, \
        f"{STOCK}: CAPE out of plausible range (min={min(capes)}, max={max(capes)})"


def test_home_shape():
    t = load_raw_parquet(HOME)
    assert len(t) >= 3000, f"{HOME}: expected >=3000 long rows, got {len(t)}"
    cols = set(t.column_names)
    assert {"date", "series", "value"} <= cols, f"{HOME}: unexpected columns {cols}"
    series = set(t.column("series").to_pylist())
    for required in ("real_home_price_index", "nominal_home_price_index"):
        assert required in series, f"{HOME}: missing series {required!r}"
    assert None not in t.column("value").to_pylist(), f"{HOME}: null values present in long table"
