"""USGS raw downloads.

The connector covers two public USGS REST surfaces:

* Water Data OGC API Features, one raw NDJSON asset per accepted collection.
* FDSN ComCat, one raw NDJSON asset for events plus two small XML-list
  metadata endpoints for catalogs and contributors.

The node module intentionally owns only raw downloads. Transforms are compiled
from the model stage.
"""
from __future__ import annotations

import csv
import io
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import httpx
import pyarrow as pa

from subsets_utils import MaintainSpec, NodeSpec, raw_asset_exists, raw_parquet_writer, raw_writer
from utils import MAX_PAGES, get_json, get_text

WATER_BASE = "https://api.waterdata.usgs.gov/ogcapi/v0"
FDSN_BASE = "https://earthquake.usgs.gov/fdsnws/event/1"

WATER_ENTITY_IDS = [
    "agency-codes",
    "altitude-datums",
    "aquifer-codes",
    "aquifer-types",
    "channel-measurements",
    "citations",
    "combined-metadata",
    "continuous",
    "coordinate-accuracy-codes",
    "coordinate-datum-codes",
    "coordinate-method-codes",
    "counties",
    "countries",
    "daily",
    "field-measurements",
    "field-measurements-metadata",
    "hydrologic-unit-codes",
    "latest-continuous",
    "latest-daily",
    "latest-field-measurements",
    "medium-codes",
    "method-categories",
    "method-citations",
    "methods",
    "monitoring-locations",
    "national-aquifer-codes",
    "parameter-codes",
    "peaks",
    "reliability-codes",
    "site-types",
    "states",
    "statistic-codes",
    "time-series-metadata",
    "time-zone-codes",
    "topographic-codes",
]

FDSN_LIST_ENDPOINTS = {
    "earthquake-catalogs": ("catalogs", "catalog"),
    "earthquake-contributors": ("contributors", "contributor"),
}

PAGE_LIMIT = 5000

# Nationally unbounded high-frequency collections are fetched as recent rolling
# windows. The latest-* collections are already live-edge snapshots. Continuous
# is especially throttle-prone at national scale, so keep it to a compact live
# sample instead of a full-day crawl.
WINDOW_DAYS = {
    "continuous": 0.125,
    "daily": 14,
    "field-measurements": 7,
}

ROLLING_ENTITY_IDS = {
    "continuous",
    "daily",
    "field-measurements",
    "latest-continuous",
    "latest-daily",
    "latest-field-measurements",
}

REFERENCE_ENTITY_IDS = {
    "agency-codes",
    "altitude-datums",
    "aquifer-codes",
    "aquifer-types",
    "citations",
    "coordinate-accuracy-codes",
    "coordinate-datum-codes",
    "coordinate-method-codes",
    "counties",
    "countries",
    "hydrologic-unit-codes",
    "medium-codes",
    "method-categories",
    "method-citations",
    "methods",
    "national-aquifer-codes",
    "parameter-codes",
    "reliability-codes",
    "site-types",
    "states",
    "statistic-codes",
    "time-zone-codes",
    "topographic-codes",
    *FDSN_LIST_ENDPOINTS,
}

PARQUET_WATER_ENTITY_IDS = {
    "combined-metadata",
    "latest-field-measurements",
    "monitoring-locations",
}

