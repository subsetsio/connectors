"""Health-invariant tests for the IBP Open Budget Survey raw download.

These run post-DAG, in-connector, and load raw through subsets_utils so they
behave identically locally and in the cloud. They catch silent degradation that
file-existence alone misses: an empty payload, a single indicator's worth of
rows (pagination broke), or every numeric value gone null (format switch).
"""

from subsets_utils import load_raw_parquet


def test_values_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_all_six_indicators_present(spec_ids):
    """All 6 IBP_OBS indicators should be pulled; fewer means a fetch dropped one."""
    sid = "ibp-open-budget-values"
    table = load_raw_parquet(sid)
    codes = set(table.column("indicator_code").to_pylist())
    expected = {
        "IBP_OBS_RANK", "IBP_OBS_OBI", "IBP_OBS_SAI_OBI",
        "IBP_OBS_LEG_OBI", "IBP_OBS_OVERSIGHT_OBI", "IBP_OBS_PUB_ENG",
    }
    assert codes == expected, f"{sid}: indicator set drifted: {expected ^ codes}"


def test_values_have_parseable_numbers(spec_ids):
    """At least most obs_value strings should parse to real numbers; if the
    column became all-null/NaN the source format changed silently."""
    sid = "ibp-open-budget-values"
    table = load_raw_parquet(sid)
    vals = table.column("obs_value").to_pylist()
    parseable = 0
    for v in vals:
        if v is None or str(v).strip().lower() == "nan" or v == "":
            continue
        try:
            float(v)
            parseable += 1
        except ValueError:
            pass
    assert parseable >= len(vals) * 0.5, (
        f"{sid}: only {parseable}/{len(vals)} obs_value parse to numbers"
    )
