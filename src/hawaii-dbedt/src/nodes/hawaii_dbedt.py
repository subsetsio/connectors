"""Hawaii DBEDT (Department of Business, Economic Development & Tourism) connector.

Catalog connector over the **UHERO Time Series REST API** (the engine behind the
DBEDT Data Warehouse SPA at https://data.uhero.hawaii.edu/dbedt/, universe
``DBEDT``). Each entity is one *leaf category* of the warehouse's topic tree
(GDP, Visitor Arrivals, Labor Force/Unemployment, Consumer Price Index, …). For
each category we pull every series it contains — across geographies (State of
Hawaii + the 4 counties) and frequencies (Annual/Quarterly/Monthly) — together
with their observations in a single request:

    GET /v1/category/series?id=<catId>&u=DBEDT&expand=true

and publish it as one long-format Delta table: one row per (series, date).

Fetch shape: **stateless full re-pull** (shape 1). The whole corpus is ~59 JSON
pulls totalling well under 1GB, the data is low-frequency with frequent
historical revisions, and the API has no incremental/since parameter — so we
never trust a stored watermark; we re-fetch and overwrite every run.

Auth: a public read-only Bearer token hardcoded in the warehouse's JS bundle
(``main-*.js``). It is not a per-user secret and needs no registration.

Rate limit: none documented and none observed (~0.8s/request, no 429s). Each
spec issues exactly one request; sibling specs share the UHERO host, so we
classify 429/5xx as transient and let exponential backoff find the pace.

Raw is a faithful all-string capture; the SQL transform casts/cleans into the
typed long-format table (the cast doubles as the correctness gate).
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

# Entity union (rank-active leaf category ids). Inlined per the no-module-IO rule.
from constants import ENTITY_IDS

_BASE = "https://api.uhero.hawaii.edu/v1"
# Public read-only token embedded in the DBEDT warehouse JS bundle — not a secret.
_TOKEN = "-VI_yuv0UzZNy4av1SM5vQlkfPK_JKnpGfMzuJR7d0M="
_HEADERS = {"Authorization": f"Bearer {_TOKEN}"}

# Long-format columns, all captured as strings (faithful raw; typed in transform).
_COLUMNS = [
    "series_id", "series_name", "title",
    "measurement_id", "measurement_name",
    "frequency", "units_label", "seasonal_adjustment",
    "geo_fips", "geo_name", "geo_handle",
    "source_description", "date", "value",
]
_SCHEMA = pa.schema([(c, pa.string()) for c in _COLUMNS])


@transient_retry()
def _fetch_category(cat_id: str) -> list:
    resp = get(
        f"{_BASE}/category/series",
        params={"id": cat_id, "u": "DBEDT", "expand": "true"},
        headers=_HEADERS,
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json().get("data") or []


def _category_from_node(node_id: str) -> str:
    """Recover the category id from the spec id (``hawaii-dbedt-<catId>``)."""
    return node_id[len("hawaii-dbedt-"):]


def _str(v) -> str:
    return "" if v is None else str(v)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    cat_id = _category_from_node(node_id)

    series_list = _fetch_category(cat_id)

    columns = {c: [] for c in _COLUMNS}
    for s in series_list:
        geo = s.get("geography") or {}
        so = s.get("seriesObservations") or {}
        results = so.get("transformationResults") or []
        # The level ('lvl') transformation carries the actual observations as
        # parallel dates[]/values[]; pc1/ytd are derived transforms we skip.
        lvl = next((t for t in results if t.get("transformation") == "lvl"), None)
        if not lvl:
            continue
        dates = lvl.get("dates") or []
        values = lvl.get("values") or []
        meta = {
            "series_id": _str(s.get("id")),
            "series_name": _str(s.get("name")),
            "title": _str(s.get("title")),
            "measurement_id": _str(s.get("measurementId")),
            "measurement_name": _str(s.get("measurementName")),
            "frequency": _str(s.get("frequencyShort")),
            "units_label": _str(s.get("unitsLabel")),
            "seasonal_adjustment": _str(s.get("seasonalAdjustment")),
            "geo_fips": _str(geo.get("fips")),
            "geo_name": _str(geo.get("name")),
            "geo_handle": _str(geo.get("handle")),
            "source_description": _str(s.get("sourceDescription")),
        }
        for date, value in zip(dates, values):
            for k, v in meta.items():
                columns[k].append(v)
            columns["date"].append(_str(date))
            columns["value"].append(_str(value))

    table = pa.table(columns, schema=_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"hawaii-dbedt-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per category: cast the faithful string raw into a
# typed long-format observations table. Drop rows whose value is not numerically
# castable (no real observation); the strict CAST of the survivors stays as a
# correctness gate for any genuinely unexpected value.
def _transform_sql(download_id: str) -> str:
    return f'''
        SELECT
            CAST(series_id AS BIGINT)                       AS series_id,
            series_name,
            title,
            TRY_CAST(NULLIF(measurement_id, '') AS BIGINT)  AS measurement_id,
            NULLIF(measurement_name, '')                    AS measurement_name,
            NULLIF(frequency, '')                           AS frequency,
            NULLIF(units_label, '')                         AS units_label,
            NULLIF(seasonal_adjustment, '')                 AS seasonal_adjustment,
            NULLIF(geo_fips, '')                            AS geo_fips,
            NULLIF(geo_name, '')                            AS geo_name,
            NULLIF(geo_handle, '')                          AS geo_handle,
            NULLIF(source_description, '')                  AS source_description,
            CAST(date AS DATE)                              AS date,
            CAST(value AS DOUBLE)                           AS value
        FROM "{download_id}"
        WHERE value IS NOT NULL
          AND value <> ''
          AND TRY_CAST(value AS DOUBLE) IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
