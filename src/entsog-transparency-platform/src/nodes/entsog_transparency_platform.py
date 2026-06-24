"""ENTSOG Transparency Platform connector — EU gas TSO transparency reporting.

Source: the single public REST API at https://transparency.entsog.eu/api/v1
(no auth, offset pagination via limit/offset). Every endpoint returns the
envelope ``{"meta": {...}, "<endpoint>": [ {row}, ... ]}``.

Fetch strategy (see the per-fn docstrings):

* The six reference / event catalogs (operatorpointdirections, interruptions,
  cmpUnavailables, cmpUnsuccessfulRequests, tariffssimulations,
  urgentmarketmessages) are small finite corpora (hundreds to ~85k rows) that
  the API serves in full WITHOUT any date filter. They use a stateless full
  re-pull every run (shape 1 — revisions picked up for free).

* operationaldata is the large long-format time-series. The date-filtered query
  returns ~100-180k rows/month, so re-pulling the whole corpus each run is still
  only ~25 min, but it cannot live in one in-memory file. It is therefore
  written as one NDJSON batch per calendar month (date-bucketed firehose layout,
  shape 3) and re-pulled in full every run — stateless, so revisions and late
  corrections are never missed. Long-validity capacity records recur across
  monthly windows; the transform de-duplicates on the stable composite ``id``.

All values are stringified before the NDJSON write so every column reads back as
VARCHAR (read_json_auto unions columns across the monthly batch files); the SQL
transforms then TRY_CAST the handful of columns each subset actually publishes.
"""
import calendar
from datetime import datetime, timezone

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)
from constants import ENTITIES, SOURCE_MIN_YEAR, SOURCE_MIN_MONTH

BASE = "https://transparency.entsog.eu/api/v1"
PREFIX = "entsog-transparency-platform-"
PAGE = 10000
# Safety ceiling: a single month/endpoint window never approaches this many
# rows. If it does, the source has grown past expectations — raise loudly rather
# than silently truncate.
MAX_OFFSET = 5_000_000


