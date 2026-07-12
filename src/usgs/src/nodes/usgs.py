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

from subsets_utils import NodeSpec, raw_writer
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
# windows. The latest-* collections are already live-edge snapshots.
WINDOW_DAYS = {
    "continuous": 1,
    "daily": 14,
}

EQ_SOURCE_MIN = "1900-01-01T00:00:00Z"
EQ_PAGE_LIMIT = 20_000


def _stringify(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, (list, dict)):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


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


def fetch_water(node_id: str) -> None:
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
                fh.write(json.dumps(_feature_row(feature), separators=(",", ":")) + "\n")
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


def fetch_earthquakes(node_id: str) -> None:
    asset = node_id
    watermark = EQ_SOURCE_MIN
    pages = 0
    total = 0
    url = f"{FDSN_BASE}/query"

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        while True:
            params = {
                "format": "csv",
                "orderby": "time-asc",
                "starttime": watermark,
                "limit": EQ_PAGE_LIMIT,
            }
            try:
                text = get_text(url, params)
            except (httpx.HTTPStatusError, httpx.RequestError) as exc:
                if total == 0:
                    raise
                print(
                    f"  WARNING {asset}: window from {watermark} failed after "
                    f"retries ({type(exc).__name__}: {exc}); finalizing partial "
                    f"catalog with {total} events from {pages} page(s)"
                )
                break

            rows = list(csv.DictReader(io.StringIO(text)))
            if not rows:
                break
            for row in rows:
                fh.write(json.dumps(row, separators=(",", ":")) + "\n")
            total += len(rows)
            pages += 1

            last_time = rows[-1].get("time")
            if not last_time:
                raise RuntimeError(f"{asset}: page {pages} row missing time")
            if len(rows) < EQ_PAGE_LIMIT:
                break
            if last_time == watermark:
                raise RuntimeError(f"{asset}: cursor stuck at {watermark}")
            watermark = last_time
            if pages >= MAX_PAGES:
                raise RuntimeError(
                    f"{asset}: hit MAX_PAGES={MAX_PAGES} at {watermark} "
                    f"({total} rows)"
                )

    print(f"  {asset}: {total} events over {pages} page(s)")


DOWNLOAD_SPECS = [
    *(NodeSpec(id=f"usgs-{entity_id}", fn=fetch_water, kind="download") for entity_id in WATER_ENTITY_IDS),
    *(NodeSpec(id=f"usgs-{entity_id}", fn=fetch_fdsn_list, kind="download") for entity_id in FDSN_LIST_ENDPOINTS),
    NodeSpec(id="usgs-earthquakes", fn=fetch_earthquakes, kind="download"),
]
