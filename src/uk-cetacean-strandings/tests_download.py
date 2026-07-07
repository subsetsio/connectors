"""Post-DAG health invariants for the UK cetacean strandings raw asset."""

from subsets_utils import load_raw_parquet


SPEC_ID = (
    "uk-cetacean-strandings-historical-uk-cetacean-strandings-1913-1989"
)


def test_historical_strandings_nonempty(spec_ids):
    if SPEC_ID not in spec_ids:
        return
    table = load_raw_parquet(SPEC_ID)
    assert 4000 <= table.num_rows <= 5000, (
        f"{SPEC_ID}: expected ~4311 rows, got {table.num_rows}"
    )


def test_historical_strandings_schema(spec_ids):
    if SPEC_ID not in spec_ids:
        return
    table = load_raw_parquet(SPEC_ID)
    required = {
        "S_W_No",
        "Date",
        "Common Name",
        "Scientific Name",
        "Latitude",
        "Longitude",
        "Aggregated_Date",
    }
    missing = required - set(table.column_names)
    assert not missing, f"{SPEC_ID}: missing expected columns {sorted(missing)}"
    assert len(table.column_names) >= 35, (
        f"{SPEC_ID}: schema unexpectedly narrow: {len(table.column_names)} columns"
    )


def test_historical_strandings_identifiers_unique(spec_ids):
    if SPEC_ID not in spec_ids:
        return
    table = load_raw_parquet(SPEC_ID)
    ids = table.column("S_W_No").to_pylist()
    nonnull = [value for value in ids if value]
    assert len(nonnull) >= 4000, f"{SPEC_ID}: too few non-null S_W_No values"
    assert len(nonnull) == len(set(nonnull)), f"{SPEC_ID}: duplicate S_W_No values"
