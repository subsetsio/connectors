"""agricoop — agriculture datasets from the data.gov.in Open Government Data
platform (Ministry / Department of Agriculture & Farmers Welfare, India).

Catalog connector: one download node per rank-accepted collect entity. Each
entity maps to exactly one data.gov.in resource (index_name), fetched via the
REST resource endpoint (research mechanism `ogd_rest`):

    https://api.data.gov.in/resource/{resource_id}?api-key=KEY&format=json&offset=&limit=

Records are flat, typed dicts whose columns differ per resource, so raw is written
as NDJSON and each transform is a thin per-resource SELECT (rename + light typing,
drop OGD plumbing columns).

Fetch shape: stateless full re-pull (shape 1). The built resources are bounded
(36 .. 246k rows) admin/statistical tables; the resource endpoint exposes no
since/modifiedAfter filter (research), so a watermark would buy nothing — we
re-fetch each resource in full and overwrite.

Auth: `api-key` is a QUERY parameter. A registered key is read from
DATA_GOV_IN_API_KEY when present; otherwise the public sample key is used. The
sample key both throttles aggressively (HTTP 429) and silently caps each page at
10 rows, so a registered key is required in production — the page loop advances by
the *actual* batch size (not the requested limit) so a capped key cannot silently
skip rows, and the MAX_PAGES ceiling raises loudly rather than truncating.
"""

import os

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_IDS, RESOURCE_ID

SLUG = "agricoop"
_PREFIX = f"{SLUG}-"
_BASE = "https://api.data.gov.in/resource/"
_SAMPLE_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
_PAGE = 1000
# Safety ceiling. With a registered key (full pages) the largest built resource
# (~246k rows) is ~250 pages; hitting this means either the resource grew far
# past expectations or an unregistered key capped pages at 10 rows — either way,
# raise rather than silently truncate or run for hours.
_MAX_PAGES = 5000


def _api_key() -> str:
    return os.environ.get("DATA_GOV_IN_API_KEY") or _SAMPLE_KEY


@transient_retry()
def _fetch_page(resource_id: str, offset: int) -> dict:
    resp = get(
        _BASE + resource_id,
        params={
            "api-key": _api_key(),
            "format": "json",
            "offset": offset,
            "limit": _PAGE,
        },
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len(_PREFIX):]
    resource_id = RESOURCE_ID[entity_id]

    rows: list[dict] = []
    offset = 0
    total = None
    pages = 0
    while True:
        payload = _fetch_page(resource_id, offset)
        if total is None:
            total = int(payload.get("total") or 0)
        batch = payload.get("records") or []
        rows.extend(batch)
        pages += 1
        # Advance by the rows actually returned, never the requested limit — a
        # throttled/sample key caps the page below `limit`, and advancing by
        # `limit` would skip the unseen rows silently.
        offset += len(batch)
        if not batch or offset >= total:
            break
        if pages >= _MAX_PAGES:
            raise RuntimeError(
                f"{asset}: exceeded {_MAX_PAGES} pages (total={total}, fetched={offset}) "
                "— resource larger than expected or page size capped (unregistered "
                "API key?); investigate before raising the cap"
            )

    # Heterogeneous schema across resources, flat typed records -> NDJSON.
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# ---- transforms: one published Delta table per resource -------------------
# Thin per-resource SELECT: rename to clean names, drop OGD plumbing columns
# (id / timestamp / row-number), TRY_CAST numeric measures (never fails the node;
# nulls on a genuinely non-numeric value). 0 rows fails the node by design.

_T = {
    # District/season crop area & production from 1997 (flagship panel).
    "agricoop-district-wise-season-wise-crop-production-statistics-from-19-c33a2e6b": '''
        SELECT
            state_name,
            district_name,
            TRY_CAST(crop_year AS INTEGER) AS crop_year,
            season,
            crop,
            TRY_CAST(area_ AS DOUBLE)       AS area,
            TRY_CAST(production_ AS DOUBLE) AS production
        FROM "{dep}"
        WHERE crop IS NOT NULL
    ''',
    # Current daily wholesale (mandi) prices snapshot.
    "agricoop-current-daily-price-of-various-commodities-from-various-mark-1abe392e": '''
        SELECT
            state,
            district,
            market,
            commodity,
            variety,
            grade,
            arrival_date,
            TRY_CAST(min_price AS DOUBLE)   AS min_price,
            TRY_CAST(max_price AS DOUBLE)   AS max_price,
            TRY_CAST(modal_price AS DOUBLE) AS modal_price
        FROM "{dep}"
        WHERE commodity IS NOT NULL
    ''',
    # Land Use Statistics — classified area by district/year/land-use class.
    "agricoop-classified-area-under-land-use-statistics-lus-3db3addf": '''
        SELECT
            state,
            district,
            year,
            class_name,
            TRY_CAST(area_in_ha AS DOUBLE) AS area_in_ha
        FROM "{dep}"
        WHERE state IS NOT NULL
    ''',
    # Land Use Statistics — irrigated area by district/year/water source.
    "agricoop-source-wise-irrigated-area-under-land-use-statistics-lus-3c17d7f6": '''
        SELECT
            state,
            district,
            year,
            irrigationsource AS irrigation_source,
            TRY_CAST(irrigatedareainha AS DOUBLE) AS irrigated_area_in_ha
        FROM "{dep}"
        WHERE state IS NOT NULL
    ''',
    # Agriculture Census — operational holdings (number & area) by state, 2 cycles.
    "agricoop-state-wise-number-and-area-of-operational-holdings-for-sched-2273cec3": '''
        SELECT
            state__ut AS state_ut,
            TRY_CAST(number___2010_11 AS DOUBLE) AS number_2010_11,
            TRY_CAST(area___2010_11 AS DOUBLE)   AS area_2010_11,
            TRY_CAST(number___2005_06 AS DOUBLE) AS number_2005_06,
            TRY_CAST(area___2005_06 AS DOUBLE)   AS area_2005_06
        FROM "{dep}"
        WHERE state__ut IS NOT NULL
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_T[s.id].format(dep=s.id),
    )
    for s in DOWNLOAD_SPECS
]
