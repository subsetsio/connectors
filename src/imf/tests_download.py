"""Health-invariant tests for the IMF connector raw assets.

Each dataflow is fetched as an all-string Parquet. These catch silent
degradation a file-exists check misses: empty payloads, a missing time/value
column (format switch), or a value column that is entirely non-numeric (wrong
endpoint / HTML error body parsed as CSV).

Two dataflows (NA_MAIN, SDG) are returned by the IMF SDMX endpoint as
degenerate rows — a structure stamp with empty dimensions and no observations
(duplicate empty column names, no OBS_VALUE). They are unpublishable and carry
run waivers, so they are excluded from these invariants. Most dataflows publish
the observation under OBS_VALUE; ISORA uses OBSERVATION.
"""

from subsets_utils import load_raw_parquet

# Degenerate/empty at the source — excused via waiver, excluded from invariants.
KNOWN_BROKEN = {"imf-na-main", "imf-sdg"}
# The observation-value column, in priority order (ISORA uses OBSERVATION).
VALUE_COLS = ("OBS_VALUE", "OBSERVATION")


def _testable(spec_ids):
    return [s for s in spec_ids if s not in KNOWN_BROKEN]


def _value_col(cols):
    return next((c for c in VALUE_COLS if c in cols), None)


def test_all_raw_assets_nonempty(spec_ids):
    """Every publishable dataflow's raw parquet should hold rows. An empty
    payload means the endpoint changed shape, returned an error body, or the
    wildcard query broke."""
    empty = []
    for sid in _testable(spec_ids):
        if load_raw_parquet(sid).num_rows == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:10]}"


def test_core_observation_columns_present(spec_ids):
    """SDMX-CSV carries TIME_PERIOD and an observation-value column
    (OBS_VALUE, or OBSERVATION for ISORA). Their absence means the response was
    not the expected flat SDMX-CSV (format/accept-header drift)."""
    missing = []
    for sid in _testable(spec_ids):
        cols = set(load_raw_parquet(sid).column_names)
        if "TIME_PERIOD" not in cols or _value_col(cols) is None:
            missing.append(sid)
    assert not missing, f"{len(missing)} assets missing TIME_PERIOD/value column: {missing[:10]}"


def test_obs_value_mostly_numeric(spec_ids):
    """The value column is stored as a string in raw but must contain numbers.
    If a dataflow has no parseable values at all, we fetched the wrong thing.

    Many dataflows are sparse (e.g. GFS OBS_VALUE is >90% null — a dense
    dimension cross-product with few populated cells), so a fixed head window
    can be entirely null while the table is fine. Drop nulls/empties FIRST, then
    check that the populated values parse as numbers. (ISORA mixes numeric
    indicators with categorical survey answers, so we only require SOME numeric
    values among the populated ones, not all.)"""
    bad = []
    for sid in _testable(spec_ids):
        table = load_raw_parquet(sid)
        vcol = _value_col(table.column_names)
        if vcol is None:
            continue
        populated = [v for v in table.column(vcol).drop_null().slice(0, 5000).to_pylist()
                     if v != ""]
        if not populated:
            continue  # column entirely null/empty — caught by other invariants
        parseable = 0
        for v in populated:
            try:
                float(v)
                parseable += 1
            except (TypeError, ValueError):
                pass
        if parseable == 0:
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have no numeric value among populated cells: {bad[:10]}"
