"""Shared fetch helpers for the Maddison Project connector.

Single academic dataset (DOI 10.34894/INZBF2), published as one Excel workbook
(mpd2023_web.xlsx) on DataverseNL. The whole corpus is ~5MB and re-published as a
new versioned release rather than updated in place, so the correct shape is a
stateless full re-pull every run (no watermark, no cursor). Each download spec
re-fetches the workbook and parses one sheet.

Mechanism: datafile_download (research-chosen). Direct file-access endpoint
returns the full file in one request, no auth, no pagination.
"""

import io

import openpyxl

from subsets_utils import get, transient_retry

# Stable DataverseNL datafile id for mpd2023_web.xlsx (the released 2023 file).
WORKBOOK_URL = "https://dataverse.nl/api/access/datafile/421302"


@transient_retry()
def load_workbook():
    """Fetch the xlsx and return a read-only openpyxl workbook."""
    resp = get(WORKBOOK_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return openpyxl.load_workbook(io.BytesIO(resp.content), read_only=True, data_only=True)


def to_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def to_float(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
