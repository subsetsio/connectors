"""USGS water data — OGC API Features (https://api.waterdata.usgs.gov/ogcapi/v0).

The modernized OGC API Features service. Each collection's `/items` endpoint is
cursor-paginated (`limit` + opaque `next` cursor). We crawl a collection end to
end and stream every feature's properties to one gzipped NDJSON raw asset.
Property values are stringified on write so the raw is type-stable regardless of
source drift; the SQL transform re-types with TRY_CAST. Point geometry (when
present) is flattened to _lat/_lon.

Freshness model — stateless full re-pull (the harness default). Every run
re-fetches the whole corpus and overwrites; revisions and late corrections are
picked up for free, and there is no watermark to go stale. The two genuine
exceptions are the high-frequency water sensor collections, which are
nationally unbounded and cannot be fully materialized:

  * `continuous` — ~5.2M rows/day nationally (15-minute sensor readings)
  * `daily`      — ~80k rows/day nationally (daily summarized values)

For these two we publish a recent rolling window via the OGC `datetime`
filter (see WINDOW_DAYS). This is a deliberate, documented scope decision —
not silent truncation; the window is relative to run time, so it always
tracks the live edge. All other collections are bounded reference / metadata /
annual tables and are crawled in full (peaks ~1M, monitoring-locations ~1.9M).

Rate limits — the water OGC service throttles with HTTP 429 under sustained
load; nodes run sequentially (DAG_PARALLELISM=1) and the shared transport
retries 429/5xx with exponential backoff, which paces the crawl to whatever
the service allows. A free API key (optional) would raise the ceiling.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import httpx

from subsets_utils import NodeSpec, SqlNodeSpec, raw_writer
from utils import MAX_PAGES, get_json

# --- source surface ----------------------------------------------------------

WATER_BASE = "https://api.waterdata.usgs.gov/ogcapi/v0"

# The 8 rank-accepted water OGC collections (== entity union minus earthquakes).
WATER_ENTITY_IDS = [
    "channel-measurements",
    "combined-metadata",
    "continuous",
    "daily",
    "field-measurements",
    "monitoring-locations",
    "peaks",
    "time-series-metadata",
]

# Page size for OGC item paging (service max is 10000). Kept moderate: the
# service is more prone to 500s when materializing very large pages at depth.
PAGE_LIMIT = 5000

# Nationally unbounded high-frequency collections — published as a recent
# rolling window (days back from run time) rather than the full historic corpus.
WINDOW_DAYS = {
    "continuous": 1,
    "daily": 14,
}


# --- shared helpers ----------------------------------------------------------

def _stringify(value) -> str | None:
    """Coerce any OGC property value to a string (None stays None) so the raw
    NDJSON is type-stable. Nested values become compact JSON strings."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, (list, dict)):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def _feature_row(feature: dict) -> dict:
    """Flatten one GeoJSON feature into a stringified property row.

    _lat/_lon are ALWAYS emitted (null when the feature has no point geometry)
    so the columns always exist in the NDJSON — a transform that reads them
    never trips a 'column not found' on a geometry-less collection."""
    props = feature.get("properties") or {}
    row = {k: _stringify(v) for k, v in props.items()}
    lon = lat = None
    geom = feature.get("geometry") or {}
    if geom.get("type") == "Point":
        coords = geom.get("coordinates") or []
        if len(coords) >= 2:
            lon, lat = _stringify(coords[0]), _stringify(coords[1])
    row["_lon"] = lon
    row["_lat"] = lat
    # Some collections carry the feature id outside properties.
    if "id" not in row and feature.get("id") is not None:
        row["id"] = _stringify(feature.get("id"))
    return row


# --- water OGC fetch ---------------------------------------------------------

