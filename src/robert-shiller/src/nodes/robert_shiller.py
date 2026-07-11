"""Download nodes for Robert Shiller's long-run market datasets."""

import io

import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_parquet

from utils import _decode_date, _http_get, _num, _resolve_xls


_HOME_SERIES = {
    "real_home_price_index": (0, 1),
    "real_building_cost_index": (2, 3),
    "us_population_millions": (2, 4),
    "long_interest_rate": (2, 5),
    "nominal_home_price_index": (7, 8),
    "nominal_building_cost_index": (10, 11),
    "cpi_monthly": (13, 14),
    "cpi_annual": (17, 18),
}

_HOME_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("series", pa.string()),
    ("value", pa.float64()),
])

_STOCK_COLS = {
    1: "sp500_price",
    2: "dividend",
    3: "earnings",
    4: "cpi",
    6: "long_interest_rate",
    7: "real_price",
    8: "real_dividend",
    9: "real_total_return_price",
    10: "real_earnings",
    11: "real_tr_scaled_earnings",
    12: "cape",
    14: "tr_cape",
    16: "excess_cape_yield",
    17: "monthly_total_bond_return",
    18: "real_total_bond_return",
    19: "real_stock_return_10y",
    20: "real_bond_return_10y",
    21: "excess_return_10y",
}

_STOCK_SCHEMA = pa.schema(
    [("date", pa.string())] + [(c, pa.float64()) for c in _STOCK_COLS.values()]
)


def fetch_home(node_id: str) -> None:
    import pandas as pd

    url = _resolve_xls("fig3")
    df = pd.read_excel(io.BytesIO(_http_get(url).content), sheet_name="Data", header=None)
    rows = []
    for name, (date_col, value_col) in _HOME_SERIES.items():
        for i in range(df.shape[0]):
            date = _decode_date(df.iloc[i, date_col])
            value = _num(df.iloc[i, value_col])
            if date is None or value is None:
                continue
            rows.append({"date": date, "series": name, "value": value})
    if not rows:
        raise RuntimeError(f"{node_id}: parsed 0 data rows from the home-price workbook")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_HOME_SCHEMA), node_id)


def fetch_stock(node_id: str) -> None:
    import pandas as pd

    url = _resolve_xls("ie_data")
    df = pd.read_excel(io.BytesIO(_http_get(url).content), sheet_name="Data", header=None)
    rows = []
    for i in range(df.shape[0]):
        date = _decode_date(df.iloc[i, 0])
        if date is None:
            continue
        rec = {"date": date}
        for idx, name in _STOCK_COLS.items():
            rec[name] = _num(df.iloc[i, idx])
        rows.append(rec)
    if not rows:
        raise RuntimeError(f"{node_id}: parsed 0 data rows from ie_data.xls")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_STOCK_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="robert-shiller-us-home-price-index", fn=fetch_home, kind="download"),
    NodeSpec(id="robert-shiller-us-stock-market", fn=fetch_stock, kind="download"),
]
