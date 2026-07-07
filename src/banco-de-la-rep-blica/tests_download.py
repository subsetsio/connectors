"""Health invariants for the Banco de la República SDMX raw assets.

Each download node writes one all-string parquet of (series, observation) rows.
These catch silent degradation — empty payloads, a WAF block page parsed to
nothing, or the SDMX structure changing out from under us.
"""

from subsets_utils import load_raw_parquet

_RAW_COLUMNS = {
    "reference_area", "subject", "expenditure", "activity", "adjustment",
    "unit_measure", "freq", "domain", "unit_mult", "time_period",
    "obs_value", "obs_status",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataflow must yield observations. 0 rows means the endpoint
    blocked us (WAF) or the SDMX shape changed."""
    for sid in _raw_spec_ids(spec_ids):
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_raw_schema_stable(spec_ids):
    """The parsed SeriesKey/Attribute/Obs columns must all be present."""
    for sid in _raw_spec_ids(spec_ids):
        cols = set(load_raw_parquet(sid).column_names)
        missing = _RAW_COLUMNS - cols
        assert not missing, f"{sid}: missing raw columns {missing}"


def test_obs_value_mostly_numeric(spec_ids):
    """obs_value is a stringified number in SDMX; a sample should parse as
    float. A column that is suddenly all non-numeric means we grabbed the
    wrong element (e.g. a status code) or a block page."""
    for sid in _raw_spec_ids(spec_ids):
        table = load_raw_parquet(sid)
        vals = table.column("obs_value").to_pylist()[:200]
        parsed = 0
        for v in vals:
            if v is None:
                continue
            try:
                float(v)
                parsed += 1
            except (TypeError, ValueError):
                pass
        assert parsed > 0, f"{sid}: no numeric obs_value in first {len(vals)} rows"


def _raw_spec_ids(spec_ids):
    return [sid for sid in spec_ids if not sid.endswith("-transform")]
