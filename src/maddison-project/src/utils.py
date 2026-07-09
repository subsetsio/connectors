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
import zipfile

import openpyxl

from subsets_utils import get, transient_retry

# Stable DataverseNL datafile id for mpd2023_web.xlsx (the released 2023 file).
DATAFILE_ID = 421302

# The singular /datafile/<id> endpoint 303-redirects to objectstore.surf.nl,
# which refuses connections from GitHub Actions runners (IPv4 connects hang,
# IPv6 is unroutable there). The plural /datafiles/<id> endpoint streams the
# same bytes as a zip from dataverse.nl itself, which is reachable. Verified
# identical: sha256 ecc5916ca12789b983fc4be437f8a354bbf4291323605324ac3e0aea4c57cbb6.
WORKBOOK_URL = f"https://dataverse.nl/api/access/datafiles/{DATAFILE_ID}"


@transient_retry()
def load_workbook():
    """Fetch the xlsx (inside Dataverse's zip envelope) and return a read-only
    openpyxl workbook."""
    resp = get(WORKBOOK_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as bundle:
        names = [n for n in bundle.namelist() if n.endswith(".xlsx")]
        assert len(names) == 1, f"expected exactly one xlsx in the bundle, got {names!r}"
        payload = bundle.read(names[0])
    return openpyxl.load_workbook(io.BytesIO(payload), read_only=True, data_only=True)


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
