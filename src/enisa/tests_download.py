"""Health-invariant tests for the ENISA EUVD connector.

These run post-DAG against the raw NDJSON assets via subsets_utils loaders, so
they catch silent degradation (truncated crawl, format switch, empty payload)
that file-existence alone misses.
"""

from subsets_utils import load_raw_ndjson


def test_vulnerabilities_substantial(spec_ids):
    """The full EUVD corpus is ~360k records; if the crawl truncated after a
    page or two we'd see a tiny count. Loose floor well below the real size."""
    if "enisa-vulnerabilities" not in spec_ids:
        return
    rows = load_raw_ndjson("enisa-vulnerabilities")
    assert len(rows) >= 200_000, f"vulnerabilities: only {len(rows)} rows; crawl likely truncated"
    ids = {r.get("id") for r in rows}
    assert None not in ids, "vulnerabilities: some rows have null id"
    # id format sanity — EUVD-YYYY-NNNNN
    sample = next(iter(ids))
    assert sample.startswith("EUVD-"), f"unexpected id format: {sample!r}"


def test_affected_products_present(spec_ids):
    """Most vulnerabilities list >=1 affected product, so the exploded table
    should be at least as large as the corpus. A tiny count means the explode
    or the crawl broke."""
    if "enisa-affected-products" not in spec_ids:
        return
    rows = load_raw_ndjson("enisa-affected-products")
    assert len(rows) >= 200_000, f"affected_products: only {len(rows)} rows; explode/crawl likely broke"
    for r in rows[:1000]:
        assert r.get("euvd_id"), "affected_products: row missing euvd_id"
        assert r.get("product_name"), "affected_products: row missing product_name"
