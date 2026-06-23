"""Health invariants for the CAPMAS raw download assets — catch silent
degradation (empty payloads, truncated crawls, format drift) that file
existence alone misses."""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, "%s: raw parquet has 0 rows" % sid


def test_subjects_shape(spec_ids):
    if "eg-capmas-subjects" not in spec_ids:
        return
    t = load_raw_parquet("eg-capmas-subjects")
    assert 15 <= len(t) <= 60, "subjects: expected ~24 sub-subjects, got %d" % len(t)
    assert {"main_subject_id", "sub_subject_id"} <= set(t.column_names)


def test_indicators_corpus(spec_ids):
    if "eg-capmas-indicators" not in spec_ids:
        return
    t = load_raw_parquet("eg-capmas-indicators")
    # The subject tree enumerated 7353 indicators; a big shortfall means the
    # crawl broke or got throttled mid-way.
    assert len(t) >= 4000, "indicators: only %d rows; expected >=4000" % len(t)
    ids = t.column("indicator_id").to_pylist()
    assert all(i is not None for i in ids), "indicators: null indicator_id present"


def test_values_corpus(spec_ids):
    if "eg-capmas-values" not in spec_ids:
        return
    t = load_raw_parquet("eg-capmas-values")
    assert len(t) >= 20000, "values: only %d observation rows; expected >=20000" % len(t)
    cols = set(t.column_names)
    assert {"indicator_id", "year", "value"} <= cols, "values: missing core columns %s" % cols
    # values must span more than a handful of indicators
    distinct_inds = len(set(t.column("indicator_id").to_pylist()))
    assert distinct_inds >= 1000, "values: only %d distinct indicators" % distinct_inds
