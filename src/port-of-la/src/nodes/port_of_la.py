"""Port of Los Angeles connector.

Source: City of Los Angeles Socrata portal (data.lacity.org). The Port of LA
publishes its statistical datasets there; each dataset is a stable 4x4 Socrata
resource id fetched via the SODA JSON endpoint
(https://data.lacity.org/resource/<id>.json).

Fetch shape: stateless full re-pull. Every dataset in scope is a small static
historical table (tens to ~100 rows), so each refresh re-pulls the whole table
in one paginated request and overwrites. No watermark/cursor — these tables no
longer update and full re-pull is trivially cheap. SODA returns every field as
a JSON string and some columns are sparsely populated, so raw is saved as NDJSON
and the transform SQL does the typing/casting.
"""

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://data.lacity.org/resource"
PAGE_SIZE = 50000  # all datasets here are far smaller than one page

# The entity union — rank-active Port-of-LA datasets (Socrata 4x4 ids).
# Copied from data/sources/port-of-la/work/entity_union.json.
ENTITY_IDS = [
    "2t3h-my34",  # Emission from Port Operations (2005-2012)
    "38a8-tm7u",  # Historical TEU Statistics
    "5a4i-e2zs",  # Historic Tonnage Data Short Ton (1920-1970)
    "i9rh-q5gx",  # Historic Tonnage Data MMRT
    "jmt8-y5rm",  # Cruise Passenger (1990-2014)
    "tsuv-4rgh",  # TEU Counts Monthly And Calendar YTD
]


@transient_retry()
def _fetch_page(resource_id: str, offset: int) -> list:
    url = f"{BASE}/{resource_id}.json"
    resp = get(
        url,
        params={"$limit": PAGE_SIZE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    """Fetch a single Socrata dataset in full and save it as NDJSON.

    The runtime passes the spec id (e.g. 'port-of-la-tsuv-4rgh'); the asset name
    IS that id. Recover the Socrata resource id by stripping the slug prefix.
    """
    asset = node_id
    resource_id = node_id[len("port-of-la-"):]

    rows = []
    offset = 0
    while True:
        page = _fetch_page(resource_id, offset)
        rows.extend(page)
        if len(page) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        if offset > 5_000_000:  # safety ceiling — these tables are tiny
            raise RuntimeError(
                f"{resource_id}: exceeded {offset} rows; source grew unexpectedly"
            )

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"port-of-la-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published table per dataset. SODA delivers every field as a string, so the
# SQL casts to typed columns. Each query reads the dataset's NDJSON view.
_TRANSFORM_SQL = {
    "port-of-la-2t3h-my34": '''
        SELECT
            CAST(ei_year AS INTEGER) AS year,
            TRY_CAST(nox_tpy AS DOUBLE) AS nox_tpy,
            TRY_CAST(sox_tpy AS DOUBLE) AS sox_tpy,
            TRY_CAST(dpm_tpy AS DOUBLE) AS dpm_tpy
        FROM "port-of-la-2t3h-my34"
        WHERE ei_year IS NOT NULL
    ''',
    "port-of-la-38a8-tm7u": '''
        SELECT
            CAST(year AS INTEGER) AS year,
            TRY_CAST(teus_in_million AS DOUBLE) AS teus_in_million
        FROM "port-of-la-38a8-tm7u"
        WHERE year IS NOT NULL
    ''',
    "port-of-la-5a4i-e2zs": '''
        SELECT
            CAST(year AS INTEGER) AS year,
            TRY_CAST(tons AS BIGINT) AS tons
        FROM "port-of-la-5a4i-e2zs"
        WHERE year IS NOT NULL
    ''',
    "port-of-la-i9rh-q5gx": '''
        SELECT
            CAST(year AS INTEGER) AS year,
            TRY_CAST(dry_bulk AS DOUBLE) AS dry_bulk,
            TRY_CAST(liquid_bulk AS DOUBLE) AS liquid_bulk,
            TRY_CAST(general_cargo AS DOUBLE) AS general_cargo,
            TRY_CAST(total AS DOUBLE) AS total
        FROM "port-of-la-i9rh-q5gx"
        WHERE year IS NOT NULL
    ''',
    "port-of-la-jmt8-y5rm": '''
        SELECT
            CAST(year AS INTEGER) AS year,
            TRY_CAST(ship_calls AS INTEGER) AS ship_calls,
            TRY_CAST(passengers AS BIGINT) AS passengers,
            TRY_CAST(passengers_per_ship AS INTEGER) AS passengers_per_ship
        FROM "port-of-la-jmt8-y5rm"
        WHERE year IS NOT NULL
    ''',
    "port-of-la-tsuv-4rgh": '''
        SELECT
            CAST(date AS DATE) AS date,
            month_year,
            TRY_CAST(monthly_total_teus AS DOUBLE) AS monthly_total_teus,
            TRY_CAST(cytd_total_teus AS DOUBLE) AS cytd_total_teus,
            TRY_CAST(previous_year_cytd AS DOUBLE) AS previous_year_cytd,
            TRY_CAST(change_total_teus_cytd AS DOUBLE) AS pct_change_total_teus_cytd
        FROM "port-of-la-tsuv-4rgh"
        WHERE date IS NOT NULL
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_TRANSFORM_SQL[s.id],
    )
    for s in DOWNLOAD_SPECS
]
