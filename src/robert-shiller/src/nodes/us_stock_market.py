"""us-stock-market (ie_data.xls, 'Data' sheet).

S&P 500 / CAPE, monthly from Jan 1871. Wide: one row per month, ~18 measures.
"""

import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import _decode_date, _http_get, _num, _resolve_xls

# Column index -> output name on the 'Data' sheet. Index 5 (date fraction) and
# 13/15 (blank spacer columns between the CAPE blocks) are intentionally omitted.
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


def fetch_stock(node_id: str) -> None:
    import pandas as pd  # lazy: keep numpy off the module-introspection import path

    asset = node_id
    url = _resolve_xls("ie_data")
    df = pd.read_excel(io.BytesIO(_http_get(url).content), sheet_name="Data", header=None)
    rows = []
    for i in range(df.shape[0]):
        d = _decode_date(df.iloc[i, 0])  # data rows have a decimal date in col 0
        if d is None:
            continue                     # skips the banner header and footnote rows
        rec = {"date": d}
        for idx, name in _STOCK_COLS.items():
            rec[name] = _num(df.iloc[i, idx])
        rows.append(rec)
    if not rows:
        raise RuntimeError(f"{asset}: parsed 0 data rows from ie_data.xls")
    table = pa.Table.from_pylist(rows, schema=_STOCK_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="robert-shiller-us-stock-market", fn=fetch_stock, kind="download"),
]


_STOCK_SELECT = ",\n                ".join(
    f"CAST({c} AS DOUBLE) AS {c}" for c in _STOCK_COLS.values()
)

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="robert-shiller-us-stock-market-transform",
        deps=["robert-shiller-us-stock-market"],
        sql=f'''
            SELECT
                CAST(date AS DATE) AS date,
                {_STOCK_SELECT}
            FROM "robert-shiller-us-stock-market"
            ORDER BY date
        ''',
    ),
]
