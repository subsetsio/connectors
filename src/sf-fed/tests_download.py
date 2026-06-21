"""Post-DAG health invariants for the sf-fed connector.

Each indicator's raw asset is a long-format melt of its workbook with columns
sheet/row_idx/period/period_date/series/value/value_text. These tests catch
silent degradation a file-existence check would miss: an endpoint that started
serving an error page (0 rows), a workbook whose data sheets vanished, or a
parser that stopped extracting numeric values.
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {"sheet", "row_idx", "period", "period_date", "series", "value", "value_text"}

# Flagship indicators with deep history — these must always carry substantial,
# mostly-numeric, date-indexed data. A regression here means the parse broke.
FLAGSHIP_MIN_ROWS = {
    "sf-fed-daily-news-sentiment-index": 10000,
    "sf-fed-total-factor-productivity-tfp": 5000,
    "sf-fed-proxy-funds-rate": 3000,
    "sf-fed-supply-and-demand-driven-pce-inflation": 3000,
}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_columns(spec_ids):
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert EXPECTED_COLS <= cols, f"{sid}: missing columns {EXPECTED_COLS - cols}"


def test_has_numeric_values(spec_ids):
    """Every indicator must yield at least some numeric observations — these are
    statistical time series, so an all-text/all-null result means the value
    parse silently failed."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        nonnull = pc.sum(pc.is_valid(table.column("value"))).as_py()
        assert nonnull and nonnull > 0, f"{sid}: no numeric values parsed"


def test_flagship_depth(spec_ids):
    for sid, floor in FLAGSHIP_MIN_ROWS.items():
        if sid not in spec_ids:
            continue
        n = len(load_raw_parquet(sid))
        assert n >= floor, f"{sid}: only {n} rows, expected >= {floor}"
