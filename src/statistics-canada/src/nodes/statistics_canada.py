"""Download nodes for Statistics Canada data cubes.

Each accepted StatCan productId is available as a full-history bulk CSV zip.
The download node resolves the canonical WDS URL, streams the zip to a local
temporary file, validates that it opens, then streams the inner data CSV to raw.
"""

import os
import tempfile
import zipfile

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, get_client, raw_writer

SLUG = "statistics-canada"
RESOLVE_URL = "https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{pid}/en"
CHUNK_SIZE = 1 << 20
CONNECT_TIMEOUT = 30.0
READ_TIMEOUT = 300.0


class SourceResponseError(RuntimeError):
    """Raised when WDS returns a successful HTTP response with no usable zip."""


def _resolve_zip_url(pid: str) -> str:
    resp = get(RESOLVE_URL.format(pid=pid), timeout=(CONNECT_TIMEOUT, 120.0))
    resp.raise_for_status()
    payload = resp.json()
    record = payload[0] if isinstance(payload, list) and payload else payload
    if not isinstance(record, dict):
        raise SourceResponseError(f"unexpected WDS resolver payload for {pid}")
    if record.get("status") != "SUCCESS" or not record.get("object"):
        raise SourceResponseError(f"WDS resolver did not return SUCCESS for {pid}")
    return str(record["object"])


def _download_zip(url: str, dest_path: str) -> None:
    client = get_client()
    with client.stream("GET", url, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)) as resp:
        resp.raise_for_status()
        with open(dest_path, "wb") as out:
            for chunk in resp.iter_bytes(CHUNK_SIZE):
                out.write(chunk)


def _data_member(zf: zipfile.ZipFile, pid: str) -> str:
    expected = f"{pid}.csv"
    if expected in zf.namelist():
        return expected
    candidates = [
        name
        for name in zf.namelist()
        if name.lower().endswith(".csv") and "metadata" not in name.lower()
    ]
    if not candidates:
        raise SourceResponseError(f"zip for {pid} contains no data CSV")
    return candidates[0]


def fetch_one(node_id: str) -> None:
    pid = node_id.removeprefix(f"{SLUG}-")
    zip_url = _resolve_zip_url(pid)
    fd, temp_path = tempfile.mkstemp(prefix=f"{node_id}-", suffix=".zip")
    os.close(fd)
    try:
        _download_zip(zip_url, temp_path)
        with zipfile.ZipFile(temp_path) as zf:
            member = _data_member(zf, pid)
            with zf.open(member) as src, raw_writer(node_id, "csv", mode="wb") as dst:
                while True:
                    chunk = src.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    dst.write(chunk)
    finally:
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
