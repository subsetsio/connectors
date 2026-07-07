import csv
import io
import re

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pacsv

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    raw_parquet_writer,
    record_source_signature,
    source_unchanged,
)


CONCEPT_RECID = "4479171"
LATEST_RECORD_URL = (
    "https://zenodo.org/api/records"
    f"?q=conceptrecid:{CONCEPT_RECID}&sort=mostrecent&size=1"
)

DIMENSION_RENAMES = {
    "source": "source",
    "scenario (PRIMAP-hist)": "scenario",
    "provenance": "provenance",
    "area (ISO3)": "area",
    "entity": "entity",
    "unit": "unit",
    "category (IPCC2006_PRIMAP)": "category",
}

RAW_SCHEMA = pa.schema(
    [
        pa.field("source", pa.string()),
        pa.field("scenario", pa.string()),
        pa.field("provenance", pa.string()),
        pa.field("area", pa.string()),
        pa.field("entity", pa.string()),
        pa.field("unit", pa.string()),
        pa.field("category", pa.string()),
        pa.field("year", pa.int16()),
        pa.field("value", pa.float64()),
        pa.field("release_version", pa.string()),
        pa.field("release_doi", pa.string()),
    ]
)


def _latest_record() -> dict:
    response = get(LATEST_RECORD_URL, timeout=(10.0, 60.0))
    response.raise_for_status()
    hits = response.json()["hits"]["hits"]
    if not hits:
        raise RuntimeError(f"No Zenodo records found for conceptrecid {CONCEPT_RECID}")
    return hits[0]


def _selected_csv_file(record: dict) -> dict:
    version = record.get("metadata", {}).get("version")
    if not version:
        raise RuntimeError("Latest Zenodo record is missing metadata.version")

    pattern = re.compile(
        rf"PRIMAP-hist_v{re.escape(version)}_final_\d{{2}}-[A-Za-z]{{3}}-\d{{4}}\.csv$"
    )
    matches = [
        file_info
        for file_info in record.get("files", [])
        if pattern.search(file_info.get("key", ""))
    ]
    if len(matches) != 1:
        keys = [file_info.get("key") for file_info in record.get("files", [])]
        raise RuntimeError(
            f"Expected one standard final CSV for PRIMAP-hist v{version}; "
            f"found {len(matches)} in {keys}"
        )
    return matches[0]


def _read_wide_csv(content: bytes) -> tuple[pa.Table, list[str]]:
    header_line = content.splitlines()[0].decode("utf-8")
    columns = next(csv.reader([header_line]))
    year_columns = [column for column in columns if column.isdigit()]
    if not year_columns:
        raise RuntimeError("PRIMAP-hist CSV has no year columns")

    column_types = {
        column: pa.string()
        for column in DIMENSION_RENAMES
    } | {
        column: pa.float64()
        for column in year_columns
    }

    table = pacsv.read_csv(
        pa.BufferReader(content),
        convert_options=pacsv.ConvertOptions(
            column_types=column_types,
            null_values=["", "NA", "NaN"],
            strings_can_be_null=True,
        ),
    )
    return table, year_columns


def _long_table_for_year(
    wide: pa.Table,
    year_column: str,
    release_version: str,
    release_doi: str,
) -> pa.Table:
    n_rows = wide.num_rows
    value = wide[year_column]
    arrays = [
        wide[source_name]
        for source_name in DIMENSION_RENAMES
    ]
    arrays.extend(
        [
            pa.array([int(year_column)] * n_rows, type=pa.int16()),
            value,
            pa.array([release_version] * n_rows, type=pa.string()),
            pa.array([release_doi] * n_rows, type=pa.string()),
        ]
    )
    table = pa.Table.from_arrays(arrays, schema=RAW_SCHEMA)
    return table.filter(pc.is_valid(table["value"]))


def fetch_emissions(node_id: str) -> None:
    record = _latest_record()
    csv_file = _selected_csv_file(record)
    csv_url = csv_file["links"]["self"]

    response = get(csv_url, timeout=(10.0, 600.0))
    response.raise_for_status()

    wide, year_columns = _read_wide_csv(response.content)
    release_version = record["metadata"]["version"]
    release_doi = record["doi"]

    with raw_parquet_writer(node_id, RAW_SCHEMA) as writer:
        for year_column in year_columns:
            table = _long_table_for_year(
                wide,
                year_column,
                release_version,
                release_doi,
            )
            if table.num_rows:
                writer.write_table(table)

    record_source_signature(node_id, csv_url, response=response)


DOWNLOAD_SPECS = [
    NodeSpec(id="primap-hist-emissions", fn=fetch_emissions, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="primap-hist-emissions",
        description=(
            "PRIMAP-hist is versioned on Zenodo and has recent March/September "
            "releases; skip only when the latest CSV validator is unchanged."
        ),
        check=lambda asset_id: source_unchanged(
            asset_id,
            _selected_csv_file(_latest_record())["links"]["self"],
        )
        and raw_asset_exists(asset_id, "parquet"),
    ),
]
