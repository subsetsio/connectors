"""ONS connector — UK Office for National Statistics CMD datasets.

Mechanism (from research): per-dataset bulk CSV via the beta CMD API.
For each dataset we GET https://api.beta.ons.gov.uk/v1/datasets/{id}, follow
links.latest_version to the version record, and stream its downloads.csv href
(download.ons.gov.uk 301-redirects to a stable static.ons.gov.uk object).

The CSV comes in two layouts, both handled generically by inspecting the header:
  - ONS "v4" wide format  : first column is `v4_N`; that column is the
                            observation value, the next N are data-marking
                            columns, the rest are dimension code/label pairs.
  - Census "Cantabular"   : the last column is `Observation` (the value); the
                            preceding columns are dimension code/label pairs.

In both cases the value column is renamed `value` (float) and every other
column is kept as a string under a snake_cased name. Schema is derived from the
header per dataset, so the CSV is streamed straight to parquet with bounded
memory (some tables, e.g. ashe-tables-20, are ~680MB).

Fetch shape: stateless full re-pull. ONS publishes whole-table snapshots per
version with no incremental/delta filter, so each refresh re-fetches the latest
version in full and overwrites. The maintain step (authored later) decides
whether a given dataset is re-fetched on a refresh.
"""
import csv
import re

import httpx
import pyarrow as pa
import pyarrow.parquet as pq
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import (
    NodeSpec,
    get,
    get_client,
    raw_parquet_writer,
)

API = "https://api.beta.ons.gov.uk/v1/datasets"
BATCH_ROWS = 50_000

# Entity union (original-case dataset ids — the API path is case-sensitive,
# `ts009` 404s where `TS009` 200s, so we preserve case here and map the
# lower-cased spec id back to the original at fetch time).
from constants import ENTITY_IDS


# --------------------------------------------------------------------------- #
# Retry / transport
# --------------------------------------------------------------------------- #
_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError,
    httpx.ProxyError,
)


class _TransientBody(Exception):
    """An empty / unparseable 200 body — ONS occasionally returns these under
    burst load; treat as transient and retry."""


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, (_TRANSIENT_EXC, _TransientBody)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    if not resp.text.strip():
        raise _TransientBody(f"empty body from {url}")
    return resp.json()


def _dataset_id(node_id: str) -> str:
    """Recover the original-case dataset id from the lower-cased spec id."""
    target = node_id[len("ons-"):]
    for eid in ENTITY_IDS:
        if eid.lower().replace("_", "-") == target:
            return eid
    raise KeyError(f"no entity union member for {node_id!r}")


def _resolve_csv_url(dataset_id: str) -> str:
    """Resolve the CSV download for the most recent version that actually
    exposes one. ONS sometimes publishes a newest version whose downloads are
    empty (csv not (re)generated) while older versions still carry a CSV — so we
    fall back through the edition's versions (returned newest-first) and take the
    highest version number that has a downloads.csv.href."""
    rec = _get_json(f"{API}/{dataset_id}")
    latest_href = rec.get("links", {}).get("latest_version", {}).get("href")
    if not latest_href:
        raise KeyError(f"{dataset_id}: no links.latest_version.href")

    # Fast path: the latest version has a CSV.
    version = _get_json(latest_href)
    csv_href = version.get("downloads", {}).get("csv", {}).get("href")
    if csv_href:
        return csv_href

    # Fallback: scan all versions of this edition, newest-first, for a CSV.
    m = re.search(r"/editions/([^/]+)/versions/", latest_href)
    if not m:
        raise KeyError(f"{dataset_id}: cannot parse edition from {latest_href}")
    edition = m.group(1)
    page = _get_json(
        f"{API}/{dataset_id}/editions/{edition}/versions?limit=1000"
    )
    for item in page.get("items", []):
        href = item.get("downloads", {}).get("csv", {}).get("href")
        if href:
            return href
    raise KeyError(f"{dataset_id}: no version (edition {edition}) exposes a CSV")


# --------------------------------------------------------------------------- #
# CSV header -> column plan
# --------------------------------------------------------------------------- #
def _clean(name: str) -> str:
    s = re.sub(r"[^0-9a-z]+", "_", name.strip().lower()).strip("_")
    return s or "col"


def _plan_columns(header: list[str]):
    """Return (out_names, value_idx). out_names[i] is the output column name for
    input column i, with the value column named 'value'. Handles both the v4
    (`v4_N` first column) and Cantabular (`Observation` last column) layouts."""
    if header and re.fullmatch(r"v4_\d+", header[0].strip(), flags=re.I):
        value_idx = 0
    elif header and header[-1].strip().lower() == "observation":
        value_idx = len(header) - 1
    else:
        raise ValueError(f"unrecognised ONS CSV header: {header[:6]}")

    out, seen = [], set()
    for i, h in enumerate(header):
        if i == value_idx:
            out.append("value")
            seen.add("value")
            continue
        base = _clean(h)
        if base == "value":
            base = "value_dim"
        nm, k = base, 1
        while nm in seen:
            nm = f"{base}_{k}"
            k += 1
        seen.add(nm)
        out.append(nm)
    return out, value_idx


def _to_float(cell: str):
    cell = cell.strip()
    if not cell:
        return None
    try:
        return float(cell)
    except ValueError:
        return None


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(5),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _stream_csv_to_parquet(node_id: str, csv_url: str) -> int:
    """Stream the dataset CSV straight to a parquet raw asset. Returns row count.
    Retried whole; raw_parquet_writer reopens 'wb' so a mid-stream retry simply
    overwrites the partial file."""
    client = get_client()
    written = 0
    with client.stream("GET", csv_url, timeout=(10.0, 300.0)) as resp:
        resp.raise_for_status()
        reader = csv.reader(resp.iter_lines())
        header = next(reader, None)
        if not header:
            raise _TransientBody(f"empty CSV from {csv_url}")
        out_names, value_idx = _plan_columns(header)
        schema = pa.schema([
            (nm, pa.float64() if i == value_idx else pa.string())
            for i, nm in enumerate(out_names)
        ])
        ncols = len(out_names)

        with raw_parquet_writer(node_id, schema) as writer:
            batch = []
            for row in reader:
                if not row:
                    continue
                # tolerate short/long rows defensively
                if len(row) < ncols:
                    row = row + [""] * (ncols - len(row))
                rec = {}
                for i in range(ncols):
                    if i == value_idx:
                        rec[out_names[i]] = _to_float(row[i])
                    else:
                        v = row[i].strip()
                        rec[out_names[i]] = v if v else None
                batch.append(rec)
                if len(batch) >= BATCH_ROWS:
                    writer.write_table(pa.Table.from_pylist(batch, schema=schema))
                    written += len(batch)
                    batch = []
            if batch:
                writer.write_table(pa.Table.from_pylist(batch, schema=schema))
                written += len(batch)
    return written


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = _dataset_id(node_id)
    csv_url = _resolve_csv_url(dataset_id)
    rows = _stream_csv_to_parquet(asset, csv_url)
    if rows == 0:
        raise ValueError(f"{dataset_id}: CSV produced 0 data rows ({csv_url})")
    print(f"  {asset}: {rows} rows from {csv_url}")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ons-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
