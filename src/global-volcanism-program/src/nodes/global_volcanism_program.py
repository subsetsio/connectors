"""Global Volcanism Program (GVP) — Smithsonian "Volcanoes of the World" (VOTW).

Access mechanism: the public GeoServer WFS (workspace ``GVP-VOTW``) at
``https://webservices.volcano.si.edu/geoserver/GVP-VOTW/wfs``. Each rank-accepted
entity is one GeoServer feature layer (typeName ``GVP-VOTW:<entity>``). We pull
the whole layer with a single WFS ``GetFeature`` request series in CSV output
(``outputFormat=csv``), paging with ``startIndex``/``count`` so we never silently
truncate a layer that outgrows one page. CSV is parsed with the stdlib csv reader
(faithful: keeps every attribute including the WKT ``GeoLocation`` column) and
stored as raw NDJSON with the source's own column names. Values land as strings
(WFS CSV is untyped text); the SQL transforms cast the known numeric columns.

Stateless full re-pull: the corpus is small (low tens of MB across all layers)
and WFS exposes no incremental filter, so each refresh re-fetches every layer in
full and the transform overwrites the published table.
"""
import io
import csv
import re

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    configure_http,
    is_transient,
    save_raw_ndjson,
)
from constants import ENTITY_IDS, WORKSPACE

SLUG = "global-volcanism-program"
WFS_URL = "https://webservices.volcano.si.edu/geoserver/GVP-VOTW/wfs"

# WFS 2.0.0 page size. The largest layer (Holocene eruptions) is ~11k features,
# so this is two-to-three pages; volcano layers fit in one.
PAGE_SIZE = 5000
# Safety ceiling: ~1M features. Real layers are far smaller; blowing past this
# means the source grew unexpectedly (or paging looped) — raise, never truncate.
MAX_PAGES = 200

# spec id -> WFS typeName. The spec id lowercases/hyphenates the entity id, which
# is lossy, so keep an explicit forward map built from the canonical entity ids.
TYPENAME_BY_SPEC = {
    f"{SLUG}-{e.lower().replace('_', '-')}": f"{WORKSPACE}:{e}" for e in ENTITY_IDS
}

# Browser-style UA: the si.edu edge (Cloudflare / GeoServer) rejects some default
# clients. Header must stay ASCII-only.
_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def _safe_col(key: str) -> str:
    """Delta-safe column name: keep the source's readable name, replace any
    non-alphanumeric/underscore run with a single underscore. Leaves clean VOTW
    names (Volcano_Number, ExplosivityIndexMax, GeoLocation) untouched."""
    k = re.sub(r"[^0-9A-Za-z_]+", "_", str(key).strip()).strip("_")
    if not k:
        k = "col"
    if k[0].isdigit():
        k = "c_" + k
    return k


def _retryable(exc: Exception) -> bool:
    # Standard transient classification plus httpx transport errors: the GeoServer
    # edge can reset/refuse connections under load (ConnectError/ReadError), which
    # is_transient does not cover on its own.
    return is_transient(exc) or isinstance(exc, httpx.TransportError)


@retry(
    retry=retry_if_exception(_retryable),
    stop=stop_after_attempt(6),
    wait=wait_exponential(multiplier=2, min=2, max=60),
    reraise=True,
)
def _get_csv_page(typename: str, start_index: int) -> str:
    """One WFS GetFeature CSV page. typeName is sent under both the 2.0.0 spelling
    (typeNames) and the legacy/vendor spelling (typeName); GeoServer honours
    whichever it expects and ignores the other."""
    params = [
        ("service", "WFS"),
        ("version", "2.0.0"),
        ("request", "GetFeature"),
        ("typeNames", typename),
        ("typeName", typename),
        ("outputFormat", "csv"),
        ("srsName", "EPSG:4326"),
        ("count", str(PAGE_SIZE)),
        ("startIndex", str(start_index)),
    ]
    resp = get(WFS_URL, params=params, timeout=(15.0, 180.0))
    resp.raise_for_status()
    ctype = resp.headers.get("content-type", "")
    text = resp.text
    # GeoServer returns service exceptions as XML with a 200; CSV begins with a
    # header row, never with '<'. Fail loudly so the retry/triage path sees it.
    if "xml" in ctype.lower() or text.lstrip().startswith("<"):
        raise RuntimeError(
            f"WFS returned a non-CSV/exception response for {typename}: "
            f"{text[:300]}"
        )
    return text


