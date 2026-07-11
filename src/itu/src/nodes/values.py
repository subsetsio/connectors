"""ITU DataHub — values subset.

Long-format observations (indicator x economy x year). For each catalogue
codeID, GET /v2/data/download?codesid=<codeID>&countriesid=<all CountryIDs>
returns a ZIP wrapping one tidy CSV. The API sits behind an AWS throughput cap
that intermittently returns a plain-text 'Throughput exceeds...' body instead of
the ZIP; that is treated as transient and retried. Indicators with no data
return a plain-text 'No data available...' body and are skipped.
"""

import csv
import io
import zipfile

import pyarrow as pa

from subsets_utils import (
    get,
    raw_parquet_writer,
    transient_retry,
)
from utils import BASE, _as_int, _catalogue_code_ids, _get_json


class ThroughputError(Exception):
    """The API returned its plain-text AWS-throughput body instead of data."""


@transient_retry(attempts=7)
def _download_indicator_csv(code_id: int, country_ids: list[int]) -> list[dict] | None:
    """Fetch one indicator's full cross-country CSV export.

    Returns the parsed CSV rows, or None when the source reports no data for
    the indicator (a permanent, non-retried condition).

    The API is quirky about status codes: the ZIP export arrives as a 200, but
    the plain-text 'No data available...' sentinel arrives with a **500** status
    (and the throughput cap likewise rides a non-200). So inspect the body
    BEFORE trusting the status — a 500 carrying 'No data available' is a real
    'this indicator has no series', not a server fault, and must not be retried.
    """
    cids = ",".join(str(c) for c in country_ids)
    resp = get(
        f"{BASE}/data/download",
        params={"codesid": code_id, "countriesid": cids, "startyear": 1960},
        timeout=(10.0, 180.0),
    )
    body = resp.content
    if body[:2] == b"PK":
        zf = zipfile.ZipFile(io.BytesIO(body))
        text = zf.read(zf.namelist()[0]).decode("utf-8-sig")
        return list(csv.DictReader(io.StringIO(text)))
    if b"No data available" in body:
        return None  # permanent: this indicator exposes no series — skip it
    if b"Throughput exceeds" in body:
        raise ThroughputError(f"throughput cap for code {code_id}")
    # Genuine HTTP error (or any other unexpected body): let raise_for_status
    # classify it — 5xx/429 are retried by the decorator, 4xx propagate.
    resp.raise_for_status()
    raise ThroughputError(f"unexpected non-ZIP body for code {code_id}: {body[:120]!r}")


def _country_ids() -> list[int]:
    return [c["CountryID"] for c in _get_json("country/all")]


_VALUES_SCHEMA = pa.schema([
    ("requested_code_id", pa.int64()),
    ("series_id", pa.string()),
    ("series_code", pa.string()),
    ("series_name", pa.string()),
    ("units", pa.string()),
    ("entity_id", pa.int64()),
    ("entity_iso", pa.string()),
    ("entity_name", pa.string()),
    ("data_value", pa.string()),
    ("data_year", pa.int64()),
    ("data_note", pa.string()),
    ("data_source", pa.string()),
])


def _values_table(code_id: int, rows: list[dict]) -> pa.Table:
    cols = {k: [] for k in _VALUES_SCHEMA.names}
    for r in rows:
        cols["requested_code_id"].append(code_id)
        cols["series_id"].append(r.get("seriesID"))
        cols["series_code"].append(r.get("seriesCode"))
        cols["series_name"].append(r.get("seriesName"))
        cols["units"].append(r.get("seriesUnits"))
        cols["entity_id"].append(_as_int(r.get("entityID")))
        cols["entity_iso"].append(r.get("entityIso"))
        cols["entity_name"].append(r.get("entityName"))
        cols["data_value"].append(r.get("dataValue"))
        cols["data_year"].append(_as_int(r.get("dataYear")))
        cols["data_note"].append(r.get("dataNote"))
        cols["data_source"].append(r.get("dataSource"))
    return pa.table(cols, schema=_VALUES_SCHEMA)


def fetch_values(node_id: str) -> None:
    asset = node_id
    code_ids, _ = _catalogue_code_ids()
    country_ids = _country_ids()

    total = 0
    failures: list[int] = []
    with raw_parquet_writer(asset, _VALUES_SCHEMA) as writer:
        for cid in code_ids:
            try:
                rows = _download_indicator_csv(cid, country_ids)
            except Exception as exc:  # noqa: BLE001 - one bad indicator must not sink the node
                print(f"  [itu-values] code {cid} failed after retries: {type(exc).__name__}: {exc}")
                failures.append(cid)
                continue
            if not rows:
                continue
            table = _values_table(cid, rows)
            if table.num_rows:
                writer.write_table(table)
                total += table.num_rows

    # A handful of indicators legitimately 500/break upstream; tolerate those but
    # fail loudly if the source is broadly down (so we never publish a thin table).
    if total == 0:
        raise RuntimeError("itu-values: no observations written across any indicator")
    if len(failures) > len(code_ids) // 4:
        raise RuntimeError(
            f"itu-values: {len(failures)}/{len(code_ids)} indicators failed "
            f"(>{len(code_ids)//4} threshold) — source likely degraded: {failures}"
        )
