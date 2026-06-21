"""Post-DAG health invariants for the Istat connector.

Each raw asset is one dataflow's SDMX-CSV rendered as NDJSON. We sample a
handful of assets (loading all 340 — some 700k+ rows — would OOM the test) and
assert they carry observations with the SDMX shape we parsed against. Silent
degradation modes this catches: the endpoint switching format (no TIME_PERIOD /
OBS_VALUE columns), or an asset coming back empty.
"""
from subsets_utils import load_raw_ndjson


def _sample(spec_ids, k=8):
    """Deterministic spread across the spec set (no RNG)."""
    ids = sorted(spec_ids)
    if len(ids) <= k:
        return ids
    step = len(ids) / k
    return [ids[int(i * step)] for i in range(k)]


def test_sampled_assets_nonempty(spec_ids):
    for sid in _sample(spec_ids):
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw NDJSON has 0 rows"


def test_sampled_assets_have_sdmx_columns(spec_ids):
    """Every observation row must carry TIME_PERIOD and OBS_VALUE — the two
    columns the transform casts/keys on. Their absence means the SDMX-CSV
    header changed shape."""
    for sid in _sample(spec_ids):
        rows = load_raw_ndjson(sid)
        head = rows[0]
        assert "TIME_PERIOD" in head, f"{sid}: missing TIME_PERIOD column ({list(head)[:8]})"
        assert "OBS_VALUE" in head, f"{sid}: missing OBS_VALUE column ({list(head)[:8]})"


def test_sampled_assets_have_numeric_values(spec_ids):
    """At least some OBS_VALUE in each sampled asset must parse as a float —
    otherwise the transform's numeric filter yields a 0-row published table."""
    for sid in _sample(spec_ids):
        rows = load_raw_ndjson(sid)
        numeric = 0
        for r in rows[:5000]:
            v = r.get("OBS_VALUE")
            if v is None:
                continue
            try:
                float(v)
                numeric += 1
            except (TypeError, ValueError):
                pass
        assert numeric > 0, f"{sid}: no numeric OBS_VALUE in first 5000 rows"
