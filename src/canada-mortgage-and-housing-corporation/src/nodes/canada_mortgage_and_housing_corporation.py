"""Canada Mortgage and Housing Corporation (CMHC) connector.

CMHC publishes ~37 datasets on the federal Open Government Portal (CKAN), of
which 35 are rank-active. Every active dataset is, in practice, one (or a few)
Statistics Canada data tables: the CKAN package's English CSV resource(s) point
at modern StatCan bulk tables (``www150.statcan.gc.ca/n1/tbl/csv/<pid>-eng.zip``,
zipped CSV in the standard StatCan long format). A handful of packages bundle
several StatCan tables; some also carry redundant legacy CANSIM duplicates
(``www20.statcan.gc.ca/.../cansim/...``) which we ignore in favour of the modern
table.

Strategy: stateless full re-pull. For each package we read its CKAN record,
select the modern English CSV resource(s), download + unzip each, parse the
StatCan long format, and normalise every table to one fixed schema (the standard
StatCan metadata columns, with the table-specific dimension columns folded into a
single ``dimensions`` string). The whole corpus is tiny (35 packages, each a few
MB), so we re-fetch everything each refresh and overwrite — revisions are picked
up for free, no watermark needed.
"""

import io
import re
import zipfile

import httpx
import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

from constants import ENTITY_IDS

SLUG = "canada-mortgage-and-housing-corporation"
CKAN = "https://open.canada.ca/data/api/3/action"

# Standard StatCan long-format columns (case-insensitive). Anything in the CSV
# header that is NOT one of these is a table-specific dimension column.
STD_COLS = {
    "ref_date", "geo", "dguid", "uom", "uom_id", "scalar_factor", "scalar_id",
    "vector", "coordinate", "value", "status", "symbol", "terminated", "decimals",
}

SCHEMA = pa.schema([
    ("product_id", pa.string()),     # StatCan table/product id (from the resource URL)
    ("ref_date", pa.string()),       # YYYY or YYYY-MM as published
    ("geo", pa.string()),
    ("dguid", pa.string()),
    ("dimensions", pa.string()),     # "name=value | name=value" for table-specific dims
    ("uom", pa.string()),
    ("scalar_factor", pa.string()),
    ("vector", pa.string()),         # StatCan series id — unique per (vector, ref_date)
    ("coordinate", pa.string()),
    ("value", pa.float64()),
    ("status", pa.string()),
    ("decimals", pa.int64()),
])


@transient_retry()
def _ckan_package(pid: str) -> dict:
    resp = get(f"{CKAN}/package_show", params={"id": pid}, timeout=(10.0, 60.0))
    resp.raise_for_status()
    body = resp.json()
    assert body.get("success"), f"CKAN package_show not success for {pid}"
    return body["result"]


@transient_retry()
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _select_csv_resources(rec: dict) -> list[dict]:
    """English CSV resources, preferring the modern StatCan bulk path. The
    legacy CANSIM (www20 / www5) duplicates carry the same data in an older
    layout — skip them when a modern resource exists."""
    en_csv = [
        r for r in rec.get("resources", [])
        if (r.get("format") or "").upper() == "CSV"
        and "en" in (r.get("language") or [])
        and (r.get("url") or "").lower().endswith(".zip")
    ]
    modern = [r for r in en_csv if "www150.statcan.gc.ca/n1/tbl/csv/" in r["url"]]
    return modern if modern else en_csv


def _product_id(url: str) -> str:
    m = re.search(r"/([0-9]+)-eng\.zip", url, re.IGNORECASE)
    return m.group(1) if m else url.rsplit("/", 1)[-1]


def _read_csv_member(content: bytes) -> tuple[list[str], list[list[str]]]:
    """Unzip a StatCan CSV bundle and return (header, rows) for the data CSV
    (the member that is not the *_MetaData.csv sidecar)."""
    import csv

    zf = zipfile.ZipFile(io.BytesIO(content))
    members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
    data_members = [n for n in members if "metadata" not in n.lower()]
    assert data_members, f"no data CSV in archive; members={zf.namelist()}"
    with zf.open(data_members[0]) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8-sig")
        reader = csv.reader(text)
        header = next(reader)
        rows = [row for row in reader]
    return header, rows


def _to_float(raw: str):
    raw = (raw or "").strip()
    if raw in ("", ".", "..", "...", "F", "x", "E"):
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _to_int(raw: str):
    raw = (raw or "").strip()
    if raw == "":
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def _normalise_table(product_id: str, header: list[str], rows: list[list[str]]) -> list[dict]:
    lower = [h.strip().lower() for h in header]
    # index lookup for standard columns
    idx = {name: lower.index(name) for name in STD_COLS if name in lower}
    dim_positions = [i for i, name in enumerate(lower) if name not in STD_COLS]

    def cell(row, name):
        i = idx.get(name)
        return row[i] if i is not None and i < len(row) else ""

    out = []
    for row in rows:
        if not row:
            continue
        dims = " | ".join(
            f"{header[i].strip()}={row[i].strip()}"
            for i in dim_positions
            if i < len(row) and row[i].strip()
        )
        out.append({
            "product_id": product_id,
            "ref_date": cell(row, "ref_date").strip() or None,
            "geo": cell(row, "geo").strip() or None,
            "dguid": cell(row, "dguid").strip() or None,
            "dimensions": dims or None,
            "uom": cell(row, "uom").strip() or None,
            "scalar_factor": cell(row, "scalar_factor").strip() or None,
            "vector": cell(row, "vector").strip() or None,
            "coordinate": cell(row, "coordinate").strip() or None,
            "value": _to_float(cell(row, "value")),
            "status": cell(row, "status").strip() or None,
            "decimals": _to_int(cell(row, "decimals")),
        })
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    pid = node_id[len(SLUG) + 1:]  # strip "canada-mortgage-and-housing-corporation-"

    rec = _ckan_package(pid)
    resources = _select_csv_resources(rec)
    assert resources, f"{pid}: no English CSV resource found"

    rows: list[dict] = []
    for res in resources:
        url = res["url"]
        product_id = _product_id(url)
        try:
            content = _download(url)
        except httpx.HTTPStatusError as exc:
            # A bundled StatCan table can be discontinued (e.g. 34101000 in the
            # Mortgage-loan-approvals package now 404s). Skip the dead resource
            # and keep the live ones; the package still has data.
            if exc.response.status_code in (403, 404, 410):
                print(f"[{pid}] skipping discontinued resource {product_id} "
                      f"({exc.response.status_code}): {url}")
                continue
            raise
        header, raw_rows = _read_csv_member(content)
        rows.extend(_normalise_table(product_id, header, raw_rows))

    assert rows, f"{pid}: parsed 0 rows from {len(resources)} resource(s)"
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                product_id,
                ref_date,
                geo,
                dguid,
                dimensions,
                uom,
                scalar_factor,
                vector,
                coordinate,
                CAST(value AS DOUBLE)   AS value,
                status,
                CAST(decimals AS BIGINT) AS decimals
            FROM "{s.id}"
        ''',
    )
    for s in DOWNLOAD_SPECS
]
