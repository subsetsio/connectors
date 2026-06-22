"""Statistics Bulgaria (NSI) — Open Data portal connector.

Mechanism: NSI Open Data portal (https://www.nsi.bg/opendata/), one stable
numeric id per dataset. We fetch each dataset's JSON-stat 2.0 document
(getopendata_json.php?l=en&id=<id>), which is self-describing: it carries the
dimension order, per-dimension category code lists AND human labels, plus the
flat row-major value array. We melt that into a tidy per-dataset table — one row
per non-null data cell with `period`, one column per breakdown dimension (holding
human labels), an optional `unit`, and a numeric `value` — and publish it 1:1.

Fetch shape: stateless full re-pull (shape 1). Each dataset is a single
self-contained document of at most a few MB; there is no server-side incremental
filter, so we re-fetch the whole dataset every run and overwrite. Freshness is
the maintain step's concern.

Each dataset has its own breakdown dimensions, so each raw asset has its own
column set; the transform is therefore a uniform thin pass-through that republishes
the parsed table (it is the correctness gate: 0 rows or a missing `value` fails
the node loudly rather than publishing garbage).
"""

import json as _json
import math
import re

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry
from constants import ENTITY_IDS

SLUG = "statistics-bulgaria"
JSON_URL = "https://www.nsi.bg/opendata/getopendata_json.php"

# Tokens the source uses for missing / suppressed values.
_MISSING = {"", "..", ":", "-", "...", ".", "n/a", "na"}


@transient_retry()  # 6 attempts, exponential backoff over transient net errors + 429 + 5xx
def _fetch_doc(dataset_id: str) -> dict:
    resp = get(JSON_URL, params={"l": "en", "id": dataset_id}, timeout=(10.0, 180.0))
    resp.raise_for_status()  # inside the retry so 5xx/429 are retried
    raw = resp.content
    # JSON-stat docs are mostly ASCII but some carry cp1252/cp1251 punctuation
    # (en-dashes, Cyrillic source notes) and are NOT valid UTF-8. Try a few.
    for enc in ("utf-8-sig", "utf-8", "cp1251", "cp1252", "latin-1"):
        try:
            return _json.loads(raw.decode(enc))
        except (UnicodeDecodeError, _json.JSONDecodeError):
            continue
    raise ValueError(f"{dataset_id}: could not decode JSON-stat response")


def _sanitize(name: str, used: set) -> str:
    """Turn a dimension label into a safe, unique snake_case column name."""
    s = re.sub(r"[^0-9a-zA-Z]+", "_", (name or "").strip().lower()).strip("_")
    if not s:
        s = "dim"
    if s[0].isdigit():
        s = "d_" + s
    base, i = s, 2
    while s in used:
        s = f"{base}_{i}"
        i += 1
    used.add(s)
    return s


def _category_order(dim: dict):
    """Return parallel (codes, labels) lists in positional order for one dimension."""
    cat = dim["category"]
    idx = cat.get("index")
    lab = cat.get("label") or {}
    if isinstance(idx, dict):
        order = [c for c, _ in sorted(idx.items(), key=lambda kv: kv[1])]
    elif isinstance(idx, list):
        order = list(idx)
    else:  # single-category dimension (e.g. a one-unit metric): keys carry order
        order = list(lab.keys())
    labels = [lab.get(c, c) for c in order]
    return order, labels


def _coerce_value(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        t = v.strip()
        if t.lower() in _MISSING:
            return None
        try:
            return float(t.replace(",", ""))
        except ValueError:
            return None
    return None


def _melt(doc: dict):
    """Melt a JSON-stat 2.0 dataset into (rows, ordered_column_names)."""
    ids = doc["id"]
    sizes = doc["size"]
    dim = doc["dimension"]
    role = doc.get("role") or {}
    time_dims = list(role.get("time") or [])
    metric_dims = list(role.get("metric") or [])

    # row-major strides
    strides = [1] * len(sizes)
    for i in range(len(sizes) - 2, -1, -1):
        strides[i] = strides[i + 1] * sizes[i + 1]

    pos = {dk: _category_order(dim[dk]) for dk in ids}

    used = {"period", "unit", "value"}
    # role.time / role.metric may name a dimension that isn't in this dataset's
    # indexed `id` list (NSI tags a constant/absent "periods" or "Units" that
    # doesn't actually vary). Only honour the role when the dimension is real;
    # otherwise the true axis (e.g. Edu_schYear) stays a labeled breakdown column
    # rather than becoming a manufactured all-null `period`/`unit`.
    period_dim = time_dims[0] if (time_dims and time_dims[0] in ids) else None
    unit_dim = metric_dims[0] if (metric_dims and metric_dims[0] in ids) else None
    colmap = {}  # dimension id -> output column name (breakdown dims only)
    for dk in ids:
        if dk == period_dim or dk == unit_dim:
            continue
        colmap[dk] = _sanitize(dim[dk].get("label") or dk, used)

    values = doc["value"]
    # JSON-stat permits value as a list (dense) or an object keyed by position.
    def value_at(p):
        if isinstance(values, list):
            return values[p] if p < len(values) else None
        return values.get(str(p))

    rows = []
    n = math.prod(sizes) if sizes else 0
    for p in range(n):
        v = _coerce_value(value_at(p))
        if v is None:
            continue
        row = {}
        for i, dk in enumerate(ids):
            cidx = (p // strides[i]) % sizes[i]
            code, label = pos[dk][0][cidx], pos[dk][1][cidx]
            if dk == period_dim:
                row["period"] = code
            elif dk == unit_dim:
                row["unit"] = label
            else:
                row[colmap[dk]] = label
        row["value"] = v
        rows.append(row)

    cols = (
        (["period"] if period_dim else [])
        + list(colmap.values())
        + (["unit"] if unit_dim else [])
        + ["value"]
    )
    return rows, cols


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = node_id[len(SLUG) + 1:]  # strip "statistics-bulgaria-"
    doc = _fetch_doc(dataset_id)
    rows, cols = _melt(doc)

    # Explicit schema is the contract: every string dimension column, value double.
    schema = pa.schema(
        [(c, pa.float64() if c == "value" else pa.string()) for c in cols]
    )
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One thin pass-through transform per dataset. Each raw asset has its own column
# set, so SELECT * republishes it; the WHERE drops any residual null values and a
# 0-row result fails the node (the correctness gate).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}" WHERE value IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