PARQUET_COLUMNS = {
    "combined-metadata": [
        "monitoring_location_id", "agency_code", "agency_name",
        "monitoring_location_number", "monitoring_location_name", "district_code",
        "country_code", "country_name", "state_code", "state_name", "county_code",
        "county_name", "minor_civil_division_code", "site_type_code", "site_type",
        "hydrologic_unit_code", "basin_code", "altitude", "altitude_accuracy",
        "altitude_method_code", "altitude_method_name", "vertical_datum",
        "vertical_datum_name", "horizontal_positional_accuracy_code",
        "horizontal_positional_accuracy", "horizontal_position_method_code",
        "horizontal_position_method_name", "original_horizontal_datum",
        "original_horizontal_datum_name", "drainage_area",
        "contributing_drainage_area", "time_zone_abbreviation",
        "uses_daylight_savings", "construction_date", "aquifer_code",
        "national_aquifer_code", "aquifer_type_code", "well_constructed_depth",
        "hole_constructed_depth", "depth_source_code", "id", "unit_of_measure",
        "parameter_name", "parameter_code", "statistic_id", "last_modified",
        "begin", "end", "data_type", "computation_identifier", "thresholds",
        "sublocation_identifier", "primary", "web_description",
        "parameter_description", "parent_time_series_id", "data_gap_interval",
        "reading_type", "_lon", "_lat",
    ],
    "latest-field-measurements": [
        "field_measurements_series_id", "field_visit_id", "parameter_code",
        "monitoring_location_id", "observing_procedure_code",
        "observing_procedure", "value", "unit_of_measure", "time", "qualifier",
        "vertical_datum", "approval_status", "measuring_agency", "last_modified",
        "control_condition", "measurement_rated", "year", "month", "day",
        "time_of_day", "_lon", "_lat", "id",
    ],
    "monitoring-locations": [
        "id", "agency_code", "agency_name", "monitoring_location_number",
        "monitoring_location_name", "district_code", "country_code",
        "country_name", "state_code", "state_name", "county_code", "county_name",
        "minor_civil_division_code", "site_type_code", "site_type",
        "hydrologic_unit_code", "basin_code", "altitude", "altitude_accuracy",
        "altitude_method_code", "altitude_method_name", "vertical_datum",
        "vertical_datum_name", "horizontal_positional_accuracy_code",
        "horizontal_positional_accuracy", "horizontal_position_method_code",
        "horizontal_position_method_name", "original_horizontal_datum",
        "original_horizontal_datum_name", "drainage_area",
        "contributing_drainage_area", "time_zone_abbreviation",
        "uses_daylight_savings", "construction_date", "aquifer_code",
        "national_aquifer_code", "aquifer_type_code", "well_constructed_depth",
        "hole_constructed_depth", "depth_source_code", "revision_note",
        "revision_created", "revision_modified", "_lon", "_lat",
    ],
}

EQ_SOURCE_MIN = "1900-01-01T00:00:00Z"
EQ_PAGE_LIMIT = 20_000
EQ_INITIAL_WINDOW_DAYS = 366


def _stringify(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, (list, dict)):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def _format_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _feature_row(feature: dict) -> dict:
    props = feature.get("properties") or {}
    row = {k: _stringify(v) for k, v in props.items()}
    lon = lat = None
    geom = feature.get("geometry") or {}
    if geom.get("type") == "Point":
        coords = geom.get("coordinates") or []
        if len(coords) >= 2:
            lon = _stringify(coords[0])
            lat = _stringify(coords[1])
    row["_lon"] = lon
    row["_lat"] = lat
    if "id" not in row and feature.get("id") is not None:
        row["id"] = _stringify(feature.get("id"))
    return row


def _parquet_schema(collection: str) -> pa.Schema:
    return pa.schema([pa.field(name, pa.string()) for name in PARQUET_COLUMNS[collection]])


def _next_href(payload: dict) -> str | None:
    return next(
        (
            link["href"]
            for link in payload.get("links", [])
            if link.get("rel") == "next"
        ),
        None,
    )


