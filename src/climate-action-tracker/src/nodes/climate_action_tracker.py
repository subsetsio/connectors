"""Climate Action Tracker (CAT) Data Explorer connector.

Two sibling Django REST Framework collections back the CAT Data Explorer:

  - country-emissions: country-level GHG emissions time series + projected
    pathways (https://climateactiontracker.org/data-portal/api/country-emissions/records/)
  - sector-indicators: sectoral decarbonisation indicators / 1.5C benchmarks
    (https://climateactiontracker.org/data-portal/api/records/)

Both are small (~8k / ~7k records, ~3MB JSON total) with NO incremental query
support (no since/cursor/modifiedAfter filter), so the correct shape is a
stateless full re-pull every run: page through {count,next,previous,results}
following the `next` URL until null, then overwrite. Revisions are picked up
for free. NOTE: `next` is returned with an http:// scheme and must be upgraded
to https before following.
"""

from datetime import datetime

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

# Page size is hard-capped at 5000 by the server regardless of request.
PAGE_SIZE = 5000
# Safety ceiling: each corpus is ~2 pages today. A live feed could grow, but a
# runaway page count means a contract change — raise rather than crawl forever.
MAX_PAGES = 200

_ENDPOINTS = {
    "climate-action-tracker-country-emissions": "https://climateactiontracker.org/data-portal/api/country-emissions/records/",
    "climate-action-tracker-sector-indicators": "https://climateactiontracker.org/data-portal/api/records/",
}

# country-emissions record schema. Only `id` is guaranteed non-null; everything
# else is marked nullable so a sparse field never breaks table construction.
_COUNTRY_EMISSIONS_SCHEMA = pa.schema([
    ("id", pa.int64()),
    ("variable", pa.string()),
    ("per_capita", pa.bool_()),
    ("region", pa.string()),
    ("scenario", pa.string()),
    ("sector", pa.string()),
    ("indicator", pa.string()),
    ("year", pa.int64()),
    ("value", pa.float64()),
    ("unit", pa.string()),
    ("version", pa.string()),
    ("comments", pa.string()),
    ("source", pa.string()),
    ("edition", pa.int64()),
])

# sector-indicators record schema.
_SECTOR_INDICATORS_SCHEMA = pa.schema([
    ("id", pa.int64()),
    ("scenario", pa.string()),
    ("sector", pa.string()),
    ("indicator", pa.string()),
    ("country", pa.string()),
    ("year", pa.int64()),
    ("variable", pa.string()),
    ("value", pa.float64()),
    ("unit", pa.string()),
    ("normalized_value", pa.float64()),
    ("edition", pa.int64()),
])

_SCHEMAS = {
    "climate-action-tracker-country-emissions": _COUNTRY_EMISSIONS_SCHEMA,
    "climate-action-tracker-sector-indicators": _SECTOR_INDICATORS_SCHEMA,
}


@transient_retry()
def _fetch_page(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _crawl(start_url: str) -> list[dict]:
    """Page through a DRF list endpoint following `next` until null."""
    rows: list[dict] = []
    # Pin page_size on the first request; `next` carries it forward.
    url = f"{start_url}?page_size={PAGE_SIZE}"
    pages = 0
    while url:
        pages += 1
        if pages > MAX_PAGES:
            raise RuntimeError(
                f"{start_url}: exceeded {MAX_PAGES} pages — source grew past "
                "expectations or pagination is looping"
            )
        payload = _fetch_page(url)
        rows.extend(payload.get("results", []))
        nxt = payload.get("next")
        # `next` is returned with an http:// scheme — upgrade to https.
        url = nxt.replace("http://", "https://", 1) if nxt else None
    return rows


def fetch_records(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    schema = _SCHEMAS[node_id]
    rows = _crawl(_ENDPOINTS[node_id])
    # Project each row onto the declared schema field set so unexpected extra
    # keys don't break table construction; missing keys become null.
    cols = [f.name for f in schema]
    projected = [{c: r.get(c) for c in cols} for r in rows]
    table = pa.Table.from_pylist(projected, schema=schema)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="climate-action-tracker-country-emissions", fn=fetch_records, kind="download"),
    NodeSpec(id="climate-action-tracker-sector-indicators", fn=fetch_records, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="climate-action-tracker-country-emissions-transform",
        deps=["climate-action-tracker-country-emissions"],
        sql='''
            SELECT
                CAST(id AS BIGINT)            AS id,
                region,
                scenario,
                sector,
                indicator,
                variable,
                CAST(year AS INTEGER)         AS year,
                CAST(value AS DOUBLE)         AS value,
                unit,
                per_capita,
                version,
                comments,
                source,
                CAST(edition AS INTEGER)      AS edition
            FROM "climate-action-tracker-country-emissions"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="climate-action-tracker-sector-indicators-transform",
        deps=["climate-action-tracker-sector-indicators"],
        sql='''
            SELECT
                CAST(id AS BIGINT)            AS id,
                country,
                scenario,
                sector,
                indicator,
                variable,
                CAST(year AS INTEGER)         AS year,
                CAST(value AS DOUBLE)         AS value,
                unit,
                CAST(normalized_value AS DOUBLE) AS normalized_value,
                CAST(edition AS INTEGER)      AS edition
            FROM "climate-action-tracker-sector-indicators"
            WHERE value IS NOT NULL
        ''',
    ),
]
