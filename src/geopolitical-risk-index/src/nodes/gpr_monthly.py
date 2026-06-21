"""Geopolitical Risk Index — global monthly index + components (wide), 1900-present.

The export file minus the per-country families and the embedded codebook columns.
"""
import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import MONTHLY_URL, _META_COLS, _fetch_xls


def _measure_table(df: pd.DataFrame, date_col: str) -> pa.Table:
    """Wide frame -> pyarrow with an explicit schema: the date column as a
    timestamp, every other column as float64. Column names are lowercased."""
    cols = [c for c in df.columns]
    fields = []
    arrays = []
    for c in cols:
        name = c.lower()
        if c == date_col:
            fields.append(pa.field(name, pa.timestamp("us")))
            arrays.append(pa.array(pd.to_datetime(df[c]), type=pa.timestamp("us")))
        else:
            fields.append(pa.field(name, pa.float64()))
            arrays.append(pa.array(pd.to_numeric(df[c], errors="coerce"), type=pa.float64()))
    return pa.Table.from_arrays(arrays, schema=pa.schema(fields))


def fetch_monthly(node_id: str) -> None:
    """Global monthly index + components — the export file minus the country
    families and the codebook columns."""
    df = _fetch_xls(MONTHLY_URL)
    drop = [c for c in df.columns if c in _META_COLS or c.startswith("GPRC_") or c.startswith("GPRHC_")]
    df = df.drop(columns=drop)
    save_raw_parquet(_measure_table(df, "month"), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="geopolitical-risk-index-gpr-monthly", fn=fetch_monthly, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="geopolitical-risk-index-gpr-monthly-transform",
        deps=["geopolitical-risk-index-gpr-monthly"],
        sql='''
            SELECT
                CAST(month AS DATE) AS month,
                * EXCLUDE (month)
            FROM "geopolitical-risk-index-gpr-monthly"
            WHERE gpr IS NOT NULL OR gprh IS NOT NULL
            ORDER BY month
        ''',
    ),
]
