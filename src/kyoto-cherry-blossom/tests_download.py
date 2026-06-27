"""Health-invariant tests for the Kyoto cherry-blossom raw assets.

Run post-DAG inside the connector, reading raw through subsets_utils loaders so
they behave identically locally and in the cloud. They catch silent degradation
that file-existence alone misses: empty payloads, a format switch that yields
all-null columns, or a truncated download.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must produce raw rows; an empty payload usually means
    the endpoint changed format or returned an error page."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_bloom_has_observations(spec_ids):
    """The bloom series must carry real day-of-year values, not an all-null
    column from a header/format change."""
    sid = "kyoto-cherry-blossom-bloom-dates"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    days = table.column("day_of_year").to_pylist()
    nonnull = [d for d in days if d is not None]
    assert len(nonnull) > 700, f"{sid}: only {len(nonnull)} non-null day_of_year values"
    assert all(80 <= d <= 130 for d in nonnull), f"{sid}: day_of_year out of expected range"


def test_temperature_has_reconstruction(spec_ids):
    """The temperature file must carry reconstructed values after the -999.9
    sentinel is stripped; an all-null column means the sentinel handling or the
    source format broke."""
    sid = "kyoto-cherry-blossom-temperature-reconstruction"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    recs = [t for t in table.column("temp_reconstructed").to_pylist() if t is not None]
    assert len(recs) > 500, f"{sid}: only {len(recs)} non-null reconstructed temps"
    assert all(t != -999.9 for t in recs), f"{sid}: -999.9 sentinel leaked into data"
