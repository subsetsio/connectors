"""Kenneth French Data Library connector.

Each accepted dataset is a stable per-dataset ZIP at
``ftp/{NAME}_CSV.zip`` containing one CSV. The CSVs are not clean tables: a
free-text preamble, then one or more *stacked* tables (a 3-factor file has a
monthly block and an annual block; a portfolio file stacks value-weighted
returns, equal-weighted returns, number of firms, average size, average BE/ME,
each over the same N portfolio columns), with whitespace-padded numbers and
``-99.99`` / ``-999`` missing-value sentinels.

To serve all ~300 heterogeneous datasets through one fetch fn, each CSV is
parsed into a uniform **long format**:

    block (int)   sequential index of the stacked sub-table within the file
    statistic     the sub-table's caption (e.g. "Average Value Weighted Returns
                  -- Monthly"); "" for simple factor files
    period        annual | monthly | weekly | daily (from the date-index width
                  and the dataset name)
    date          ISO yyyy-mm-dd (annual -> Jan 1, monthly -> day 1)
    variable      the column header (series / portfolio name); positional
                  ``col_NN`` for the headerless breakpoint files
    value         the observation (sentinel rows dropped)

Stateless full re-pull: each file is small and the whole corpus re-downloads in
a few minutes, so there is no watermark/cursor — every run overwrites the raw
long table. The transform is a pure cast-and-passthrough.
"""

import io
import re
import zipfile

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    raw_parquet_writer,
)
from constants import ENTITY_IDS, SPEC_TO_ENTITY, spec_id

BASE_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"

LONG_SCHEMA = pa.schema([
    ("block", pa.int32()),
    ("statistic", pa.string()),
    ("period", pa.string()),
    ("date", pa.string()),
    ("variable", pa.string()),
    ("value", pa.float64()),
])

_SENTINELS = {"", "-99.99", "-999", "-99.999", "-999.99"}


def _is_index(tok: str) -> bool:
    tok = tok.strip()
    return tok.isdigit() and len(tok) in (4, 6, 8)


def _to_date(tok: str):
    """Map a YYYY / YYYYMM / YYYYMMDD index token to (iso_date, period)."""
    tok = tok.strip()
    if len(tok) == 4:
        return f"{tok}-01-01", "annual"
    if len(tok) == 6:
        return f"{tok[:4]}-{tok[4:6]}-01", "monthly"
    return f"{tok[:4]}-{tok[4:6]}-{tok[6:8]}", "daily"


def _value(tok: str):
    tok = tok.strip()
    if tok in _SENTINELS:
        return None
    try:
        v = float(tok)
    except ValueError:
        return None
    # numeric sentinels (handles padded variants like "-99.9900")
    if abs(v + 99.99) < 1e-6 or abs(v + 999.0) < 1e-6 or abs(v + 999.99) < 1e-6:
        return None
    return v


def _dedupe(names):
    """Ensure column headers are unique within a block (some files repeat one)."""
    seen, out = {}, []
    for n in names:
        if n in seen:
            seen[n] += 1
            out.append(f"{n}.{seen[n]}")
        else:
            seen[n] = 0
            out.append(n)
    return out


def _iter_blocks(text: str, weekly: bool):
    """Yield (block_index, statistic, period, dates, variables, values) for each
    stacked sub-table in a French CSV. Sentinel-valued cells are dropped."""
    lines = text.splitlines()
    # group consecutive non-blank lines into raw blocks
    raw_blocks, cur = [], []
    for ln in lines:
        if ln.strip() == "":
            if cur:
                raw_blocks.append(cur)
                cur = []
        else:
            cur.append(ln)
    if cur:
        raw_blocks.append(cur)

    block_idx = 0
    for block in raw_blocks:
        header_i = None
        first_data = None
        for i, ln in enumerate(block):
            first_field = ln.split(",", 1)[0]
            if header_i is None and first_data is None and first_field.strip() == "" and "," in ln:
                header_i = i
            if _is_index(first_field):
                first_data = i
                break
        if first_data is None:
            continue  # preamble / pure-text block

        if header_i is not None and header_i < first_data:
            cap_lines = block[:header_i]
            colnames = [c.strip() for c in block[header_i].split(",")][1:]
        else:
            cap_lines = block[:first_data]
            ncols = len(block[first_data].split(",")) - 1
            colnames = [f"col_{j + 1:02d}" for j in range(ncols)]
        colnames = _dedupe(colnames)

        statistic = re.sub(r"\s+", " ", " ".join(c.strip() for c in cap_lines)).strip()

        dates, variables, values = [], [], []
        period = None
        for ln in block[first_data:]:
            fields = ln.split(",")
            if not _is_index(fields[0]):
                continue
            d, per = _to_date(fields[0])
            if per == "daily" and weekly:
                per = "weekly"
            period = per
            for name, raw in zip(colnames, fields[1:]):
                v = _value(raw)
                if v is None:
                    continue
                dates.append(d)
                variables.append(name)
                values.append(v)

        if dates:
            yield block_idx, statistic, period, dates, variables, values
            block_idx += 1


def _download_zip(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity = SPEC_TO_ENTITY[node_id]
    weekly = "weekly" in entity.lower()

    content = _download_zip(f"{BASE_URL}{entity}_CSV.zip")
    z = zipfile.ZipFile(io.BytesIO(content))
    member = z.namelist()[0]
    text = z.read(member).decode("latin-1")

    wrote = False
    with raw_parquet_writer(asset, LONG_SCHEMA) as writer:
        for block_idx, statistic, period, dates, variables, values in _iter_blocks(text, weekly):
            n = len(dates)
            table = pa.table(
                {
                    "block": pa.array([block_idx] * n, pa.int32()),
                    "statistic": pa.array([statistic] * n, pa.string()),
                    "period": pa.array([period] * n, pa.string()),
                    "date": pa.array(dates, pa.string()),
                    "variable": pa.array(variables, pa.string()),
                    "value": pa.array(values, pa.float64()),
                },
                schema=LONG_SCHEMA,
            )
            writer.write_table(table)
            wrote = True

    if not wrote:
        raise AssertionError(f"{asset}: parsed zero data rows from {member}")


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
