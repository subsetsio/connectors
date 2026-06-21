"""FHWA connector — Federal Highway Administration datasets on USDOT's Socrata
portal (datahub.transportation.gov).

Mechanism: Socrata (chosen by rank, api_suitability 85). Each subset is one
Socrata 4x4 dataset, exported in full as JSON via /resource/<id>.json with
$limit/$offset paging ($order=:id for stable pages). No auth required.

Fetch shape: stateless full re-pull. Every dataset is small (largest ~16.6k
rows), so we re-pull the whole table each run and overwrite — revisions and
late corrections are picked up for free. Raw is written as NDJSON because the
Socrata JSON API returns every value as a string and omits fields that are null
for a given row (e.g. VMT-421C has no lanemiles before 1980); NDJSON tolerates
that drift and the transform SQL re-types on read.
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

# Entity union — the rank-active FHWA Socrata datasets (4x4 ids).
ENTITY_IDS = [
    "54nx-se7f",  # Public Road Mileage, Lane Miles, VMT (VMT-421C)
    "hvfw-tcmn",  # Net Motor Fuel Volume Taxed by State (MF-202)
    "ix2d-bsqq",  # Revenues Used by States for Highways (SF-1)
    "mt5m-skz3",  # Truck Size and Weight Enforcement Data
    "taz8-hut2",  # Status of the Highway Trust Fund (FE-210)
]

_BASE = "https://datahub.transportation.gov/resource"
_PAGE = 50000           # Socrata serves large single pages; all tables fit well under this
_MAX_PAGES = 1000       # safety ceiling — raises on hit, never silently truncates


@transient_retry()
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

# ---------------------------------------------------------------------------
# Transforms — one published Delta table per subset. The Socrata JSON API hands
# every value back as a string, so each transform TRY_CASTs to the real type and
# drops rows whose key columns are null.
# ---------------------------------------------------------------------------

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fhwa-54nx-se7f-transform",
        deps=["fhwa-54nx-se7f"],
        sql='''
            SELECT
                CAST(year AS INTEGER)              AS year,
                TRY_CAST(roadmiles AS BIGINT)      AS public_road_miles,
                TRY_CAST(lanemiles AS BIGINT)      AS lane_miles,
                TRY_CAST(vmt AS BIGINT)            AS vehicle_miles_of_travel_millions
            FROM "fhwa-54nx-se7f"
            WHERE year IS NOT NULL AND TRY_CAST(year AS INTEGER) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="fhwa-hvfw-tcmn-transform",
        deps=["fhwa-hvfw-tcmn"],
        sql='''
            SELECT
                CAST(year AS INTEGER)        AS year,
                state                        AS state,
                TRY_CAST(gallons AS BIGINT)  AS gallons_taxed
            FROM "fhwa-hvfw-tcmn"
            WHERE year IS NOT NULL AND state IS NOT NULL
              AND TRY_CAST(year AS INTEGER) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="fhwa-ix2d-bsqq-transform",
        deps=["fhwa-ix2d-bsqq"],
        sql='''
            SELECT
                CAST(year AS INTEGER)        AS year,
                state                        AS state,
                revenues                     AS revenue_source,
                TRY_CAST(dollars AS BIGINT)  AS dollars
            FROM "fhwa-ix2d-bsqq"
            WHERE year IS NOT NULL AND state IS NOT NULL AND revenues IS NOT NULL
              AND TRY_CAST(year AS INTEGER) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="fhwa-mt5m-skz3-transform",
        deps=["fhwa-mt5m-skz3"],
        sql='''
            SELECT
                CAST(year AS INTEGER)                               AS year,
                state                                               AS state,
                TRY_CAST(vehicles_weighed_fixed AS BIGINT)          AS vehicles_weighed_fixed_scale,
                TRY_CAST(vehicles_weighed_wim AS BIGINT)            AS vehicles_weighed_wim_scale,
                TRY_CAST(vehicles_weighed_portable AS BIGINT)       AS vehicles_weighed_portable_scale,
                TRY_CAST(vehicles_weighed_semi_portable AS BIGINT)  AS vehicles_weighed_semi_portable_scale,
                TRY_CAST(oversize_violation_current_year AS BIGINT) AS oversize_violations,
                TRY_CAST(overweight_violation_current_year AS BIGINT) AS overweight_violations,
                TRY_CAST(non_divisible_trip_permits AS BIGINT)      AS non_divisible_trip_permits,
                TRY_CAST(non_divisible_annual_permits AS BIGINT)    AS non_divisible_annual_permits,
                TRY_CAST(divisible_trip_permits AS BIGINT)          AS divisible_trip_permits,
                TRY_CAST(divisible_annual_permits AS BIGINT)        AS divisible_annual_permits
            FROM "fhwa-mt5m-skz3"
            WHERE year IS NOT NULL AND state IS NOT NULL
              AND TRY_CAST(year AS INTEGER) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="fhwa-taz8-hut2-transform",
        deps=["fhwa-taz8-hut2"],
        sql='''
            SELECT
                CAST(fiscal_year AS INTEGER)      AS fiscal_year,
                TRY_CAST(receipts AS BIGINT)      AS receipts,
                TRY_CAST(expenditures AS BIGINT)  AS expenditures,
                TRY_CAST(balance AS BIGINT)       AS balance
            FROM "fhwa-taz8-hut2"
            WHERE fiscal_year IS NOT NULL
              AND TRY_CAST(fiscal_year AS INTEGER) IS NOT NULL
        ''',
    ),
]
