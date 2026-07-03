import os
import random
import time

import httpx

from . import tracking
from .retry import TRANSIENT_EXC

_client = None
_client_config = {
    'timeout': int(os.environ.get('HTTP_TIMEOUT', '30')),
    'headers': {'User-Agent': os.environ.get('HTTP_USER_AGENT', 'DataIntegrations/1.0')}
}

# Transient-retry policy for the shared client. Every connector fetching
# through subsets_utils.get/post/... gets this for free: a lone connection
# reset / timeout, or a 429/5xx response, retries with exponential backoff
# instead of failing the node (and, before the continuation fix, the whole
# run chain — see orchestrator.py). HTTP_RETRY_ATTEMPTS caps total attempts
# (default 4); set it to 1 to disable retries. Connector-level
# @transient_retry decorators stack on top for sources that need more.
_RETRY_MAX_WAIT_S = 60.0

# Indirection so tests can stub the backoff sleep without patching time.sleep
# globally.
_sleep = time.sleep


def _retry_attempts() -> int:
    try:
        return max(1, int(os.environ.get('HTTP_RETRY_ATTEMPTS', '4')))
    except ValueError:
        return 4


def _retryable_status(status: int) -> bool:
    """Mirror retry.is_transient's status predicate: 429 and any 5xx."""
    return status == 429 or 500 <= status < 600


def _retry_wait(attempt: int, response: httpx.Response | None = None) -> float:
    """Backoff before the next attempt: exponential (2s, 4s, 8s, ... capped)
    plus jitter; a parseable Retry-After header wins when it asks for longer,
    capped at the same max."""
    wait = min(_RETRY_MAX_WAIT_S, 2.0 * (2 ** (attempt - 1)))
    if response is not None:
        retry_after = response.headers.get('Retry-After')
        if retry_after:
            try:
                wait = min(max(float(retry_after), wait), _RETRY_MAX_WAIT_S)
            except ValueError:
                pass  # HTTP-date form — keep the exponential backoff
    return wait + random.uniform(0, wait / 4)


def _repeatable(kwargs: dict) -> bool:
    """Only retry requests whose body can be re-sent. bytes/str/dict/list are
    repeatable; a generator or file-like stream is consumed by the first
    attempt, so those requests get exactly one try."""
    for key in ('content', 'data', 'files'):
        val = kwargs.get(key)
        if val is not None and not isinstance(val, (bytes, str, dict, list, tuple)):
            return False
    return True


def _get_or_create_client() -> httpx.Client:
    global _client

    if _client is None:
        _client = httpx.Client(
            timeout=_client_config['timeout'],
            headers=_client_config['headers'],
            follow_redirects=True
        )

    return _client


def _logged_request(method: str, url: str, **kwargs) -> httpx.Response:
    """Execute an HTTP request, recording every attempt into the run record.

    Transient failures — the network-level TRANSIENT_EXC set and 429/5xx
    responses — retry with exponential backoff up to HTTP_RETRY_ATTEMPTS
    (default 4) total attempts. Each attempt is logged as its own row in
    http_requests.csv. The contract to callers is unchanged: responses are
    returned, never raised — a still-failing final response comes back as-is
    for the caller's raise_for_status(); a still-failing final exception is
    re-raised.
    """
    client = _get_or_create_client()
    attempts = _retry_attempts() if _repeatable(kwargs) else 1

    for attempt in range(1, attempts + 1):
        start = time.time()
        error = None
        status = None
        response = None
        exc = None

        try:
            response = client.request(method, url, **kwargs)
            status = response.status_code
        except Exception as e:
            error = str(e)
            exc = e
        finally:
            duration_ms = int((time.time() - start) * 1000)
            tracking.record_http(method, url, status, duration_ms=duration_ms, error=error)

        if exc is not None:
            if attempt < attempts and isinstance(exc, TRANSIENT_EXC):
                wait = _retry_wait(attempt)
                print(f"[http] {method} {url} raised {type(exc).__name__}: {exc} — "
                      f"retry {attempt}/{attempts - 1} in {wait:.1f}s")
                _sleep(wait)
                continue
            raise exc

        if attempt < attempts and _retryable_status(response.status_code):
            wait = _retry_wait(attempt, response)
            print(f"[http] {method} {url} -> {response.status_code} — "
                  f"retry {attempt}/{attempts - 1} in {wait:.1f}s")
            response.close()
            _sleep(wait)
            continue

        return response


def get(url: str, **kwargs) -> httpx.Response:
    return _logged_request("GET", url, **kwargs)


def head(url: str, **kwargs) -> httpx.Response:
    return _logged_request("HEAD", url, **kwargs)


def post(url: str, **kwargs) -> httpx.Response:
    return _logged_request("POST", url, **kwargs)


def put(url: str, **kwargs) -> httpx.Response:
    return _logged_request("PUT", url, **kwargs)


def delete(url: str, **kwargs) -> httpx.Response:
    return _logged_request("DELETE", url, **kwargs)


def get_client() -> httpx.Client:
    return _get_or_create_client()


def configure_http(**config):
    global _client_config, _client
    _client_config.update(config)
    if _client:
        _client.close()
        _client = None
