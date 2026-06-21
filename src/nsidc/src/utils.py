"""Shared helpers for the NSIDC Sea Ice Index (G02135) connector.

The source (https://noaadata.apps.nsidc.org/NOAA/G02135) is a static nginx
file server serving a handful of small CSVs. Every subset downloads its CSV(s),
parses them in Python (multi-line headers, fixed-width-ish padding, a noisy
quoted 'Source Data' column DuckDB can't ingest), and writes one typed parquet.
"""

from subsets_utils import get, transient_retry

BASE_URL = "https://noaadata.apps.nsidc.org/NOAA/G02135"

# Sentinel for missing values in the source CSVs.
_MISSING = "-9999"


@transient_retry()
def download_csv(path: str) -> str:
    url = f"{BASE_URL}/{path}"
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def parse_float(s: str | None) -> float | None:
    if s is None:
        return None
    s = s.strip()
    if not s or s == _MISSING:
        return None
    return float(s)
