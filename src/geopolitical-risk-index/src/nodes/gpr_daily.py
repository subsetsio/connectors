"""Geopolitical Risk Index — daily index + moving averages, 1985-present."""
import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import DAILY_URL, _META_COLS, _fetch_xls


def fetch_daily(node_id: str) -> None:
    """Daily index + moving averages. Keep the parsed 'date' column and the
    free-text 'event' annotation; drop the redundant integer DAY key and the
    codebook columns."""
    df = _fetch_xls(DAILY_URL)
    df = df.drop(columns=[c for c in df.columns if c in _META_COLS or c == "DAY"])

    event = df["event"].astype("object").where(df["event"].notna(), None)
    measure_cols = [c for c in df.columns if c not in ("date", "event")]

    fields = [pa.field("date", pa.timestamp("us"))]
    arrays = [pa.array(pd.to_datetime(df["date"]), type=pa.timestamp("us"))]
    for c in measure_cols:
        fields.append(pa.field(c.lower(), pa.float64()))
        arrays.append(pa.array(pd.to_numeric(df[c], errors="coerce"), type=pa.float64()))
    fields.append(pa.field("event", pa.string()))
    arrays.append(pa.array(event, type=pa.string()))

    save_raw_parquet(pa.Table.from_arrays(arrays, schema=pa.schema(fields)), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="geopolitical-risk-index-gpr-daily", fn=fetch_daily, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="geopolitical-risk-index-gpr-daily-transform",
        deps=["geopolitical-risk-index-gpr-daily"],
        sql='''
            SELECT
                CAST(date AS DATE) AS date,
                * EXCLUDE (date)
            FROM "geopolitical-risk-index-gpr-daily"
            WHERE gprd IS NOT NULL
            ORDER BY date
        ''',
    ),
]
