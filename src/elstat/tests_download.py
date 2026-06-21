"""Post-DAG health invariants for the ELSTAT connector.

These run in-connector after the download nodes, loading raw through the same
subsets_utils loader the fetch fn used (ndjson). They catch silent degradation
that file-existence checks miss: empty payloads, non-numeric values, missing
labels.
"""

from subsets_utils import load_raw_ndjson


def _download_ids(spec_ids):
    # spec_ids includes both download and transform node ids; only download
    # nodes write raw ndjson assets.
    return [s for s in spec_ids if not s.endswith("-transform")]


def test_all_raw_assets_nonempty(spec_ids):
    """Every publication in scope was verified to expose at least one Excel data
    table with numeric cells; an empty asset means the page scrape, the Excel
    classification, or the melt silently broke for that publication."""
    empty = []
    for sid in _download_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty: {empty[:15]}"


def test_values_are_finite_numbers(spec_ids):
    """The melt only emits parsed finite floats. A null/NaN/str value means a
    non-numeric cell leaked into the value column."""
    bad = []
    for sid in _download_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        for r in rows[:500]:
            v = r.get("value")
            if not isinstance(v, (int, float)) or v != v:
                bad.append((sid, r))
                break
    assert not bad, f"non-numeric values found in {len(bad)} assets, e.g. {bad[:5]}"


def test_rows_carry_labels(spec_ids):
    """Each observation must carry its source file and a column label so the
    long table is interpretable."""
    bad = []
    for sid in _download_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        for r in rows[:500]:
            if not r.get("source_file") or not r.get("col_label"):
                bad.append((sid, r))
                break
    assert not bad, f"rows missing source_file/col_label in {len(bad)} assets, e.g. {bad[:5]}"
