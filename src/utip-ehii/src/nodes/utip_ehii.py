from io import BytesIO

import pandas as pd
import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    record_source_signature,
    save_raw_parquet,
    source_unchanged,
)


EHII_URL = "http://www.utip.lbj.utexas.edu/data/UtipUnidoEhiiV2017_v.1.xlsx"
YEAR_PREFIX = "y"

SCHEMA = pa.schema(
    [
        pa.field("country_code", pa.int64()),
        pa.field("country_alpha3", pa.string()),
        pa.field("country_name", pa.string()),
        pa.field("measure", pa.string()),
        pa.field("year", pa.int16()),
        pa.field("value", pa.float64()),
    ]
)


def _sheet_to_rows(content: bytes, sheet_name: str) -> list[dict]:
    df = pd.read_excel(BytesIO(content), sheet_name=sheet_name, engine="openpyxl")
    expected_prefix = ["country", "code", "countryname"]
    if list(df.columns[:3]) != expected_prefix:
        raise ValueError(f"{sheet_name}: unexpected leading columns {list(df.columns[:3])}")

    value_columns = [
        col
        for col in df.columns
        if isinstance(col, str) and col.startswith(YEAR_PREFIX) and col[1:].isdigit()
    ]
    if value_columns[0] != "y1963" or value_columns[-1] != "y2015":
        raise ValueError(f"{sheet_name}: unexpected year range {value_columns[0]}-{value_columns[-1]}")

    long = df.melt(
        id_vars=expected_prefix,
        value_vars=value_columns,
        var_name="year",
        value_name="value",
    ).dropna(subset=["value"])
    long["measure"] = sheet_name
    long["year"] = long["year"].str.removeprefix(YEAR_PREFIX).astype("int16")
    long = long.rename(
        columns={
            "country": "country_code",
            "code": "country_alpha3",
            "countryname": "country_name",
        }
    )

    rows = long[
        ["country_code", "country_alpha3", "country_name", "measure", "year", "value"]
    ].to_dict(orient="records")
    for row in rows:
        row["country_code"] = int(row["country_code"])
        row["country_alpha3"] = str(row["country_alpha3"])
        row["country_name"] = str(row["country_name"])
        row["year"] = int(row["year"])
        row["value"] = float(row["value"])
    return rows


def fetch_ehii(node_id: str) -> None:
    response = get(EHII_URL, timeout=(10.0, 120.0))
    response.raise_for_status()

    rows = []
    for sheet_name in ("gini", "theil"):
        rows.extend(_sheet_to_rows(response.content, sheet_name))

    if not rows:
        raise ValueError("EHII workbook produced no observations")

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, node_id)
    record_source_signature(node_id, EHII_URL, response=response)


DOWNLOAD_SPECS = [
    NodeSpec(id="utip-ehii-ehii", fn=fetch_ehii, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="utip-ehii-ehii",
        description=(
            "No published cadence; source page describes a revised 1963-2015 "
            "historical workbook. Freshness checked by HTTP ETag/Last-Modified."
        ),
        check=lambda asset_id: source_unchanged(asset_id, EHII_URL)
        and raw_asset_exists(asset_id, "parquet"),
    ),
]
