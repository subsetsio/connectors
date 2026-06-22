"""Health-invariant tests for the COBS connector raw assets."""

from subsets_utils import load_raw_ndjson


def test_comets_nonempty():
    """comet_list.api should yield the full comet catalog; an empty/tiny pull
    means the enumeration endpoint changed or failed silently."""
    rows = load_raw_ndjson("cobs-comets")
    assert len(rows) >= 1500, f"cobs-comets: only {len(rows)} comets"
    assert all(r.get("id") is not None for r in rows[:50]), "cobs-comets: null ids"


def test_observations_nonempty_and_flat():
    """The per-comet sweep should produce a large flat observation corpus with
    the comet_id we inject and a parseable obs_date."""
    rows = load_raw_ndjson("cobs-observations")
    assert len(rows) >= 100000, f"cobs-observations: only {len(rows)} rows"
    sample = rows[0]
    for col in ("obs_date", "comet_id", "magnitude", "obs_type"):
        assert col in sample, f"cobs-observations: missing column {col}"
    assert sample["comet_id"] is not None, "cobs-observations: null comet_id"