def fetch_layer(node_id: str) -> None:
    configure_http(headers={"User-Agent": _UA})
    typename = TYPENAME_BY_SPEC[node_id]

    rows: list[dict] = []
    start = 0
    for page in range(MAX_PAGES):
        text = _get_csv_page(typename, start)
        reader = csv.DictReader(io.StringIO(text))
        page_rows = [
            {_safe_col(k): (v if v != "" else None) for k, v in rec.items()}
            for rec in reader
        ]
        rows.extend(page_rows)
        if len(page_rows) < PAGE_SIZE:
            break
        start += PAGE_SIZE
    else:
        raise RuntimeError(
            f"{node_id}: WFS paging hit MAX_PAGES={MAX_PAGES} without draining "
            f"{typename}; the layer grew past expectations — raise the ceiling."
        )

    if not rows:
        raise RuntimeError(f"{node_id}: WFS GetFeature returned 0 features for {typename}")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_layer,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Per-subset publish SQL. For the two layers whose exact attribute schema is known
# (Holocene volcanoes & eruptions) we TRY_CAST the numeric columns to proper types
# while preserving every other column via `* EXCLUDE`. The Pleistocene volcanoes
# and E3 emissions layers were not probeable from the authoring environment, so
# they publish their attributes faithfully as-is (untyped text) — a clean SELECT *.
_VOLCANOES_ID = f"{SLUG}-smithsonian-votw-holocene-volcanoes"
_ERUPTIONS_ID = f"{SLUG}-smithsonian-votw-holocene-eruptions"

_SQL_BY_SPEC = {
    _VOLCANOES_ID: f'''
        SELECT
            * EXCLUDE (Volcano_Number, Last_Eruption_Year, Latitude, Longitude, Elevation),
            TRY_CAST(Volcano_Number AS BIGINT)     AS Volcano_Number,
            TRY_CAST(Last_Eruption_Year AS BIGINT) AS Last_Eruption_Year,
            TRY_CAST(Latitude AS DOUBLE)           AS Latitude,
            TRY_CAST(Longitude AS DOUBLE)          AS Longitude,
            TRY_CAST(Elevation AS DOUBLE)          AS Elevation
        FROM "{_VOLCANOES_ID}"
    ''',
    _ERUPTIONS_ID: f'''
        SELECT
            * EXCLUDE (
                Volcano_Number, Eruption_Number, ExplosivityIndexMax,
                StartDateYear, StartDateYearUncertainty, StartDateMonth, StartDateDay,
                StartDateDayUncertainty, EndDateYear, EndDateYearUncertainty,
                EndDateMonth, EndDateDay, EndDateDayUncertainty
            ),
            TRY_CAST(Volcano_Number AS BIGINT)            AS Volcano_Number,
            TRY_CAST(Eruption_Number AS BIGINT)           AS Eruption_Number,
            TRY_CAST(ExplosivityIndexMax AS INTEGER)      AS ExplosivityIndexMax,
            TRY_CAST(StartDateYear AS INTEGER)            AS StartDateYear,
            TRY_CAST(StartDateYearUncertainty AS INTEGER) AS StartDateYearUncertainty,
            TRY_CAST(StartDateMonth AS INTEGER)           AS StartDateMonth,
            TRY_CAST(StartDateDay AS INTEGER)             AS StartDateDay,
            TRY_CAST(StartDateDayUncertainty AS INTEGER)  AS StartDateDayUncertainty,
            TRY_CAST(EndDateYear AS INTEGER)              AS EndDateYear,
            TRY_CAST(EndDateYearUncertainty AS INTEGER)   AS EndDateYearUncertainty,
            TRY_CAST(EndDateMonth AS INTEGER)             AS EndDateMonth,
            TRY_CAST(EndDateDay AS INTEGER)               AS EndDateDay,
            TRY_CAST(EndDateDayUncertainty AS INTEGER)    AS EndDateDayUncertainty
        FROM "{_ERUPTIONS_ID}"
    ''',
}


def _sql_for(spec_id: str) -> str:
    return _SQL_BY_SPEC.get(spec_id, f'SELECT * FROM "{spec_id}"')


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_sql_for(s.id),
    )
    for s in DOWNLOAD_SPECS
]
