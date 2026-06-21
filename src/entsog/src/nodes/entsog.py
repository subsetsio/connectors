"""ENTSOG Transparency Platform connector.

One public REST API (https://transparency.entsog.eu/api/v1/, no auth) backs the
whole EU gas-transmission transparency platform. Two fetch shapes:

* Full-corpus reference / snapshot endpoints (operators, operatorpointdirections,
  connectionpoints, interconnections, urgentmarketmessages, tariffssimulations,
  tariffsfulls): a few hundred to ~12k rows; pulled in one offset-paginated sweep
  and overwritten each run.

* Date-windowed time-series (operationaldata, interruptions, cmp*): the platform
  archives data on a rolling ~5-year basis (queries older than that return a 404
  "archived" message) and a 60-second per-query server timeout forces narrow
  windows. We backfill from ~today-5y forward in date buckets (operationaldata and
  interruptions monthly; the small cmp* feeds yearly), writing one raw batch per
  page and advancing a per-bucket watermark in state so the supervisor can
  interrupt + resume. Long-span rows (e.g. an interruption spanning several years)
  are returned by every overlapping window, so each time-series transform dedups
  by the source `id`.

operationaldata is queried by date window only — its `indicator` (Physical Flow,
Nomination, Allocation, GCV, firm/interruptible capacities, ...) is a column, not
a separate fetch. The `indicator` query param is unreliable on this endpoint and
is deliberately not used.
"""
from datetime import date, datetime, timedelta, timezone

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    load_state,
    save_state,
    transient_retry,
)

BASE = "https://transparency.entsog.eu/api/v1/"
STATE_VERSION = 1
PAGE = 50000             # rows per request; one page (~48MB) stays under the 60s timeout
FULL_PAGE = 50000
OVERLAP_BUCKETS = 2      # re-fetch the most recent buckets each refresh for revisions
ROLLING_YEARS = 5        # platform archives data older than ~5 years
MAX_PAGES = 5000         # absolute safety ceiling — raises, never silently truncates

# node-id stem (entsog-<lower>) -> real (case-sensitive) endpoint name
REAL_ENDPOINT = {
    "operators": "operators",
    "operatorpointdirections": "operatorpointdirections",
    "connectionpoints": "connectionpoints",
    "interconnections": "interconnections",
    "urgentmarketmessages": "urgentmarketmessages",
    "tariffssimulations": "tariffssimulations",
    "tariffsfulls": "tariffsfulls",
    "operationaldata": "operationaldata",
    "interruptions": "interruptions",
    "cmpunavailables": "cmpUnavailables",
    "cmpunsuccessfulrequests": "cmpUnsuccessfulRequests",
    "cmpauctions": "cmpAuctions",
}

FULL_ENTITIES = [
    "operators",
    "operatorpointdirections",
    "connectionpoints",
    "interconnections",
    "urgentmarketmessages",
    "tariffssimulations",
    "tariffsfulls",
]

# date-windowed time-series -> bucket granularity
TS_ENTITIES = {
    "operationaldata": "month",
    "interruptions": "month",
    "cmpunavailables": "year",
    "cmpunsuccessfulrequests": "year",
    "cmpauctions": "year",
}


# --------------------------------------------------------------------------- #
# transport
# --------------------------------------------------------------------------- #


@transient_retry()
def _request(endpoint: str, params: dict) -> httpx.Response:
    resp = get(BASE + endpoint, params=params, timeout=(10.0, 180.0))
    # 429 / 5xx -> raise so the decorator retries (504 gateway timeouts included)
    if resp.status_code == 429 or 500 <= resp.status_code < 600:
        resp.raise_for_status()
    return resp


def _get_rows(endpoint: str, params: dict):
    """Return the list of records, or None when the API reports no data for the
    query (404 'No result found' or the rolling-archive notice). Other 4xx raise."""
    resp = _request(endpoint, params)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    doc = resp.json()
    key = next((k for k in doc if k != "meta" and isinstance(doc[k], list)), None)
    return doc.get(key, []) if key else []


