"""Post-DAG health invariants for the CCP connector raw assets.

Catches silent degradation that file-existence alone misses: a truncated zip,
an endpoint that switched format, or the box page layout changing so the
scraper grabs the wrong (empty) link.
"""
from subsets_utils import load_raw_ndjson, load_raw_parquet

SLUG = "comparative-constitutions-project"


def test_bulk_panels_nonempty_and_keyed(spec_ids):
    """The two coded panels must hold thousands of country-year rows and carry
    the structural key columns (cowcode/country/year). Far fewer rows or a
    missing key column means the scrape grabbed the wrong zip or the CSV
    format changed."""
    expected_min = {f"{SLUG}-ccp-cnc": 10000, f"{SLUG}-ccp-cce": 5000}
    for sid, lo in expected_min.items():
        if sid not in spec_ids:
            continue
        table = load_raw_parquet(sid)
        assert table.num_rows >= lo, f"{sid}: {table.num_rows} rows < {lo}"
        cols = set(table.column_names)
        for key in ("cowcode", "country", "year"):
            assert key in cols, f"{sid}: missing key column {key!r}"


def test_constitutions_corpus(spec_ids):
    """The Constitute corpus should be ~240 constitution records with unique
    ids; a short list means the API returned a partial/error payload."""
    sid = f"{SLUG}-constitutions"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    assert len(rows) >= 150, f"{sid}: only {len(rows)} constitution records (<150)"
    ids = [r.get("id") for r in rows]
    assert all(ids), f"{sid}: some records have empty id"
    assert len(set(ids)) == len(ids), f"{sid}: duplicate constitution ids"
