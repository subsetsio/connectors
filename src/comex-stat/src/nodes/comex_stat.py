"""Comex Stat (Brazilian foreign trade statistics, MDIC/SERPRO) connector.

Mechanism: bulk CSV download (chosen mechanism `bulk_csv`). Two fetch shapes:

* Transaction corpora — one CSV per (flow, year) at /balanca/bd/comexstat-bd/.
  We resolve the latest year from the REST dates endpoint, then stream every year
  from 1997 to latest into ONE parquet asset per flow via `raw_parquet_writer`
  (bounded memory; the published Delta table covers the full history). Stateless
  full re-pull every refresh — the current year's file is overwritten in place as
  new months publish and closed years are occasionally revised, so we never trust
  a stored watermark.
* Reference tables — single auxiliary CSV each under /balanca/bd/tabelas/.

All CSVs are semicolon-delimited, double-quoted, UTF-8. We read every column as a
string (codes carry significant leading zeros — NCM, country, customs unit) and
cast only measures/year/month in the transform SQL.

TLS note: the origin omits its intermediate certificate; `utils.ensure_ca()`
completes the chain in certifi's bundle so verification stays enabled.
"""

import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
    save_raw_parquet,
)

from constants import (
    BULK_BASE,
    DATES_URL,
    START_YEAR,
    TRANSACTION_FILES,
    REFERENCE_FILES,
)
from utils import ensure_ca


# --- helpers -----------------------------------------------------------------

@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _fetch_json(url: str):
    resp = get(url, timeout=(10.0, 60.0))
    resp.raise_for_status()
    return resp.json()


def _read_csv_all_string(raw: bytes) -> pa.Table:
    """Parse a semicolon-delimited, quoted CSV with every column typed as string.

    Encoding is inconsistent across the source: transaction files are ASCII/UTF-8,
    the auxiliary reference tables are ISO-8859-1 (Portuguese names). Try UTF-8,
    fall back to ISO-8859-1 on invalid byte sequences."""
    header = raw.split(b"\n", 1)[0].decode("ascii", errors="replace").replace('"', "").strip()
    cols = [c for c in header.split(";") if c]
    parse = pacsv.ParseOptions(delimiter=";")
    convert = pacsv.ConvertOptions(
        column_types={c: pa.string() for c in cols},
        strings_can_be_null=True,
    )
    for encoding in ("utf-8", "ISO-8859-1"):
        try:
            return pacsv.read_csv(
                io.BytesIO(raw),
                read_options=pacsv.ReadOptions(encoding=encoding),
                parse_options=parse,
                convert_options=convert,
            )
        except pa.lib.ArrowInvalid:
            if encoding == "ISO-8859-1":
                raise
    raise AssertionError("unreachable")


def _latest_year() -> int:
    """Latest year with published data, per the REST dates endpoint."""
    data = _fetch_json(DATES_URL)
    return int(data["data"]["year"])


def _txn_url(subdir: str, prefix: str, year: int, suffix: str) -> str:
    return f"{BULK_BASE}/{subdir}/{prefix}_{year}{suffix}.csv"


# --- fetch fns ---------------------------------------------------------------

def fetch_transactions(node_id: str) -> None:
    """Stream every yearly CSV (1997..latest) for one trade flow into a single
    parquet asset. Schema is fixed from the first year; headers are stable across
    years, and any drift raises loudly rather than silently dropping columns."""
    ensure_ca()
    subdir, prefix, suffix = TRANSACTION_FILES[node_id]
    latest = _latest_year()
    years = list(range(START_YEAR, latest + 1))

    first = _read_csv_all_string(_fetch_bytes(_txn_url(subdir, prefix, years[0], suffix)))
    schema = first.schema
    expected = set(schema.names)

    with raw_parquet_writer(node_id, schema) as writer:
        writer.write_table(first)
        for year in years[1:]:
            table = _read_csv_all_string(_fetch_bytes(_txn_url(subdir, prefix, year, suffix)))
            if set(table.column_names) != expected:
                raise AssertionError(
                    f"{node_id}: column drift in {prefix}_{year}{suffix}.csv: "
                    f"{table.column_names} != {schema.names}"
                )
            writer.write_table(table.select(schema.names))


def fetch_reference(node_id: str) -> None:
    """Fetch a single auxiliary reference table (small enough to hold in memory)."""
    ensure_ca()
    stem = REFERENCE_FILES[node_id]
    raw = _fetch_bytes(f"{BULK_BASE}/tabelas/{stem}.csv")
    table = _read_csv_all_string(raw)
    save_raw_parquet(table, node_id)


# --- download specs ----------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="comex-stat-exports-ncm", fn=fetch_transactions, kind="download"),
    NodeSpec(id="comex-stat-imports-ncm", fn=fetch_transactions, kind="download"),
    NodeSpec(id="comex-stat-exports-municipality", fn=fetch_transactions, kind="download"),
    NodeSpec(id="comex-stat-imports-municipality", fn=fetch_transactions, kind="download"),
    NodeSpec(id="comex-stat-isic-cuci", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-nbm", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-ncm", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-ncm-cgce", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-ncm-cuci", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-ncm-fat-agreg", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-ncm-grupo", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-ncm-isic", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-ncm-ppe", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-ncm-ppi", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-ncm-sh", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-ncm-siit", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-ncm-unidade", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-pais", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-pais-bloco", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-uf", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-uf-mun", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-urf", fn=fetch_reference, kind="download"),
    NodeSpec(id="comex-stat-via", fn=fetch_reference, kind="download"),
]
