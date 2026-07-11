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
import csv
import io
import zipfile
import re

import httpx

from subsets_utils import MaintainSpec, NodeSpec, get, raw_asset_exists, raw_writer

BASE_URL = "https://api.insee.fr/melodi"
# Melodi serves pretty-printed JSON over chunked transfer with NO Content-Length,
# so httpx cannot detect a truncated body — a mid-stream connection drop yields a
# partial response that fails to parse (json.JSONDecodeError "Unterminated string").
# These drops are flaky/random, and their probability rises sharply with response
# size: at maxResult=50000 (~38MB on the widest datacube) every attempt truncated
# and all retries were exhausted; at ~7-9MB responses complete reliably and the
# rare drop is recovered by the retry decorator below (which treats a decode error
# as transient). 10000 obs/page keeps the widest datacube (~760 B/obs) near 7.5MB
# while staying large enough that the 30 req/min rate limit, not request count,
# stays the throughput bound.
PAGE_SIZE = 10000
MIN_PAGE_SIZE = 1000
MAX_PAGES = 10000   # safety ceiling (~100M obs/datacube); largest real datacube ~1430 pages
RANGE_CHUNK_SIZE = 1024 * 1024
RANGE_ATTEMPTS = 3

from constants import ENTITY_IDS

def _get_json(url: str, params: dict | None = None) -> dict:
    resp = get(url, params=params, headers={"Accept": "application/json"},
               timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _csv_product_url(entity_id: str) -> str:
    """Return the primary packaged CSV product for a Melodi datacube."""
    catalog = _get_json(f"{BASE_URL}/catalog/all")
    for item in catalog:
        if item.get("identifier") != entity_id:
            continue
        products = item.get("product") or []
        for product in products:
            if (
                product.get("format") == "CSV"
                and product.get("language") == "FR"
                and product.get("accessURL")
            ):
                return product["accessURL"]
        for product in products:
            if product.get("format") == "CSV" and product.get("accessURL"):
                return product["accessURL"]
    raise RuntimeError(f"{entity_id}: no packaged CSV product found in Melodi catalog")


def _get_range(url: str, start: int, end: int) -> bytes:
    expected = end - start + 1
    last_error: BaseException | None = None
    for _ in range(RANGE_ATTEMPTS):
        try:
            resp = get(
                url,
                headers={
                    "Accept": "application/octet-stream",
                    "Range": f"bytes={start}-{end}",
                },
                timeout=(10.0, 120.0),
            )
            resp.raise_for_status()
            if resp.status_code != 206:
                raise RuntimeError(
                    f"range request returned {resp.status_code}, expected 206"
                )
            if len(resp.content) != expected:
                raise RuntimeError(
                    f"range {start}-{end} returned {len(resp.content)} bytes, "
                    f"expected {expected}"
                )
            return resp.content
        except (httpx.HTTPError, RuntimeError) as exc:
            last_error = exc
    raise RuntimeError(f"{url}: failed range {start}-{end}") from last_error


def _download_packaged_zip(url: str) -> bytes:
    first = get(
        url,
        headers={"Accept": "application/octet-stream", "Range": "bytes=0-0"},
        timeout=(10.0, 60.0),
    )
    first.raise_for_status()
    content_range = first.headers.get("content-range") or ""
    match = re.match(r"bytes 0-0/(\d+)$", content_range)
    if first.status_code != 206 or not match:
        raise RuntimeError(f"{url}: packaged CSV endpoint does not support ranges")
    size = int(match.group(1))
    chunks = [first.content]
    for start in range(1, size, RANGE_CHUNK_SIZE):
        end = min(size - 1, start + RANGE_CHUNK_SIZE - 1)
        chunks.append(_get_range(url, start, end))
    payload = b"".join(chunks)
    if len(payload) != size:
        raise RuntimeError(f"{url}: assembled {len(payload)} bytes, expected {size}")
    return payload


def _row_from_csv(row: dict) -> dict:
    out = {key: (None if value == "" else value) for key, value in row.items()}
    value = out.get("OBS_VALUE")
    out["OBS_VALUE"] = float(value) if value is not None else None
    out["OBS_MEASURE"] = out.get("OBS_MEASURE") or "OBS_VALUE"
    out["OBS_STATUS"] = out.get("OBS_STATUS")
    return out


def _fetch_csv_product(asset: str, entity_id: str) -> None:
    url = _csv_product_url(entity_id)
    payload = _download_packaged_zip(url)
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        data_names = [
            name for name in zf.namelist()
            if name.lower().endswith("_data.csv") or name.lower().endswith("data.csv")
        ]
        if not data_names:
            raise RuntimeError(f"{entity_id}: packaged CSV zip has no data CSV")
        with zf.open(data_names[0]) as raw, io.TextIOWrapper(
            raw, encoding="utf-8-sig", newline=""
        ) as text, raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
            reader = csv.DictReader(text, delimiter=";")
            total = 0
            for row in reader:
                fh.write(json.dumps(_row_from_csv(row), ensure_ascii=False))
                fh.write("\n")
                total += 1
    print(f"  {asset}: wrote {total} observations from packaged CSV product")


def _page_params(offset: int, page_size: int) -> dict:
    return {"maxResult": page_size, "page": (offset // page_size) + 1}


def _can_shrink_page(exc: BaseException, page_size: int) -> bool:
    if page_size <= MIN_PAGE_SIZE:
        return False
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    # A truncated/incomplete body (connection cut mid-stream on large pages)
    # surfaces as a JSON decode error on resp.json() despite a 200. Smaller
    # pages materially reduce that failure mode.
    return isinstance(exc, json.JSONDecodeError)


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
    page_size = PAGE_SIZE
    offset = 0
    total = 0
    pages = 0

    try:
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
            while True:
                pages += 1
                if pages > MAX_PAGES:
                    raise RuntimeError(
                        f"{asset}: exceeded MAX_PAGES={MAX_PAGES} for {entity_id} "
                        "— source grew past expectations; raise the ceiling deliberately"
                    )
                try:
                    doc = _get_json(url, _page_params(offset, page_size))
                except (httpx.HTTPStatusError, json.JSONDecodeError) as exc:
                    if not _can_shrink_page(exc, page_size):
                        raise
                    next_size = max(MIN_PAGE_SIZE, page_size // 2)
                    print(
                        f"  {asset}: page at offset {offset} failed with "
                        f"{type(exc).__name__}; retrying with maxResult={next_size}"
                    )
                    page_size = next_size
                    continue

                observations = doc.get("observations") or []
                for obs in observations:
                    fh.write(json.dumps(_flatten(obs), ensure_ascii=False))
                    fh.write("\n")
                total += len(observations)
                offset += len(observations)
                paging = doc.get("paging") or {}
                if not paging.get("next") or paging.get("isLast"):
                    break

        print(f"  {asset}: wrote {total} observations across {pages} page(s)")
    except httpx.HTTPStatusError as exc:
        code = exc.response.status_code
        if code != 429 and not 500 <= code < 600:
            raise
        print(
            f"  {asset}: Melodi JSON pagination failed with HTTP {code}; "
            "falling back to packaged CSV product"
        )
        _fetch_csv_product(asset, entity_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"insee-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=f"insee-{eid.lower().replace('_', '-')}",
        description=(
            "Weekly refresh cadence for INSEE Melodi datacubes; no per-cube "
            "incremental or validator signal is exposed by the API "
            "(inferred from connector maintenance cadence)."
        ),
        check=lambda aid: raw_asset_exists(aid, "ndjson.gz", max_age_days=7),
    )
    for eid in ENTITY_IDS
]
