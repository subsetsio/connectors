"""Health-invariant tests for the CBS (Netherlands) connector.

Run post-DAG, in-connector, against the data through subsets_utils loaders.
These catch silent degradation that file-existence alone misses: empty
TypedDataSet payloads, a format switch away from NDJSON, or a dimension
code-list join that quietly stopped resolving labels.
"""

from subsets_utils import load_raw_ndjson

THEMES_SPEC = "cbs-netherlands-cbs-themes"


def _sample(spec_ids):
    """First, middle and last few assets — a wholesale failure shows up in any."""
    ordered = sorted(sid for sid in spec_ids if sid != THEMES_SPEC)
    n = len(ordered)
    idxs = sorted({0, 1, n // 2, n - 2, n - 1} & set(range(n)))
    return [ordered[i] for i in idxs]


def test_raw_assets_have_rows(spec_ids):
    """A representative sample of download assets must hold rows.

    Loading every one of ~1531 gzipped NDJSON assets is wasteful; sampling
    catches a wrong endpoint, an auth wall, or a format change just as well.
    """
    if not spec_ids:
        return
    sample = _sample(spec_ids)

    nonempty = 0
    for sid in sample:
        rows = load_raw_ndjson(sid)
        assert isinstance(rows, list), f"{sid}: expected a list of records"
        if rows:
            nonempty += 1
    assert nonempty > 0, (
        f"every sampled asset {sample} was empty — the Feed fetch is degraded"
    )


def test_dimension_labels_resolved(spec_ids):
    """Every StatLine row carries at least one `<Dim>_label`, and the labels
    are populated.

    The label columns are joined in the fetch fn from each table's own code-list
    entity sets. If CBS renames a code-list key, or starts padding codes
    differently, the join silently yields all-null labels and the published
    tables become unreadable code grids. That failure is invisible to a row
    count, so assert on it directly.
    """
    if not spec_ids:
        return

    for sid in _sample(spec_ids):
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        label_cols = [c for c in rows[0] if c.endswith("_label")]
        assert label_cols, f"{sid}: no `<Dim>_label` columns — the code-list join was dropped"

        for col in label_cols:
            resolved = sum(1 for r in rows if r.get(col) is not None)
            assert resolved, (
                f"{sid}: `{col}` is null on all {len(rows)} rows — the dimension "
                "code-list join stopped matching (code padding or key rename?)"
            )


def test_row_id_column_dropped(spec_ids):
    """`ID` is a serving-side row counter, not table content; the fetch fn strips
    it. Its reappearance means the normalisation was bypassed."""
    if not spec_ids:
        return
    for sid in _sample(spec_ids):
        rows = load_raw_ndjson(sid)
        if rows:
            assert "ID" not in rows[0], f"{sid}: serving-side 'ID' column leaked into raw"


def test_themes_taxonomy_shape(spec_ids):
    """The taxonomy is reference data with a parent/child tree — assert the
    columns downstream joins depend on."""
    if THEMES_SPEC not in set(spec_ids):
        return
    rows = load_raw_ndjson(THEMES_SPEC)
    assert len(rows) >= 20, f"{THEMES_SPEC}: only {len(rows)} themes — catalog truncated?"
    for col in ("ID", "ParentID", "Number", "Title"):
        assert col in rows[0], f"{THEMES_SPEC}: missing '{col}' — Themes entity set changed"
