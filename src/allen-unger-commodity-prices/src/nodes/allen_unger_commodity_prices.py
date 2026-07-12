"""Allen-Unger Global Commodity Prices connector.

Single static academic deposit archived on the DANS Data Station (a Dataverse
instance, persistent DOI 10.17026/dans-zsu-xavf, "The Allen Unger Commodities
Dataset", v2.1). The original publisher site (gcpdb.info) is dead, so DANS is
the canonical source.

Fetch shape: stateless full re-pull. The deposit has three ingested TSV tables
that download whole in one request and fit comfortably in RAM, so there is no
watermark or cursor; every run re-fetches and overwrites.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet

DATAVERSE_BASE = "https://ssh.datastations.nl/api"
SLUG = "allen-unger-commodity-prices"

FILE_IDS = {
    "commodities": 183974,
    "currencies": 183975,
    "measures": 183973,
}

SOURCE_HEADERS = {
    "commodities": [
        "Commodity", "Variety", "Market", "Original Measure", "Standard Measure",
        "Original Currency", "Standard Currency", "Item_Years",
        "Item_Value_Original", "Item_Value_Standardized", "Notes", "Source_Raw",
    ],
    "currencies": [
        "Geography", "Variety", "Market", "Name", "Year", "Factor", "Unit",
        "Metal", "Source Location", "Source", "Notes", "Interpolated",
        "Constructed",
    ],
    "measures": [
        "Measure_Name", "Measure", "Measure_SubType", "Market", "Factor",
        "Units", "Type", "SubType", "Alternative_Name", "Source_Raw",
    ],
}

RAW_COLUMNS = {
    "commodities": [
        "commodity", "variety", "market", "original_measure", "standard_measure",
        "original_currency", "standard_currency", "item_year",
        "item_value_original", "item_value_standardized", "notes", "source_raw",
    ],
    "currencies": [
        "geography", "variety", "market", "name", "year", "factor", "unit",
        "metal", "source_location", "source", "notes", "interpolated",
        "constructed",
    ],
    "measures": [
        "measure_name", "measure", "measure_subtype", "market", "factor",
        "units", "type", "subtype", "alternative_name", "source_raw",
    ],
}

SCHEMAS = {
    "commodities": pa.schema([
        ("commodity", pa.string()),
        ("variety", pa.string()),
        ("market", pa.string()),
        ("original_measure", pa.string()),
        ("standard_measure", pa.string()),
        ("original_currency", pa.string()),
        ("standard_currency", pa.string()),
        ("item_year", pa.int64()),
        ("item_value_original", pa.float64()),
        ("item_value_standardized", pa.float64()),
        ("notes", pa.string()),
        ("source_raw", pa.string()),
    ]),
    "currencies": pa.schema([
        ("geography", pa.string()),
        ("variety", pa.string()),
        ("market", pa.string()),
        ("name", pa.string()),
        ("year", pa.int64()),
        ("factor", pa.float64()),
        ("unit", pa.string()),
        ("metal", pa.string()),
        ("source_location", pa.string()),
        ("source", pa.string()),
        ("notes", pa.string()),
        ("interpolated", pa.bool_()),
        ("constructed", pa.bool_()),
    ]),
    "measures": pa.schema([
        ("measure_name", pa.string()),
        ("measure", pa.string()),
        ("measure_subtype", pa.string()),
        ("market", pa.string()),
        ("factor", pa.float64()),
        ("units", pa.string()),
        ("type", pa.string()),
        ("subtype", pa.string()),
        ("alternative_name", pa.string()),
        ("source_raw", pa.string()),
    ]),
}

PARSERS = {
    "commodities": [
        "str", "str", "str", "str", "str", "str", "str", "int", "float",
        "float", "str", "str",
    ],
    "currencies": [
        "str", "str", "str", "str", "int", "float", "str", "str", "str",
        "str", "str", "bool", "bool",
    ],
    "measures": [
        "str", "str", "str", "str", "float", "str", "str", "str", "str",
        "str",
    ],
}


def _download_tab(file_id: int) -> bytes:
    # Ingested .tab is UTF-8 tab-separated (charset=UTF-8). The whole-dataset zip
    # and ?format=original CSV exist too, but the ingested .tab is the cleanest
    # single-request path.
    resp = get(f"{DATAVERSE_BASE}/access/datafile/{file_id}", timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _clean(value: str):
    value = value.strip()
    return value or None


def _to_int(value: str):
    value = value.strip()
    return int(value) if value else None


def _to_float(value: str):
    value = value.strip()
    return float(value) if value else None


def _to_bool(value: str):
    value = value.strip().upper()
    if not value:
        return None
    if value == "TRUE":
        return True
    if value == "FALSE":
        return False
    raise ValueError(f"unexpected boolean value: {value!r}")


def _parse(value: str, kind: str):
    if kind == "str":
        return _clean(value)
    if kind == "int":
        return _to_int(value)
    if kind == "float":
        return _to_float(value)
    if kind == "bool":
        return _to_bool(value)
    raise AssertionError(f"unknown parser kind: {kind}")


def _entity_from_node_id(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise AssertionError(f"unexpected node id: {node_id}")
    entity = node_id.removeprefix(prefix)
    if entity not in FILE_IDS:
        raise AssertionError(f"unknown entity: {entity}")
    return entity


def fetch_dataverse_table(node_id: str) -> None:
    entity = _entity_from_node_id(node_id)
    # Free-text fields carry occasional U+FFFD replacement chars baked in at DANS
    # ingest time; errors="replace" keeps the decode total and leaves keys/numeric
    # columns unaffected.
    text = _download_tab(FILE_IDS[entity]).decode("utf-8", errors="replace")
    reader = csv.reader(io.StringIO(text), delimiter="\t")
    header = next(reader)
    if header != SOURCE_HEADERS[entity]:
        raise AssertionError(f"unexpected upstream header: {header}")

    columns = RAW_COLUMNS[entity]
    parsers = PARSERS[entity]
    cols = {name: [] for name in columns}
    for row in reader:
        if not row:
            continue
        if len(row) != len(columns):
            raise AssertionError(f"ragged row ({len(row)} cols): {row[:3]}")
        for name, value, parser in zip(columns, row, parsers, strict=True):
            cols[name].append(_parse(value, parser))

    table = pa.table({name: cols[name] for name in columns}, schema=SCHEMAS[entity])
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="allen-unger-commodity-prices-commodities",
        fn=fetch_dataverse_table,
        kind="download",
    ),
    NodeSpec(
        id="allen-unger-commodity-prices-currencies",
        fn=fetch_dataverse_table,
        kind="download",
    ),
    NodeSpec(
        id="allen-unger-commodity-prices-measures",
        fn=fetch_dataverse_table,
        kind="download",
    ),
]
