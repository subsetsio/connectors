"""Health invariants for the NYC TLC raw downloads.

Trip series are batched (one parquet per month, asset id
``<spec-id>-<YYYY-MM>``); the zone lookup is a single CSV. We assert each
series produced monthly batches with rows, and the zone lookup decoded to a
real table — catching silent truncation, empty payloads, or a format switch
that file-existence alone would miss.
"""

from subsets_utils import load_raw_parquet, load_raw_file, list_raw_files

ZONE_ID = "nyc-tlc-taxi-zone-lookup"


def test_trip_series_have_monthly_batches_with_rows(spec_ids):
    for sid in spec_ids:
        if sid == ZONE_ID:
            continue
        files = list_raw_files(f"{sid}-*.parquet")
        assert files, f"{sid}: no monthly batch parquet files found"
        # Each batch file is itself an asset (<sid>-YYYY-MM.parquet); load the
        # first and confirm it carries rows.
        first_asset = files[0].rsplit("/", 1)[-1][: -len(".parquet")]
        table = load_raw_parquet(first_asset)
        assert table.num_rows > 0, f"{first_asset}: batch parquet has 0 rows"


def test_zone_lookup_decoded(spec_ids):
    if ZONE_ID not in spec_ids:
        return
    text = load_raw_file(ZONE_ID, "csv")
    assert isinstance(text, str), "zone lookup did not decode as text/CSV"
    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert len(lines) >= 200, f"zone lookup has only {len(lines)} lines; expected ~266"
    assert "LocationID" in lines[0], f"unexpected zone header: {lines[0]!r}"
