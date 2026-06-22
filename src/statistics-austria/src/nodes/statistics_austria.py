"""Statistics Austria — Open Government Data (data.statistik.gv.at).

Catalog connector. Each rank-accepted OGD id is a self-contained statistical
cube published as a semicolon-delimited CSV bundle on a plain static
fileserver:

    https://data.statistik.gv.at/data/{ID}.csv            main fact table
    https://data.statistik.gv.at/data/{ID}_HEADER.csv     column code -> label
    https://data.statistik.gv.at/data/{ID}_{C-DIM}.csv    dimension codelist

Schemas differ per dataset (different dimension columns), so this is the
catalog shape: one generic ``fetch_one`` over the entity union, one
pass-through transform per subset.

The main CSV uses coded cells: a dimension column ``C-BUNDESLAND-0`` holds
values like ``BUNDESLAND-1`` whose label ("Burgenland") lives in the matching
codelist CSV; measure columns hold numbers with a comma decimal separator
(``13,8`` = 13.8). ``fetch_one`` resolves codes to English/German labels and
types each column (int / float / string), all defensively — a missing HEADER
or codelist (some datasets ship neither) falls back to the raw value, never a
node failure. Only a missing/!=200 *main* CSV fails the node, loudly.

Stateless full re-pull every run: the corpus is a few hundred small CSVs, so
there is no incremental filter to use (the source exposes none) and no state —
each run overwrites. Freshness gating is the maintain step's job.
"""

import csv
import io
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)
from constants import ENTITY_IDS

SLUG = "statistics-austria"
DATA_BASE = "https://data.statistik.gv.at/data"

# spec.id lowercases the original id losslessly; map back to the real id.
_SUFFIX_TO_ID = {eid.lower().replace("_", "-"): eid for eid in ENTITY_IDS}

_INT_RE = re.compile(r"^-?\d+$")
_DEC_RE = re.compile(r"^-?\d+[.,]\d+$")


@transient_retry()  # 6 attempts, exponential backoff; reraises on exhaustion
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()  # inside the retry: 5xx/429 -> retried, 4xx -> raise
    return resp.content.decode("utf-8-sig", "replace")


def _fetch_optional(url: str):
    """Companion files (HEADER, codelists) are best-effort: a 404 or any other
    failure means 'no labels available', not a node failure."""
    try:
        return _fetch_text(url)
    except Exception:
        return None


def _read_semicolon(text: str):
    rows = list(csv.reader(io.StringIO(text), delimiter=";"))
    rows = [r for r in rows if any(c.strip() for c in r)]  # drop blank lines
    if not rows:
        return [], []
    return rows[0], rows[1:]


def _label_map(text):
    """Parse a code;name;...;en_name;... file into {code: best_label}.

    Prefers the English label when present, else the German one. Used for both
    HEADER (column labels) and per-dimension codelists (value labels)."""
    if not text:
        return {}
    header, data = _read_semicolon(text)
    if not header:
        return {}
    idx = {name.strip().lower(): i for i, name in enumerate(header)}
    code_i = idx.get("code", 0)
    name_i = idx.get("name")
    en_i = idx.get("en_name")
    out = {}
    for row in data:
        if code_i >= len(row):
            continue
        code = row[code_i].strip()
        if not code:
            continue
        en = row[en_i].strip() if en_i is not None and en_i < len(row) else ""
        de = row[name_i].strip() if name_i is not None and name_i < len(row) else ""
        label = en or de
        if label:
            out[code] = label
    return out


def _sanitize(name: str, used: set) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", "_", (name or "").strip().lower()).strip("_")
    if not s:
        s = "col"
    if s[0].isdigit():
        s = "c_" + s
    base, n = s, 2
    while s in used:
        s = f"{base}_{n}"
        n += 1
    used.add(s)
    return s


def _coerce_column(values):
    """Decide a column's type from its non-empty values and coerce.

    All-integer -> int; all-numeric (some decimals) -> float (comma or dot
    decimal); otherwise leave as string. Empty cells become None."""
    nonempty = [v for v in values if v != ""]
    if not nonempty:
        return values  # all blank -> keep strings (None applied by caller)
    if all(_INT_RE.match(v) for v in nonempty):
        return [int(v) if v != "" else None for v in values]
    if all(_INT_RE.match(v) or _DEC_RE.match(v) for v in nonempty):
        return [float(v.replace(",", ".")) if v != "" else None for v in values]
    return [v if v != "" else None for v in values]


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    eid = _SUFFIX_TO_ID[node_id[len(SLUG) + 1:]]

    main = _fetch_text(f"{DATA_BASE}/{eid}.csv")  # missing main -> node fails
    header, data = _read_semicolon(main)
    if not header or not data:
        raise ValueError(f"{eid}: main CSV has no data rows")

    col_labels = _label_map(_fetch_optional(f"{DATA_BASE}/{eid}_HEADER.csv"))

    used: set = set()
    columns = []  # (clean_name, coerced_values)
    for j, raw_col in enumerate(header):
        raw_col = raw_col.strip()
        vals = [(row[j].strip() if j < len(row) else "") for row in data]

        is_dim = raw_col.startswith("C-")
        if is_dim:
            # resolve coded values -> labels via the dimension's codelist
            code_map = _label_map(_fetch_optional(f"{DATA_BASE}/{eid}_{raw_col}.csv"))
            if code_map:
                vals = [code_map.get(v, v) for v in vals]
            vals = [v if v != "" else None for v in vals]  # keep as string labels
        else:
            vals = _coerce_column(vals)

        clean = _sanitize(col_labels.get(raw_col, raw_col), used)
        columns.append((clean, vals))

    n = len(data)
    rows = [{name: vals[i] for name, vals in columns} for i in range(n)]
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per subset: a thin pass-through of the cleaned,
# typed raw. The empty-result-fails-the-node rule is our correctness floor —
# a dataset that parsed to nothing trips here instead of publishing an empty
# table.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
