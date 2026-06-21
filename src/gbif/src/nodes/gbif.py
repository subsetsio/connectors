"""GBIF connector — published subsets are AGGREGATE statistics, not raw records.

GBIF aggregates ~3.9 billion species-occurrence records from ~122K datasets. We
never download the raw records; instead each subset is a faceted aggregate from
the public REST API (https://api.gbif.org/v1, no auth):

  GET /occurrence/search?limit=0&facet=<field>&facetLimit=<N>
      -> {"count": ..., "facets": [{"field": ..., "counts": [{"name","count"}]}]}

limit=0 returns no records, only the marginal distribution; facetLimit is raised
well above the default (10) so every facet value is captured.

Two fetch shapes:
  * single facet  -> one marginal distribution: (facet_value, count)
  * year panel    -> enumerate an outer dimension's facet values, then run a
                     year facet filtered to each value: (dim, year, count)

Strategy is stateless full re-pull every refresh (shape 1 in the implement
guide): facets are recomputed live server-side, are tiny, and there is no
incremental/delta filter for aggregates — so we just re-snapshot each run and
overwrite. Freshness gating is the maintain step's job.
"""

from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://api.gbif.org/v1"
FACET_LIMIT = 2000  # > observed max distinct (year=527, country=252) so nothing is truncated

# entity_id -> (endpoint, facet_field). One marginal distribution: (facet_value, count).
SINGLE_FACET = {
    "occurrences-by-year": ("occurrence/search", "year"),
    "occurrences-by-publishing-country": ("occurrence/search", "publishingCountry"),
    "occurrences-by-issue": ("occurrence/search", "issue"),
    "occurrences-by-license": ("occurrence/search", "license"),
    "datasets-by-type": ("dataset/search", "type"),
    "datasets-by-publishing-country": ("dataset/search", "publishingCountry"),
}

# entity_id -> (endpoint, outer_facet, filter_param, inner_facet). Year panel:
# enumerate outer_facet values, then facet inner over each via filter_param.
PANEL_FACET = {
    "occurrences-by-year-and-country": ("occurrence/search", "country", "country", "year"),
    "occurrences-by-year-and-kingdom": ("occurrence/search", "kingdomKey", "kingdomKey", "year"),
    "occurrences-by-year-and-basis-of-record": ("occurrence/search", "basisOfRecord", "basisOfRecord", "year"),
}

ENTITY_IDS = list(SINGLE_FACET) + list(PANEL_FACET)

MAX_OUTER_VALUES = 5000  # safety ceiling: outer dimension shouldn't explode past this


@sleep_and_retry
@limits(calls=5, period=1)  # polite cap; GBIF throttles only after a higher per-window threshold
@transient_retry()
def _fetch_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_facet(endpoint: str, facet: str, extra_params: dict | None = None):
    """Return [(name, count), ...] for a single facet field."""
    params = {"limit": 0, "facet": facet, "facetLimit": FACET_LIMIT}
    if extra_params:
        params.update(extra_params)
    data = _fetch_json(f"{BASE}/{endpoint}", params)
    facets = data.get("facets") or []
    if not facets:
        return []
    return [(c["name"], c["count"]) for c in facets[0].get("counts", [])]


def _fetch_single(endpoint: str, facet: str) -> list[dict]:
    return [{"facet_value": name, "n": count} for name, count in _fetch_facet(endpoint, facet)]


def _fetch_panel(endpoint: str, outer_facet: str, filter_param: str, inner_facet: str) -> list[dict]:
    outer_values = [name for name, _ in _fetch_facet(endpoint, outer_facet)]
    if len(outer_values) > MAX_OUTER_VALUES:
        raise RuntimeError(
            f"outer facet {outer_facet} returned {len(outer_values)} values "
            f"(> safety cap {MAX_OUTER_VALUES}) — source shape changed"
        )
    rows = []
    for value in outer_values:
        inner = _fetch_facet(endpoint, inner_facet, extra_params={filter_param: value})
        for inner_name, count in inner:
            rows.append({"facet_value": value, "year": inner_name, "n": count})
    return rows


