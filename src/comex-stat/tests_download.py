"""Health-invariant tests for Comex Stat raw assets. Run post-DAG in-connector;
they catch silent degradation (truncated streams, format/encoding drift) that
file existence alone misses."""

from subsets_utils import load_raw_parquet

_TRANSACTION_IDS = {
    "comex-stat-exports-ncm",
    "comex-stat-imports-ncm",
    "comex-stat-exports-municipality",
    "comex-stat-imports-municipality",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every raw parquet must hold rows. An empty payload usually means the
    endpoint changed format, the chain broke, or parsing silently produced nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_transactions_span_many_years(spec_ids):
    """The yearly streaming loop must cover the full history (1997..latest). If it
    broke after one year we'd see a single distinct CO_ANO."""
    for sid in spec_ids:
        if sid not in _TRANSACTION_IDS:
            continue
        table = load_raw_parquet(sid)
        assert "CO_ANO" in table.column_names, f"{sid}: missing CO_ANO column"
        years = set(table.column("CO_ANO").to_pylist())
        assert len(years) >= 25, f"{sid}: only {len(years)} distinct years; year loop likely truncated"


def test_reference_keys_present(spec_ids):
    """Reference tables must carry their key column and look like real lookups."""
    expectations = {
        "comex-stat-ncm": ("CO_NCM", 5000),
        "comex-stat-pais": ("CO_PAIS", 100),
        "comex-stat-uf-mun": ("CO_MUN_GEO", 1000),
    }
    for sid, (key, min_rows) in expectations.items():
        if sid not in spec_ids:
            continue
        table = load_raw_parquet(sid)
        assert key in table.column_names, f"{sid}: missing key column {key}"
        assert len(table) >= min_rows, f"{sid}: only {len(table)} rows (<{min_rows})"
