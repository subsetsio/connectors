from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download node should write at least one row. An empty payload
    means the JSON envelope changed, pagination broke, or auth/format shifted."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_summary_one_row_per_year(spec_ids):
    """summary is one aggregate row per year across the timespan; a sharp drop
    means the year-range discovery or the year-required endpoint broke."""
    if "itc-summary" not in spec_ids:
        return
    rows = load_raw_ndjson("itc-summary")
    years = [r["year"] for r in rows]
    assert len(years) == len(set(years)), "duplicate years in summary"
    assert len(years) >= 10, f"summary has only {len(years)} years; expected the full 2014+ span"


def test_activities_corpus_size(spec_ids):
    """The activities catalog reported ~230 activities; a big shortfall means
    pagination capped after page 1."""
    if "itc-activities" not in spec_ids:
        return
    rows = load_raw_ndjson("itc-activities")
    idents = {r["identifier"] for r in rows}
    assert len(idents) >= 100, f"only {len(idents)} distinct activities; expected >=100"
