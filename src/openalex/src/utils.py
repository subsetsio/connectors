"""Shared OpenAlex transport and parse helpers.

Two access paths are shared across the per-subset node files:

- The anonymous OpenAlex S3 snapshot (bucket `openalex`, read over HTTPS) backs
  the seven reference entity/taxonomy tables. `iter_entity_rows` streams every
  gzipped JSON-lines partition listed in an entity's top-level `manifest`,
  applying a per-entity flattener.

- The REST API's `group_by` backs the two statistical aggregations.
  `works_group` issues one cheap list call. A `mailto` is always sent (polite
  pool); if OPENALEX_API_KEY is set it is also sent (raises the daily budget).

This module holds transport + genuinely-shared parsing only; no NodeSpecs.
"""

import gzip
import json
import os

from subsets_utils import get, transient_retry

API = "https://api.openalex.org"
S3 = "https://openalex.s3.amazonaws.com"
MAILTO = "openalex-connector@subsets.io"


# ---------------------------------------------------------------------------
# transport: retry transient (429/5xx/network), surface everything else
# ---------------------------------------------------------------------------


@transient_retry()
def get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def api_json(path: str, params: dict) -> dict:
    p = {"mailto": MAILTO, **params}
    key = os.environ.get("OPENALEX_API_KEY")
    if key:
        p["api_key"] = key
    resp = get(f"{API}{path}", params=p, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def short(v):
    """Last path segment of an OpenAlex/UN id URL ('.../fields/22' -> '22')."""
    if not isinstance(v, str):
        return v
    if "://" in v:
        return v.rstrip("/").rsplit("/", 1)[-1]
    return v


def join(lst):
    if not lst:
        return None
    return "; ".join(str(x) for x in lst if x is not None) or None


def stats(rec, k):
    ss = rec.get("summary_stats") or {}
    return ss.get(k)


# ---------------------------------------------------------------------------
# download: S3 snapshot reference entities
# ---------------------------------------------------------------------------

def iter_entity_rows(entity: str, flatten):
    """Stream every snapshot record for `entity`, flattened. Generator so the
    full corpus is never all resident as dict objects at once."""
    manifest = json.loads(get_bytes(f"{S3}/data/jsonl/{entity}/manifest.json"))
    files = manifest.get("files") or []
    if not files:
        raise AssertionError(f"{entity}: snapshot manifest has no files")
    for entry in files:
        url = entry["url"].replace("s3://openalex/", f"{S3}/")
        blob = gzip.decompress(get_bytes(url))
        for line in blob.split(b"\n"):
            if not line.strip():
                continue
            yield flatten(json.loads(line))


# ---------------------------------------------------------------------------
# download: REST group_by aggregations
# ---------------------------------------------------------------------------

def works_group(group_by: str, filt: str | None = None) -> list[dict]:
    params = {"group_by": group_by, "per-page": 200}
    if filt:
        params["filter"] = filt
    return api_json("/works", params).get("group_by") or []
