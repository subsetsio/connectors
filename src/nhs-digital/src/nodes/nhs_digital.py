"""NHS Digital connector.

Mechanism (from research): the data.gov.uk CKAN backend
(`ckan.publishing.service.gov.uk`) carries NHS Digital's publication catalogue,
and each package's `resources[]` embeds the file download URLs. Only resources
hosted on the live `files.digital.nhs.uk` CDN are fetchable (HTTP 200, no auth);
all other hosts (hscic.gov.uk, ic.nhs.uk, content.digital.nhs.uk,
digital.nhs.uk) are dead or Cloudflare-gated and are skipped.

Each accepted entity is one CKAN *package* — a statistical publication that
bundles several heterogeneous files (tidy CSVs, Excel workbooks, zipped CSVs)
with differing column lists. The implement contract publishes exactly one Delta
table per package, so every file in a package is melted to a single uniform
long schema: (source_file, row_index, column, value). This is robust to the
bundle's heterogeneity (no cross-file schema drift) and keeps the published
table queryable: filter on `column` / `source_file` to recover any field.

Fetch shape: stateless full re-pull. The live corpus is small (after excluding
the multi-hundred-GB GP-prescribing package, which is not publishable as one
table through this stale mirror) so every refresh re-fetches the package's
current resource set and overwrites. No watermark/cursor — the catalogue
exposes no usable incremental filter, and full re-pull picks up revisions for
free.
"""
import io
import math
import re
import zipfile

import pandas as pd
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

CKAN = "https://ckan.publishing.service.gov.uk/api/3/action"
_DATA_EXT = re.compile(r"\.(csv|xlsx|xls|zip)$", re.I)
_FLUSH_ROWS = 200_000

# The entity union (rank-active packages). Copied from
# data/sources/nhs-digital/work/entity_union.json.
ENTITY_IDS = [
    "general_pharmaceutical_services",
    "national-audit-of-pulmonary-hypertension-12th-annual-report-2020-21",
    "national-audit-of-pulmonary-hypertension-13th-annual-report-2021-22",
    "national-diabetes-audit-2020-21-type-1-diabetes",
    "national-diabetes-audit-report-1-care-processes-and-treatment-targets-2016-17",
    "national-diabetes-audit-report-1-care-processes-and-treatment-targets-2017-18-full-report",
    "national-diabetes-foot-care-audit-2014-2018",
    "national-diabetes-inpatient-audit-nadia-2018",
    "national-diabetes-inpatient-audit-nadia-2019",
    "national-diabetes-inpatient-safety-audit-ndisa-2018-2021",
    "national-diabetes-transition-audit-2011-2017",
    "ndfa-interval-review-july-2014-march-2021",
    "nhs-outcomes-framework-indicators",
]


def _node_id(entity_id: str) -> str:
    return f"nhs-digital-{entity_id.lower().replace('_', '-')}"


# node id -> the package's true CKAN name (the underscore/dash mangling in the
# node id is not reversible, so map it explicitly).
PACKAGE_BY_NODE = {_node_id(eid): eid for eid in ENTITY_IDS}

SCHEMA = pa.schema(
    [
        ("source_file", pa.string()),
        ("row_index", pa.int64()),
        ("column", pa.string()),
        ("value", pa.string()),
    ]
)


@transient_retry()
def _ckan_package(pkg: str) -> dict:
    resp = get(f"{CKAN}/package_show", params={"id": pkg}, timeout=(10.0, 60.0))
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"CKAN package_show failed for {pkg}: {body.get('error')}")
    return body["result"]


@transient_retry()
def _download_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _clean(cell) -> str | None:
    """Normalise a parsed cell to a non-empty string, or None to drop it."""
    if cell is None:
        return None
    if isinstance(cell, float) and math.isnan(cell):
        return None
    s = str(cell).strip()
    if s == "" or s.lower() == "nan":
        return None
    return s


