"""UK Nature's Calendar (Woodland Trust) — phenology connector.

Source: the public Umbraco JSON API behind the site's "Live maps"
(https://naturescalendar.woodlandtrust.org.uk/umbraco/api). No auth.

Two published subsets:
  * species_events — reference catalog of the ~179 (species, event) phenology
    series the project records (one row per series). Built from
    SpeciesGroups/List?withChildItems=true.
  * observations — long-format citizen-science point observations across every
    species-event x year. Built by iterating
    observations/listbydate?speciesId=&eventId=&year= for every species-event
    and every year from START_YEAR to the current year.

Fetch shape: stateless full re-pull (shape 1). The observations endpoint has no
incremental filter — its only selector is a discrete `year` (whole-year
snapshots), and both ids are mandatory (omitting either 404s/400s), so there is
no bulk path and no delta query. The whole corpus (~200k-400k records, the UK's
largest phenology database) re-pulls each run via a thread pool; the server
serializes per-series but parallelises across distinct (species, event) pairs,
giving ~10 req/s at 16 workers (~9 min for the full grid). Empty (species,
event, year) combinations return HTTP 200 with items:[] and are simply skipped.
"""

from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

BASE = "https://naturescalendar.woodlandtrust.org.uk/umbraco/api"
START_YEAR = 1998          # earliest year with meaningful coverage (data ramps
                           # from ~1998; pre-1998 returns single-digit/empty).
MAX_WORKERS = 16
FLUSH_ROWS = 50_000        # buffer size for the streamed observations parquet

SE_SCHEMA = pa.schema([
    ("species_id", pa.int64()),
    ("event_id", pa.int64()),
    ("species_name", pa.string()),
    ("latin_name", pa.string()),
    ("nbn_taxonomy", pa.string()),
    ("species_group", pa.string()),
    ("event_name", pa.string()),
    ("event_type", pa.string()),
    ("range_month_from", pa.int64()),
    ("range_day_from", pa.int64()),
    ("range_month_to", pa.int64()),
    ("range_day_to", pa.int64()),
])