def fetch_water(node_id: str) -> None:
    asset = node_id
    collection = node_id.removeprefix("usgs-")
    params: dict | None = {"f": "json", "limit": PAGE_LIMIT}

    window = WINDOW_DAYS.get(collection)
    if window is not None:
        now = datetime.now(tz=timezone.utc).replace(microsecond=0)
        start = now - timedelta(days=window)
        params["datetime"] = f"{_format_z(start)}/{_format_z(now)}"

    url = f"{WATER_BASE}/collections/{collection}/items"
    pages = 0
    total = 0

    if collection in PARQUET_WATER_ENTITY_IDS:
        with raw_parquet_writer(asset, _parquet_schema(collection)) as writer:
            while True:
                try:
                    payload = get_json(url, params)
                except (httpx.HTTPStatusError, httpx.RequestError) as exc:
                    if total == 0:
                        raise
                    print(
                        f"  WARNING {asset}: page {pages + 1} failed after retries "
                        f"({type(exc).__name__}: {exc}); finalizing partial crawl "
                        f"with {total} rows from {pages} page(s)"
                    )
                    break

                features = payload.get("features") or []
                rows = [_feature_row(feature) for feature in features]
                if rows:
                    table = pa.Table.from_pylist(rows, schema=writer.schema)
                    writer.write_table(table)
                total += len(features)
                pages += 1

                next_href = _next_href(payload)
                if not next_href or not features:
                    break
                if pages >= MAX_PAGES:
                    raise RuntimeError(
                        f"{asset}: hit MAX_PAGES={MAX_PAGES} without draining "
                        f"({total} rows so far)"
                    )
                url = next_href
                params = None
    else:
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
            while True:
                try:
                    payload = get_json(url, params)
                except (httpx.HTTPStatusError, httpx.RequestError) as exc:
                    if total == 0:
                        raise
                    print(
                        f"  WARNING {asset}: page {pages + 1} failed after retries "
                        f"({type(exc).__name__}: {exc}); finalizing partial crawl "
                        f"with {total} rows from {pages} page(s)"
                    )
                    break

                features = payload.get("features") or []
                for feature in features:
                    row = _feature_row(feature)
                    fh.write(json.dumps(row, separators=(",", ":")) + "\n")
                total += len(features)
                pages += 1

                next_href = _next_href(payload)
                if not next_href or not features:
                    break
                if pages >= MAX_PAGES:
                    raise RuntimeError(
                        f"{asset}: hit MAX_PAGES={MAX_PAGES} without draining "
                        f"({total} rows so far)"
                    )
                url = next_href
                params = None

    print(f"  {asset}: {total} rows over {pages} page(s)")


def fetch_fdsn_list(node_id: str) -> None:
    asset = node_id
    entity = node_id.removeprefix("usgs-")
    endpoint, value_col = FDSN_LIST_ENDPOINTS[entity]
    text = get_text(f"{FDSN_BASE}/{endpoint}", params=None)
    root = ET.fromstring(text)

    rows = []
    for child in root:
        value = (child.text or "").strip()
        if value:
            rows.append({value_col: value})

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for row in rows:
            fh.write(json.dumps(row, separators=(",", ":")) + "\n")
    print(f"  {asset}: {len(rows)} rows")


