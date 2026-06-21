"""us-home-price-index (Fig3-1 (1).xls, 'Data' sheet).

Real & nominal home price index, building cost, population, long rate, CPI;
1890-. Long: (date, series, value) -- the series have heterogeneous date coverage
(monthly home prices from 1953, annual otherwise), so a long shape is the only
honest one.
"""

import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import _decode_date, _http_get, _num, _resolve_xls

# Each series sits in its own (date_col, value_col) pair; coverage differs per
# series, so we emit a long (date, series, value) table.
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


def fetch_home(node_id: str) -> None:
    import pandas as pd  # lazy: keep numpy off the module-introspection import path

    asset = node_id
    url = _resolve_xls("fig3")
    df = pd.read_excel(io.BytesIO(_http_get(url).content), sheet_name="Data", header=None)
    rows = []
    for name, (dc, vc) in _HOME_SERIES.items():
        for i in range(df.shape[0]):
            d = _decode_date(df.iloc[i, dc])
            v = _num(df.iloc[i, vc])
            if d is None or v is None:
                continue
            rows.append({"date": d, "series": name, "value": v})
    if not rows:
        raise RuntimeError(f"{asset}: parsed 0 data rows from the home-price workbook")
    table = pa.Table.from_pylist(rows, schema=_HOME_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="robert-shiller-us-home-price-index", fn=fetch_home, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="robert-shiller-us-home-price-index-transform",
        deps=["robert-shiller-us-home-price-index"],
        sql='''
            SELECT
                CAST(date AS DATE) AS date,
                series,
                CAST(value AS DOUBLE) AS value
            FROM "robert-shiller-us-home-price-index"
            WHERE value IS NOT NULL
            ORDER BY series, date
        ''',
    ),
]
