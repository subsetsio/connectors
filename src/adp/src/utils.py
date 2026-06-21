"""Shared HTTP + parse helpers for the ADP report families.

Both report families (ner_employment, pay_insights) are static-CDN bulk
downloads (mechanism `bulk_history_csv`): a stable root index JSON whose
`reportDownloadLink` points at a history ZIP containing one long-format CSV
covering the entire corpus. The discovery + download + CSV-read path is
identical for both, so it lives here. No NodeSpec definitions belong in this
module — it is HTTP + genuinely-shared parsing only.
"""
import csv
import io
import zipfile

from subsets_utils import get, transient_retry


@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def parse_float(v):
    if v is None:
        return None
    v = v.strip()
    return float(v) if v else None


def read_history_csv(index_url: str) -> list[dict]:
    """Resolve the index to its current history ZIP and return the CSV rows."""
    index = _get_json(index_url)
    zip_url = index["reportDownloadLink"]
    raw = _get_bytes(zip_url)
    zf = zipfile.ZipFile(io.BytesIO(raw))
    csv_name = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
    text = zf.read(csv_name).decode("utf-8")
    return list(csv.DictReader(io.StringIO(text)))
