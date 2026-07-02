"""Shared transient-error detection + retry policy.

Hand-rolled copies of this lived in ~250 connector node modules — the same
``_TRANSIENT_EXC`` tuple, ``_is_transient`` predicate, and ``@retry(...)`` config,
copy-pasted verbatim. Centralizing it here means the retry policy has one home.

A connector that wants the standard behaviour writes::

    from subsets_utils import transient_retry

    @transient_retry()
    def _get_json(url): ...

Override the defaults per call site when a source needs it, e.g.
``@transient_retry(attempts=8, min_wait=2, max_wait=60)``. A connector with a
genuinely different *predicate* (extra exception types, different status codes)
keeps its own ``retry_if_exception`` — this helper covers the common case, not
every case. See ``hardened/refactors/transient-retry/`` for the invariant.
"""
from __future__ import annotations

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

# Network-layer failures that are safe to retry (connection / timeout / protocol).
TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError, httpx.ProxyError,
)


def is_transient(exc: BaseException) -> bool:
    """True for retryable failures: transient network errors, HTTP 429, and 5xx."""
    if isinstance(exc, TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


def transient_retry(*, attempts: int = 6, min_wait: float = 4, max_wait: float = 120):
    """The connector-standard retry decorator.

    Retries :func:`is_transient` failures with exponential backoff, then reraises.
    Defaults match the config that was copy-pasted across connectors
    (``stop_after_attempt(6)``, ``wait_exponential(min=4, max=120)``).
    """
    return retry(
        retry=retry_if_exception(is_transient),
        stop=stop_after_attempt(attempts),
        wait=wait_exponential(min=min_wait, max=max_wait),
        reraise=True,
    )