OBS_SCHEMA = pa.schema([
    ("observation_id", pa.int64()),
    ("observation_date", pa.string()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("species_id", pa.int64()),
    ("species_name", pa.string()),
    ("event_id", pa.int64()),
    ("event_name", pa.string()),
    ("town", pa.string()),
    ("county", pa.string()),
    ("recorder_id", pa.int64()),
])


@transient_retry()
def _get_json(url, **params):
    resp = get(url, params=params or None, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_catalog():
    """The 3-level species-group -> species -> event tree."""
    return _get_json(f"{BASE}/SpeciesGroups/List", withChildItems="true")


def _walk_species_events(catalog):
    """Yield (group, species_node, event_leaf) for every species-event leaf."""
    for group in catalog:
        for species in group.get("childItems") or []:
            if species.get("id") is None:
                continue
            for leaf in species.get("childItems") or []:
                if leaf.get("id") is None:
                    continue
                yield group, species, leaf


def fetch_species_events(node_id: str) -> None:
    """Download the species-event reference catalog (one row per series)."""
    asset = node_id
    catalog = _fetch_catalog()
    rows = []
    for group, species, leaf in _walk_species_events(catalog):
        se = leaf.get("speciesEvent") or {}
        rows.append({
            "species_id": species.get("id"),
            "event_id": leaf.get("id"),
            "species_name": species.get("name"),
            "latin_name": species.get("latinName"),
            "nbn_taxonomy": species.get("nbnTaxonomy"),
            "species_group": group.get("name"),
            "event_name": leaf.get("name"),
            "event_type": (leaf.get("eventType") or {}).get("name"),
            "range_month_from": se.get("rangeMonthFrom"),
            "range_day_from": se.get("rangeDayFrom"),
            "range_month_to": se.get("rangeMonthTo"),
            "range_day_to": se.get("rangeDayTo"),
        })
    table = pa.Table.from_pylist(rows, schema=SE_SCHEMA)
    save_raw_parquet(table, asset)


def _fetch_observation_year(task):
    """Fetch one (species, event, year) and return flat observation rows."""
    species_id, event_id, year = task
    payload = _get_json(
        f"{BASE}/observations/listbydate",
        speciesId=species_id, eventId=event_id, year=year,
    )
    out = []
    for day in payload.get("items") or []:
        for obs in day.get("observations") or []:
            out.append({
                "observation_id": obs.get("id"),
                "observation_date": obs.get("observationDate"),
                "latitude": obs.get("latitude"),
                "longitude": obs.get("longitude"),
                "species_id": (obs.get("species") or {}).get("id"),
                "species_name": (obs.get("species") or {}).get("name"),
                "event_id": (obs.get("event") or {}).get("id"),
                "event_name": (obs.get("event") or {}).get("name"),
                "town": obs.get("town"),
                "county": obs.get("county"),
                "recorder_id": obs.get("recorderId"),
            })
    return out


def fetch_observations(node_id: str) -> None:
    """Download all observations across every species-event x year.

    Stateless full re-pull, streamed to one parquet asset in row-group flushes
    so peak memory stays bounded regardless of corpus growth.
    """
    asset = node_id
    catalog = _fetch_catalog()
    pairs = [
        (species.get("id"), leaf.get("id"))
        for _g, species, leaf in _walk_species_events(catalog)
    ]
    current_year = datetime.now(tz=timezone.utc).year
    years = range(START_YEAR, current_year + 1)
    tasks = [(sid, eid, y) for (sid, eid) in pairs for y in years]

    buffer = []
    total = 0
    with raw_parquet_writer(asset, OBS_SCHEMA) as writer:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            for rows in pool.map(_fetch_observation_year, tasks):
                if rows:
                    buffer.extend(rows)
                if len(buffer) >= FLUSH_ROWS:
                    writer.write_table(pa.Table.from_pylist(buffer, schema=OBS_SCHEMA))
                    total += len(buffer)
                    buffer = []
        if buffer:
            writer.write_table(pa.Table.from_pylist(buffer, schema=OBS_SCHEMA))
            total += len(buffer)
    print(f"  -> {asset}: {total} observations across {len(pairs)} series, "
          f"{years.start}-{years.stop - 1}")


DOWNLOAD_SPECS = [
    NodeSpec(id="natures-calendar-species-events", fn=fetch_species_events, kind="download"),
    NodeSpec(id="natures-calendar-observations", fn=fetch_observations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="natures-calendar-species-events-transform",
        deps=["natures-calendar-species-events"],
        sql='''
            SELECT
                CAST(species_id AS BIGINT)  AS species_id,
                CAST(event_id   AS BIGINT)  AS event_id,
                species_name,
                latin_name,
                nbn_taxonomy,
                species_group,
                event_name,
                event_type,
                CAST(range_month_from AS INTEGER) AS expected_month_from,
                CAST(range_day_from   AS INTEGER) AS expected_day_from,
                CAST(range_month_to   AS INTEGER) AS expected_month_to,
                CAST(range_day_to     AS INTEGER) AS expected_day_to
            FROM "natures-calendar-species-events"
            WHERE species_id IS NOT NULL AND event_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="natures-calendar-observations-transform",
        deps=["natures-calendar-observations"],
        sql='''
            SELECT
                CAST(observation_id AS BIGINT) AS observation_id,
                CAST(observation_date AS DATE) AS observation_date,
                CAST(EXTRACT(year FROM CAST(observation_date AS DATE)) AS INTEGER) AS year,
                CAST(species_id AS BIGINT) AS species_id,
                species_name,
                CAST(event_id AS BIGINT) AS event_id,
                event_name,
                CAST(latitude  AS DOUBLE) AS latitude,
                CAST(longitude AS DOUBLE) AS longitude,
                CAST(recorder_id AS BIGINT) AS recorder_id,
                town,
                county
            FROM "natures-calendar-observations"
            WHERE observation_date IS NOT NULL
              AND observation_id IS NOT NULL
        ''',
    ),
]
