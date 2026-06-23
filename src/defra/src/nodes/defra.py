"""DEFRA — Environment Agency Data Services Platform (environment.data.gov.uk).

Two verified, no-auth, Open-Government-Licence linked-data REST corpora:

* **flood-monitoring** — real-time river/tidal level, flow and rainfall network.
  We publish the station catalog, the measure catalog, the flood-warning-area
  reference, and the latest reading per measure (a network-wide snapshot).
* **hydrology** — river flow/level, groundwater, rainfall and quality network.
  We publish the station catalog, the measure catalog, and a rolling recent
  window of daily readings across all stations.

Fetch shape: stateless full re-pull. The reference lists and the flood `?latest`
snapshot are single requests; hydrology readings are pulled one complete day at
a time over a recent rolling window (the full history is far too large to
re-pull every run, and the API has no all-readings firehose — only a per-day
filter). Each fetch flattens the JSON-LD `{meta, items}` envelope to flat scalar
records and writes NDJSON; the SQL transforms cast and publish one Delta table
each.
"""

import json
from datetime import date, timedelta

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
    raw_writer,
)

BASE = "https://environment.data.gov.uk"

# Reference-list page size: comfortably above every collection's row count
# (largest is ~32k hydrology measures). If a response ever hits this it means
# the collection grew past our assumption and was silently truncated -> raise.
LIST_LIMIT = 200_000

# Per-day hard row cap for hydrology readings (the API's documented hard cap).
# One day is ~310k rows today; a response at the cap means the day needs
# paginating, so we raise rather than publish a truncated day.
READINGS_HARD_CAP = 2_000_000

# Rolling window of complete days of hydrology readings to publish each run.
READINGS_WINDOW_DAYS = 7


@transient_retry()
def _get_json(url, params=None):
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _as_text(v):
    """Coerce a JSON-LD value to plain text; join multi-valued fields."""
    if v is None:
        return None
    if isinstance(v, list):
        joined = "; ".join(str(x) for x in v if x is not None)
        return joined or None
    return str(v)


def _last_segment(v):
    """Last path segment of a linked-data URI (the local id); pass non-URIs
    through unchanged. Handles {'@id': ...} dicts and single-item lists."""
    if isinstance(v, dict):
        v = v.get("@id")
    if isinstance(v, list):
        v = v[0] if v else None
    if not isinstance(v, str):
        return None
    return v.rstrip("/").rsplit("/", 1)[-1]


def _list_items(url, params):
    doc = _get_json(url, params=params)
    items = doc.get("items", [])
    if not isinstance(items, list):
        items = [items]
    limit = params.get("_limit")
    if limit is not None and len(items) >= limit:
        raise RuntimeError(
            f"{url}: returned {len(items)} items at the _limit ceiling "
            f"({limit}) — collection grew past assumption / truncated."
        )
    return items


# ---------------------------------------------------------------- flood-monitoring

def fetch_flood_stations(node_id: str) -> None:
    items = _list_items(
        f"{BASE}/flood-monitoring/id/stations.json", {"_limit": LIST_LIMIT}
    )
    rows = [
        {
            "station_reference": it.get("stationReference"),
            "notation": it.get("notation"),
            "label": _as_text(it.get("label")),
            "river_name": _as_text(it.get("riverName")),
            "catchment_name": _as_text(it.get("catchmentName")),
            "town": _as_text(it.get("town")),
            "lat": it.get("lat"),
            "long": it.get("long"),
            "easting": it.get("easting"),
            "northing": it.get("northing"),
            "date_opened": it.get("dateOpened"),
            "status": _last_segment(it.get("status")),
            "rloi_id": _as_text(it.get("RLOIid")),
        }
        for it in items
    ]
    save_raw_ndjson(rows, node_id)


def fetch_flood_measures(node_id: str) -> None:
    items = _list_items(
        f"{BASE}/flood-monitoring/id/measures.json", {"_limit": LIST_LIMIT}
    )
    rows = [
        {
            "notation": it.get("notation"),
            "label": _as_text(it.get("label")),
            "parameter": _as_text(it.get("parameter")),
            "parameter_name": _as_text(it.get("parameterName")),
            "qualifier": _as_text(it.get("qualifier")),
            "unit": _last_segment(it.get("unit")),
            "unit_name": _as_text(it.get("unitName")),
            "period": it.get("period"),
            "value_type": _as_text(it.get("valueType")),
            "datum_type": _last_segment(it.get("datumType")),
            "station_reference": it.get("stationReference"),
        }
        for it in items
    ]
    save_raw_ndjson(rows, node_id)


