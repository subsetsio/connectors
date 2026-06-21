"""Shared HTTP + CSV helpers for the Stack Overflow survey connector.

The official survey archive lives in the StackExchange/Survey GitHub repo, one
folder per release year (2011-2025). Files are Git-LFS tracked: the github.com/raw
URL 302-redirects to media.githubusercontent.com and serves the real CSV bytes;
subsets_utils.get follows redirects.
"""
import io

from subsets_utils import get, transient_retry

RAW_BASE = "https://github.com/StackExchange/Survey/raw/refs/heads/main/packages/archive"


@transient_retry()
def fetch_bytes(url: str) -> bytes:
    # Long read timeout: the LFS-backed results.csv files reach ~196MB.
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def read_csv(content: bytes, **kwargs):
    """Read a survey CSV, tolerating the encoding drift across years.

    Recent files are UTF-8 (with BOM); early files (2011-2013) are Windows
    cp1252. Try utf-8-sig, then cp1252, then latin-1 (which decodes any byte) as
    a last resort so a fetch never dies on a stray high byte.
    """
    import pandas as pd

    last_exc = None
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return pd.read_csv(io.BytesIO(content), dtype=str, encoding=enc, **kwargs)
        except UnicodeDecodeError as e:
            last_exc = e
    raise last_exc
