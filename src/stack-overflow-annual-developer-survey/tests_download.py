"""Health invariants for the Stack Overflow Developer Survey raw assets.

Catch silent degradation that file-existence alone misses: empty payloads,
truncated downloads, the LFS pointer being saved instead of the real CSV,
or the per-year question set collapsing to a handful of columns.
"""
from subsets_utils import load_raw_parquet

SLUG = "stack-overflow-annual-developer-survey"


def test_all_raw_assets_nonempty(spec_ids):
    """Every fetched asset must hold rows. Empty usually means the LFS
    redirect broke or the endpoint changed format."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_results_have_wide_schema(spec_ids):
    """Each yearly results table is a wide survey (dozens of question
    columns). A single/handful-of-column table means the CSV header parse
    silently degraded (e.g. wrong delimiter or an LFS pointer)."""
    for sid in spec_ids:
        if "-results-" not in sid:
            continue
        table = load_raw_parquet(sid)
        ncols = table.num_columns
        assert ncols >= 20, f"{sid}: only {ncols} columns; expected a wide survey (>=20)"
        # An LFS pointer parsed as CSV would yield ~1-3 tiny rows.
        assert len(table) >= 1000, f"{sid}: only {len(table)} rows; expected thousands of respondents"


def test_codebook_shape(spec_ids):
    """The combined codebook must carry the normalized 3-column shape and
    span multiple survey years (2016+)."""
    cid = f"{SLUG}-schema-codebook"
    if cid not in spec_ids:
        return
    table = load_raw_parquet(cid)
    cols = set(table.column_names)
    assert {"survey_year", "column_name", "question_text"} <= cols, f"codebook columns: {cols}"
    years = set(table.column("survey_year").to_pylist())
    assert len(years) >= 8, f"codebook spans only {len(years)} years; expected >=8 (2016+)"
