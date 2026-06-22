"""Damodaran Online (NYU Stern) — industry/region corporate-finance datasets.

Mechanism: per-entity bulk download of legacy BIFF .xls files from a static
faculty web directory (`/pc/datasets/<name>.xls`). One download node per dataset
family; each family is fetched across its regional variants (US, Europe, Japan,
Aus/NZ/Canada, Emerging, China, India, Global) where they exist.

Fetch shape: stateless full re-pull. The source publishes a single annual
snapshot (early January) and exposes no incremental query, so every refresh
re-fetches the current files in full and overwrites. Cheap: <40 families x <=8
small (<200KB) files.

Why we parse in the fetch fn: DuckDB cannot read legacy BIFF .xls, so a SQL
transform can't consume the raw bytes directly. The fetch fn reads each workbook
with pandas/xlrd, locates the headline industry/country table (anchored on a
known header-cell label, sheet-hinted per family), and melts it to a uniform
LONG schema [region, category, metric, value]. This is drift-proof: Damodaran's
column layouts vary across datasets, so a single wide schema per family is
brittle while long format absorbs any column set. The SQL transform is then a
thin typed projection (dropping the constant region column for single-region
families).

Scope: the current snapshot only. Yearly archives exist under /pc/archives/ but
their column *names* drift heavily year-to-year, which would fragment the metric
vocabulary of a unioned long table; the current snapshot gives a coherent,
comparable metric set per family.
"""

import io
import math

import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry
from constants import FAMILIES, ENTITY_IDS, REGION_TOKEN, REGIONS

BASE = "https://pages.stern.nyu.edu/~adamodar/pc/datasets"

RAW_SCHEMA = pa.schema([
    ("region", pa.string()),
    ("category", pa.string()),
    ("metric", pa.string()),
    ("value", pa.float64()),
])

_SKIP_TOKENS = {"", "nan", "na", "n/a", "#div/0!", "#n/a", "#value!", "#ref!", "#name?", "nm"}


def _clean(v) -> str:
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.lower() == "nan" else s


def _norm(v) -> str:
    return " ".join(_clean(v).lower().split())


def _clean_header(v) -> str:
    """Header label, with integral-float year columns normalized: pandas reads
    a bare-year header cell as int in one file and float in another, which would
    fragment the same metric into '2023' and '2023.0' across regions."""
    s = _clean(v)
    try:
        f = float(s)
    except ValueError:
        return s
    return str(int(f)) if f == int(f) else s


def _to_number(v):
    """Return a finite float for numeric-looking cells, else None."""
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        f = float(v)
        return f if math.isfinite(f) else None
    s = str(v).strip().replace(",", "").replace("%", "")
    if s.lower() in _SKIP_TOKENS:
        return None
    try:
        f = float(s)
    except ValueError:
        return None
    return f if math.isfinite(f) else None


def _find_header(df: pd.DataFrame, anchor: str):
    """Index of the header row: first row whose first cell starts with the
    anchor label AND that carries >=3 non-empty cells (excludes title rows)."""
    a = _norm(anchor)
    for i in range(min(len(df), 60)):
        row = df.iloc[i].tolist()
        if _norm(row[0]).startswith(a) and sum(1 for v in row if _clean(v)) >= 3:
            return i
    return None


def _parse_table(content: bytes, anchor: str, sheet_hint):
    """Melt the headline table of one workbook into (category, metric, value) tuples."""
    xls = pd.ExcelFile(io.BytesIO(content))
    order = [sheet_hint] if (sheet_hint and sheet_hint in xls.sheet_names) else []
    order += [s for s in xls.sheet_names if s not in order]
    for sheet in order:
        df = pd.read_excel(xls, sheet_name=sheet, header=None)
        hi = _find_header(df, anchor)
        if hi is None:
            continue
        header = [_clean_header(x) for x in df.iloc[hi].tolist()]
        rows = []
        for k in range(hi + 1, len(df)):
            r = df.iloc[k].tolist()
            category = _clean(r[0])
            if not category:
                break  # blank first cell ends the data block
            for j in range(1, len(header)):
                metric = header[j]
                if not metric:
                    continue
                num = _to_number(r[j]) if j < len(r) else None
                if num is not None:
                    rows.append((category, metric, num))
        if rows:
            return rows
    return []


@transient_retry()
def _download(url: str):
    """Fetch one .xls. Returns bytes on 200, None on a permanent 404/410
    (a region variant that doesn't exist). Transient errors are retried."""
    resp = get(url, timeout=(10.0, 120.0))
    if resp.status_code in (404, 410):
        return None
    resp.raise_for_status()
    return resp.content


def _targets(slug: str, fam: dict):
    """List of (region_label, url) to fetch for this family."""
    if not fam["regional"]:
        return [("US", f"{BASE}/{fam['us_file']}.xls")]
    out = []
    for region in REGIONS:
        base = fam["us_file"] if region == "US" else fam["regional_base"]
        stem = f"{base}{REGION_TOKEN[region]}"
        out.append((region, f"{BASE}/{stem}.xls"))
    return out


def fetch_one(node_id: str) -> None:
    """Download every regional variant of one family, parse + melt to long format,
    and write a single parquet raw asset named after the spec id."""
    slug = node_id[len("damodaran-"):]
    fam = FAMILIES[slug]
    rows = []
    for region, url in _targets(slug, fam):
        content = _download(url)
        if content is None:
            print(f"{node_id}: no file for region {region} ({url}) — skipping region")
            continue
        for category, metric, value in _parse_table(content, fam["anchor"], fam["sheet"]):
            rows.append({"region": region, "category": category, "metric": metric, "value": value})

    if not rows:
        raise RuntimeError(f"{node_id}: parsed 0 rows from all region files")

    table = pa.Table.from_pylist(rows, schema=RAW_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"damodaran-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


def _transform_sql(slug: str, dep_id: str) -> str:
    if FAMILIES[slug]["regional"]:
        cols = "region, category, metric"
    else:
        # single-region family: region is constant, drop it
        cols = "category, metric"
    return (
        f'SELECT {cols}, CAST(value AS DOUBLE) AS value '
        f'FROM "{dep_id}" '
        f'WHERE value IS NOT NULL AND category IS NOT NULL AND metric IS NOT NULL'
    )


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=_transform_sql(spec.id[len("damodaran-"):], spec.id),
    )
    for spec in DOWNLOAD_SPECS
]
