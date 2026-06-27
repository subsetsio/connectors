"""Health-invariant tests for the National Bank of Kazakhstan FX connector.

Raw is written as per-year batches (`national-bank-fx-rates-<year>.parquet`), so
these tests discover the batch files by glob rather than by the bare spec id.
"""

import pyarrow.parquet as pq

from subsets_utils import list_raw_files, raw_parquet_localpath


def test_year_batches_present():
    """At least the deep historical span (~1999 onward) should produce many
    year batches; a single batch means the year loop broke after one iteration."""
    files = list_raw_files("national-bank-fx-rates-*.parquet")
    assert len(files) >= 5, (
        f"only {len(files)} year batch(es) found: {files} — expected one per "
        f"year from 1999 onward"
    )


def test_batches_nonempty_and_have_codes():
    """Every year batch must hold rows with non-empty currency codes — an empty
    or code-less batch means the feed format changed or a date range came back
    blank without being skipped."""
    files = list_raw_files("national-bank-fx-rates-*.parquet")
    assert files, "no national-bank-fx-rates year batches found at all"
    for rel in files:
        # rel is like "national-bank-fx-rates-2020.parquet"
        asset_id = rel.rsplit("/", 1)[-1].removesuffix(".parquet")
        with raw_parquet_localpath(asset_id) as path:
            table = pq.read_table(path)
        assert table.num_rows > 0, f"{rel}: 0 rows"
        codes = table.column("currency_code").to_pylist()
        assert any(codes), f"{rel}: all currency_code values empty"
        assert "USD" in codes, f"{rel}: USD missing — parse or coverage error"
