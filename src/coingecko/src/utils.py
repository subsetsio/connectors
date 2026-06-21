"""Shared HTTP + parsing helpers for the CoinGecko connector.

REST v3 (https://api.coingecko.com/api/v3). Auth works keyless but is heavily
throttled and 429s readily. If a CoinGecko Demo API key is present in the
environment (COINGECKO_API_KEY / COINGECKO_DEMO_API_KEY) it is sent as the
x-cg-demo-api-key header to lift the limit. 429/5xx are retried with
exponential backoff (the 429 Retry-After is honoured by the backoff finding the
natural pace).
"""

import os

from ratelimit import limits, sleep_and_retry

from subsets_utils import get, transient_retry

BASE = "https://api.coingecko.com/api/v3"

# Safety ceiling for paginated endpoints — fires (raises) only if the source
# grows far past expectations; normal pagination terminates on an empty page.
MAX_PAGES = 200


def _auth_headers() -> dict:
    key = os.environ.get("COINGECKO_API_KEY") or os.environ.get("COINGECKO_DEMO_API_KEY")
    return {"x-cg-demo-api-key": key} if key else {}


@sleep_and_retry
@limits(calls=25, period=60)  # ~80% of the 30/min demo limit; polite when keyless
def _rate_gate() -> None:
    return None


@transient_retry(attempts=8)
def _get_json(path: str, params: dict | None = None):
    _rate_gate()
    resp = get(BASE + path, params=params or {}, headers=_auth_headers(), timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _paginate(path: str, base_params: dict, per_page: int = 250):
    out = []
    for page in range(1, MAX_PAGES + 1):
        params = {**base_params, "per_page": per_page, "page": page}
        batch = _get_json(path, params)
        if not batch:
            return out
        out.extend(batch)
        if len(batch) < per_page:
            return out
    raise RuntimeError(f"{path}: exceeded MAX_PAGES={MAX_PAGES}; source grew past expectations")


def _num(v):
    # Coerce to Python float so pyarrow stores it directly. Building the table
    # straight from JSON ints triggers pyarrow's *exact* int->double safe cast,
    # which rejects huge values (meme-coin supplies > 2**53); pre-converting to
    # float accepts the (analytically harmless) precision loss instead.
    return float(v) if v is not None else None
