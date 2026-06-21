"""INSEE connector — Melodi open-data API (https://api.insee.fr/melodi).

Mechanism: melodi (REST, JSON, no auth). One publishable subset per Melodi
datacube. For each entity we fetch GET /data/{identifier}?maxResult=100000&page=N,
following response.paging.next until it is absent / isLast is true, and stream
each observation to one NDJSON.gz raw asset.

Fetch shape: stateless full re-pull (the default). Melodi exposes no incremental
since/modifiedAfter filter, so each refresh re-fetches the whole datacube and the
transform overwrites the Delta table — revisions are picked up for free. Datacubes
range from ~hundreds to ~14M observations, so raw is streamed page-by-page rather
than buffered in memory.

Each observation is {dimensions:{...}, measures:{<KEY>:{value}}, attributes?:{...}}.
The dimension key set is fixed per datacube (its DSD) but varies across datacubes,
so raw is NDJSON (heterogeneous across assets). We flatten every dimension to a
column, lift the single measure to OBS_VALUE (+ OBS_MEASURE name), and keep the
OBS_STATUS attribute when present. TIME_PERIOD is left as the source string
(annual=YYYY, monthly=YYYY-MM, daily=YYYY-MM-DD) for downstream parsing.

Rate limit: Melodi is documented at 30 req/min (429 beyond). Each NodeSpec runs in
its own process with no cross-process limiter available, so we lean on the retry
decorator's exponential backoff (429 is transient) to find the natural pace and
honour Retry-After when present.
"""

from __future__ import annotations

import json

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, raw_writer

BASE_URL = "https://api.insee.fr/melodi"
PAGE_SIZE = 50000   # smaller pages -> smaller responses, less prone to mid-body truncation
MAX_PAGES = 10000   # safety ceiling (~500M obs); largest real datacube ~290 pages

from constants import ENTITY_IDS

_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError, httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    # A truncated/incomplete body (connection cut mid-stream on large pages)
    # surfaces as a JSON decode error on resp.json() despite a 200 — transient,
    # so retry rather than failing the node.
    if isinstance(exc, json.JSONDecodeError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(10),          # 429s under cross-process contention need headroom
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_json(url: str, params: dict | None = None) -> dict:
    resp = get(url, params=params, headers={"Accept": "application/json"},
               timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _entity_id_from_node(node_id: str) -> str:
    """insee-ds-prenom -> DS_PRENOM (recover the source identifier)."""
    return node_id[len("insee-"):].upper().replace("-", "_")


def _flatten(obs: dict) -> dict:
    """Flatten one Melodi observation to a single record.

    Dimensions become string columns (TIME_PERIOD among them). The single
    measure is lifted to OBS_VALUE (float) + OBS_MEASURE (its key). OBS_STATUS
    is kept from attributes when present.
    """
    row = dict(obs.get("dimensions") or {})
    measures = obs.get("measures") or {}
    obs_value = None
    obs_measure = None
    for key, payload in measures.items():
        obs_measure = key
        val = payload.get("value") if isinstance(payload, dict) else payload
        obs_value = float(val) if val is not None else None
        break  # Melodi datacubes carry a single measure per observation
    row["OBS_MEASURE"] = obs_measure
    row["OBS_VALUE"] = obs_value
    attrs = obs.get("attributes")
    row["OBS_STATUS"] = attrs.get("OBS_STATUS") if isinstance(attrs, dict) else None
    return row


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime hands us the spec id; it IS the raw asset name
    entity_id = _entity_id_from_node(node_id)

    url = f"{BASE_URL}/data/{entity_id}"
    params: dict | None = {"maxResult": PAGE_SIZE, "page": 1}
    total = 0
    pages = 0

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        while True:
            pages += 1
            if pages > MAX_PAGES:
                raise RuntimeError(
                    f"{asset}: exceeded MAX_PAGES={MAX_PAGES} for {entity_id} "
                    "— source grew past expectations; raise the ceiling deliberately"
                )
            doc = _get_json(url, params)
            for obs in doc.get("observations") or []:
                fh.write(json.dumps(_flatten(obs), ensure_ascii=False))
                fh.write("\n")
                total += 1
            paging = doc.get("paging") or {}
            nxt = paging.get("next")
            if not nxt or paging.get("isLast"):
                break
            url, params = nxt, None  # next URL already carries maxResult + page

    print(f"  {asset}: wrote {total} observations across {pages} page(s)")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"insee-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per datacube: pass dimensions through as columns,
# keep observations that carry a value. OBS_VALUE is written as a float so
# read_json_auto types it DOUBLE; the WHERE both drops value-less rows and acts
# as the 0-row correctness gate.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}" WHERE OBS_VALUE IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
