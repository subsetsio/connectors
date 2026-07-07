"""PVGIS country solar radiation and PV potential summaries."""

import io

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


WORKBOOKS = {
    "pvgis-country-stats-classic-2007": {
        "url": "https://re.jrc.ec.europa.eu/pvg_download/PVGIS_EU30_country_stats_Nov2007.xls",
        "filename": "PVGIS_EU30_country_stats_Nov2007.xls",
        "workbook_version": "classic_2007",
        "methodology": "classic PVGIS ground-station/interpolation inputs",
    },
    "pvgis-country-stats-classic-cmsaf-2012": {
        "url": "https://re.jrc.ec.europa.eu/pvg_download/PVGIS_EU33_country_stats_201208.xls",
        "filename": "PVGIS_EU33_country_stats_201208.xls",
        "workbook_version": "classic_cmsaf_2012",
        "methodology": "mixed classic PVGIS and CMSAF satellite-based inputs",
    },
}

DATA_SHEETS = {
    "g13_horizont",
    "g13_optim",
    "g13_vertical",
    "optimum angle",
    "opt_horiz",
    "opt_vert",
}

SCHEMA = pa.schema(
    [
        ("source_file", pa.string()),
        ("workbook_version", pa.string()),
        ("methodology", pa.string()),
        ("sheet", pa.string()),
        ("country_code", pa.string()),
        ("country_name", pa.string()),
        ("metric_group", pa.string()),
        ("statistic", pa.string()),
        ("value", pa.float64()),
    ]
)


def _country_lookup(book: pd.ExcelFile) -> dict[str, str]:
    explanation = pd.read_excel(book, sheet_name="explanation", header=None)
    countries: dict[str, str] = {}
    for _, row in explanation.iterrows():
        code = row.get(2)
        name = row.get(3)
        if isinstance(code, str) and isinstance(name, str):
            code = code.strip()
            if len(code) in (2, 3):
                countries[code] = name.strip()
    if len(countries) < 25:
        raise AssertionError(f"unexpected country lookup size: {len(countries)}")
    return countries


def _rows_from_workbook(content: bytes, meta: dict[str, str]) -> list[dict]:
    book = pd.ExcelFile(io.BytesIO(content), engine="xlrd")
    missing = DATA_SHEETS - set(book.sheet_names)
    if missing:
        raise AssertionError(f"missing expected sheets: {sorted(missing)}")

    countries = _country_lookup(book)
    rows: list[dict] = []
    for sheet in book.sheet_names:
        if sheet == "explanation":
            continue
        if sheet not in DATA_SHEETS:
            raise AssertionError(f"unexpected sheet: {sheet}")

        frame = pd.read_excel(book, sheet_name=sheet, header=None)
        metric_group = None
        for col_idx in range(1, frame.shape[1]):
            heading = frame.iat[0, col_idx]
            if pd.notna(heading):
                metric_group = str(heading).strip()

            statistic = frame.iat[1, col_idx]
            if metric_group is None or pd.isna(statistic):
                continue
            statistic = str(statistic).strip()

            for row_idx in range(2, len(frame)):
                country_code = frame.iat[row_idx, 0]
                value = frame.iat[row_idx, col_idx]
                if not isinstance(country_code, str) or pd.isna(value):
                    continue

                country_code = country_code.strip()
                if not country_code:
                    continue
                rows.append(
                    {
                        "source_file": meta["filename"],
                        "workbook_version": meta["workbook_version"],
                        "methodology": meta["methodology"],
                        "sheet": sheet,
                        "country_code": country_code,
                        "country_name": countries.get(country_code),
                        "metric_group": metric_group,
                        "statistic": statistic,
                        "value": float(value),
                    }
                )
    return rows


def fetch_country_stats(node_id: str) -> None:
    meta = WORKBOOKS[node_id]
    response = get(meta["url"], timeout=(10.0, 120.0))
    response.raise_for_status()
    rows = _rows_from_workbook(response.content, meta)
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, node_id)
    record_source_signature(node_id, meta["url"], response=response)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="pvgis-country-stats-classic-2007",
        fn=fetch_country_stats,
        kind="download",
    ),
    NodeSpec(
        id="pvgis-country-stats-classic-cmsaf-2012",
        fn=fetch_country_stats,
        kind="download",
    ),
]


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="pvgis-country-stats-classic-2007",
        description="Frozen historical workbook; skip when the source Last-Modified/ETag is unchanged.",
        check=lambda asset_id: source_unchanged(asset_id, WORKBOOKS[asset_id]["url"])
        and raw_asset_exists(asset_id, "parquet"),
    ),
    MaintainSpec(
        asset_id="pvgis-country-stats-classic-cmsaf-2012",
        description="Frozen historical workbook; skip when the source Last-Modified/ETag is unchanged.",
        check=lambda asset_id: source_unchanged(asset_id, WORKBOOKS[asset_id]["url"])
        and raw_asset_exists(asset_id, "parquet"),
    ),
]
