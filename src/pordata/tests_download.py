"""Post-DAG health invariants for the PORDATA connector.

These run in-connector after the download nodes, loading raw through the same
subsets_utils loader the fetch used (save_raw_ndjson -> load_raw_ndjson). They
catch silent degradation that file-existence alone misses: a page that stopped
embedding its table (parser yields 0 rows), or values that stopped parsing
(every cell None) because the page format drifted.
"""

from subsets_utils import load_raw_ndjson


def test_most_assets_nonempty(spec_ids):
    """Each indicator page should embed a data table. A few may legitimately be
    chart-only, but a widespread emptiness means the GET path or the parser
    broke. Require the vast majority to carry rows."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    frac = len(empty) / max(1, len(spec_ids))
    assert frac <= 0.05, (
        f"{len(empty)}/{len(spec_ids)} raw assets are empty "
        f"({frac:.1%}); >5% empty means the scrape/parser degraded. e.g. {empty[:5]}"
    )


def test_values_actually_parse(spec_ids):
    """Across a non-empty asset, at least some cells must parse to numbers. An
    asset that is all-null value means the numeric extraction stopped matching
    (page switched decimal/grouping or wrapped values in new markup)."""
    checked = all_null = 0
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        checked += 1
        if all(r.get("value") is None for r in rows):
            all_null += 1
    assert checked > 0, "no non-empty assets found at all"
    frac = all_null / checked
    assert frac <= 0.05, (
        f"{all_null}/{checked} non-empty assets have zero parseable values "
        f"({frac:.1%}); numeric parsing likely broke"
    )