def fetch_flood_readings(node_id: str) -> None:
    # `?latest` returns the most recent reading for every measure (one snapshot
    # row per measure) and bypasses the default page limit.
    doc = _get_json(f"{BASE}/flood-monitoring/data/readings.json?latest")
    items = doc.get("items", [])
    rows = [
        {
            "measure_id": _last_segment(it.get("measure")),
            "measure_uri": it.get("measure")
            if isinstance(it.get("measure"), str)
            else None,
            "date_time": it.get("dateTime"),
            "value": it.get("value"),
        }
        for it in items
    ]
    save_raw_ndjson(rows, node_id)


def fetch_flood_areas(node_id: str) -> None:
    # The flood-warning *areas* — the stable backbone of the warnings service
    # (the live `floods` feed lists only currently-active warnings and is often
    # empty in dry spells, which would fail a 0-row transform).
    items = _list_items(
        f"{BASE}/flood-monitoring/id/floodAreas.json", {"_limit": LIST_LIMIT}
    )
    rows = [
        {
            "notation": it.get("notation"),
            "label": _as_text(it.get("label")),
            "description": _as_text(it.get("description")),
            "county": _as_text(it.get("county")),
            "ea_area_name": _as_text(it.get("eaAreaName")),
            "river_or_sea": _as_text(it.get("riverOrSea")),
            "fwd_code": _as_text(it.get("fwdCode")),
            "quick_dial_number": _as_text(it.get("quickDialNumber")),
            "lat": it.get("lat"),
            "long": it.get("long"),
        }
        for it in items
    ]
    save_raw_ndjson(rows, node_id)


# ---------------------------------------------------------------- hydrology

def fetch_hydrology_stations(node_id: str) -> None:
    items = _list_items(
        f"{BASE}/hydrology/id/stations.json", {"_limit": LIST_LIMIT}
    )
    rows = [
        {
            "notation": it.get("notation"),
            "label": _as_text(it.get("label")),
            "river_name": _as_text(it.get("riverName")),
            "lat": it.get("lat"),
            "long": it.get("long"),
            "easting": it.get("easting"),
            "northing": it.get("northing"),
            "date_opened": it.get("dateOpened"),
            "status": _last_segment(it.get("status")),
            "station_guid": _as_text(it.get("stationGuid")),
            "wiski_id": _as_text(it.get("wiskiID")),
        }
        for it in items
    ]
    save_raw_ndjson(rows, node_id)


def fetch_hydrology_measures(node_id: str) -> None:
    items = _list_items(
        f"{BASE}/hydrology/id/measures.json", {"_limit": LIST_LIMIT}
    )
    rows = [
        {
            "notation": it.get("notation"),
            "label": _as_text(it.get("label")),
            "parameter": _as_text(it.get("parameter")),
            "parameter_name": _as_text(it.get("parameterName")),
            "observed_property": _last_segment(it.get("observedProperty")),
            "period": it.get("period"),
            "period_name": _as_text(it.get("periodName")),
            "value_statistic": _last_segment(it.get("valueStatistic")),
            "unit": _last_segment(it.get("unit")),
            "unit_name": _as_text(it.get("unitName")),
            "station": _last_segment(it.get("station")),
            "observation_type": _last_segment(it.get("observationType")),
        }
        for it in items
    ]
    save_raw_ndjson(rows, node_id)


def fetch_hydrology_readings(node_id: str) -> None:
    # No all-readings firehose: pull one complete day at a time over a recent
    # rolling window. Stream NDJSON so peak memory stays at one day (~310k rows).
    end = date.today() - timedelta(days=1)  # last complete day
    days = [end - timedelta(days=i) for i in range(READINGS_WINDOW_DAYS)]
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as w:
        for d in days:
            ds = d.isoformat()
            items = _list_items(
                f"{BASE}/hydrology/data/readings.json",
                {"date": ds, "_limit": READINGS_HARD_CAP},
            )
            for it in items:
                w.write(
                    json.dumps(
                        {
                            "measure_id": _last_segment(it.get("measure")),
                            "date": it.get("date"),
                            "date_time": it.get("dateTime"),
                            "value": it.get("value"),
                            "quality": _as_text(it.get("quality")),
                        }
                    )
                    + "\n"
                )


