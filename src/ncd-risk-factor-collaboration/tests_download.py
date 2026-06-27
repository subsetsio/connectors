"""Health-invariant tests for the NCD-RisC raw download assets.

Each download asset is a uniform tidy long-format parquet. These catch silent
degradation (empty payload, lost geographic levels, a parse that dropped every
indicator) that file existence alone misses.
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {
    "entity", "iso", "sex", "year", "age_group", "estimate_type",
    "geographic_level", "indicator", "value", "lower_95", "upper_95",
}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_uniform(spec_ids):
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert cols == EXPECTED_COLS, f"{sid}: columns {cols} != {EXPECTED_COLS}"


def test_country_level_present(spec_ids):
    """Country-level rows are the most valuable slice; every risk factor ships
    country files (height via the per-country ZIP). Absence means the country
    fetch silently dropped."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        levels = set(t.column("geographic_level").to_pylist())
        assert "country" in levels, f"{sid}: no country-level rows (levels={levels})"


def test_value_within_uncertainty(spec_ids):
    """The central estimate should sit within its 95% interval where both
    bounds exist. Gross violations mean the lower/upper columns got misaligned
    to the wrong indicator during the unpivot."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        lo, hi, v = t.column("lower_95"), t.column("upper_95"), t.column("value")
        both = pc.and_(pc.is_valid(lo), pc.is_valid(hi))
        if pc.sum(pc.cast(both, "int64")).as_py() == 0:
            continue
        ok = pc.and_(pc.less_equal(lo, v), pc.less_equal(v, hi))
        ok = pc.if_else(both, ok, True)
        bad = pc.sum(pc.cast(pc.invert(ok), "int64")).as_py()
        frac = bad / len(t)
        assert frac < 0.02, f"{sid}: {frac:.1%} of rows have value outside [lower_95, upper_95]"
