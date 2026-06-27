"""Post-DAG health invariants for the NBS exchange-rate connector.

Raw is written as yearly firehose batches (`<spec-id>-<year>.parquet`), so we load
via the batch glob rather than a single asset file."""

from subsets_utils import list_raw_files, load_raw_parquet


def _batch_assets(spec_id):
    return [rel[: -len(".parquet")] for rel in list_raw_files(f"{spec_id}-*.parquet")]


def test_raw_batches_present_and_nonempty(spec_ids):
    """Each download spec must have at least one yearly batch with rows. Zero
    batches or all-empty batches means the export endpoint changed shape, the
    date/month walk broke, or parsing silently dropped everything."""
    for sid in spec_ids:
        assets = _batch_assets(sid)
        assert assets, f"{sid}: no yearly batch parquet files found"
        total = sum(load_raw_parquet(a).num_rows for a in assets)
        assert total > 0, f"{sid}: all {len(assets)} yearly batches are empty"


def test_daily_has_long_history(spec_ids):
    """The daily feed spans 1999..now (~25+ years); far fewer batches means the
    backfill stalled or the year range regressed."""
    sid = "national-bank-of-slovakia-exchange-rate-daily"
    if sid not in spec_ids:
        return
    assets = _batch_assets(sid)
    assert len(assets) >= 20, f"{sid}: only {len(assets)} yearly batches; expected the full 1999+ history"


def test_daily_columns(spec_ids):
    sid = "national-bank-of-slovakia-exchange-rate-daily"
    if sid not in spec_ids:
        return
    assets = _batch_assets(sid)
    cols = set(load_raw_parquet(assets[0]).column_names)
    assert {"date", "currency", "rate"} <= cols, f"{sid}: unexpected columns {cols}"


def test_foreign_columns(spec_ids):
    sid = "national-bank-of-slovakia-exchange-rate-foreign-monthly"
    if sid not in spec_ids:
        return
    assets = _batch_assets(sid)
    cols = set(load_raw_parquet(assets[0]).column_names)
    assert {"valid_from", "country", "currency_code", "currency_name", "value"} <= cols, (
        f"{sid}: unexpected columns {cols}"
    )
