"""Health-invariant tests for the SSA download stage.

Each OASDI layer is one row per US state/territory (~57 rows). These tests
catch silent degradation: empty payloads, truncated downloads (pagination
broke), or a layer that lost its state column.
"""

from subsets_utils import load_raw_ndjson

# Every accepted layer carries a state/territory column under one of these names.
_STATE_COLS = ("State_Territory", "State_Terr")


def test_all_raw_assets_nonempty(spec_ids):
    """Every layer should return rows. SSA reports ~52-57 state/territory rows
    per layer; far fewer means the query degraded or the schema changed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) >= 50, f"{sid}: got {len(rows)} rows; expected >=50"


def test_state_column_present(spec_ids):
    """Each layer must carry a recognizable state/territory column — the join
    key for the published tables."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        keys = set(rows[0].keys())
        assert any(c in keys for c in _STATE_COLS), (
            f"{sid}: no state column among {_STATE_COLS}; keys={sorted(keys)[:10]}"
        )


def test_total_is_numeric(spec_ids):
    """The 'Total'/'Total_Beneficiaries' measure must be present and numeric on
    every row — a null/string total means the attribute schema shifted."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        total_key = "Total_Beneficiaries" if "Total_Beneficiaries" in rows[0] else "Total"
        assert total_key in rows[0], f"{sid}: no total column"
        numeric = [r for r in rows if isinstance(r.get(total_key), (int, float))]
        assert len(numeric) >= 50, (
            f"{sid}: only {len(numeric)} rows have numeric {total_key}"
        )