DOWNLOAD_SPECS = [
    NodeSpec(id="defra-flood-monitoring-stations", fn=fetch_flood_stations, kind="download"),
    NodeSpec(id="defra-flood-monitoring-measures", fn=fetch_flood_measures, kind="download"),
    NodeSpec(id="defra-flood-monitoring-readings", fn=fetch_flood_readings, kind="download"),
    NodeSpec(id="defra-flood-monitoring-floods", fn=fetch_flood_areas, kind="download"),
    NodeSpec(id="defra-hydrology-stations", fn=fetch_hydrology_stations, kind="download"),
    NodeSpec(id="defra-hydrology-measures", fn=fetch_hydrology_measures, kind="download"),
    NodeSpec(id="defra-hydrology-readings", fn=fetch_hydrology_readings, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="defra-flood-monitoring-stations-transform",
        deps=["defra-flood-monitoring-stations"],
        sql='''
            SELECT
                notation,
                station_reference,
                label,
                river_name,
                catchment_name,
                town,
                TRY_CAST(lat AS DOUBLE)      AS lat,
                TRY_CAST(long AS DOUBLE)     AS lon,
                TRY_CAST(easting AS DOUBLE)  AS easting,
                TRY_CAST(northing AS DOUBLE) AS northing,
                TRY_CAST(date_opened AS DATE) AS date_opened,
                status,
                rloi_id
            FROM "defra-flood-monitoring-stations"
            WHERE notation IS NOT NULL AND notation <> ''
        ''',
    ),
    SqlNodeSpec(
        id="defra-flood-monitoring-measures-transform",
        deps=["defra-flood-monitoring-measures"],
        sql='''
            SELECT
                notation,
                station_reference,
                label,
                parameter,
                parameter_name,
                qualifier,
                unit,
                unit_name,
                TRY_CAST(period AS BIGINT) AS period_seconds,
                value_type,
                datum_type
            FROM "defra-flood-monitoring-measures"
            WHERE notation IS NOT NULL AND notation <> ''
        ''',
    ),
    SqlNodeSpec(
        id="defra-flood-monitoring-readings-transform",
        deps=["defra-flood-monitoring-readings"],
        sql='''
            SELECT
                measure_id,
                TRY_CAST(date_time AS TIMESTAMP) AS observed_at,
                TRY_CAST(value AS DOUBLE) AS value
            FROM "defra-flood-monitoring-readings"
            WHERE measure_id IS NOT NULL
              AND TRY_CAST(value AS DOUBLE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="defra-flood-monitoring-floods-transform",
        deps=["defra-flood-monitoring-floods"],
        sql='''
            SELECT
                notation,
                label,
                description,
                county,
                ea_area_name,
                river_or_sea,
                fwd_code,
                quick_dial_number,
                TRY_CAST(lat AS DOUBLE)  AS lat,
                TRY_CAST(long AS DOUBLE) AS lon
            FROM "defra-flood-monitoring-floods"
            WHERE notation IS NOT NULL AND notation <> ''
        ''',
    ),
    SqlNodeSpec(
        id="defra-hydrology-stations-transform",
        deps=["defra-hydrology-stations"],
        sql='''
            SELECT
                notation,
                label,
                river_name,
                TRY_CAST(lat AS DOUBLE)      AS lat,
                TRY_CAST(long AS DOUBLE)     AS lon,
                TRY_CAST(easting AS DOUBLE)  AS easting,
                TRY_CAST(northing AS DOUBLE) AS northing,
                TRY_CAST(date_opened AS DATE) AS date_opened,
                station_guid,
                wiski_id
            FROM "defra-hydrology-stations"
            WHERE notation IS NOT NULL AND notation <> ''
        ''',
    ),
    SqlNodeSpec(
        id="defra-hydrology-measures-transform",
        deps=["defra-hydrology-measures"],
        sql='''
            SELECT
                notation,
                station,
                label,
                parameter,
                parameter_name,
                observed_property,
                value_statistic,
                TRY_CAST(period AS BIGINT) AS period_seconds,
                period_name,
                unit,
                unit_name,
                observation_type
            FROM "defra-hydrology-measures"
            WHERE notation IS NOT NULL AND notation <> ''
        ''',
    ),
    SqlNodeSpec(
        id="defra-hydrology-readings-transform",
        deps=["defra-hydrology-readings"],
        sql='''
            SELECT
                measure_id,
                TRY_CAST(date AS DATE) AS date,
                TRY_CAST(date_time AS TIMESTAMP) AS observed_at,
                TRY_CAST(value AS DOUBLE) AS value,
                quality
            FROM "defra-hydrology-readings"
            WHERE measure_id IS NOT NULL
              AND TRY_CAST(value AS DOUBLE) IS NOT NULL
        ''',
    ),
]
