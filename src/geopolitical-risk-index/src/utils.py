"""Shared helpers for the Geopolitical Risk Index connector.

Source: two fixed-name Excel files on https://www.matteoiacoviello.com. Both are
legacy .xls / BIFF (needs xlrd), tiny, and overwritten in place each month, so
every node does a stateless full re-pull and parses sheet 0 in pandas.
"""
import io

import pandas as pd

from subsets_utils import get, transient_retry

MONTHLY_URL = "https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls"
DAILY_URL = "https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.xls"

# Embedded codebook columns in the monthly/daily files — metadata, not data.
_META_COLS = ("var_name", "var_label")


@transient_retry()
def _fetch_xls(url: str) -> pd.DataFrame:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return pd.read_excel(io.BytesIO(resp.content), sheet_name=0, engine="xlrd")
