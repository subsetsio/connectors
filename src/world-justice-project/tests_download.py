"""Post-DAG health invariants for the World Justice Project connector.

Each product is a hand-curated bulk file parsed into long/tabular parquet. These
tests catch silent degradation: an upstream layout change, a renamed sheet/CSV
member, or an empty/truncated download that file existence alone would miss.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every product must produce rows. Empty usually means the sheet/CSV was
    renamed upstream or the download truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_rule_of_law_index_shape(spec_ids):
    """ROL is the flagship: many countries x years x ~53 indicators, scores in
    [0,1]. Guards against a wide->long unpivot that silently collapsed."""
    sid = "world-justice-project-rule-of-law-index"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert len(t) > 50000, f"{sid}: only {len(t)} rows; unpivot likely broke"
    cols = set(t.column_names)
    assert {"country", "year", "indicator", "score"} <= cols, f"{sid}: missing core columns {cols}"
    scores = [s for s in t.column("score").to_pylist() if s is not None]
    assert scores, f"{sid}: all scores null"
    assert min(scores) >= 0 and max(scores) <= 1, (
        f"{sid}: scores out of [0,1] range: min={min(scores)} max={max(scores)}"
    )
    assert len(set(t.column("indicator").to_pylist())) >= 40, (
        f"{sid}: too few distinct indicators — sub-factor columns may be missing"
    )


def test_eurovoices_has_scores(spec_ids):
    sid = "world-justice-project-eurovoices"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert len(t) > 1000, f"{sid}: only {len(t)} rows"
    assert "nuts_id" in t.column_names, f"{sid}: missing nuts_id column"
    scores = [s for s in t.column("score").to_pylist() if s is not None]
    assert scores, f"{sid}: all scores null"


def test_atlas_catalog(spec_ids):
    sid = "world-justice-project-atlas-of-legal-needs"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert len(t) > 50, f"{sid}: only {len(t)} survey rows; header parsing may be off"
    assert "study_name" in t.column_names, f"{sid}: missing study_name column"
