"""Shared NBER fetch helpers.

The macrohistory subsets (values + series) both enumerate the same Apache
directory indexes under data.nber.org/databases/macrohistory/rectdata/, so the
HTTP client, chapter/frequency tables, and the chapter-index parser live here.
"""
import re

import httpx

from subsets_utils import get, transient_retry

MACRO_BASE = "https://data.nber.org/databases/macrohistory/rectdata"

CHAPTER_NAMES = {
    "01": "Production of Commodities",
    "02": "Construction",
    "03": "Transportation and Public Utilities",
    "04": "Prices",
    "05": "Stocks of Commodities",
    "06": "Distribution of Commodities",
    "07": "Foreign Trade",
    "08": "Income and Employment",
    "09": "Financial Status of Business",
    "10": "Savings and Investment",
    "11": "Securities Markets",
    "12": "Volume of Transactions",
    "13": "Interest Rates",
    "14": "Money and Banking",
    "15": "Government Finance",
    "16": "Leading Indicators",
}
FREQ_NAMES = {"a": "annual", "m": "monthly", "q": "quarterly"}


@transient_retry(min_wait=2, max_wait=60)
def _get(url: str) -> httpx.Response:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _list_chapter_stems(chapter: str) -> list[str]:
    """Parse a chapter directory index into the list of .dat file stems."""
    html = _get(f"{MACRO_BASE}/{chapter}/").text
    dats = sorted(set(re.findall(r'href="([^"/]+\.dat)"', html)))
    return [d[:-4] for d in dats]  # strip ".dat"
