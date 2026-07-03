"""UKHSA Data Dashboard connector.

One published subset (`values`): the long-format time-series corpus of the UK
Health Security Agency data dashboard. The API is strictly hierarchical and has
no bulk export, so the corpus is assembled by traversing

    themes -> sub_themes -> topics -> geography_types -> geographies -> metrics

and paging the leaf (metric, geography) endpoints, each of which returns the
full history for that single series under one stable schema.

Geography scope
---------------
The API exposes seven geography types; the sub-regional ones explode the leaf
count into the hundreds of thousands with little query value:

    Nation (1)  Government Office Region (9)  NHS Region (7)  UKHSA Region (9)
    NHS Trust (277)  Lower Tier Local Authority (318)  Upper Tier LA (150)

This connector deliberately scopes the crawl to the national + regional levels
(`GEOGRAPHY_TYPES`), which carry the flagship, most-queried public-health series
while keeping a full re-pull tractable in one run. This is an explicit,
documented scope decision (logged at run time) -- NOT a silent truncation; the
finer geographies can be added later by extending GEOGRAPHY_TYPES.

Refresh strategy: stateless full re-pull. There is no incremental query filter
(no since/modifiedAfter/cursor), so every run re-traverses the hierarchy and
overwrites. Revisions and late corrections are picked up for free.
"""

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    configure_http,
    raw_parquet_writer,
    transient_retry,
)

BASE = "https://api.ukhsa-dashboard.data.gov.uk"

# National + regional levels only -- see module docstring.
GEOGRAPHY_TYPES = {
    "Nation",
    "Government Office Region",
    "NHS Region",
    "UKHSA Region",
}

PAGE_SIZE = 365            # API hard max
MAX_PAGES_PER_LEAF = 2000  # backstop against a pagination loop; raises if hit
WRITE_BATCH_ROWS = 50_000  # flush a parquet row group roughly this often

# The leaf time-series record schema (stable across the whole API). Numeric
# axis columns and the late-arriving in_reporting_delay_period flag are nullable
# because annual/older series omit some of them. date is kept as a string and
# cast to DATE in the transform.
SCHEMA = pa.schema([
    ("theme", pa.string()),
    ("sub_theme", pa.string()),
    ("topic", pa.string()),
    ("geography_type", pa.string()),
    ("geography", pa.string()),
    ("geography_code", pa.string()),
    ("metric", pa.string()),
    ("metric_group", pa.string()),
    ("stratum", pa.string()),
    ("sex", pa.string()),
    ("age", pa.string()),
    ("year", pa.int64()),
    ("month", pa.int64()),
    ("epiweek", pa.int64()),
    ("date", pa.string()),
    ("metric_value", pa.float64()),
    ("in_reporting_delay_period", pa.bool_()),
])

_FIELD_NAMES = [f.name for f in SCHEMA]


# --- HTTP with retry --------------------------------------------------------


