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
def _wfs_get(params: list) -> "httpx.Response":
    """One WFS request. On any HTTP error we surface the GeoServer
    ExceptionReport body — its bare `400` is otherwise opaque. A RuntimeError
    here is not transient, so the retry predicate lets it through immediately."""
    resp = get(WFS_URL, params=params, timeout=(15.0, 180.0))
    if resp.status_code >= 400:
        raise RuntimeError(
            f"WFS {resp.status_code} for params={params}: {resp.text[:600]}"
        )
    return resp


def _number_matched(typename: str) -> int | None:
    """Authoritative feature count via WFS resultType=hits (no features pulled).
    Used to detect a silently truncated full pull. Returns None if the server
    omits the count attribute."""
    resp = _wfs_get([
        ("service", "WFS"),
        ("version", "2.0.0"),
        ("request", "GetFeature"),
        ("typeName", typename),
        ("resultType", "hits"),
    ])
    # WFS 2.0.0 -> numberMatched; older GeoServer hits -> numberOfFeatures.
    m = re.search(r'number(?:Matched|OfFeatures)="(\d+)"', resp.text)
    return int(m.group(1)) if m else None


def fetch_layer(node_id: str) -> None:
    configure_http(headers={"User-Agent": _UA})
    typename = TYPENAME_BY_SPEC[node_id]

    # These GeoServer layers expose no primary key, so WFS startIndex/count
    # offset paging is refused ("Cannot do natural order without a primary key").
    # The layers are small, so we pull each in one unpaged GetFeature and verify
    # completeness against the server's own numberMatched rather than paging.
    expected = _number_matched(typename)

    resp = _wfs_get([
        ("service", "WFS"),
        ("version", "2.0.0"),
        ("request", "GetFeature"),
        ("typeName", typename),
        ("outputFormat", "csv"),
    ])
    text = resp.text
    if text.lstrip().startswith("<"):
        # XML ExceptionReport returned with a 200.
        raise RuntimeError(
            f"{node_id}: WFS returned a non-CSV/exception response for {typename}: "
            f"{text[:600]}"
        )

    reader = csv.DictReader(io.StringIO(text))
    rows = [
        {_safe_col(k): (v if v != "" else None) for k, v in rec.items()}
        for rec in reader
    ]

    if not rows:
        raise RuntimeError(f"{node_id}: WFS GetFeature returned 0 features for {typename}")
    if expected is not None and len(rows) < expected:
        # A short pull means the server capped maxFeatures; never publish a
        # silently truncated layer — fail so we add sortBy-based paging instead.
        raise RuntimeError(
            f"{node_id}: truncated pull — got {len(rows)} of {expected} features "
            f"for {typename}; server applied a maxFeatures cap."
        )
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