def fetch_water(node_id: str) -> None:
    """Crawl one OGC collection's items end to end (or within a rolling window
    for the unbounded high-frequency collections) and stream every feature to
    one gzipped NDJSON raw asset.

    The runtime passes the spec id (e.g. 'usgs-daily'); the collection is the
    id minus the 'usgs-' prefix, and the id is also the asset name to write.
    """
    asset = node_id
    collection = node_id.removeprefix("usgs-")

    params: dict | None = {"f": "json", "limit": PAGE_LIMIT}
    window = WINDOW_DAYS.get(collection)
    if window is not None:
        now = datetime.now(tz=timezone.utc)
        start = now - timedelta(days=window)
        params["datetime"] = f"{start.isoformat()}/{now.isoformat()}"

    url = f"{WATER_BASE}/collections/{collection}/items"
    pages = 0
    total = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        while True:
            try:
                payload = get_json(url, params)
            except (httpx.HTTPStatusError, httpx.RequestError) as exc:
                # A page that stays broken through all retries (a persistent
                # server-side 500 on one cursor, say) must NOT abort the whole
                # connector. If we already have data, finalize the partial crawl
                # loudly; if the very first page failed, fail honestly.
                if total == 0:
                    raise
                print(
                    f"  WARNING {asset}: page {pages + 1} failed after retries "
                    f"({type(exc).__name__}: {exc}); finalizing partial crawl "
                    f"with {total} rows from {pages} page(s)"
                )
                break
            features = payload.get("features") or []
            for feat in features:
                fh.write(json.dumps(_feature_row(feat)) + "\n")
            total += len(features)
            pages += 1

            next_href = next(
                (
                    link["href"]
                    for link in payload.get("links", [])
                    if link.get("rel") == "next"
                ),
                None,
            )
            if not next_href or not features:
                break
            if pages >= MAX_PAGES:
                raise RuntimeError(
                    f"{asset}: hit MAX_PAGES={MAX_PAGES} without draining "
                    f"({total} rows so far) — cursor likely not advancing"
                )
            # The next link embeds cursor + datetime + limit; follow it verbatim.
            url = next_href
            params = None
    print(f"  {asset}: {total} rows over {pages} page(s)")


# --- download specs ----------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id=f"usgs-{eid}", fn=fetch_water, kind="download")
    for eid in WATER_ENTITY_IDS
]


