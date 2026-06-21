"""Shared HTTP/retry helpers for the Banco Central do Brasil (BCB) connector.

`load_nodes()` skips files whose name starts with `_`, so this module is
invisible to the spec scanner: it holds the cross-cutting client + the Olinda
OData paging/function helpers used by several subset files, and NOTHING else
(no NodeSpec definitions). Each subset module imports from here so the HTTP
plumbing lives exactly once.

Date format note: PTAX functions expect MM-DD-YYYY date string literals.
"""
import os

import httpx

from subsets_utils import get, transient_retry

SLUG = "banco-central-do-brasil"
OLINDA = "https://olinda.bcb.gov.br/olinda/servico"

STATE_VERSION = 1


def _env_int(name: str, default: int) -> int:
    """Operational override for a pacing constant; production defaults stand
    unless the run sets an env var (used to shrink a single validation run)."""
    raw = os.environ.get(name)
    return int(raw) if raw and raw.lstrip("-").isdigit() else default


# Bound EVERY phase. A bare 2-tuple becomes httpx.Timeout(connect, read, write=None,
# pool=None) — i.e. write/pool waits are *infinite*, so a stalled socket or an
# exhausted connection pool blocks forever. A full Timeout caps all four phases.
_TIMEOUT = httpx.Timeout(connect=10.0, read=120.0, write=30.0, pool=30.0)


@transient_retry()
def _fetch_json(url, params=None):
    resp = get(url, params=params, timeout=_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _skip_reason(exc: httpx.HTTPError) -> str:
    """Human-readable cause for a skipped sub-request — HTTP status when the
    server answered, else the transport-error type (post-retry timeout, etc.)."""
    if isinstance(exc, httpx.HTTPStatusError):
        return f"HTTP {exc.response.status_code}"
    return type(exc).__name__


def _odata_all(service: str, resource: str, params: dict) -> list[dict]:
    """Page a plain Olinda entity set with $top/$skip until exhausted.

    Olinda returns the whole set in one response (no @odata.nextLink), but we
    page defensively so a future server-side cap can't silently truncate us.
    """
    url = f"{OLINDA}/{service}/versao/v1/odata/{resource}"
    page = 50000
    skip = 0
    out: list[dict] = []
    while True:
        q = {"$format": "json", "$top": page, "$skip": skip, **params}
        rows = _fetch_json(url, q).get("value", [])
        out.extend(rows)
        if len(rows) < page:
            break
        skip += page
    return out


def _odata_function(service: str, func: str, args: dict, extra: dict | None = None) -> list[dict]:
    """Call an Olinda FunctionImport: Func(p1=@p1,...)?@p1='..'&$format=json."""
    keys = list(args)
    sig = ",".join(f"{k}=@{k}" for k in keys)
    url = f"{OLINDA}/{service}/versao/v1/odata/{func}({sig})"
    params = {f"@{k}": v for k, v in args.items()}
    params["$format"] = "json"
    if extra:
        params.update(extra)
    return _fetch_json(url, params).get("value", [])


def _entity(node_id: str) -> str:
    """The entity stem of a node id: everything after the `<slug>-` prefix."""
    return node_id[len(SLUG) + 1:]
