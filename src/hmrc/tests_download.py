"""Post-DAG health invariants for the HMRC connector.

The fact tables are written as per-period batch files (`<spec>-<period>.parquet`);
Commodity is a single file. These tests catch silent degradation — empty
payloads, a format/schema switch, or pagination that quietly stopped after the
first page.
"""
from subsets_utils import load_raw_parquet, list_raw_files

_BATCHED = {"hmrc-ots", "hmrc-rts", "hmrc-trade", "hmrc-import", "hmrc-export", "hmrc-yearlytrade"}
_EXT = ".parquet"


def _load_first_batch(sid):
    files = list_raw_files(f"{sid}-*{_EXT}")
    assert files, f"{sid}: no batch parquet files written"
    asset = files[0][: -len(_EXT)]
    return asset, load_raw_parquet(asset)


def test_raw_assets_present_and_nonempty(spec_ids):
    """Every spec must have written real rows — batched specs at least one
    non-empty period file, Commodity its single file."""
    for sid in spec_ids:
        if sid in _BATCHED:
            asset, t = _load_first_batch(sid)
            assert len(t) > 0, f"{sid}: first batch {asset} has 0 rows"
        else:  # hmrc-commodity
            t = load_raw_parquet(sid)
            assert len(t) > 1000, f"{sid}: commodity has only {len(t)} rows (expected ~16k)"


def test_value_columns_present(spec_ids):
    """OTS/RTS carry monetary Value; absence means the response schema changed."""
    for sid in ("hmrc-ots", "hmrc-rts"):
        if sid not in spec_ids:
            continue
        _, t = _load_first_batch(sid)
        assert "Value" in t.column_names, f"{sid}: missing Value column ({t.column_names})"
        assert "MonthId" in t.column_names, f"{sid}: missing MonthId column"


def test_batched_specs_cover_many_periods(spec_ids):
    """A monthly fact table spanning ~2000-present should land dozens of period
    files; a handful would mean the period loop stopped early."""
    for sid in ("hmrc-ots",):
        if sid not in spec_ids:
            continue
        files = list_raw_files(f"{sid}-*{_EXT}")
        assert len(files) >= 24, f"{sid}: only {len(files)} period files (expected dozens)"
