"""AHRQ — MEPS public-use files (PUFs).

MEPS (Medical Expenditure Panel Survey) is AHRQ's flagship public statistical
product. Each accepted entity is one MEPS Household-Component PUF: survey
microdata (one row per person/event/record depending on file type) with its
own variable list. We publish one Delta table per PUF.

Fetch strategy (mechanism `meps_pufs`, bulk_download):
  1. For each PUF number (e.g. "HC-251") scrape its detail page to resolve the
     exact zipped-XLSX download link (path varies: data_files/pufs/<pid>/<pid>xlsx.zip).
  2. Download the zip, extract the single .xlsx, and convert it to parquet with
     DuckDB's excel reader (all_varchar=true — MEPS files are very wide, up to
     ~1400 heterogeneous columns, so we keep every column as text and let the
     transform publish it faithfully rather than risk per-column type inference
     failures across 100 distinct schemas).

Refresh: stateless full re-pull. PUFs are immutable once released and the
accepted set is bounded (~100 modern files), so we just re-fetch each run; the
maintain step (authored later) gates whether a given node actually runs.
Only files from ~2017 onward (which ship XLSX) are in the accepted union;
older PUFs are ASCII-fixed-width only and were scored below the publish
threshold.
"""
import io
import os
import re
import tempfile
import zipfile
from urllib.parse import urljoin

import duckdb

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_IDS

DETAIL_URL = (
    "https://meps.ahrq.gov/mepsweb/data_stats/"
    "download_data_files_detail.jsp?cboPufNumber={puf}"
)
HTTP_TIMEOUT = (10.0, 300.0)  # (connect, read); files are tens of MB


def _puf_number(node_id: str) -> str:
    """Recover the MEPS PUF number from a spec id: 'ahrq-hc-251' -> 'HC-251'."""
    stem = node_id[len("ahrq-"):] if node_id.startswith("ahrq-") else node_id
    return stem.upper()


@transient_retry()
def _resolve_xlsx_url(puf: str) -> str:
    """Scrape the PUF detail page and return the absolute zipped-XLSX URL."""
    detail = DETAIL_URL.format(puf=puf)
    resp = get(detail, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    m = re.search(r'href="([^"]*xlsx\.zip)"', resp.text, re.IGNORECASE)
    if not m:
        raise RuntimeError(f"{puf}: no xlsx.zip link found on detail page {detail}")
    return urljoin(detail, m.group(1))


@transient_retry()
def _download_zip(url: str) -> bytes:
    resp = get(url, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    return resp.content


def _duckdb_excel() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    try:
        con.execute("LOAD excel")
    except Exception:
        con.execute("INSTALL excel")
        con.execute("LOAD excel")
    return con


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    puf = _puf_number(node_id)

    url = _resolve_xlsx_url(puf)
    blob = _download_zip(url)

    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(".xlsx")]
        if not names:
            raise RuntimeError(f"{puf}: archive {url} contains no .xlsx member")
        xlsx_bytes = zf.read(names[0])

    tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    try:
        tmp.write(xlsx_bytes)
        tmp.flush()
        tmp.close()
        con = _duckdb_excel()
        try:
            # all_varchar=true: keep every MEPS variable as text (these files
            # are very wide and mix codes/values; faithful pass-through beats
            # brittle inference). Path is a controlled tempfile.
            path = tmp.name.replace("'", "''")
            table = con.execute(
                f"SELECT * FROM read_xlsx('{path}', all_varchar=true)"
            ).fetch_arrow_table()
        finally:
            con.close()
    finally:
        os.unlink(tmp.name)

    if table.num_rows == 0:
        raise RuntimeError(f"{puf}: parsed XLSX has 0 rows ({url})")

    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ahrq-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per PUF. The raw parquet is already the faithful
# microdata table (all columns text); the transform is a thin pass-through that
# also acts as the correctness gate (0 rows => node failure).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
