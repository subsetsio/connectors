"""FHWA connector — Federal Highway Administration datasets on USDOT's Socrata
portal (datahub.transportation.gov).

Mechanism: Socrata (chosen by rank, api_suitability 85). Each subset is one
Socrata 4x4 dataset, exported in full as JSON via /resource/<id>.json with
$limit/$offset paging ($order=:id for stable pages). No auth required.

Fetch shape: stateless full re-pull. Small tables are fetched through the
Socrata JSON API and written as NDJSON because values arrive as strings and
null fields are omitted per row. The six HPMS roadway-section snapshots are
12M-29M rows each, so they page Socrata's CSV API through a bounded
CSV-to-NDJSON conversion and verify count(*) before accepting the raw file.
NDJSON keeps the raw SQL-readable without relying on DuckDB CSV sampling to
discover late quoted comma fields.
"""

import csv
import json

from subsets_utils import (
    NodeSpec,
    get,
    raw_writer,
    save_raw_ndjson,
)

# Entity union — the rank-active FHWA Socrata datasets (4x4 ids).
ENTITY_IDS = [
    "4kzx-kud8",  # Roadway Sections South 2018
    "54nx-se7f",  # Public Road Mileage, Lane Miles, VMT (VMT-421C)
    "6bch-d3uv",  # Roadway Sections Mid-America 2018
    "8fiq-4cn6",  # Toll ID Elements
    "bm4c-faz3",  # Roadway Sections North 2018
    "hvfw-tcmn",  # Net Motor Fuel Volume Taxed by State (MF-202)
    "ihrz-ddnk",  # Roadway Sections Mid-America 2019
    "ix2d-bsqq",  # Revenues Used by States for Highways (SF-1)
    "jc5k-rzm8",  # Highway Performance Monitoring System (HPMS)
    "mt5m-skz3",  # Truck Size and Weight Enforcement Data
    "nhvr-exvq",  # Highway Data Element Dictionary
    "rkzg-z7ht",  # Roadway Sections West 2019
    "taz8-hut2",  # Status of the Highway Trust Fund (FE-210)
    "v9ae-hsuk",  # Roadway Sections West 2018
]

ROADWAY_ENTITY_IDS = {
    "4kzx-kud8",
    "6bch-d3uv",
    "bm4c-faz3",
    "ihrz-ddnk",
    "rkzg-z7ht",
    "v9ae-hsuk",
}

_BASE = "https://datahub.transportation.gov/resource"
_PAGE = 50000           # small-table JSON page size
_MAX_PAGES = 1000       # safety ceiling — raises on hit, never silently truncates
_ROADWAY_REQUIRED_COLUMNS = {"route_id", "year_record"}


def _fetch_page(fxf: str, offset: int) -> list[dict]:
    resp = get(
        f"{_BASE}/{fxf}.json",
        params={"$limit": _PAGE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def _source_count(fxf: str) -> int:
    resp = get(
        f"{_BASE}/{fxf}.json",
        params={"$select": "count(*)"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return int(resp.json()[0]["count"])


def _fetch_csv_page(fxf: str, offset: int) -> list[dict]:
    resp = get(
        f"{_BASE}/{fxf}.csv",
        params={"$limit": _PAGE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    reader = csv.DictReader(resp.text.splitlines())
    fieldnames = {field.lower() for field in (reader.fieldnames or [])}
    if not _ROADWAY_REQUIRED_COLUMNS.issubset(fieldnames):
        raise RuntimeError(
            f"{fxf}: CSV page at offset {offset} did not have roadway columns; "
            f"got {reader.fieldnames!r}"
        )
    return list(reader)


def fetch_one(node_id: str) -> None:
    asset = node_id                      # the spec id IS the asset name
    fxf = node_id[len("fhwa-"):]         # recover the Socrata 4x4 id

    if fxf in ROADWAY_ENTITY_IDS:
        expected_rows = _source_count(fxf)
        rows_written = 0
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
            while rows_written < expected_rows:
                batch = _fetch_csv_page(fxf, rows_written)
                if not batch:
                    break
                for row in batch:
                    out.write(json.dumps(row, separators=(",", ":")))
                    out.write("\n")
                rows_written += len(batch)
        if rows_written != expected_rows:
            raise RuntimeError(
                f"{asset}: downloaded {rows_written} rows, expected {expected_rows} "
                "from Socrata count(*)"
            )
        return

    rows: list[dict] = []
    for page in range(_MAX_PAGES):
        batch = _fetch_page(fxf, page * _PAGE)
        rows.extend(batch)
        if len(batch) < _PAGE:
            break
    else:
        raise RuntimeError(
            f"{asset}: hit _MAX_PAGES={_MAX_PAGES} ({_PAGE} rows/page) without "
            f"draining the dataset — source grew past expectations"
        )

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"fhwa-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
