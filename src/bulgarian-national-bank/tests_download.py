"""Health-invariant tests for the Bulgarian National Bank connector.

Run post-DAG, in-connector, so they read raw via the same subsets_utils loaders
the download nodes wrote with. They catch silent degradation that file existence
alone misses: empty payloads, truncated downloads, the endpoint switching format.
"""

from subsets_utils import load_raw_parquet

FX_ID = "bulgarian-national-bank-exchange-rates"
SDMX_COLUMNS = {"keyfamily", "freq", "series_key", "series_name", "period", "value"}
FX_COLUMNS = {
    "date", "currency_code", "currency_name",
    "ratio", "rate_bgn", "reverse_rate", "gold",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. An empty payload usually means
    the endpoint switched format or returned an error stub."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_exchange_rates_schema():
    """The FX asset must keep its full column set; a missing column means the
    ROWSET layout changed under us."""
    cols = set(load_raw_parquet(FX_ID).column_names)
    assert FX_COLUMNS <= cols, f"{FX_ID}: missing columns {FX_COLUMNS - cols}"


def test_sdmx_assets_schema(spec_ids):
    """Every SDMX asset must expose the long-form series/period/value columns;
    a missing column means the SpreadsheetML unpivot drifted."""
    for sid in spec_ids:
        if sid == FX_ID:
            continue
        cols = set(load_raw_parquet(sid).column_names)
        assert SDMX_COLUMNS <= cols, f"{sid}: missing SDMX columns {SDMX_COLUMNS - cols}"
