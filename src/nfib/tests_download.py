"""Health invariants for NFIB SBET raw downloads."""

from subsets_utils import load_raw_parquet


def test_optimism_index_nonempty_and_spans_history(spec_ids):
    """The optimism index is monthly since 1986-01; far fewer than ~450 rows
    means the proc switched shape or the date range was clipped."""
    if "nfib-optimism-index" not in spec_ids:
        return
    t = load_raw_parquet("nfib-optimism-index")
    assert t.num_rows >= 450, f"optimism index has only {t.num_rows} rows (expected ~485)"
    years = {d.year for d in t.column("date").to_pylist()}
    assert 1986 in years, "optimism index missing the 1986 history start"


def test_survey_responses_complete(spec_ids):
    """All ~25 survey questions, each a per-answer-code monthly distribution.
    A big drop in row count or question coverage means a question silently
    stopped returning data."""
    if "nfib-survey-responses" not in spec_ids:
        return
    t = load_raw_parquet("nfib-survey-responses")
    assert t.num_rows >= 50000, f"survey_responses has only {t.num_rows} rows (expected ~75k)"
    codes = set(t.column("question_code").to_pylist())
    assert len(codes) >= 24, f"only {len(codes)} distinct survey questions present (expected ~25)"
    # percent should be a real distribution, not all-null/zero
    pcts = [p for p in t.column("percent").to_pylist() if p is not None]
    assert any(p > 0 for p in pcts), "survey_responses percent column is empty/all-zero"
