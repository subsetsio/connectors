"""Post-download health invariants for the NHTSA connector."""

from subsets_utils import load_raw_parquet, load_raw_ndjson

# Minimum row counts — well below the true corpus sizes (recalls ~28k+
# campaigns/many more component-rows, complaints ~1.7M, investigations ~150k,
# safety ratings ~tens of thousands) but high enough to trip a truncated or
# format-broken download.
_FLAT_MIN_ROWS = {
    "nhtsa-recalls": 100_000,
    "nhtsa-complaints": 1_000_000,
    "nhtsa-investigations": 100_000,
}


def test_flat_files_nonempty_and_full(spec_ids):
    for sid, floor in _FLAT_MIN_ROWS.items():
        if sid not in spec_ids:
            continue
        table = load_raw_parquet(sid)
        assert len(table) >= floor, (
            f"{sid}: {len(table)} rows, expected >= {floor} "
            f"(download truncated or flat-file layout changed)"
        )


def test_recalls_key_columns_present(spec_ids):
    if "nhtsa-recalls" not in spec_ids:
        return
    cols = set(load_raw_parquet("nhtsa-recalls").column_names)
    for c in ("RECORD_ID", "CAMPNO", "MAKETXT", "DO_NOT_DRIVE"):
        assert c in cols, f"nhtsa-recalls missing expected column {c}"


def test_safety_ratings_nonempty(spec_ids):
    if "nhtsa-safety-ratings" not in spec_ids:
        return
    rows = load_raw_ndjson("nhtsa-safety-ratings")
    assert len(rows) >= 5_000, (
        f"nhtsa-safety-ratings: {len(rows)} records, expected >= 5000 "
        f"(traversal broke or API shape changed)"
    )
    assert any(r.get("OverallRating") for r in rows[:200]), (
        "nhtsa-safety-ratings: no OverallRating in first 200 records"
    )
