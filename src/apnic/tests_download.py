"""Health-invariant tests for the APNIC connector raw assets."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows. Empty payloads usually mean
    the endpoint switched format, was rate-limited, or returned an error body."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_ipv6_covers_many_economies(spec_ids):
    """The IPv6 per-economy union must span well over a hundred economies; a
    handful means economy discovery (via aspop) silently degraded."""
    sid = "apnic-ipv6-capability"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    n = len(set(table.column("economy").to_pylist()))
    assert n >= 150, f"{sid}: only {n} distinct economies; expected >=150"


def test_delegated_has_all_resource_types(spec_ids):
    """The delegated file must contain asn, ipv4 and ipv6 records; a missing
    type means the line filter dropped a category."""
    sid = "apnic-delegated-resources"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    types = set(table.column("resource_type").to_pylist())
    assert {"asn", "ipv4", "ipv6"} <= types, f"{sid}: resource types present = {types}"
