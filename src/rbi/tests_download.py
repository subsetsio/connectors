"""Health-invariant tests for the RBI connector — run post-DAG, in-connector."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. Empty payloads usually mean the
    endpoint switched format, the session/auth flow broke, or RBI changed the
    response envelope."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_fx_reserves_shape():
    """FX reserves must cover all five components with deep weekly history; a
    sharp drop means a component code or the date window silently broke."""
    t = load_raw_parquet("rbi-foreign-exchange-reserves")
    assert len(t) > 1000, f"FX reserves only {len(t)} rows; expected thousands"
    codes = set(t.column("reserve_code").to_pylist())
    assert {"FCA", "GOLD", "SDR", "TR", "IMF"} <= codes, f"missing components: {codes}"
    freqs = set(t.column("frequency").to_pylist())
    assert {"Weekly", "Monthly"} <= freqs, f"missing frequencies: {freqs}"
    amounts = [a for a in t.column("amount").to_pylist() if a is not None]
    assert amounts, "FX reserves has no non-null amounts"


def test_policy_rates_present():
    """The headline rates snapshot should carry the core policy rates."""
    t = load_raw_parquet("rbi-key-policy-rates")
    assert len(t) >= 5, f"only {len(t)} policy rates; expected the full headline set"
    names = " ".join(n or "" for n in t.column("name").to_pylist())
    assert "Repo Rate" in names, f"Policy Repo Rate missing from rates: {names}"
