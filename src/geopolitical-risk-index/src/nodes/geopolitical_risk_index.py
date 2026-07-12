"""Download nodes for the Caldara-Iacoviello Geopolitical Risk Index."""

import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_parquet
from utils import DAILY_URL, MONTHLY_URL, _META_COLS, _fetch_xls


def _measure_table(df: pd.DataFrame, date_col: str) -> pa.Table:
    fields = []
    arrays = []
    for col in df.columns:
        name = col.lower()
        if col == date_col:
            fields.append(pa.field(name, pa.timestamp("us")))
            arrays.append(pa.array(pd.to_datetime(df[col]), type=pa.timestamp("us")))
        else:
            fields.append(pa.field(name, pa.float64()))
            arrays.append(pa.array(pd.to_numeric(df[col], errors="coerce"), type=pa.float64()))
    return pa.Table.from_arrays(arrays, schema=pa.schema(fields))


def fetch_monthly(node_id: str) -> None:
    df = _fetch_xls(MONTHLY_URL)
    drop = [
        col
        for col in df.columns
        if col in _META_COLS or col.startswith("GPRC_") or col.startswith("GPRHC_")
    ]
    save_raw_parquet(_measure_table(df.drop(columns=drop), "month"), node_id)


def fetch_daily(node_id: str) -> None:
    df = _fetch_xls(DAILY_URL)
    df = df.drop(columns=[col for col in df.columns if col in _META_COLS or col == "DAY"])

    fields = [pa.field("date", pa.timestamp("us"))]
    arrays = [pa.array(pd.to_datetime(df["date"]), type=pa.timestamp("us"))]
    for col in [c for c in df.columns if c not in ("date", "event")]:
        fields.append(pa.field(col.lower(), pa.float64()))
        arrays.append(pa.array(pd.to_numeric(df[col], errors="coerce"), type=pa.float64()))
    fields.append(pa.field("event", pa.string()))
    event = df["event"].astype("object").where(df["event"].notna(), None)
    arrays.append(pa.array(event, type=pa.string()))

    save_raw_parquet(pa.Table.from_arrays(arrays, schema=pa.schema(fields)), node_id)


def fetch_country_monthly(node_id: str) -> None:
    df = _fetch_xls(MONTHLY_URL)
    recent_cols = [col for col in df.columns if col.startswith("GPRC_")]
    hist_cols = [col for col in df.columns if col.startswith("GPRHC_")]

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
    NodeSpec(id="geopolitical-risk-index-gpr-country-monthly", fn=fetch_country_monthly),
    NodeSpec(id="geopolitical-risk-index-gpr-daily", fn=fetch_daily),
    NodeSpec(id="geopolitical-risk-index-gpr-monthly", fn=fetch_monthly),
]

