"""Health-invariant tests for the caic-avalanche-accidents raw assets.

Run post-DAG, in-connector. They catch silent degradation that file existence
alone misses: an empty payload (export switched format / Apps-Script redeploy),
a truncated download, or the wrong sheet parsed.
"""

from subsets_utils import load_raw_parquet

FATALITIES_ID = "caic-avalanche-accidents-us-avalanche-fatalities"
DETAIL_ID = "caic-avalanche-accidents-colorado-accident-detail"


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_fatalities_shape():
    """The flagship table is comprehensive (~1016 rows) and every row is a
    fatal accident, so the killed count must be populated."""
    t = load_raw_parquet(FATALITIES_ID)
    assert len(t) >= 900, f"{FATALITIES_ID}: only {len(t)} rows; expected >=900"
    killed = t.column("killed").to_pylist()
    assert all(k is not None and k >= 1 for k in killed), \
        "fatality rows must each have killed >= 1"


def test_detail_has_rich_fields():
    """The Colorado detail feed must carry its distinguishing rich columns with
    real (non-all-null) values, else it's just a degraded mirror."""
    t = load_raw_parquet(DETAIL_ID)
    assert len(t) >= 20, f"{DETAIL_ID}: only {len(t)} rows; expected >=20"
    for col in ("elevation", "aspect", "trigger"):
        vals = t.column(col).to_pylist()
        assert any(v is not None for v in vals), f"{DETAIL_ID}: {col} is all-null"