def _parse_z(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _count_earthquakes(start: datetime, end: datetime) -> int:
    text = get_text(
        f"{FDSN_BASE}/count",
        {
            "format": "text",
            "starttime": _format_z(start),
            "endtime": _format_z(end),
        },
    ).strip()
    return int(text or "0")


def _earthquake_windows(start: datetime, end: datetime):
    stack = [(start, end)]
    while stack:
        window_start, window_end = stack.pop()
        if window_start >= window_end:
            continue
        count = _count_earthquakes(window_start, window_end)
        if count == 0:
            continue
        if count <= EQ_PAGE_LIMIT:
            yield window_start, window_end, count
            continue
        midpoint = window_start + (window_end - window_start) / 2
        if midpoint <= window_start or midpoint >= window_end:
            raise RuntimeError(
                "usgs-earthquakes: cannot split dense FDSN window "
                f"{_format_z(window_start)}/{_format_z(window_end)} "
                f"with {count} events"
            )
        stack.append((midpoint, window_end))
        stack.append((window_start, midpoint))


def fetch_earthquakes(node_id: str) -> None:
    asset = node_id
    pages = 0
    total = 0
    url = f"{FDSN_BASE}/query"
    cursor = _parse_z(EQ_SOURCE_MIN)
    stop = datetime.now(tz=timezone.utc).replace(microsecond=0)

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        while cursor < stop:
            next_cursor = min(cursor + timedelta(days=EQ_INITIAL_WINDOW_DAYS), stop)
            try:
                windows = list(_earthquake_windows(cursor, next_cursor))
            except (httpx.HTTPStatusError, httpx.RequestError) as exc:
                if total == 0:
                    raise
                print(
                    f"  WARNING {asset}: count window {_format_z(cursor)}/"
                    f"{_format_z(next_cursor)} failed after retries "
                    f"({type(exc).__name__}: {exc}); finalizing partial catalog "
                    f"with {total} events from {pages} page(s)"
                )
                break

            for start, end, expected in windows:
                params = {
                    "format": "csv",
                    "orderby": "time-asc",
                    "starttime": _format_z(start),
                    "endtime": _format_z(end),
                    "limit": EQ_PAGE_LIMIT,
                }
                try:
                    text = get_text(url, params)
                except (httpx.HTTPStatusError, httpx.RequestError) as exc:
                    if total == 0:
                        raise
                    print(
                        f"  WARNING {asset}: query window {_format_z(start)}/"
                        f"{_format_z(end)} failed after retries "
                        f"({type(exc).__name__}: {exc}); finalizing partial "
                        f"catalog with {total} events from {pages} page(s)"
                    )
                    return

                rows = list(csv.DictReader(io.StringIO(text)))
                if len(rows) > expected:
                    raise RuntimeError(
                        f"{asset}: query returned {len(rows)} rows for "
                        f"{expected}-event window {_format_z(start)}/"
                        f"{_format_z(end)}"
                    )
                for row in rows:
                    # FDSN appears to treat endtime inclusively. Keeping windows
                    # logically half-open prevents boundary duplicates.
                    row_time = row.get("time")
                    if row_time and _parse_z(row_time) >= end and end < stop:
                        continue
                    fh.write(json.dumps(row, separators=(",", ":")) + "\n")
                total += len(rows)
                pages += 1

                if pages >= MAX_PAGES:
                    raise RuntimeError(
                        f"{asset}: hit MAX_PAGES={MAX_PAGES} at {_format_z(end)} "
                        f"({total} rows)"
                    )

            cursor = next_cursor

    print(f"  {asset}: {total} events over {pages} page(s)")


DOWNLOAD_SPECS = [
    *(NodeSpec(id=f"usgs-{entity_id}", fn=fetch_water, kind="download") for entity_id in WATER_ENTITY_IDS),
    *(NodeSpec(id=f"usgs-{entity_id}", fn=fetch_fdsn_list, kind="download") for entity_id in FDSN_LIST_ENDPOINTS),
    NodeSpec(id="usgs-earthquakes", fn=fetch_earthquakes, kind="download"),
]

MAINTAIN_SPECS = [
    *(
        MaintainSpec(
            asset_id=f"usgs-{entity_id}",
            description=(
                "Fresh for one day via raw manifest age; USGS Water Data OGC "
                "live/rolling collections update continuously or daily "
                "(https://api.waterdata.usgs.gov/ogcapi/v0)."
            ),
            check=lambda aid: raw_asset_exists(
                aid,
                "parquet" if aid.removeprefix("usgs-") in PARQUET_WATER_ENTITY_IDS else "ndjson.gz",
                max_age_days=1,
            ),
        )
        for entity_id in sorted(ROLLING_ENTITY_IDS)
    ),
    *(
        MaintainSpec(
            asset_id=f"usgs-{entity_id}",
            description=(
                "Fresh for 30 days via raw manifest age; USGS Water Data/FDSN "
                "reference metadata changes infrequently "
                "(https://api.waterdata.usgs.gov/ogcapi/v0, "
                "https://earthquake.usgs.gov/fdsnws/event/1)."
            ),
            check=lambda aid: raw_asset_exists(aid, "ndjson.gz", max_age_days=30),
        )
        for entity_id in sorted(REFERENCE_ENTITY_IDS)
    ),
    *(
        MaintainSpec(
            asset_id=f"usgs-{entity_id}",
            description=(
                "Fresh for seven days via raw manifest age; USGS Water Data "
                "large observational collections are refreshed on the connector "
                "weekly cadence (https://api.waterdata.usgs.gov/ogcapi/v0)."
            ),
            check=lambda aid: raw_asset_exists(
                aid,
                "parquet" if aid.removeprefix("usgs-") in PARQUET_WATER_ENTITY_IDS else "ndjson.gz",
                max_age_days=7,
            ),
        )
        for entity_id in sorted(
            set(WATER_ENTITY_IDS)
            - ROLLING_ENTITY_IDS
            - REFERENCE_ENTITY_IDS
        )
    ),
    MaintainSpec(
        asset_id="usgs-earthquakes",
        description=(
            "Fresh for seven days via raw manifest age; USGS FDSN ComCat is "
            "queried on the connector weekly cadence "
            "(https://earthquake.usgs.gov/fdsnws/event/1)."
        ),
        check=lambda aid: raw_asset_exists(aid, "ndjson.gz", max_age_days=7),
    ),
]
