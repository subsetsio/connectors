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

Raw format: Parquet, one file per package with an explicit per-column schema
inferred in Python. Each package's single CSV has a stable column set, so
parquet fits. We infer each column as int64 / double / string from its values
and write that exact schema — which keeps numeric columns properly typed while
leaving time-of-day ("19:00") and date-like text as strings. That matters:
DuckDB's read_json_auto would re-infer such strings as TIME, a type Delta Lake
rejects; pinning string at the raw layer avoids that and is Delta-safe.
"""

from __future__ import annotations

import csv
import io

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_IDS

_INT64_MIN, _INT64_MAX = -(2 ** 63), 2 ** 63 - 1

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


def _parse_columns(content: bytes) -> tuple[list[str], dict[str, list]]:
    """Parse a CSV into (column order, {col: [str|None, ...]}). Lenient:
    pads/truncates ragged rows to the header width, skips blank rows."""
    reader = csv.reader(io.StringIO(_decode(content)))
    try:
        header = next(reader)
    except StopIteration:
        return [], {}
    cols = _clean_headers(header)
    ncol = len(cols)
    data: dict[str, list] = {c: [] for c in cols}
    for row in reader:
        if not row or all(c == "" for c in row):
            continue
        vals = (row + [None] * ncol)[:ncol]
        for i, c in enumerate(cols):
            v = vals[i]
            data[c].append(v if v not in ("", None) else None)
    return cols, data


def _is_int(v: str) -> bool:
    s = v[1:] if v[:1] in ("+", "-") else v
    if not s.isdigit():
        return False
    if len(s) > 1 and s[0] == "0":
        return False  # leading-zero code (ward/postcode) — keep as string
    return _INT64_MIN <= int(v) <= _INT64_MAX


def _is_float(v: str) -> bool:
    if v.strip().lower() in ("nan", "inf", "-inf", "infinity", "-infinity"):
        return False  # don't let these collapse a column to float
    try:
        float(v)
        return True
    except ValueError:
        return False


def _column_array(values: list) -> pa.Array:
    """Infer int64 / double / string for a column and build the typed array."""
    nonnull = [v for v in values if v is not None]
    if nonnull and all(_is_int(v) for v in nonnull):
        return pa.array([int(v) if v is not None else None for v in values], type=pa.int64())
    if nonnull and all(_is_float(v) for v in nonnull):
        return pa.array([float(v) if v is not None else None for v in values], type=pa.float64())
    return pa.array(values, type=pa.string())


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
    cols, data = _parse_columns(content)
    if not cols:
        raise RuntimeError(f"{entity_id}: CSV had no header row")
    arrays = [_column_array(data[c]) for c in cols]
    table = pa.table({c: arr for c, arr in zip(cols, arrays)})
    save_raw_parquet(table, asset)


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