# --------------------------------------------------------------------------- #
# date buckets
# --------------------------------------------------------------------------- #
def _today() -> date:
    return datetime.now(timezone.utc).date()


def _source_min() -> date:
    t = _today()
    return date(t.year - ROLLING_YEARS, t.month, 1)


def _month_buckets(start: date, end: date):
    cur = date(start.year, start.month, 1)
    out = []
    while cur <= end:
        nxt = date(cur.year + 1, 1, 1) if cur.month == 12 else date(cur.year, cur.month + 1, 1)
        frm = max(cur, start)
        to = min(nxt - timedelta(days=1), end)
        out.append((f"{cur.year:04d}-{cur.month:02d}", frm.isoformat(), to.isoformat()))
        cur = nxt
    return out


def _year_buckets(start: date, end: date):
    out = []
    for y in range(start.year, end.year + 1):
        frm = max(date(y, 1, 1), start)
        to = min(date(y, 12, 31), end)
        out.append((str(y), frm.isoformat(), to.isoformat()))
    return out


# --------------------------------------------------------------------------- #
# fetch fns
# --------------------------------------------------------------------------- #
def fetch_full(node_id: str) -> None:
    """Full-corpus sweep for a reference/snapshot endpoint -> one ndjson asset."""
    endpoint = REAL_ENDPOINT[node_id[len("entsog-"):]]
    rows = []
    offset = 0
    page = 0
    while True:
        batch = _get_rows(endpoint, {"limit": FULL_PAGE, "offset": offset})
        if not batch:
            break
        rows.extend(batch)
        if len(batch) < FULL_PAGE:
            break
        offset += FULL_PAGE
        page += 1
        if page > MAX_PAGES:
            raise RuntimeError(f"{endpoint}: exceeded MAX_PAGES — source grew unexpectedly")
    save_raw_ndjson(rows, node_id)


def _fetch_bucket(node_id: str, endpoint: str, key: str, frm: str, to: str) -> None:
    offset = 0
    page = 0
    while True:
        rows = _get_rows(endpoint, {"from": frm, "to": to, "limit": PAGE, "offset": offset})
        if rows is None:        # archived window or no data — nothing to write
            break
        if not rows:
            break
        save_raw_ndjson(rows, f"{node_id}-{key}-p{page}")
        if len(rows) < PAGE:
            break
        offset += PAGE
        page += 1
        if page > MAX_PAGES:
            raise RuntimeError(f"{endpoint} {key}: exceeded MAX_PAGES at offset {offset}")


def fetch_timeseries(node_id: str) -> None:
    """Date-bucketed backfill/refresh. Writes one raw batch per page and advances a
    per-bucket watermark so an interrupted run resumes without re-crawling history."""
    entity = node_id[len("entsog-"):]
    endpoint = REAL_ENDPOINT[entity]
    gran = TS_ENTITIES[entity]

    start, end = _source_min(), _today()
    buckets = _month_buckets(start, end) if gran == "month" else _year_buckets(start, end)
    keys = [b[0] for b in buckets]

    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    watermark = state.get("watermark")
    if watermark in keys:
        start_idx = max(0, keys.index(watermark) - OVERLAP_BUCKETS)
    else:
        start_idx = 0

    for key, frm, to in buckets[start_idx:]:
        _fetch_bucket(node_id, endpoint, key, frm, to)   # raw first
        save_state(node_id, {"schema_version": STATE_VERSION, "watermark": key})


# --------------------------------------------------------------------------- #
# download specs — one per entity-union entry
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id=f"entsog-{e}", fn=fetch_full, kind="download")
    for e in FULL_ENTITIES
] + [
    NodeSpec(id=f"entsog-{e}", fn=fetch_timeseries, kind="download")
    for e in TS_ENTITIES
]


