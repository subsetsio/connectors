"""Allen-Unger Global Commodity Prices connector.

Single static academic deposit archived on the DANS Data Station (a Dataverse
instance, persistent DOI 10.17026/dans-zsu-xavf, "The Allen Unger Commodities
Dataset", v2.1). The original publisher site (gcpdb.info) is dead, so DANS is the
canonical source. The deposit holds three ingested tables; only the core price
table (Commodities, fileId 183974) clears the publish threshold.

Fetch shape: stateless full re-pull. The deposit is a single ~37MB tab file that
downloads whole in one request and fits comfortably in RAM, so there is no
watermark/cursor — every run re-fetches and overwrites. Freshness (whether to run
at all) is the maintain step's job; a deposit version bump would be picked up for
free on the next run.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

DATAVERSE_BASE = "https://ssh.datastations.nl/api"
# fileId of Commodities.tab inside DANS deposit doi:10.17026/dans-zsu-xavf.
COMMODITIES_FILE_ID = 183974

# Header of the upstream tab file, in order — asserted on every fetch so a silent
# upstream schema change trips loudly instead of misaligning columns.
SOURCE_HEADER = [
    "Commodity", "Variety", "Market", "Original Measure", "Standard Measure",
    "Original Currency", "Standard Currency", "Item_Years",
    "Item_Value_Original", "Item_Value_Standardized", "Notes", "Source_Raw",
]

RAW_COLUMNS = [
    "commodity", "variety", "market", "original_measure", "standard_measure",
    "original_currency", "standard_currency", "item_year",
    "item_value_original", "item_value_standardized", "notes", "source_raw",
]

SCHEMA = pa.schema([
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
])


@transient_retry()
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


def fetch_commodities(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    # Free-text Notes/Source_Raw fields carry U+FFFD replacement chars baked in at
    # DANS ingest time (a lossy non-UTF8 -> UTF-8 conversion upstream); errors=
    # "replace" keeps the decode total and never touches the numeric/key columns.
    text = _download_tab(COMMODITIES_FILE_ID).decode("utf-8", errors="replace")
    reader = csv.reader(io.StringIO(text), delimiter="\t")
    header = next(reader)
    if header != SOURCE_HEADER:
        raise AssertionError(f"unexpected upstream header: {header}")

    cols = {name: [] for name in RAW_COLUMNS}
    for row in reader:
        if not row:
            continue
        if len(row) != 12:
            raise AssertionError(f"ragged row ({len(row)} cols): {row[:3]}")
        cols["commodity"].append(_clean(row[0]))
        cols["variety"].append(_clean(row[1]))
        cols["market"].append(_clean(row[2]))
        cols["original_measure"].append(_clean(row[3]))
        cols["standard_measure"].append(_clean(row[4]))
        cols["original_currency"].append(_clean(row[5]))
        cols["standard_currency"].append(_clean(row[6]))
        cols["item_year"].append(_to_int(row[7]))
        cols["item_value_original"].append(_to_float(row[8]))
        cols["item_value_standardized"].append(_to_float(row[9]))
        cols["notes"].append(_clean(row[10]))
        cols["source_raw"].append(_clean(row[11]))

    table = pa.table({name: cols[name] for name in RAW_COLUMNS}, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="allen-unger-commodity-prices-commodities",
        fn=fetch_commodities,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="allen-unger-commodity-prices-commodities-transform",
        deps=["allen-unger-commodity-prices-commodities"],
        sql='''
            SELECT
                commodity,
                variety,
                market,
                original_measure,
                standard_measure,
                original_currency,
                standard_currency,
                CAST(item_year AS INTEGER)        AS year,
                item_value_original               AS value_original,
                item_value_standardized           AS value_standardized,
                notes,
                source_raw                        AS source
            FROM "allen-unger-commodity-prices-commodities"
            WHERE item_year IS NOT NULL
              AND commodity IS NOT NULL
              AND market IS NOT NULL
        ''',
    ),
]
