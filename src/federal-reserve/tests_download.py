"""Health-invariant tests for the Federal Reserve DDP connector.

Run post-DAG, in-connector. They catch silent degradation that file existence
alone misses: an empty/truncated SDMX dump, a Cloudflare HTML page parsed into
zero rows, or the fixed raw schema drifting.
"""
from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {
    "release", "series_name", "freq_code", "frequency", "unit", "unit_mult",
    "currency", "short_description", "long_description", "series_attributes",
    "time_period", "obs_value", "obs_status",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every release must yield observations. Zero rows means the zip came back
    as a challenge page, the release was renamed, or the XML format changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_stable(spec_ids):
    """The fixed core schema must be present on every release."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_time_periods_look_like_dates(spec_ids):
    """TIME_PERIOD is always YYYY-MM-DD in the FRB SDMX dump; if that stops
    holding the downstream DATE cast silently nulls out, so guard it here."""
    import re
    pat = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for sid in spec_ids:
        tp = load_raw_parquet(sid).column("time_period").to_pylist()
        sample = [t for t in tp[:2000] if t is not None]
        bad = [t for t in sample if not pat.match(t)]
        assert not bad, f"{sid}: unexpected time_period formats e.g. {bad[:5]}"


def test_flagship_releases_substantial(spec_ids):
    """H.15 (Selected Interest Rates) is daily across many series — it must hold
    far more than a token number of rows. Catches a partial/truncated parse."""
    h15 = "federal-reserve-h15"
    if h15 in spec_ids:
        n = len(load_raw_parquet(h15))
        assert n >= 100_000, f"{h15}: only {n} rows; expected >=100k for daily H.15"