# --------------------------------------------------------------------------- #
# transforms — one published Delta table per subset
# --------------------------------------------------------------------------- #
def _ts_sql(view: str, cols: str) -> str:
    """Time-series projection deduped by source id (overlapping windows repeat
    long-span rows)."""
    return f'''
        SELECT {cols}
        FROM (
            SELECT *,
                   row_number() OVER (
                       PARTITION BY id
                       ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) DESC NULLS LAST
                   ) AS _rn
            FROM "{view}"
            WHERE id IS NOT NULL
        )
        WHERE _rn = 1
    '''


V_OPD = "entsog-operationaldata"
V_INT = "entsog-interruptions"
V_CMU = "entsog-cmpunavailables"
V_CMR = "entsog-cmpunsuccessfulrequests"
V_CMA = "entsog-cmpauctions"

TRANSFORM_SQL = {
    "entsog-operators": '''
        SELECT
            operatorKey                                AS operator_key,
            operatorLabel                              AS operator_label,
            operatorCountryKey                         AS country_key,
            operatorCountryLabel                       AS country_label,
            operatorTypeLabel                          AS operator_type,
            tsoEicCode                                 AS tso_eic_code,
            gasDayStartHour                            AS gas_day_start_hour,
            balancingModel                             AS balancing_model,
            TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) AS last_update,
            id
        FROM "entsog-operators"
        WHERE operatorKey IS NOT NULL
    ''',
    "entsog-operatorpointdirections": '''
        SELECT
            pointKey                                   AS point_key,
            pointLabel                                 AS point_label,
            operatorKey                                AS operator_key,
            operatorLabel                              AS operator_label,
            directionKey                               AS direction_key,
            TRY_CAST(validFrom AS TIMESTAMPTZ)         AS valid_from,
            TRY_CAST(validTo AS TIMESTAMPTZ)           AS valid_to,
            tSOCountry                                 AS tso_country,
            tSOBalancingZone                           AS tso_balancing_zone,
            crossBorderPointType                       AS cross_border_point_type,
            adjacentCountry                            AS adjacent_country,
            pointType                                  AS point_type,
            TRY_CAST(hasData AS BOOLEAN)               AS has_data,
            TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) AS last_update,
            id
        FROM "entsog-operatorpointdirections"
        WHERE id IS NOT NULL
    ''',
    "entsog-connectionpoints": '''
        SELECT
            pointKey                                   AS point_key,
            pointLabel                                 AS point_label,
            pointEicCode                               AS point_eic_code,
            pointType                                  AS point_type,
            commercialType                             AS commercial_type,
            importFromCountryKey                       AS import_from_country_key,
            importFromCountryLabel                     AS import_from_country_label,
            TRY_CAST(isInterconnection AS BOOLEAN)     AS is_interconnection,
            TRY_CAST(isCrossBorder AS BOOLEAN)         AS is_cross_border,
            euCrossing                                 AS eu_crossing,
            TRY_CAST(hasData AS BOOLEAN)               AS has_data,
            infrastructureKey                          AS infrastructure_key,
            infrastructureLabel                        AS infrastructure_label,
            id
        FROM "entsog-connectionpoints"
        WHERE pointKey IS NOT NULL
    ''',
    "entsog-interconnections": '''
        SELECT
            pointKey                                   AS point_key,
            pointLabel                                 AS point_label,
            fromCountryKey                             AS from_country_key,
            fromOperatorKey                            AS from_operator_key,
            fromBzKey                                  AS from_bz_key,
            fromDirectionKey                           AS from_direction_key,
            toCountryKey                               AS to_country_key,
            toOperatorKey                              AS to_operator_key,
            toBzKey                                    AS to_bz_key,
            toDirectionKey                             AS to_direction_key,
            TRY_CAST(validFrom AS TIMESTAMPTZ)         AS valid_from,
            TRY_CAST(validto AS TIMESTAMPTZ)           AS valid_to,
            TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) AS last_update,
            id
        FROM "entsog-interconnections"
        WHERE id IS NOT NULL
    ''',
    "entsog-urgentmarketmessages": '''
        SELECT
            id,
            messageId                                  AS message_id,
            marketParticipantKey                       AS market_participant_key,
            marketParticipantName                      AS market_participant_name,
            messageType                                AS message_type,
            TRY_CAST(publicationDateTime AS TIMESTAMPTZ) AS publication_datetime,
            eventStatus                                AS event_status,
            eventType                                  AS event_type,
            TRY_CAST(eventStart AS TIMESTAMPTZ)        AS event_start,
            TRY_CAST(eventStop AS TIMESTAMPTZ)         AS event_stop,
            unavailabilityType                         AS unavailability_type,
            unavailabilityReason                       AS unavailability_reason,
            balancingZoneKey                           AS balancing_zone_key,
            balancingZoneName                          AS balancing_zone_name,
            affectedAssetName                          AS affected_asset_name,
            direction,
            TRY_CAST(unavailableCapacity AS DOUBLE)    AS unavailable_capacity,
            TRY_CAST(availableCapacity AS DOUBLE)      AS available_capacity,
            TRY_CAST(technicalCapacity AS DOUBLE)      AS technical_capacity,
            unitMeasure                                AS unit_measure,
            TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) AS last_update
        FROM "entsog-urgentmarketmessages"
        WHERE id IS NOT NULL
    ''',
    "entsog-tariffssimulations": '''
        SELECT
            id,
            operatorKey                                AS operator_key,
            operatorLabel                              AS operator_label,
            pointKey                                   AS point_key,
            pointLabel                                 AS point_label,
            directionKey                               AS direction_key,
            countryCode                                AS country_code,
            tariffCapacityType                         AS tariff_capacity_type,
            tariffCapacityUnit                         AS tariff_capacity_unit,
            productType                                AS product_type,
            operatorCurrency                           AS operator_currency,
            TRY_CAST(productSimulationCostInLocalCurrency AS DOUBLE) AS cost_local_currency,
            TRY_CAST(productSimulationCostInEURO AS DOUBLE)         AS cost_eur,
            TRY_CAST(periodFrom AS TIMESTAMPTZ)        AS period_from,
            TRY_CAST(periodTo AS TIMESTAMPTZ)          AS period_to,
            TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) AS last_update
        FROM "entsog-tariffssimulations"
        WHERE id IS NOT NULL
    ''',
    "entsog-tariffsfulls": '''
        SELECT
            id,
            operatorKey                                AS operator_key,
            operatorLabel                              AS operator_label,
            pointKey                                   AS point_key,
            pointLabel                                 AS point_label,
            directionKey                               AS direction_key,
            countryCode                                AS country_code,
            tariffCapacityType                         AS tariff_capacity_type,
            tariffCapacityUnit                         AS tariff_capacity_unit,
            productType                                AS product_type,
            operatorCurrency                           AS operator_currency,
            TRY_CAST(applicableTariffPerEURKWhDValue AS DOUBLE) AS tariff_eur_kwh_d,
            TRY_CAST(applicableTariffPerEURKWhHValue AS DOUBLE) AS tariff_eur_kwh_h,
            TRY_CAST(applicableTariffInCommonUnitValue AS DOUBLE) AS tariff_common_unit,
            applicableTariffInCommonUnitUnit           AS tariff_common_unit_label,
            TRY_CAST(productPeriodFrom AS TIMESTAMPTZ) AS product_period_from,
            TRY_CAST(productPeriodTo AS TIMESTAMPTZ)   AS product_period_to,
            TRY_CAST(periodFrom AS TIMESTAMPTZ)        AS period_from,
            TRY_CAST(periodTo AS TIMESTAMPTZ)          AS period_to,
            TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) AS last_update
        FROM "entsog-tariffsfulls"
        WHERE id IS NOT NULL
    ''',
    V_OPD: _ts_sql(V_OPD, '''
            id,
            indicator,
            pointKey      AS point_key,
            pointLabel    AS point_label,
            operatorKey   AS operator_key,
            operatorLabel AS operator_label,
            directionKey  AS direction_key,
            tsoEicCode    AS tso_eic_code,
            periodType    AS period_type,
            TRY_CAST(periodFrom AS TIMESTAMPTZ) AS period_from,
            TRY_CAST(periodTo AS TIMESTAMPTZ)   AS period_to,
            TRY_CAST(value AS DOUBLE)           AS value,
            unit,
            flowStatus            AS flow_status,
            capacityType          AS capacity_type,
            capacityBookingStatus AS capacity_booking_status,
            TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) AS last_update
    '''),
    V_INT: _ts_sql(V_INT, '''
            id,
            indicator,
            pointKey      AS point_key,
            pointLabel    AS point_label,
            operatorKey   AS operator_key,
            operatorLabel AS operator_label,
            directionKey  AS direction_key,
            interruptionType       AS interruption_type,
            capacityType           AS capacity_type,
            capacityCommercialType AS capacity_commercial_type,
            TRY_CAST(periodFrom AS TIMESTAMPTZ) AS period_from,
            TRY_CAST(periodTo AS TIMESTAMPTZ)   AS period_to,
            TRY_CAST(value AS DOUBLE)           AS value,
            unit,
            TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) AS last_update
    '''),
    V_CMU: _ts_sql(V_CMU, '''
            id,
            indicator,
            pointKey     AS point_key,
            operatorKey  AS operator_key,
            directionKey AS direction_key,
            allocationProcess AS allocation_process,
            capacityType      AS capacity_type,
            TRY_CAST(periodFrom AS TIMESTAMPTZ) AS period_from,
            TRY_CAST(periodTo AS TIMESTAMPTZ)   AS period_to,
            TRY_CAST(value AS DOUBLE)           AS value,
            unit,
            TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) AS last_update
    '''),
    V_CMR: _ts_sql(V_CMR, '''
            id,
            pointKey     AS point_key,
            operatorKey  AS operator_key,
            directionKey AS direction_key,
            TRY_CAST(periodFrom AS TIMESTAMPTZ) AS period_from,
            TRY_CAST(periodTo AS TIMESTAMPTZ)   AS period_to,
            TRY_CAST(requestedVolume AS DOUBLE)   AS requested_volume,
            TRY_CAST(allocatedVolume AS DOUBLE)   AS allocated_volume,
            TRY_CAST(unallocatedVolume AS DOUBLE) AS unallocated_volume,
            TRY_CAST(occurenceCount AS BIGINT)    AS occurrence_count,
            TRY_CAST(value AS DOUBLE)             AS value,
            unit,
            TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) AS last_update
    '''),
    V_CMA: _ts_sql(V_CMA, '''
            id,
            pointKey     AS point_key,
            operatorKey  AS operator_key,
            directionKey AS direction_key,
            TRY_CAST(auctionFrom AS TIMESTAMPTZ)  AS auction_from,
            TRY_CAST(auctionTo AS TIMESTAMPTZ)    AS auction_to,
            TRY_CAST(capacityFrom AS TIMESTAMPTZ) AS capacity_from,
            TRY_CAST(capacityTo AS TIMESTAMPTZ)   AS capacity_to,
            TRY_CAST(auctionPremium AS DOUBLE)    AS auction_premium,
            TRY_CAST(clearedPrice AS DOUBLE)      AS cleared_price,
            TRY_CAST(reservePrice AS DOUBLE)      AS reserve_price,
            unit,
            TRY_CAST(lastUpdateDateTime AS TIMESTAMPTZ) AS last_update
    '''),
}

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=TRANSFORM_SQL[s.id])
    for s in DOWNLOAD_SPECS
]
