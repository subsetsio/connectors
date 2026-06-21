"""Hugging Face Hub connector.

Publishes a snapshot of the three listable repo catalogs on the Hugging Face
Hub — models, datasets, spaces. Each is a homogeneous corpus (one row per repo)
with quantitative metadata: downloads, likes, trendingScore, plus createdAt /
lastModified / tags and a few repo-kind-specific fields.

Shape: stateless full re-pull (snapshot). The list endpoints ARE the bulk
mechanism — there is no separate dump — so each refresh pages through the entire
catalog following the RFC5988 Link-header cursor and overwrites the raw asset.
The catalog has no history (only current state), so a full snapshot every run is
correct; revisions are picked up for free. Raw is streamed to one parquet file
per catalog via raw_parquet_writer (the corpora are large: ~1.9M models, ~450k
datasets, ~650k spaces), so memory stays bounded.

Auth is optional: the public catalog is fully readable anonymously. If HF_TOKEN
is present it is sent as a bearer token purely to raise the rate limit (anon 500
API req / 5-min window per IP -> 1000 with a free-tier token). 429s are handled
by the retry decorator's exponential backoff regardless.
"""

import os
import re

import httpx
import pyarrow as pa
from tenacity import retry, retry_if_exception, stop_after_attempt

from subsets_utils import NodeSpec, SqlNodeSpec, get, is_transient, raw_parquet_writer

ENTITY_IDS = ["models", "datasets", "spaces"]

# Absolute safety ceiling: ~1.9M models / 1000 per page ≈ 1900 pages today.
# This fires (and RAISES) only if the corpus grows ~5x past expectations,
# surfacing unexpected source growth rather than silently truncating.
MAX_PAGES = 20000
PAGE_SIZE = 1000

# Per-catalog config. `columns` is the (json_key, arrow_type) contract; the
# expand[] request asks for exactly these non-default fields. `transform_sql`
# is the published table's DuckDB body (one SqlNodeSpec leaf per catalog).
_INT = pa.int64()
_STR = pa.string()
_BOOL = pa.bool_()
_TAGS = pa.list_(pa.string())

CONFIGS = {
    "models": {
        "path": "models",
        "columns": [
            ("id", _STR),
            ("author", _STR),
            ("downloads", _INT),
            ("likes", _INT),
            ("trendingScore", _INT),
            ("pipeline_tag", _STR),
            ("library_name", _STR),
            ("gated", _STR),
            ("private", _BOOL),
            ("createdAt", _STR),
            ("lastModified", _STR),
            ("tags", _TAGS),
        ],
    },
    "datasets": {
        "path": "datasets",
        "columns": [
            ("id", _STR),
            ("author", _STR),
            ("downloads", _INT),
            ("likes", _INT),
            ("trendingScore", _INT),
            ("gated", _STR),
            ("private", _BOOL),
            ("createdAt", _STR),
            ("lastModified", _STR),
            ("tags", _TAGS),
        ],
    },
    "spaces": {
        "path": "spaces",
        "columns": [
            ("id", _STR),
            ("author", _STR),
            ("likes", _INT),
            ("trendingScore", _INT),
            ("sdk", _STR),
            ("private", _BOOL),
            ("createdAt", _STR),
            ("lastModified", _STR),
            ("tags", _TAGS),
        ],
    },
}

# Columns coerced to a plain string in the raw write (the API may return
# false / "auto" / "manual" for gated, so it is not cleanly boolean).
_STRINGIFY = {"gated"}

def _auth_headers() -> dict:
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    return {"Authorization": f"Bearer {token}"} if token else {}


def _reset_seconds(resp: httpx.Response) -> float | None:
    """Seconds until the rate-limit window resets, from the IETF RateLimit
    header (`"api";r=0;t=118`) or a `Retry-After` fallback."""
    rl = resp.headers.get("ratelimit") or resp.headers.get("RateLimit")
    if rl:
        m = re.search(r"t=(\d+)", rl)
        if m:
            return float(m.group(1))
    ra = resp.headers.get("retry-after")
    if ra and ra.isdigit():
        return float(ra)
    return None