def _csv_rows(content: bytes) -> list[list[str]]:
    import csv

    for enc in ("utf-8-sig", "latin-1"):
        try:
            text = content.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = content.decode("utf-8", "replace")
    return list(csv.reader(io.StringIO(text)))


def _excel_tables(content: bytes, name: str):
    """Yield (source_name, rows) for every sheet of an Excel workbook."""
    sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, header=None, dtype=str)
    for sheet_name, df in sheets.items():
        yield f"{name}::{sheet_name}", df.values.tolist()


def _iter_tables(ext: str, content: bytes, name: str, _depth: int = 0):
    """Yield (source_name, list-of-rows) for a downloaded file. Zips recurse
    into their CSV/Excel members."""
    ext = ext.lower()
    if ext == "csv":
        yield name, _csv_rows(content)
    elif ext in ("xls", "xlsx"):
        yield from _excel_tables(content, name)
    elif ext == "zip" and _depth < 3:
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            members = []
            for member in zf.namelist():
                base = member.split("?")[0]
                m = _DATA_EXT.search(base)
                if not m or member.endswith("/"):
                    continue
                inner_ext = m.group(1).lower()
                if inner_ext == "zip":
                    continue  # don't recurse into nested zips
                members.append((member, base, inner_ext))
            # NHS Digital zips ship the same tables as both .csv and .xls; when
            # CSV copies exist, melt only those (cleaner headers, no duplication).
            if any(e == "csv" for _, _, e in members):
                members = [mb for mb in members if mb[2] == "csv"]
            for member, base, inner_ext in members:
                yield from _iter_tables(
                    inner_ext,
                    zf.read(member),
                    f"{name}::{base.rsplit('/', 1)[-1]}",
                    _depth + 1,
                )


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    pkg = PACKAGE_BY_NODE[node_id]
    record = _ckan_package(pkg)

    urls = []
    for res in record.get("resources", []):
        u = res.get("url") or ""
        base = u.split("?")[0]
        m = _DATA_EXT.search(base)
        if "files.digital.nhs.uk" in u and m:
            urls.append((u, m.group(1).lower()))
    if not urls:
        raise RuntimeError(
            f"{asset}: package '{pkg}' has no live files.digital.nhs.uk resources"
        )
    # Packages commonly publish the same table as both .csv and .xls/.xlsx. When
    # direct CSV resources exist, drop the standalone Excel duplicates (zips are
    # kept — they are handled with the same CSV preference internally).
    if any(ext == "csv" for _, ext in urls):
        urls = [(u, ext) for u, ext in urls if ext in ("csv", "zip")]

    buf: list[dict] = []
    total = 0
    with raw_parquet_writer(asset, SCHEMA) as writer:
        for url, ext in urls:
            base = url.split("?")[0]
            content = _download_bytes(url)
            fname = base.rsplit("/", 1)[-1]
            for source_name, rows in _iter_tables(ext, content, fname):
                if not rows:
                    continue
                header = [_clean(c) for c in rows[0]]
                for ri, row in enumerate(rows[1:], start=1):
                    for ci, cell in enumerate(row):
                        v = _clean(cell)
                        if v is None:
                            continue
                        col = header[ci] if ci < len(header) and header[ci] else f"col_{ci}"
                        buf.append(
                            {
                                "source_file": source_name,
                                "row_index": ri,
                                "column": col,
                                "value": v,
                            }
                        )
                        total += 1
                        if len(buf) >= _FLUSH_ROWS:
                            writer.write_table(pa.Table.from_pylist(buf, schema=SCHEMA))
                            buf = []
        if buf:
            writer.write_table(pa.Table.from_pylist(buf, schema=SCHEMA))

    if total == 0:
        raise RuntimeError(
            f"{asset}: parsed 0 non-empty cells from {len(urls)} file(s) in '{pkg}'"
        )


DOWNLOAD_SPECS = [
    NodeSpec(id=_node_id(eid), fn=fetch_one, kind="download") for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                source_file,
                row_index,
                "column",
                value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
