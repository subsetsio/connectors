"""FHWA connector — Federal Highway Administration datasets on USDOT's Socrata
portal (datahub.transportation.gov).

Mechanism: Socrata (chosen by rank, api_suitability 85). Each subset is one
Socrata 4x4 dataset, exported in full as JSON via /resource/<id>.json with
$limit/$offset paging ($order=:id for stable pages). No auth required.

Fetch shape: stateless full re-pull. Small tables are fetched through the
Socrata JSON API and written as NDJSON because values arrive as strings and
null fields are omitted per row. The six HPMS roadway-section snapshots are
12M-29M rows each, so they stream Socrata's CSV export through a bounded
CSV-to-NDJSON conversion instead of accumulating JSON pages in memory. NDJSON
keeps the raw SQL-readable without relying on DuckDB CSV sampling to discover
late quoted comma fields.
"""

import csv
import json

from subsets_utils import (
    NodeSpec,
    get,
    get_client,
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
_VIEWS = "https://datahub.transportation.gov/api/views"
_PAGE = 50000           # small-table JSON page size
_MAX_PAGES = 1000       # safety ceiling — raises on hit, never silently truncates
_STREAM_CHUNK = 1024 * 1024


def _fetch_page(fxf: str, offset: int) -> list[dict]:
    resp = get(
        f"{_BASE}/{fxf}.json",
        params={"$limit": _PAGE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id                      # the spec id IS the asset name
    fxf = node_id[len("fhwa-"):]         # recover the Socrata 4x4 id

    if fxf in ROADWAY_ENTITY_IDS:
        url = f"{_VIEWS}/{fxf}/rows.csv?accessType=DOWNLOAD"
        with get_client().stream("GET", url, timeout=(10.0, 300.0)) as resp:
            resp.raise_for_status()
            reader = csv.DictReader(resp.iter_lines())
            with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
                for row in reader:
                    out.write(json.dumps(row, separators=(",", ":")))
                    out.write("\n")
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
