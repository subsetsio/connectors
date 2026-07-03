"""CBO connector — Congressional Budget Office Open Data Repository.

Source: the official machine-readable mirror of CBO's Budget and Economic Data
at github.com/us-cbo/cbo-data. A root catalog.json (DCAT / project-open-data)
lists 13 datasets; we publish the 12 the rank step accepted. Each dataset has
several distributions (a CSV per release-vintage x file_type); a distribution's
downloadURL is repo-relative and fetched from raw.githubusercontent.com.

The CSVs are NOT uniformly shaped. Most are tidy long (date, variable, value),
some carry an extra estimate_type/section column, and a few (demographic,
spending_detail, long_term_economic's lfp_rates) are wide per-file_type tables
with their own dimension columns. Column names even drift across vintages of one
dataset (e.g. number_of_people vs people). So we do NOT impose a fixed schema:
each download fetches every distribution of one dataset, tags rows with their
vintage + file_type, takes the union of all columns (missing -> null), and writes
one NDJSON asset. The SQL transform then publishes that asset verbatim as one
Delta table per dataset — file_type/vintage are dimensions within the table.

Two NDJSON correctness measures applied at fetch time so the runtime's
read_json_auto (no union_by_name, default sample) infers the table cleanly:
  1. Drift stringification — a column that is numeric in one distribution and
     string in another (e.g. `date` = 2001 vs "2001q1", `age` = 14 vs "0-4")
     is cast to string everywhere, else DuckDB infers a quote-leaking JSON type.
  2. Sample priming — the first PRIME_ROWS rows of every distribution are hoisted
     to the front of the file, guaranteeing each column has a typed non-null value
     inside read_json_auto's sample window (otherwise a sparse column whose values
     fall past the window is inferred as JSON).
"""

from __future__ import annotations

import io
import math

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson

# NOTE: pandas is imported lazily inside fetch_one, not at module level. The
# harness's spec-introspection imports this module with its own repo on sys.path,
# where `import secrets` (pulled in transitively by numpy.random when pandas
# loads) resolves to the harness's hardened/secrets.py instead of the stdlib and
# crashes. Deferring the import keeps module import clean; the cloud run imports
# pandas normally inside the connector venv.

CATALOG_URL = "https://raw.githubusercontent.com/us-cbo/cbo-data/main/catalog.json"
RAW_BASE = "https://raw.githubusercontent.com/us-cbo/cbo-data/main/"

# First N rows of each distribution hoisted to the file head so every column is
# typed within read_json_auto's default sample window.
PRIME_ROWS = 50

# The rank-accepted entity union — catalog `identifier`s, copied from
# data/sources/cbo/work/entity_union.json. One download + one transform each.
ENTITY_IDS = [
    "automatic_stabilizers",
    "demographic",
    "economic_projections",
    "historical_budget",
    "historical_economic",
    "long_term_budget",
    "long_term_economic",
    "revenue_detail",
    "spending_detail",
    "tax_parameters",
    "ten_year_budget",
    "trust_fund",
]


def _entity_from_node_id(node_id: str) -> str:
    """`cbo-historical-economic` -> `historical_economic` (the catalog id)."""
    return node_id[len("cbo-"):].replace("-", "_")


def _is_nan(v) -> bool:
    return isinstance(v, float) and math.isnan(v)


def fetch_one(node_id: str) -> None:
    """Fetch every distribution of one CBO dataset into a single NDJSON asset.

    Recovers the catalog identifier from the spec id, walks the catalog's
    distributions for that dataset, downloads each CSV, and writes the
    column-unioned rows (tagged with vintage + file_type) as `node_id`.
    """
    import pandas as pd

    def _col_kind(series) -> str:
        return "num" if pd.api.types.is_numeric_dtype(series) else "str"

    entity = _entity_from_node_id(node_id)

    catalog = get(CATALOG_URL, timeout=60).json()
    dataset = next(
        (d for d in catalog.get("datasets", []) if d.get("identifier") == entity),
        None,
    )
    if dataset is None:
        raise ValueError(
            f"{node_id}: dataset {entity!r} not found in CBO catalog "
            f"({len(catalog.get('datasets', []))} datasets present)"
        )

    distributions = dataset.get("distribution", [])
    if not distributions:
        raise ValueError(f"{node_id}: dataset {entity!r} has no distributions")

    frames: list[pd.DataFrame] = []
    for dist in distributions:
        download_url = dist.get("downloadURL")
        if not download_url:
            raise ValueError(f"{node_id}: distribution missing downloadURL: {dist}")
        text = get(RAW_BASE + download_url, timeout=120).text
        frame = pd.read_csv(io.StringIO(text))
        # vintage + file_type are dimensions within the published table.
        frame["vintage"] = str(dist.get("vintage"))
        frame["file_type"] = str(dist.get("file_type"))
        frames.append(frame)

    # Columns that are numeric in one distribution and string in another must be
    # stringified everywhere — otherwise read_json_auto infers a JSON type that
    # leaks quotes into published string values.
    kinds: dict[str, set[str]] = {}
    for frame in frames:
        for col in frame.columns:
            kinds.setdefault(col, set()).add(_col_kind(frame[col]))
    stringify = {col for col, ks in kinds.items() if ks == {"num", "str"}}

    # Stable union of all columns across distributions (preserves first-seen order).
    all_cols: list[str] = []
    for frame in frames:
        for col in frame.columns:
            if col not in all_cols:
                all_cols.append(col)

    def _to_rows(frame: pd.DataFrame) -> list[dict]:
        for col in stringify:
            if col in frame.columns:
                frame[col] = frame[col].map(
                    lambda v: None if (v is None or _is_nan(v)) else str(v)
                )
        frame = frame.reindex(columns=all_cols)
        return [
            {k: (None if _is_nan(v) else v) for k, v in record.items()}
            for record in frame.to_dict(orient="records")
        ]

    per_frame = [_to_rows(frame) for frame in frames]

    # Prime the sample window: a representative slice of every distribution first,
    # then the remainder. Guarantees each column is typed early in the file.
    head: list[dict] = []
    tail: list[dict] = []
    for rows in per_frame:
        head.extend(rows[:PRIME_ROWS])
        tail.extend(rows[PRIME_ROWS:])

    save_raw_ndjson(head + tail, node_id)


def _node_id(entity: str) -> str:
    return f"cbo-{entity.replace('_', '-')}"


DOWNLOAD_SPECS = [
    NodeSpec(id=_node_id(entity), fn=fetch_one, kind="download")
    for entity in ENTITY_IDS
]

# One published Delta table per dataset: the union NDJSON verbatim. file_type and
# vintage columns let consumers slice to a single release / sub-table.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_node_id(entity)}-transform",
        deps=(_node_id(entity),),
        sql=f'SELECT * FROM "{_node_id(entity)}"',
        temporal="vintage",
    )
    for entity in ENTITY_IDS
]
