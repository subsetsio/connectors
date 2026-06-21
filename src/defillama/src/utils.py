"""Shared HTTP + parse helpers for the DefiLlama connector.

All data comes from the DefiLlama free open API (no auth) across three hosts:
api.llama.fi (TVL + /overview adapters), yields.llama.fi (/pools), and
stablecoins.llama.fi (/stablecoins). Every published subset is a single
unpaginated full-table endpoint, so the shape is **stateless full re-pull**.
None of these endpoints expose a since/cursor/modifiedAfter filter, so there is
no incremental path; the corpus is small (largest payload ~10MB) and re-pulls
in seconds.
"""
import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import get


_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError, httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # DefiLlama intermittently 402s the /overview adapter endpoints under
        # bursty concurrent traffic even on the free tier; back off and retry.
        return code in (402, 429) or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _join_chains(v):
    return ",".join(v) if isinstance(v, list) else None