def fetch_one(node_id: str) -> None:
    """Fetch one aggregate subset. Runtime passes the spec id; it IS the asset name."""
    asset = node_id
    entity = node_id[len("gbif-"):]
    if entity in SINGLE_FACET:
        endpoint, facet = SINGLE_FACET[entity]
        rows = _fetch_single(endpoint, facet)
    elif entity in PANEL_FACET:
        endpoint, outer_facet, filter_param, inner_facet = PANEL_FACET[entity]
        rows = _fetch_panel(endpoint, outer_facet, filter_param, inner_facet)
    else:
        raise ValueError(f"unknown entity {entity!r} for node {node_id}")
    if not rows:
        raise RuntimeError(f"{node_id}: facet query returned no rows")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"gbif-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# ---- Transforms: one published Delta table per subset. ----
# Single-facet raw is {facet_value, n}; panel raw is {facet_value, year, n}.
# Counts can exceed int32 (US has 1.4B occurrences) -> BIGINT. Years are kept
# only when they parse to a positive integer (GBIF year facets carry a few junk
# values); this is a sanity filter, not a hardcoded range.

_T = {
    "gbif-occurrences-by-year": '''
        SELECT TRY_CAST(facet_value AS INTEGER) AS year,
               CAST(n AS BIGINT)                AS occurrence_count
        FROM "gbif-occurrences-by-year"
        WHERE TRY_CAST(facet_value AS INTEGER) IS NOT NULL
          AND TRY_CAST(facet_value AS INTEGER) > 0
        ORDER BY year
    ''',
    "gbif-occurrences-by-publishing-country": '''
        SELECT facet_value         AS publishing_country,
               CAST(n AS BIGINT)    AS occurrence_count
        FROM "gbif-occurrences-by-publishing-country"
        WHERE facet_value IS NOT NULL
        ORDER BY occurrence_count DESC
    ''',
    "gbif-occurrences-by-issue": '''
        SELECT facet_value         AS issue,
               CAST(n AS BIGINT)    AS occurrence_count
        FROM "gbif-occurrences-by-issue"
        WHERE facet_value IS NOT NULL
        ORDER BY occurrence_count DESC
    ''',
    "gbif-occurrences-by-license": '''
        SELECT facet_value         AS license,
               CAST(n AS BIGINT)    AS occurrence_count
        FROM "gbif-occurrences-by-license"
        WHERE facet_value IS NOT NULL
        ORDER BY occurrence_count DESC
    ''',
    "gbif-datasets-by-type": '''
        SELECT facet_value         AS dataset_type,
               CAST(n AS BIGINT)    AS dataset_count
        FROM "gbif-datasets-by-type"
        WHERE facet_value IS NOT NULL
        ORDER BY dataset_count DESC
    ''',
    "gbif-datasets-by-publishing-country": '''
        SELECT facet_value         AS publishing_country,
               CAST(n AS BIGINT)    AS dataset_count
        FROM "gbif-datasets-by-publishing-country"
        WHERE facet_value IS NOT NULL
        ORDER BY dataset_count DESC
    ''',
    "gbif-occurrences-by-year-and-country": '''
        SELECT facet_value                AS country,
               TRY_CAST(year AS INTEGER)  AS year,
               CAST(n AS BIGINT)          AS occurrence_count
        FROM "gbif-occurrences-by-year-and-country"
        WHERE facet_value IS NOT NULL
          AND TRY_CAST(year AS INTEGER) IS NOT NULL
          AND TRY_CAST(year AS INTEGER) > 0
        ORDER BY country, year
    ''',
    "gbif-occurrences-by-year-and-kingdom": '''
        SELECT TRY_CAST(facet_value AS INTEGER) AS kingdom_key,
               TRY_CAST(year AS INTEGER)        AS year,
               CAST(n AS BIGINT)                AS occurrence_count
        FROM "gbif-occurrences-by-year-and-kingdom"
        WHERE TRY_CAST(facet_value AS INTEGER) IS NOT NULL
          AND TRY_CAST(year AS INTEGER) IS NOT NULL
          AND TRY_CAST(year AS INTEGER) > 0
        ORDER BY kingdom_key, year
    ''',
    "gbif-occurrences-by-year-and-basis-of-record": '''
        SELECT facet_value                AS basis_of_record,
               TRY_CAST(year AS INTEGER)  AS year,
               CAST(n AS BIGINT)          AS occurrence_count
        FROM "gbif-occurrences-by-year-and-basis-of-record"
        WHERE facet_value IS NOT NULL
          AND TRY_CAST(year AS INTEGER) IS NOT NULL
          AND TRY_CAST(year AS INTEGER) > 0
        ORDER BY basis_of_record, year
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{download_id}-transform", deps=[download_id], sql=sql)
    for download_id, sql in _T.items()
]
