"""Health-invariant tests for the CBS (Netherlands) connector.

Run post-DAG, in-connector, against the data through subsets_utils loaders.
These catch silent degradation that file-existence alone misses: empty
TypedDataSet payloads, a format switch away from NDJSON, or a fetch that wrote
zero rows for every table (which would mean the Feed shape changed).
"""

from subsets_utils import load_raw_ndjson


def test_raw_assets_have_rows(spec_ids):
    """A representative sample of download assets must hold rows.

    Loading every one of ~1666 gzipped NDJSON assets in a test is wasteful;
    sample the first, middle, and last few so a wholesale failure (wrong
    endpoint, auth wall, format change) is caught without rereading the corpus.
    """
    if not spec_ids:
        return
    ordered = sorted(spec_ids)
    n = len(ordered)
    idxs = sorted({0, 1, n // 2, n - 2, n - 1} & set(range(n)))
    sample = [ordered[i] for i in idxs]

    nonempty = 0
    for sid in sample:
        rows = load_raw_ndjson(sid)
        assert isinstance(rows, list), f"{sid}: expected a list of records"
        if rows:
            nonempty += 1
            assert "ID" in rows[0], (
                f"{sid}: TypedDataSet row missing 'ID' column — Feed shape changed"
            )
    assert nonempty > 0, (
        f"every sampled asset {sample} was empty — the Feed fetch is degraded"
    )
