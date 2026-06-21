"""Shared HTTP + catalog parsing for the Central Reserve Bank of Peru connector.

Both published subsets read the same semicolon-delimited, ISO-8859-1 metadata
file; the catalog row parser and the retrying HTTP client live here so the
``series`` and ``values`` node files share one copy.
"""

import csv
import io

import httpx

from subsets_utils import get, transient_retry

_METADATA_URL = "https://estadisticas.bcrp.gob.pe/estadisticas/series/metadata"

# Metadata column positions (verified on the live file header).
_C_CODE, _C_CAT, _C_GRP, _C_NAME, _C_DESC = 0, 1, 2, 3, 4
_C_GEO, _C_SOURCE, _C_FREQ = 8, 9, 10
_C_PUBGRP, _C_AREA, _C_UPDATED, _C_START, _C_END = 12, 13, 14, 15, 16


@transient_retry()
def _http_get(url: str) -> httpx.Response:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp


def _fetch_catalog_rows() -> list[list[str]]:
    """Return the metadata catalog as a list of trimmed string rows (no header).

    The file is semicolon-delimited and Latin-1 encoded.
    """
    resp = _http_get(_METADATA_URL)
    text = resp.content.decode("latin-1")
    reader = csv.reader(io.StringIO(text), delimiter=";")
    rows = [r for r in reader if any(c.strip() for c in r)]
    # rows[0] is the header
    out = []
    for r in rows[1:]:
        if len(r) <= _C_END or not r[_C_CODE].strip():
            continue
        out.append([c.strip() for c in r])
    return out


def _cell(row: list[str], i: int) -> str:
    return row[i] if i < len(row) else ""