@transient_retry(min_wait=2, max_wait=60)
def _get_json(url, params=None):
    resp = get(
        url,
        params=params,
        headers={"Accept": "application/json"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


# --- hierarchy traversal ----------------------------------------------------

def _child_collection(item_url):
    """Return the child collection of a named-item endpoint as [(name, link)].

    The API alternates shapes: a named-item endpoint (e.g. /themes/<theme>)
    returns a single-element list whose dict maps the child level to its
    *collection* URL, e.g. [{"sub_themes": ".../sub_themes/"}]; the collection
    URL then returns the real [{name, link}] listing. The root /themes/ is a
    collection already and is handled by _listing directly."""
    resp = _get_json(item_url)
    direct = _listing(resp)
    if direct:
        return direct
    if isinstance(resp, list) and resp and isinstance(resp[0], dict):
        for v in resp[0].values():
            if isinstance(v, str) and v.startswith("http"):
                return _listing(_get_json(v))
    return []


def _listing(resp):
    out = []
    if isinstance(resp, list):
        for item in resp:
            if isinstance(item, dict) and item.get("name") and item.get("link"):
                out.append((item["name"], item["link"]))
    return out


def _iter_leaves():
    """Yield (metric_name, leaf_url) for every (metric, geography) under the
    in-scope geography types."""
    themes = _listing(_get_json(f"{BASE}/themes/"))
    if not themes:
        raise RuntimeError("themes endpoint returned no themes")
    for _theme, theme_link in themes:
        for _sub, sub_link in _child_collection(theme_link):
            for _topic, topic_link in _child_collection(sub_link):
                for gtype_name, gtype_link in _child_collection(topic_link):
                    if gtype_name not in GEOGRAPHY_TYPES:
                        continue
                    for _geo, geo_link in _child_collection(gtype_link):
                        for metric_name, metric_link in _child_collection(geo_link):
                            yield metric_name, metric_link


# --- row coercion -----------------------------------------------------------

def _to_int(v):
    if v is None or v == "":
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _to_float(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _to_str(v):
    return None if v is None else str(v)


def _row(rec):
    return {
        "theme": _to_str(rec.get("theme")),
        "sub_theme": _to_str(rec.get("sub_theme")),
        "topic": _to_str(rec.get("topic")),
        "geography_type": _to_str(rec.get("geography_type")),
        "geography": _to_str(rec.get("geography")),
        "geography_code": _to_str(rec.get("geography_code")),
        "metric": _to_str(rec.get("metric")),
        "metric_group": _to_str(rec.get("metric_group")),
        "stratum": _to_str(rec.get("stratum")),
        "sex": _to_str(rec.get("sex")),
        "age": _to_str(rec.get("age")),
        "year": _to_int(rec.get("year")),
        "month": _to_int(rec.get("month")),
        "epiweek": _to_int(rec.get("epiweek")),
        "date": _to_str(rec.get("date")),
        "metric_value": _to_float(rec.get("metric_value")),
        "in_reporting_delay_period": rec.get("in_reporting_delay_period"),
    }


def _iter_leaf_rows(leaf_url):
    """Page through one leaf, yielding coerced row dicts. A permanent 4xx on a
    single leaf (e.g. a metric withdrawn for one geography) is logged and the
    leaf is skipped rather than failing the whole crawl."""
    url, params = leaf_url, {"page_size": PAGE_SIZE}
    pages = 0
    try:
        while url:
            payload = _get_json(url, params=params)
            params = None  # `next` already carries the query string
            for rec in payload.get("results", []):
                yield _row(rec)
            url = payload.get("next")
            pages += 1
            if pages > MAX_PAGES_PER_LEAF:
                raise RuntimeError(
                    f"leaf {leaf_url} exceeded {MAX_PAGES_PER_LEAF} pages -- "
                    "pagination likely looping"
                )
    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        if code == 429 or 500 <= code < 600:
            raise  # transient -- let retry/runner handle it
        print(f"  ! skipping leaf {leaf_url}: HTTP {code}")


# --- download node ----------------------------------------------------------

def fetch_values(node_id: str) -> None:
    asset = node_id
    configure_http(headers={"Accept": "application/json"})

    leaves = 0
    total_rows = 0
    batch = []
    with raw_parquet_writer(asset, SCHEMA) as writer:
        for _metric, leaf_url in _iter_leaves():
            leaves += 1
            for row in _iter_leaf_rows(leaf_url):
                batch.append(row)
                if len(batch) >= WRITE_BATCH_ROWS:
                    writer.write_table(pa.Table.from_pylist(batch, schema=SCHEMA))
                    total_rows += len(batch)
                    batch = []
            if leaves % 200 == 0:
                print(f"  .. {leaves} leaves crawled, {total_rows + len(batch):,} rows")
        if batch:
            writer.write_table(pa.Table.from_pylist(batch, schema=SCHEMA))
            total_rows += len(batch)

    print(f"  -> {asset}: {leaves} leaves, {total_rows:,} rows "
          f"(geography types: {sorted(GEOGRAPHY_TYPES)})")
    if total_rows == 0:
        raise RuntimeError("crawl produced 0 rows -- API shape may have changed")


DOWNLOAD_SPECS = [
    NodeSpec(id="ukhsa-values", fn=fetch_values, kind="download"),
]


# --- transform: publish one Delta table -------------------------------------

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ukhsa-values-transform",
        deps=["ukhsa-values"],
        temporal="date",
        sql='''
            SELECT DISTINCT
                theme,
                sub_theme,
                topic,
                geography_type,
                geography,
                geography_code,
                metric,
                metric_group,
                stratum,
                sex,
                age,
                CAST(year AS INTEGER)            AS year,
                CAST(month AS INTEGER)           AS month,
                CAST(epiweek AS INTEGER)         AS epiweek,
                CAST(date AS DATE)               AS date,
                CAST(metric_value AS DOUBLE)     AS metric_value,
                in_reporting_delay_period
            FROM "ukhsa-values"
            WHERE date IS NOT NULL
              AND metric_value IS NOT NULL
        ''',
    ),
]
