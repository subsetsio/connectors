"""Shared HTTP + xlsx helpers for the SIPRI connector.

SIPRI's landing pages embed a year+version suffix in each .xlsx filename that
changes on every release, so the database landing pages are scraped for the
current href rather than hardcoding a URL.
"""

import io
import re

import openpyxl

from subsets_utils import get, transient_retry

SIPRI_HOST = "https://www.sipri.org"


@transient_retry()
def get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def abs_url(href: str) -> str:
    href = href.strip()
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        return SIPRI_HOST + href
    return href


def find_xlsx(landing_path: str, pattern: str) -> str:
    """Scrape a SIPRI database landing page for the current .xlsx href whose
    filename contains `pattern` (filenames carry a year+version that changes
    each release, so they cannot be hardcoded)."""
    html = get_text(SIPRI_HOST + landing_path)
    hrefs = re.findall(r'href="([^"]+\.xlsx[^"]*)"', html)
    for h in hrefs:
        if pattern.lower() in h.lower():
            return abs_url(h)
    raise RuntimeError(f"no .xlsx matching '{pattern}' found on {landing_path}; hrefs={hrefs}")


def load_wb(url: str):
    return openpyxl.load_workbook(io.BytesIO(get_bytes(url)), read_only=True, data_only=True)


def isnum(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)
