"""Shared HTTP + parsing helpers for the Treasury TIC connector.

ticdata.treasury.gov is a static-file publishing portal (no query API). Every
published table is a tab-delimited '.txt' (or comma '.csv') file at a stable URL,
overwritten in place on each monthly release. These helpers are shared by the
MFH merge fetch and the detailed SLT-table fetch.
"""
import re

from subsets_utils import get, transient_retry

# --------------------------------------------------------------------------- #
# URLs
# --------------------------------------------------------------------------- #
BASE_RC = "https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents"

# Tokens that represent a missing/suppressed numeric value across all tables.
_NULL_TOKENS = {"", "------", "n/a", "N/A", "--", "(*)", "*"}
_FOOTNOTE_RE = re.compile(r"\s+\d+/\s*$")  # trailing footnote marker e.g. "Belgium  5/"


# --------------------------------------------------------------------------- #
# HTTP with retry/backoff
# --------------------------------------------------------------------------- #
@transient_retry()
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text


# --------------------------------------------------------------------------- #
# Parsing helpers
# --------------------------------------------------------------------------- #
def _val(s):
    s = (s or "").strip()
    if s in _NULL_TOKENS:
        return None
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def _clean_country(c: str) -> str:
    return _FOOTNOTE_RE.sub("", c).strip()
