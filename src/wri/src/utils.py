"""Shared HTTP helpers for the WRI connector (Climate Watch bulk export).

The paged JSON endpoints are hard-capped at 50 rows/page, so we use the same
API's bulk export instead: GET /api/v1/data/<endpoint>/download.csv returns a
ZIP containing one full-corpus CSV per dataset. One request per dataset.
"""

import io
import zipfile

from subsets_utils import get, transient_retry

BASE = "https://www.climatewatchdata.org/api/v1/data"


@transient_retry()
def download_zip(endpoint: str) -> bytes:
    """Fetch the dataset's bulk-export ZIP (full corpus, one request)."""
    resp = get(f"{BASE}/{endpoint}/download.csv", timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def open_member(content: bytes, member: str):
    """Return a text reader over one CSV member inside the export ZIP."""
    zf = zipfile.ZipFile(io.BytesIO(content))
    if member not in zf.namelist():
        raise AssertionError(f"expected '{member}' in zip, got {zf.namelist()}")
    return io.TextIOWrapper(zf.open(member), encoding="utf-8", newline="")
