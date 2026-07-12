"""Chartbook of Economic Inequality connector.

Single-dataset academic source: one tidy/long Excel file (DataInput...xls) holds
the entire corpus — 25 countries, ~1900-2015, 5 inequality dimensions. The file
is small (~2MB, 18792 rows), static, and has no incremental query surface, so the
fetch is a stateless full re-pull: download the .xls, parse it to a long table,
overwrite the raw parquet. A MaintainSpec (later step) gates whether this runs.

The published subset filters to rows that actually carry a value (~4799 of 18792;
the source pre-materializes every (country, year, dimension, series) slot, most
empty) and types the columns.
"""
import io
import re

import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet

XLS_URL = (
    "https://chartbookofeconomicinequality.com/wp-content/uploads/"
    "DataForDownload/DataInput_ChartbookOfEconomicInequality.xls"
)

# The .xls sheet header (note the upstream typo 'meaure'); we rename to clean
# snake_case below.
_COLUMNS = [
    "country",
    "year",
    "dimension",
    "measure",
    "series_key",
    "series",
    "description",
    "value",
]

SCHEMA = pa.schema([
    ("country", pa.string()),
    ("year", pa.int64()),
    ("dimension", pa.string()),
    ("measure", pa.string()),
    ("series_key", pa.string()),
    ("series", pa.int64()),
    ("description", pa.string()),
    ("value", pa.float64()),
])

_SERIES_FILTERS = {
    "dispersion-of-earnings-gini-coefficient": ("Dispersion of Earnings", "Gini Coefficient"),
    "dispersion-of-earnings-p25-p50": ("Dispersion of Earnings", "P25/P50"),
    "dispersion-of-earnings-p80-p50": ("Dispersion of Earnings", "P80/P50"),
    "dispersion-of-earnings-p90-p50": ("Dispersion of Earnings", "P90/P50"),
    "dispersion-of-earnings-p90-p50-ratio": ("Dispersion of Earnings", "P90/P50 ratio"),
    "overall-income-inequality-gini-coefficient": ("Overall Income Inequality", "Gini Coefficient"),
    "poverty-measures-poverty-rate": ("Poverty Measures", "Poverty rate"),
    "top-income-shares-top-0-01pct": ("Top Income Shares", "Top 0.01%"),
    "top-income-shares-top-0-05pct": ("Top Income Shares", "Top 0.05%"),
    "top-income-shares-top-0-1pct": ("Top Income Shares", "Top 0.1%"),
    "top-income-shares-top-0-5pct": ("Top Income Shares", "Top 0.5%"),
    "top-income-shares-top-1pct": ("Top Income Shares", "Top 1%"),
    "wealth-inequality-gini-coefficient": ("Wealth Inequality", "Gini Coefficient"),
    "wealth-inequality-top-1pct": ("Wealth Inequality", "Top 1%"),
}

_SPEC_PREFIX = "chartbook-economic-inequality-"


def _download_xls() -> bytes:
    resp = get(XLS_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _slug(*parts: object) -> str:
    slug = "-".join(str(part).strip() for part in parts).lower()
    slug = slug.replace("%", "pct").replace("/", "-")
    return re.sub(r"[^a-z0-9]+", "-", slug).strip("-")


def _read_chartbook() -> pd.DataFrame:
    raw = _download_xls()
    df = pd.read_excel(io.BytesIO(raw), sheet_name=0, engine="xlrd", keep_default_na=False)
    if list(df.columns) != [
        "country", "year", "dimension of inequality", "meaure of inequality",
        "series", "description", "value",
    ]:
        raise AssertionError(f"unexpected sheet header: {list(df.columns)!r}")
    df.columns = ["country", "year", "dimension", "measure", "series", "description", "value"]

    for col in ["country", "dimension", "measure", "description"]:
        df[col] = df[col].astype("string").str.strip()

    # 'series' is a 1/2/3 series number; nullable in the source for empty slots.
    # Coerce numerics explicitly because keep_default_na=False preserves text
    # placeholders such as "N/A" that pandas would otherwise turn into floats.
    df["series"] = pd.to_numeric(df["series"], errors="coerce").astype("Int64")
    df["year"] = pd.to_numeric(df["year"], errors="raise").astype("int64")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["series_key"] = [_slug(dim, measure) for dim, measure in zip(df["dimension"], df["measure"])]
    return df


def _save_frame(df: pd.DataFrame, asset_id: str) -> None:
    table = pa.Table.from_pandas(df[_COLUMNS], schema=SCHEMA, preserve_index=False)
    save_raw_parquet(table, asset_id)


def fetch_values(node_id: str) -> None:
    _save_frame(_read_chartbook(), node_id)


def fetch_series(node_id: str) -> None:
    entity_id = node_id.removeprefix(_SPEC_PREFIX)
    try:
        dimension, measure = _SERIES_FILTERS[entity_id]
    except KeyError as exc:
        raise AssertionError(f"unknown Chartbook series entity: {entity_id}") from exc
    df = _read_chartbook()
    filtered = df[(df["dimension"] == dimension) & (df["measure"] == measure)]
    if filtered.empty:
        raise AssertionError(f"no rows found for {dimension!r} / {measure!r}")
    _save_frame(filtered, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="chartbook-economic-inequality-chartbook-inequality-values",
        fn=fetch_values,
        kind="download",
    ),
    *[
        NodeSpec(
            id=f"chartbook-economic-inequality-{entity_id}",
            fn=fetch_series,
            kind="download",
        )
        for entity_id in sorted(_SERIES_FILTERS)
    ],
]
