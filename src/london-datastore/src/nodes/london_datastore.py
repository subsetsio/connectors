"""London Datastore connector — GLA DataPress (CKAN fork) data portal.

Catalog connector. Each rank-active entity is a CKAN package that exposes
exactly one CSV resource (the rank step restricted the build to single-CSV
packages — the cleanly buildable, one-package-one-table core). For each
package we resolve its current CSV resource via the CKAN `package_show`
action API and stream the file into a uniform-keyed NDJSON raw asset; the
SQL transform then publishes one Delta table per package.

Strategy: stateless full re-pull. The whole corpus is a few-hundred small/
mid CSVs; we re-fetch every refresh and overwrite. No watermark/cursor —
there is no usable incremental filter (CKAN exposes metadata_modified only
for sorting), and re-pulling picks up upstream revisions for free.

Raw format: NDJSON (zstd). CSVs are heterogeneous across packages, so a
fixed parquet schema makes no sense; we parse each CSV leniently in Python
(robust to encoding, quoting, ragged rows) and emit one JSON object per
data row with the cleaned header as keys (all values as strings/null). The
keys are uniform within an asset, so DuckDB's read_json_auto detects a clean
schema for the transform.
"""

from __future__ import annotations

import csv
import io

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "london-datastore"
PREFIX = f"{SLUG}-"
API = "https://data.london.gov.uk/api/action"


@transient_retry()
def _api(action: str, **params):
    """Call a CKAN action endpoint, returning the `result` payload."""
    resp = get(f"{API}/{action}", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"CKAN {action} returned success!=true for {params}")
    return body["result"]


@transient_retry()
def _download(url: str) -> bytes:
    """Fetch a resource file's bytes."""
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _is_csv(resource: dict) -> bool:
    fmt = (resource.get("format") or "").strip().lower()
    if fmt == "csv":
        return True
    url = (resource.get("url") or "").split("?")[0].lower()
    return url.endswith(".csv")


def _clean_headers(names: list[str]) -> list[str]:
    """Make column names non-empty and unique, preserving order."""
    used: set[str] = set()
    out: list[str] = []
    for i, raw in enumerate(names):
        name = (raw or "").strip() or f"col_{i + 1}"
        candidate = name
        n = 1
        while candidate in used:
            n += 1
            candidate = f"{name}_{n}"
        used.add(candidate)
        out.append(candidate)
    return out


def _decode(content: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return content.decode(enc)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", "replace")


def _iter_rows(content: bytes):
    """Yield one dict per CSV data row, keyed by cleaned header. Lenient:
    pads/truncates ragged rows to the header width."""
    reader = csv.reader(io.StringIO(_decode(content)))
    try:
        header = next(reader)
    except StopIteration:
        return
    cols = _clean_headers(header)
    ncol = len(cols)
    for row in reader:
        if not row or all(c == "" for c in row):
            continue
        vals = (row + [None] * ncol)[:ncol]
        yield {cols[i]: (vals[i] if vals[i] not in ("", None) else None) for i in range(ncol)}


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len(PREFIX):]
    pkg = _api("package_show", id=entity_id)
    csv_resources = [r for r in (pkg.get("resources") or []) if _is_csv(r)]
    if not csv_resources:
        raise RuntimeError(
            f"{entity_id}: no CSV resource found — rank restricted the build to "
            "single-CSV packages, so this means the package changed upstream"
        )
    # Single-CSV by rank construction; if the package gained resources, take
    # the largest CSV so we publish the substantive table.
    resource = max(csv_resources, key=lambda r: int(r.get("size") or 0))
    content = _download(resource["url"])
    save_raw_ndjson(_iter_rows(content), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per package: read the raw NDJSON view straight
# through. The CSV is already one coherent table; the transform is a thin
# pass-through (read_json_auto types the columns; an empty result fails the
# node, which is the correctness gate on a truncated/empty download).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=f'SELECT * FROM "{spec.id}"',
    )
    for spec in DOWNLOAD_SPECS
]
