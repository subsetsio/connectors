"""Health invariants for the NASA connector's raw assets.

Every load goes through the manifest-aware subsets_utils loaders — the same
resolution the transform runtime uses — so the tests hold in full runs,
maintain-skipped runs, and targeted retries alike (a run-dir listing would
see nothing in a retry run and false-alarm).

Exoplanet TAP tables are typed parquet; JPL/GISTEMP/EONET assets are NDJSON.
The format sets are explicit so a spec falling through unchecked is itself a
failure, not a silent skip.
"""

from subsets_utils import load_raw_ndjson, load_raw_parquet

PARQUET_SPECS = {
    "nasa-ps", "nasa-pscomppars", "nasa-toi", "nasa-k2pandc", "nasa-ml",
    "nasa-stellarhosts", "nasa-td", "nasa-cumulative",
    "nasa-q1-q17-dr25-koi", "nasa-q1-q17-dr25-sup-koi", "nasa-q1-q17-dr25-tce",
}
NDJSON_SPECS = {
    "nasa-cad", "nasa-fireball", "nasa-sentry", "nasa-nhats", "nasa-events",
    "nasa-gistemp-monthly-anomalies", "nasa-gistemp-zonal-annual",
}


def test_every_spec_has_a_known_format(spec_ids):
    unknown = set(spec_ids) - PARQUET_SPECS - NDJSON_SPECS
    assert not unknown, f"specs with no declared raw format: {sorted(unknown)}"


def test_parquet_assets_nonempty_and_wide(spec_ids):
    """Exoplanet parquet must hold rows and its full column set — guards
    against a TAP error page or a truncated dump slipping through."""
    for sid in PARQUET_SPECS & set(spec_ids):
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: parquet has 0 rows"
        assert table.num_columns >= 80, (
            f"{sid}: only {table.num_columns} columns — TAP dump truncated?"
        )


def test_ndjson_assets_nonempty(spec_ids):
    """JPL / GISTEMP / EONET assets must hold real records. Empty usually
    means the endpoint changed shape or the parse silently dropped rows."""
    for sid in NDJSON_SPECS & set(spec_ids):
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: ndjson has 0 rows"
        assert isinstance(rows[0], dict) and rows[0], f"{sid}: empty record"