def _wait_strategy(retry_state) -> float:
    """On a 429, sleep exactly until the rate-limit window resets (HF enforces
    a fixed 5-minute window; a fixed exponential cap can't reliably outlast it).
    Otherwise back off exponentially for transient network/5xx errors."""
    exc = retry_state.outcome.exception()
    if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 429:
        reset = _reset_seconds(exc.response)
        if reset is not None:
            return min(reset + 3.0, 330.0)
        return 60.0
    return min(4.0 * (2 ** (retry_state.attempt_number - 1)), 120.0)


@retry(
    retry=retry_if_exception(is_transient),
    stop=stop_after_attempt(12),
    wait=_wait_strategy,
    reraise=True,
)
def _get(url: str, params=None, headers=None) -> httpx.Response:
    resp = get(url, params=params, headers=headers, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp


def _next_url(link_header: str | None) -> str | None:
    if not link_header:
        return None
    m = re.search(r'<([^>]+)>;\s*rel="next"', link_header)
    return m.group(1) if m else None


def _schema_for(columns) -> pa.Schema:
    return pa.schema([(name, typ) for name, typ in columns])


def _rows_to_batch(rows, columns) -> pa.RecordBatch:
    arrays = []
    for name, typ in columns:
        if name == "tags":
            col = [r.get("tags") or [] for r in rows]
        elif name in _STRINGIFY:
            col = [None if r.get(name) is None else str(r.get(name)) for r in rows]
        else:
            col = [r.get(name) for r in rows]
        arrays.append(pa.array(col, type=typ))
    return pa.record_batch(arrays, schema=_schema_for(columns))


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("huggingface-"):]
    cfg = CONFIGS[entity]
    columns = cfg["columns"]
    schema = _schema_for(columns)
    headers = _auth_headers()

    expand = [name for name, _ in columns if name != "id"]
    url = f"https://huggingface.co/api/{cfg['path']}"
    params = [("limit", PAGE_SIZE)] + [("expand[]", e) for e in expand]

    pages = 0
    total = 0
    with raw_parquet_writer(asset, schema) as writer:
        while True:
            if pages >= MAX_PAGES:
                raise RuntimeError(
                    f"{asset}: hit MAX_PAGES={MAX_PAGES} (>{total} rows) without "
                    "exhausting the cursor — source grew past expectations"
                )
            resp = _get(url, params=params, headers=headers)
            rows = resp.json()
            pages += 1
            if rows:
                writer.write_batch(_rows_to_batch(rows, columns))
                total += len(rows)
            nxt = _next_url(resp.headers.get("link"))
            if not nxt:
                break
            url = nxt
            params = None  # the next URL already encodes limit + expand + cursor

    if total == 0:
        raise RuntimeError(f"{asset}: crawl produced 0 rows")
    print(f"  {asset}: {total} rows across {pages} pages")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"huggingface-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


def _transform_sql(entity: str) -> str:
    """Thin parse-and-type pass: dedup by repo id (cursor crawls can briefly
    double-list a repo that shifts pages mid-crawl), drop null ids, parse the
    ISO-8601 timestamps, and cast the quantitative columns."""
    asset = f"huggingface-{entity}"
    select_cols = [
        "id",
        "author",
    ]
    if entity in ("models", "datasets"):
        select_cols.append("CAST(downloads AS BIGINT) AS downloads")
    select_cols.append("CAST(likes AS BIGINT) AS likes")
    select_cols.append("CAST(trendingScore AS BIGINT) AS trending_score")
    if entity == "models":
        select_cols += ["pipeline_tag", "library_name", "gated"]
    if entity == "datasets":
        select_cols.append("gated")
    if entity == "spaces":
        select_cols.append("sdk")
    select_cols += [
        "private",
        "try_strptime(createdAt, '%Y-%m-%dT%H:%M:%S.%fZ') AS created_at",
        "try_strptime(lastModified, '%Y-%m-%dT%H:%M:%S.%fZ') AS last_modified",
        "tags",
    ]
    cols = ",\n            ".join(select_cols)
    return f'''
        SELECT
            {cols}
        FROM (
            SELECT *, row_number() OVER (
                PARTITION BY id ORDER BY lastModified DESC
            ) AS _rn
            FROM "{asset}"
            WHERE id IS NOT NULL
        )
        WHERE _rn = 1
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id[len("huggingface-"):]),
    )
    for s in DOWNLOAD_SPECS
]