# --- transforms — one published Delta table per subset -----------------------
# Each transform reads its NDJSON raw view (all source columns are VARCHAR),
# TRY_CASTs to real types, drops rows without a key, and DISTINCTs away any
# boundary-overlap duplicates. A 0-row result fails the node by design.

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="usgs-monitoring-locations-transform",
        deps=["usgs-monitoring-locations"],
        sql='''
            SELECT DISTINCT
                "id"                                         AS id,
                "monitoring_location_number"                 AS monitoring_location_number,
                "monitoring_location_name"                   AS monitoring_location_name,
                "agency_code"                                AS agency_code,
                "agency_name"                                AS agency_name,
                "site_type"                                  AS site_type,
                "site_type_code"                             AS site_type_code,
                "state_name"                                 AS state_name,
                "county_name"                                AS county_name,
                "country_name"                               AS country_name,
                "hydrologic_unit_code"                       AS hydrologic_unit_code,
                "aquifer_code"                               AS aquifer_code,
                "national_aquifer_code"                      AS national_aquifer_code,
                TRY_CAST("altitude" AS DOUBLE)               AS altitude,
                TRY_CAST("drainage_area" AS DOUBLE)          AS drainage_area,
                TRY_CAST("_lat" AS DOUBLE)                   AS latitude,
                TRY_CAST("_lon" AS DOUBLE)                   AS longitude,
                "construction_date"                          AS construction_date,
                "revision_modified"                          AS revision_modified
            FROM "usgs-monitoring-locations"
            WHERE "id" IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="usgs-peaks-transform",
        deps=["usgs-peaks"],
        sql='''
            SELECT DISTINCT
                "id"                                AS id,
                "monitoring_location_id"            AS monitoring_location_id,
                "parameter_code"                    AS parameter_code,
                TRY_CAST("water_year" AS INTEGER)   AS water_year,
                TRY_CAST("value" AS DOUBLE)         AS value,
                "unit_of_measure"                   AS unit_of_measure,
                "qualifier"                         AS qualifier,
                TRY_CAST("time" AS DATE)            AS date,
                "peak_since"                        AS peak_since,
                "last_modified"                     AS last_modified
            FROM "usgs-peaks"
            WHERE "monitoring_location_id" IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="usgs-daily-transform",
        deps=["usgs-daily"],
        sql='''
            SELECT DISTINCT
                "monitoring_location_id"            AS monitoring_location_id,
                "parameter_code"                    AS parameter_code,
                "statistic_id"                      AS statistic_id,
                "time_series_id"                    AS time_series_id,
                TRY_CAST("time" AS DATE)            AS date,
                TRY_CAST("value" AS DOUBLE)         AS value,
                "unit_of_measure"                   AS unit_of_measure,
                "qualifier"                         AS qualifier,
                "approval_status"                   AS approval_status,
                "last_modified"                     AS last_modified
            FROM "usgs-daily"
            WHERE "time_series_id" IS NOT NULL AND "time" IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="usgs-continuous-transform",
        deps=["usgs-continuous"],
        sql='''
            SELECT DISTINCT
                "monitoring_location_id"            AS monitoring_location_id,
                "parameter_code"                    AS parameter_code,
                "statistic_id"                      AS statistic_id,
                "time_series_id"                    AS time_series_id,
                TRY_CAST("time" AS TIMESTAMP)       AS time,
                TRY_CAST("value" AS DOUBLE)         AS value,
                "unit_of_measure"                   AS unit_of_measure,
                "qualifier"                         AS qualifier,
                "approval_status"                   AS approval_status,
                "last_modified"                     AS last_modified
            FROM "usgs-continuous"
            WHERE "time_series_id" IS NOT NULL AND "time" IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="usgs-field-measurements-transform",
        deps=["usgs-field-measurements"],
        sql='''
            SELECT DISTINCT
                "field_measurements_series_id"      AS field_measurements_series_id,
                "field_visit_id"                    AS field_visit_id,
                "monitoring_location_id"            AS monitoring_location_id,
                "parameter_code"                    AS parameter_code,
                TRY_CAST("value" AS DOUBLE)         AS value,
                "unit_of_measure"                   AS unit_of_measure,
                TRY_CAST("time" AS TIMESTAMP)       AS time,
                "reading_type"                      AS reading_type,
                "measuring_agency"                  AS measuring_agency,
                "qualifier"                         AS qualifier,
                "last_modified"                     AS last_modified
            FROM "usgs-field-measurements"
            WHERE "monitoring_location_id" IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="usgs-channel-measurements-transform",
        deps=["usgs-channel-measurements"],
        sql='''
            SELECT DISTINCT
                "id"                                    AS id,
                "field_visit_id"                        AS field_visit_id,
                "monitoring_location_id"                AS monitoring_location_id,
                "measurement_number"                    AS measurement_number,
                "measurement_type"                      AS measurement_type,
                "channel_material"                      AS channel_material,
                "channel_name"                          AS channel_name,
                TRY_CAST("channel_width" AS DOUBLE)     AS channel_width,
                "channel_width_unit"                    AS channel_width_unit,
                TRY_CAST("channel_area" AS DOUBLE)      AS channel_area,
                "channel_area_unit"                     AS channel_area_unit,
                TRY_CAST("channel_velocity" AS DOUBLE)  AS channel_velocity,
                "channel_velocity_unit"                 AS channel_velocity_unit,
                TRY_CAST("channel_flow" AS DOUBLE)      AS channel_flow,
                "channel_flow_unit"                     AS channel_flow_unit,
                TRY_CAST("time" AS TIMESTAMP)           AS time,
                "last_modified"                         AS last_modified
            FROM "usgs-channel-measurements"
            WHERE "id" IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="usgs-combined-metadata-transform",
        deps=["usgs-combined-metadata"],
        sql='''
            SELECT DISTINCT
                "id"                                AS id,
                "monitoring_location_id"            AS monitoring_location_id,
                "monitoring_location_name"          AS monitoring_location_name,
                "agency_code"                       AS agency_code,
                "site_type"                         AS site_type,
                "state_name"                        AS state_name,
                "county_name"                       AS county_name,
                "parameter_code"                    AS parameter_code,
                "parameter_name"                    AS parameter_name,
                "statistic_id"                      AS statistic_id,
                "computation_identifier"            AS computation_identifier,
                "data_type"                         AS data_type,
                "unit_of_measure"                   AS unit_of_measure,
                TRY_CAST("begin" AS TIMESTAMP)      AS begin_time,
                TRY_CAST("end" AS TIMESTAMP)        AS end_time,
                TRY_CAST("_lat" AS DOUBLE)          AS latitude,
                TRY_CAST("_lon" AS DOUBLE)          AS longitude,
                "last_modified"                     AS last_modified
            FROM "usgs-combined-metadata"
            WHERE "id" IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="usgs-time-series-metadata-transform",
        deps=["usgs-time-series-metadata"],
        sql='''
            SELECT DISTINCT
                "id"                                        AS id,
                "monitoring_location_id"                    AS monitoring_location_id,
                "parameter_code"                            AS parameter_code,
                "parameter_name"                            AS parameter_name,
                "statistic_id"                              AS statistic_id,
                "computation_identifier"                    AS computation_identifier,
                "computation_period_identifier"             AS computation_period_identifier,
                "unit_of_measure"                           AS unit_of_measure,
                TRY_CAST("begin" AS TIMESTAMP)              AS begin_time,
                TRY_CAST("end" AS TIMESTAMP)                AS end_time,
                TRY_CAST("begin_utc" AS TIMESTAMP)          AS begin_utc,
                TRY_CAST("end_utc" AS TIMESTAMP)            AS end_utc,
                "state_name"                                AS state_name,
                "hydrologic_unit_code"                      AS hydrologic_unit_code,
                "web_description"                           AS web_description,
                "last_modified"                             AS last_modified
            FROM "usgs-time-series-metadata"
            WHERE "id" IS NOT NULL
        ''',
    ),
]
