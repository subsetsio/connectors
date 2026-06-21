"""Geopolitical Risk Index — per-country monthly index (long), 1900-present.

The export file carries one column per country in two families — GPRC_<ISO3>
(recent) and GPRHC_<ISO3> (historical); we melt both and join on (month, country).
"""
import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import MONTHLY_URL, _fetch_xls


def fetch_country_monthly(node_id: str) -> None:
    """Per-country monthly index, reshaped long. The export file carries one
    column per country in two families — GPRC_<ISO3> (recent) and
    GPRHC_<ISO3> (historical); we melt both and join on (month, country)."""
    df = _fetch_xls(MONTHLY_URL)
    recent_cols = [c for c in df.columns if c.startswith("GPRC_")]
    hist_cols = [c for c in df.columns if c.startswith("GPRHC_")]

    recent = df[["month"] + recent_cols].melt(
        id_vars="month", var_name="country", value_name="gprc"
    )
    recent["country"] = recent["country"].str.removeprefix("GPRC_")

    hist = df[["month"] + hist_cols].melt(
        id_vars="month", var_name="country", value_name="gprhc"
    )
    hist["country"] = hist["country"].str.removeprefix("GPRHC_")

    long = recent.merge(hist, on=["month", "country"], how="outer")

    table = pa.Table.from_arrays(
        [
            pa.array(pd.to_datetime(long["month"]), type=pa.timestamp("us")),
            pa.array(long["country"].astype(str), type=pa.string()),
            pa.array(pd.to_numeric(long["gprc"], errors="coerce"), type=pa.float64()),
            pa.array(pd.to_numeric(long["gprhc"], errors="coerce"), type=pa.float64()),
        ],
        schema=pa.schema(
            [
                pa.field("month", pa.timestamp("us")),
                pa.field("country", pa.string()),
                pa.field("gprc", pa.float64()),
                pa.field("gprhc", pa.float64()),
            ]
        ),
    )
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="geopolitical-risk-index-gpr-country-monthly", fn=fetch_country_monthly, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="geopolitical-risk-index-gpr-country-monthly-transform",
        deps=["geopolitical-risk-index-gpr-country-monthly"],
        sql='''
            SELECT
                CAST(month AS DATE) AS month,
                country,
                gprc,
                gprhc
            FROM "geopolitical-risk-index-gpr-country-monthly"
            WHERE gprc IS NOT NULL OR gprhc IS NOT NULL
            ORDER BY month, country
        ''',
    ),
]
