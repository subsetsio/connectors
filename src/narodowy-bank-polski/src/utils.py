"""Shared HTTP + windowing helpers for the NBP connector.

The NBP Web API (https://api.nbp.pl/api/) is public, no auth. Every subset is a
stateless full re-pull walked in <=90-day windows (the API caps a single
date-range query at 93 days). A 404 means "no published table for that span"
(only possible at the very end of the range / future) and is skipped.
"""

from datetime import date, timedelta

import httpx

from subsets_utils import get, transient_retry

_BASE = "https://api.nbp.pl/api"
_WINDOW_DAYS = 90  # under the API's hard 93-day-per-query cap
_FX_START = date(2002, 1, 2)


@transient_retry()
def _get_json(path: str):
    """GET <base>/<path>?format=json. Raises HTTPStatusError (404 included)."""
    resp = get(f"{_BASE}/{path}", params={"format": "json"}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _windows(start: date):
    """Yield (start_iso, end_iso) spans of <=_WINDOW_DAYS covering start..today."""
    today = date.today()
    cur = start
    while cur <= today:
        win_end = min(cur + timedelta(days=_WINDOW_DAYS - 1), today)
        yield cur.isoformat(), win_end.isoformat()
        cur = win_end + timedelta(days=1)


def _fetch_windows(path_template: str, start: date):
    """Fetch every window for an endpoint, skipping 404 (no data) spans.

    Returns the concatenated list of upstream records across all windows.
    """
    out = []
    for w_start, w_end in _windows(start):
        path = path_template.format(start=w_start, end=w_end)
        try:
            out.extend(_get_json(path))
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                # No published data in this span (e.g. a fully-future window).
                continue
            raise
    return out