@transient_retry()
def _get_page(endpoint: str, params: dict):
    """Fetch one page. Returns the parsed JSON envelope, or None when the server
    answers 404 — ENTSOG uses 404 for an empty date window (e.g. months with no
    data), which is a normal "nothing here", not an error to retry or raise on.
    transient_retry handles 429/5xx/network; a non-404 4xx raises (permanent)."""
    resp = get(f"{BASE}/{endpoint}", params=params, timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def _fetch_all(endpoint: str, base_params: dict) -> list[dict]:
    """Page through one endpoint+window via limit/offset until a short page."""
    rows: list[dict] = []
    offset = 0
    while True:
        params = dict(base_params, limit=PAGE, offset=offset)
        payload = _get_page(endpoint, params)
        if payload is None:  # 404 → empty window
            break
        batch = payload.get(endpoint, [])
        rows.extend(batch)
        if len(batch) < PAGE:
            break
        offset += PAGE
        if offset > MAX_OFFSET:
            raise RuntimeError(
                f"{endpoint} {base_params}: exceeded MAX_OFFSET={MAX_OFFSET} "
                "— source larger than expected, refusing to silently truncate"
            )
    return rows


def _stringify(row: dict) -> dict:
    """Coerce every value to a string (or None) so each NDJSON column reads back
    as a uniform VARCHAR regardless of the JSON type the API emitted."""
    return {k: (None if v is None else str(v)) for k, v in row.items()}


def _months(sy: int, sm: int, ey: int, em: int):
    """Yield (year, month) from (sy,sm) through (ey,em) inclusive."""
    y, m = sy, sm
    while (y, m) <= (ey, em):
        yield y, m
        m += 1
        if m > 12:
            m = 1
            y += 1


def fetch_simple(node_id: str) -> None:
    """Stateless full re-pull of one reference/event catalog. The endpoint is
    recovered from the spec id (the maintain step, authored later, decides
    whether this runs; if invoked, we fetch)."""
    endpoint = ENTITIES[node_id[len(PREFIX):]]
    rows = [_stringify(r) for r in _fetch_all(endpoint, {})]
    save_raw_ndjson(rows, node_id)


def fetch_operationaldata(node_id: str) -> None:
    """Stateless monthly-batched full re-pull of the operationaldata time-series.
    Loops month-by-month from the documented floor to the live edge (current
    month); empty/404 months are skipped. Each non-empty month is written as its
    own NDJSON batch (`<node_id>-YYYY-MM`) so memory stays bounded; the transform
    glob-unions and de-duplicates them on `id`."""
    now = datetime.now(timezone.utc)
    for y, m in _months(SOURCE_MIN_YEAR, SOURCE_MIN_MONTH, now.year, now.month):
        last = calendar.monthrange(y, m)[1]
        window = {"from": f"{y}-{m:02d}-01", "to": f"{y}-{m:02d}-{last:02d}"}
        rows = _fetch_all("operationaldata", window)
        if not rows:
            continue
        rows = [_stringify(r) for r in rows]
        save_raw_ndjson(rows, f"{node_id}-{y}-{m:02d}")


DOWNLOAD_SPECS = [
    NodeSpec(id="entsog-transparency-platform-operationaldata",
             fn=fetch_operationaldata, kind="download"),
    NodeSpec(id="entsog-transparency-platform-operatorpointdirections",
             fn=fetch_simple, kind="download"),
    NodeSpec(id="entsog-transparency-platform-interruptions",
             fn=fetch_simple, kind="download"),
    NodeSpec(id="entsog-transparency-platform-cmpunavailables",
             fn=fetch_simple, kind="download"),
    NodeSpec(id="entsog-transparency-platform-cmpunsuccessfulrequests",
             fn=fetch_simple, kind="download"),
    NodeSpec(id="entsog-transparency-platform-tariffssimulations",
             fn=fetch_simple, kind="download"),
    NodeSpec(id="entsog-transparency-platform-urgentmarketmessages",
             fn=fetch_simple, kind="download"),
]


# ---------------------------------------------------------------------------
# Transforms — one published Delta table per subset. Each is a thin de-dup +
# cast pass over its raw NDJSON view. Identifiers are matched case-insensitively
# by DuckDB, so the source camelCase column names resolve unquoted.
# ---------------------------------------------------------------------------

_OPERATIONALDATA_SQL = '''
WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-operationaldata"
)
SELECT
    id,
    indicator,
    periodType                                  AS period_type,
    TRY_CAST(periodFrom AS TIMESTAMP)           AS period_from,
    TRY_CAST(periodTo AS TIMESTAMP)             AS period_to,
    operatorKey                                 AS operator_key,
    operatorLabel                               AS operator_label,
    pointKey                                    AS point_key,
    pointLabel                                  AS point_label,
    directionKey                                AS direction_key,
    unit,
    TRY_CAST(NULLIF(value, '') AS DOUBLE)       AS value,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP)   AS last_update
FROM ranked
WHERE rn = 1 AND TRY_CAST(NULLIF(value, '') AS DOUBLE) IS NOT NULL
'''

_OPERATORPOINTDIRECTIONS_SQL = '''
WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-operatorpointdirections"
)
SELECT
    id,
    pointKey                            AS point_key,
    pointLabel                          AS point_label,
    operatorKey                         AS operator_key,
    operatorLabel                       AS operator_label,
    directionKey                        AS direction_key,
    TRY_CAST(validFrom AS TIMESTAMP)    AS valid_from,
    TRY_CAST(validTo AS TIMESTAMP)      AS valid_to,
    tSOCountry                          AS tso_country,
    tSOBalancingZone                    AS tso_balancing_zone,
    crossBorderPointType               AS cross_border_point_type,
    pointType                           AS point_type,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP) AS last_update
FROM ranked
WHERE rn = 1
'''

_INTERRUPTIONS_SQL = '''
WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-interruptions"
)
SELECT
    id,
    TRY_CAST(periodFrom AS TIMESTAMP)       AS period_from,
    TRY_CAST(periodTo AS TIMESTAMP)         AS period_to,
    operatorKey                             AS operator_key,
    operatorLabel                           AS operator_label,
    pointKey                                AS point_key,
    pointLabel                              AS point_label,
    directionKey                            AS direction_key,
    indicator,
    interruptionType                        AS interruption_type,
    capacityType                            AS capacity_type,
    unit,
    TRY_CAST(NULLIF(value, '') AS DOUBLE)   AS value,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP) AS last_update
FROM ranked
WHERE rn = 1 AND TRY_CAST(NULLIF(value, '') AS DOUBLE) IS NOT NULL
'''

# CMP unavailable-capacity records are sparse by nature (mostly "no congestion"
# placeholders); the `value`/measure fields are structurally empty, so we publish
# the populated dimension + remark columns and the partially-populated period.
_CMPUNAVAILABLES_SQL = '''
WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-cmpunavailables"
)
SELECT
    id,
    operatorKey                             AS operator_key,
    operatorLabel                           AS operator_label,
    pointKey                                AS point_key,
    pointLabel                              AS point_label,
    directionKey                            AS direction_key,
    allocationProcess                       AS allocation_process,
    TRY_CAST(periodFrom AS TIMESTAMP)       AS period_from,
    TRY_CAST(periodTo AS TIMESTAMP)         AS period_to,
    NULLIF(generalRemarks, '')              AS general_remarks,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP) AS last_update
FROM ranked
WHERE rn = 1
'''

# CMP unsuccessful-request records are likewise sparse (mostly "no unfulfilled
# requests" placeholders); the period columns are structurally empty here (dates
# live in the auction/capacity fields, themselves usually "N/A"), so we keep the
# populated dims, the (sparse but meaningful) volume measures, and the remark.
_CMPUNSUCCESSFULREQUESTS_SQL = '''
WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-cmpunsuccessfulrequests"
)
SELECT
    id,
    operatorKey                                     AS operator_key,
    operatorLabel                                   AS operator_label,
    pointKey                                        AS point_key,
    pointLabel                                      AS point_label,
    directionKey                                    AS direction_key,
    TRY_CAST(NULLIF(requestedVolume, '') AS DOUBLE)   AS requested_volume,
    TRY_CAST(NULLIF(allocatedVolume, '') AS DOUBLE)   AS allocated_volume,
    TRY_CAST(NULLIF(unallocatedVolume, '') AS DOUBLE) AS unallocated_volume,
    TRY_CAST(NULLIF(occurenceCount, '') AS BIGINT)    AS occurence_count,
    NULLIF(generalRemarks, '')                      AS general_remarks,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP)         AS last_update
FROM ranked
WHERE rn = 1
'''

_TARIFFSSIMULATIONS_SQL = '''
WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-tariffssimulations"
)
SELECT
    id,
    operatorKey                                                AS operator_key,
    operatorLabel                                              AS operator_label,
    pointKey                                                   AS point_key,
    pointLabel                                                 AS point_label,
    directionKey                                               AS direction_key,
    countryCode                                                AS country_code,
    fromBZ                                                     AS from_bz,
    toBZ                                                       AS to_bz,
    productType                                                AS product_type,
    tariffCapacityType                                         AS tariff_capacity_type,
    operatorCurrency                                           AS operator_currency,
    TRY_CAST(NULLIF(productSimulationCostInLocalCurrency, '') AS DOUBLE) AS cost_local,
    TRY_CAST(NULLIF(productSimulationCostInEURO, '') AS DOUBLE)          AS cost_eur,
    TRY_CAST(periodFrom AS TIMESTAMP)                          AS period_from,
    TRY_CAST(periodTo AS TIMESTAMP)                            AS period_to,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP)                  AS last_update
FROM ranked
WHERE rn = 1
'''

_URGENTMARKETMESSAGES_SQL = '''
WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-urgentmarketmessages"
)
SELECT
    id,
    messageId                                          AS message_id,
    marketParticipantName                              AS market_participant_name,
    messageType                                        AS message_type,
    eventType                                          AS event_type,
    eventStatus                                        AS event_status,
    TRY_CAST(publicationDateTime AS TIMESTAMP)         AS publication_date,
    TRY_CAST(eventStart AS TIMESTAMP)                  AS event_start,
    TRY_CAST(eventStop AS TIMESTAMP)                   AS event_stop,
    balancingZoneName                                  AS balancing_zone_name,
    TRY_CAST(NULLIF(unavailableCapacity, '') AS DOUBLE) AS unavailable_capacity,
    TRY_CAST(NULLIF(availableCapacity, '') AS DOUBLE)   AS available_capacity,
    TRY_CAST(NULLIF(technicalCapacity, '') AS DOUBLE)   AS technical_capacity,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP)          AS last_update
FROM ranked
WHERE rn = 1
'''

_SQL = {
    "entsog-transparency-platform-operationaldata": _OPERATIONALDATA_SQL,
    "entsog-transparency-platform-operatorpointdirections": _OPERATORPOINTDIRECTIONS_SQL,
    "entsog-transparency-platform-interruptions": _INTERRUPTIONS_SQL,
    "entsog-transparency-platform-cmpunavailables": _CMPUNAVAILABLES_SQL,
    "entsog-transparency-platform-cmpunsuccessfulrequests": _CMPUNSUCCESSFULREQUESTS_SQL,
    "entsog-transparency-platform-tariffssimulations": _TARIFFSSIMULATIONS_SQL,
    "entsog-transparency-platform-urgentmarketmessages": _URGENTMARKETMESSAGES_SQL,
}

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_SQL[s.id])
    for s in DOWNLOAD_SPECS
]
