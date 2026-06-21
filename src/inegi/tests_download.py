"""Post-DAG health invariants for the INEGI connector.

Catch silent degradation that file-existence alone misses: a catalog endpoint
switching format, the values stream truncating after a single batch, or the
public token being rejected (which would empty the CL_* assets).
"""

from subsets_utils import load_raw_parquet


def test_catalog_assets_nonempty(spec_ids):
    """Every CL_* reference asset should hold rows."""
    catalog_ids = [s for s in spec_ids if s != "inegi-values"]
    for sid in catalog_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"
        assert set(table.column_names) == {"code", "description"}, (
            f"{sid}: unexpected columns {table.column_names}"
        )


def test_indicator_catalog_complete():
    """CL_INDICATOR enumerated ~31,817 indicators; a tiny count means the
    catalog call degraded or the token was rejected."""
    table = load_raw_parquet("inegi-indicators")
    assert len(table) >= 25000, (
        f"inegi-indicators: {len(table)} rows; expected >=25000 (~31817 seen)"
    )


def test_values_nonempty_and_broad():
    """The observation stream must carry rows spanning many indicators —
    not just the first batch."""
    table = load_raw_parquet("inegi-values")
    assert len(table) > 100_000, f"inegi-values: only {len(table)} rows"
    cols = set(table.column_names)
    for required in ("indicator_id", "time_period", "obs_value"):
        assert required in cols, f"inegi-values missing column {required}"
    distinct_indicators = len(set(table.column("indicator_id").to_pylist()))
    assert distinct_indicators >= 1000, (
        f"inegi-values: only {distinct_indicators} distinct indicators; "
        "the values stream likely truncated after the first batches"
    )


def test_values_have_numeric_observations():
    """At least most obs_value strings must parse to float — otherwise the
    response format changed and the transform CAST would drop everything."""
    table = load_raw_parquet("inegi-values")
    sample = table.column("obs_value").to_pylist()[:2000]
    parsed = 0
    for v in sample:
        if v is None:
            continue
        try:
            float(v)
            parsed += 1
        except (TypeError, ValueError):
            pass
    assert parsed >= 0.8 * len(sample), (
        f"only {parsed}/{len(sample)} obs_value entries are numeric"
    )
