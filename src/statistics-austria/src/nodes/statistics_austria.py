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
import zipfile

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)
from constants import ENTITY_IDS

SLUG = "statistics-austria"
DATA_BASE = "https://data.statistik.gv.at/data"

# spec.id lowercases the original id losslessly; map back to the real id.
_SUFFIX_TO_ID = {eid.lower().replace("_", "-"): eid for eid in ENTITY_IDS}

_INT_RE = re.compile(r"^-?\d+$")
_DEC_RE = re.compile(r"^-?\d+[.,]\d+$")


def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content.decode("utf-8-sig", "replace")


def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _fetch_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_optional(url: str):
    """Companion files (HEADER, codelists) are best-effort: a 404 or any other
    failure means 'no labels available', not a node failure."""
    try:
        return _fetch_text(url)
    except Exception:
        return None


def _read_semicolon(text: str):
    # newline="" lets csv own line-termination: some files carry stray CRs and
    # NUL padding past the last row (e.g. OGDEXT_VORNAMEN_1_C-GESCHLECHT-0).
    text = text.replace("\x00", "")
    rows = list(csv.reader(io.StringIO(text, newline=""), delimiter=";"))
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
    try:
        header, data = _read_semicolon(text)
    except csv.Error:
        return {}  # unparseable companion -> no labels, same as a missing one
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


def _resource_map(metadata: dict) -> dict[str, str]:
    resources = {}
    for resource in metadata.get("resources") or []:
        name = (resource.get("name") or "").strip()
        url = (resource.get("url") or "").strip()
        if name and url:
            resources[name] = url
    return resources


def _rows_from_table(text: str, *, source_file: str, col_labels: dict | None = None) -> list[dict]:
    header, data = _read_semicolon(text)
    if not header or not data:
        return []

    used: set = {"source_file", "row_number"}
    columns = []
    for j, raw_col in enumerate(header):
        raw_col = raw_col.strip()
        vals = [(row[j].strip() if j < len(row) else "") for row in data]
        clean = _sanitize((col_labels or {}).get(raw_col, raw_col), used)
        # KLASSDB ZIPs concatenate several classification/correspondence CSVs.
        # The same logical field can be numeric-looking in one member and
        # alphanumeric in another, so keep ZIP payload columns as strings.
        columns.append((clean, [v if v != "" else None for v in vals]))

    rows = []
    for i in range(len(data)):
        row = {
            "source_file": source_file,
            "row_number": i + 1,
        }
        row.update({name: vals[i] for name, vals in columns})
        rows.append(row)
    return rows


def _rows_from_standard_bundle(eid: str, resources: dict[str, str]) -> list[dict]:
    main_url = resources.get(eid) or f"{DATA_BASE}/{eid}.csv"
    main = _fetch_text(main_url)
    header, data = _read_semicolon(main)
    if not header or not data:
        raise ValueError(f"{eid}: main CSV has no data rows")

    header_url = resources.get(f"{eid}_HEADER", f"{DATA_BASE}/{eid}_HEADER.csv")
    col_labels = _label_map(_fetch_optional(header_url))

    used: set = {"source_file", "row_number"}
    columns = []
    for j, raw_col in enumerate(header):
        raw_col = raw_col.strip()
        vals = [(row[j].strip() if j < len(row) else "") for row in data]

        is_dim = raw_col.startswith("C-")
        if is_dim:
            code_url = resources.get(f"{eid}_{raw_col}", f"{DATA_BASE}/{eid}_{raw_col}.csv")
            code_map = _label_map(_fetch_optional(code_url))
            if code_map:
                vals = [code_map.get(v, v) for v in vals]
            vals = [v if v != "" else None for v in vals]
        else:
            vals = _coerce_column(vals)

        clean = _sanitize(col_labels.get(raw_col, raw_col), used)
        columns.append((clean, vals))

    rows = []
    for i in range(len(data)):
        row = {
            "source_file": f"{eid}.csv",
            "row_number": i + 1,
        }
        row.update({name: vals[i] for name, vals in columns})
        rows.append(row)
    return rows


def _rows_from_zip(eid: str, zip_url: str) -> list[dict]:
    blob = _fetch_bytes(zip_url)
    rows = []
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        for info in sorted(zf.infolist(), key=lambda i: i.filename):
            if info.is_dir() or not info.filename.lower().endswith(".csv"):
                continue
            text = zf.read(info).decode("utf-8-sig", "replace")
            rows.extend(_rows_from_table(text, source_file=info.filename))
    if not rows:
        raise ValueError(f"{eid}: zip resource has no CSV data rows")
    keys = set().union(*(row.keys() for row in rows))
    for row in rows:
        for key in keys:
            row.setdefault(key, None)
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    eid = _SUFFIX_TO_ID[node_id[len(SLUG) + 1:]]

    metadata = _fetch_json(f"https://data.statistik.gv.at/ogd/json?dataset={eid}")
    resources = _resource_map(metadata)
    zip_url = resources.get(eid)
    if zip_url and zip_url.lower().endswith(".zip"):
        rows = _rows_from_zip(eid, zip_url)
    else:
        rows = _rows_from_standard_bundle(eid, resources)
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
