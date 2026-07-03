"""Source-side freshness signal for MaintainSpec checks.

Two halves, deliberately split:

  `source_unchanged(asset_id, url)` — READ-ONLY probe for use inside a
  MaintainSpec check. HEADs the url (falling back to a headers-only ranged
  GET when the server rejects HEAD) and compares the source's current
  ETag / Last-Modified against the signature persisted in the asset's
  state. Returns True ONLY when a stored signature exists AND matches.
  No signature stored, no signature offered by the server, or any probe
  failure all mean False (fetch) — never guess. It never writes state.

  `record_source_signature(asset_id, url, response=...)` — called by the
  download fn strictly AFTER a successful fetch; persists the signature
  the fetch was served under. Because the signature only advances on
  success, a failed fetch can never cause a false "fresh" skip later.

Typical wiring in a node module:

    from subsets_utils import (MaintainSpec, NodeSpec, get, raw_asset_exists,
                               record_source_signature, save_raw_file,
                               source_unchanged)

    URL = "https://example.org/data.csv"

    def fetch_data(node_id: str) -> None:
        resp = get(URL, timeout=(10.0, 120.0))
        resp.raise_for_status()
        save_raw_file(resp.content, node_id, "csv")
        record_source_signature(node_id, URL, response=resp)

    MAINTAIN_SPECS = [
        MaintainSpec(
            asset_id="acme-data",
            description="Updated monthly per https://example.org/data (Last-Modified)",
            check=lambda aid: source_unchanged(aid, URL) and raw_asset_exists(aid, "csv"),
        ),
    ]

Maintain checks run in the PARENT orchestrator process before any node
subprocess spawns (orchestrator._apply_maintain_skips), so keep them cheap:
one HEAD per asset. `FORCE_REFRESH=1` bypasses every check.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone

from . import tracking
from .http_client import get_client, head
from .io import load_state, save_state

# Fetch-fn-managed state key holding `{url: {etag?, last_modified?, recorded_at}}`.
# Deliberately NOT underscore-prefixed: the signature belongs to the download
# fn's own state namespace (record_source_signature is called from fetch fns),
# and save_state reserves underscore keys for the orchestrator.
STATE_KEY = "source_signatures"

# HEAD responses that mean "method unsupported, try a ranged GET" rather than
# "resource gone/denied" (which stays a plain probe failure → fetch).
_HEAD_UNSUPPORTED = (405, 501)


def _signature(headers) -> dict | None:
    """Extract the validator headers a signature is built from, or None when
    the server offers neither."""
    etag = headers.get("ETag")
    last_modified = headers.get("Last-Modified")
    if not etag and not last_modified:
        return None
    sig: dict = {}
    if etag:
        sig["etag"] = etag
    if last_modified:
        sig["last_modified"] = last_modified
    return sig


def _norm_etag(value: str) -> str:
    """Compare ETags weak-insensitively: some origins serve `W/"x"` on HEAD
    and `"x"` on GET for the same representation."""
    return value[2:] if value.startswith("W/") else value


def _probe_headers(url: str, timeout: float):
    """Current response headers for `url` via HEAD, or a headers-only ranged
    GET when the server rejects HEAD. Returns httpx.Headers, or None when the
    source refused both probes. Uses the shared retrying client (http_client),
    so transient failures already got their backoff before we give up."""
    resp = head(url, timeout=timeout)
    if resp.status_code < 400:
        return resp.headers
    if resp.status_code not in _HEAD_UNSUPPORTED:
        return None

    # HEAD unsupported: ranged GET, streamed so the body is never read — a
    # server that ignores Range would otherwise ship the whole file into the
    # parent process. Logged by hand since http_client's helpers buffer bodies.
    start = time.time()
    status = None
    error = None
    headers = None
    try:
        with get_client().stream(
            "GET", url, headers={"Range": "bytes=0-0"}, timeout=timeout
        ) as r:
            status = r.status_code
            headers = r.headers
    except Exception as e:  # noqa: BLE001 — probe failure means "fetch", not crash
        error = str(e)
    finally:
        tracking.record_http("GET", url, status,
                             duration_ms=int((time.time() - start) * 1000),
                             error=error)
    if headers is None or (status is not None and status >= 400):
        return None
    return headers


def source_unchanged(asset_id: str, url: str, *, timeout: float = 30.0) -> bool:
    """True iff a signature recorded for (asset, url) exists AND matches the
    source's current ETag / Last-Modified.

    Read-only — never persists anything (`record_source_signature` owns the
    write side, after a successful fetch). Every uncertain outcome returns
    False so the fetch runs: no stored signature, the server offering no
    validator headers, or any probe failure.
    """
    sigs = load_state(asset_id).get(STATE_KEY)
    stored = sigs.get(url) if isinstance(sigs, dict) else None
    if not isinstance(stored, dict):
        return False
    stored_etag = stored.get("etag")
    stored_lm = stored.get("last_modified")
    if not stored_etag and not stored_lm:
        return False

    try:
        headers = _probe_headers(url, timeout)
    except Exception as e:  # noqa: BLE001 — a failed probe must mean "fetch"
        print(f"[maintain] {asset_id}: probe of {url} failed "
              f"({type(e).__name__}: {e}) — treating as changed")
        return False
    if headers is None:
        return False
    current = _signature(headers)
    if current is None:
        return False  # server offers no signature now — never guess

    if stored_etag and current.get("etag"):
        return _norm_etag(stored_etag) == _norm_etag(current["etag"])
    if stored_lm and current.get("last_modified"):
        return stored_lm == current["last_modified"]
    return False  # stored and current signatures don't share a comparable field


def record_source_signature(asset_id: str, url: str, *, response=None,
                            timeout: float = 30.0) -> dict | None:
    """Persist the source signature for (asset, url) — call AFTER a successful
    fetch, and only then. Advancing the signature exclusively on success is
    what makes `source_unchanged` safe: a failed fetch leaves the old
    signature in place, so the next run still fetches.

    `response`: the httpx response the fetch was served from (headers are read
    off it — no extra request). When omitted, the url is HEADed instead.

    Returns the stored signature dict, or None when no ETag/Last-Modified was
    obtainable (nothing is persisted in that case — `source_unchanged` would
    return False regardless, so an absent signature just means "always fetch").
    """
    if response is not None:
        headers = response.headers
    else:
        try:
            headers = _probe_headers(url, timeout)
        except Exception as e:  # noqa: BLE001 — never fail a successful fetch over this
            print(f"[maintain] {asset_id}: signature probe of {url} failed "
                  f"({type(e).__name__}: {e}) — no signature recorded")
            return None
    if headers is None:
        return None
    sig = _signature(headers)
    if sig is None:
        return None
    sig["recorded_at"] = datetime.now(timezone.utc).isoformat()

    state = load_state(asset_id)
    sigs = state.get(STATE_KEY)
    if not isinstance(sigs, dict):
        sigs = {}
    sigs[url] = sig
    state[STATE_KEY] = sigs
    save_state(asset_id, state)
    return sig
