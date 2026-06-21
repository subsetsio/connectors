from subsets_utils import load_raw_parquet


def test_country_stats_populated(spec_ids):
    """The per-country time series should hold rows for many countries across a
    long history; a near-empty asset means the API changed or fetch degraded."""
    sid = "ripe-ncc-country-resource-stats"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert len(t) > 100_000, f"{sid}: only {len(t)} rows; expected >100k"
    countries = set(t.column("country").to_pylist())
    assert len(countries) >= 100, f"{sid}: only {len(countries)} countries"


def test_rir_allocations_populated(spec_ids):
    """The RIR registry should hold the full ~260k resource records across all
    three resource types; truncation means the file or parse broke."""
    sid = "ripe-ncc-rir-allocations"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert len(t) > 100_000, f"{sid}: only {len(t)} rows; expected >100k"
    types = set(t.column("type").to_pylist())
    assert {"ipv4", "ipv6", "asn"} <= types, f"{sid}: missing types, got {types}"
