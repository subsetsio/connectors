"""CFPB HMDA — HMDA Data Browser on ffiec.cfpb.gov.

`hmda-filers` is the annual reporting-institution list (small JSON per year).
`hmda-loan-records` is the nationwide loan/application register: per filing year,
GET /view/nationwide/csv?years=YYYY which 301-redirects to a precomputed
nationwide CSV; we stream each year to its own gzipped-CSV batch file. Both
entities discover filing years the same way — probe forward from 2018 (the
post-2018 schema epoch) until a year has no filers.
"""

from __future__ import annotations

import tempfile

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    save_raw_ndjson,
    raw_writer,
)
from utils import _ensure_ua, _http_get

_HMDA_API = "https://ffiec.cfpb.gov/v2/data-browser-api/view"
_HMDA_START_YEAR = 2018  # first HMDA filing year under the modern (Reg C 2018) schema
_HMDA_YEAR_CEILING = _HMDA_START_YEAR + 50  # safety bound for the discovery loop


def _hmda_filing_years() -> list[int]:
    """Discover available HMDA filing years from the source: probe the filers
    endpoint forward from the schema epoch until a year reports no institutions.
    """
    years: list[int] = []
    year = _HMDA_START_YEAR
    while year < _HMDA_YEAR_CEILING:
        resp = _http_get(f"{_HMDA_API}/filers", timeout=60, params={"years": str(year)})
        # A not-yet-published year returns 4xx (the data browser answers 400 for
        # years with no dataset) — that is the upper bound of availability.
        if resp.status_code >= 400:
            break
        institutions = resp.json().get("institutions") or []
        if not institutions:
            break
        years.append(year)
        year += 1
    if year >= _HMDA_YEAR_CEILING:
        raise RuntimeError(
            f"HMDA year discovery hit the {_HMDA_YEAR_CEILING} ceiling — "
            "the filers endpoint never returned an empty year"
        )
    if not years:
        raise RuntimeError("HMDA filers endpoint returned no years from 2018 onward")
    return years


def fetch_hmda_filers(node_id: str) -> None:
    """One row per HMDA-reporting institution per filing year (lei, name, count,
    period). Small JSON per year, concatenated into one NDJSON asset."""
    rows: list[dict] = []
    for year in _hmda_filing_years():
        resp = _http_get(f"{_HMDA_API}/filers", timeout=60, params={"years": str(year)})
        resp.raise_for_status()
        institutions = resp.json().get("institutions") or []
        rows.extend(institutions)
        print(f"  {node_id}: {year} -> {len(institutions)} filers")
    if not rows:
        raise ValueError(f"{node_id}: no HMDA filers fetched")
    save_raw_ndjson(rows, node_id)


@retry(
    retry=retry_if_exception_type((httpx.TransportError, httpx.TimeoutException)),
    wait=wait_exponential(multiplier=2, max=60),
    stop=stop_after_attempt(3),
    reraise=True,
)
def _stream_hmda_year(node_id: str, year: int) -> tuple[tuple[str, ...], int]:
    """Download one filing year's nationwide loan-level CSV and convert it to an
    all-string Parquet batch asset `<node_id>-<year>`. Returns (columns, nrows).

    Parquet via DuckDB `all_varchar=true`: read_csv_auto infers per-file types,
    and HMDA values drift across years (e.g. `total_units` is integer in 2018 but
    carries ranges like "5-24" in 2020), so a multi-file CSV glob fails on a
    schema mismatch the runtime can't reconcile (no union_by_name). Forcing every
    column to VARCHAR yields one identical schema across all year files; numeric
    typing is left to consumers."""
    import os
    import gzip
    import shutil
    import duckdb

    _ensure_ua()
    client = get_client()
    url = f"{_HMDA_API}/nationwide/csv"
    csv_tmp = tempfile.NamedTemporaryFile(suffix=f".{year}.csv.gz", delete=False)
    pq_tmp = tempfile.NamedTemporaryFile(suffix=f".{year}.parquet", delete=False)
    csv_tmp.close()
    pq_tmp.close()
    try:
        with client.stream("GET", url, params={"years": str(year)}, timeout=1800) as resp:
            resp.raise_for_status()
            with gzip.open(csv_tmp.name, "wb") as g:
                for chunk in resp.iter_bytes(8 * 1024 * 1024):
                    g.write(chunk)

        # Inline the paths rather than bind them — DuckDB cannot use prepared
        # parameters for table-function / COPY file targets. Temp paths are
        # process-private (no injection surface).
        csv_path = csv_tmp.name.replace("'", "''")
        pq_path = pq_tmp.name.replace("'", "''")
        con = duckdb.connect()
        try:
            con.execute(
                f"COPY (SELECT * FROM read_csv('{csv_path}', all_varchar=true, header=true)) "
                f"TO '{pq_path}' (FORMAT parquet, COMPRESSION zstd)"
            )
            cols = tuple(
                r[0] for r in con.execute(
                    f"DESCRIBE SELECT * FROM read_parquet('{pq_path}')"
                ).fetchall()
            )
            nrows = con.execute(
                f"SELECT count(*) FROM read_parquet('{pq_path}')"
            ).fetchone()[0]
        finally:
            con.close()
        if nrows == 0:
            raise ValueError(f"{node_id}: {year} produced 0 loan records after CSV->parquet")

        with open(pq_tmp.name, "rb") as src, raw_writer(
            f"{node_id}-{year}", "parquet", mode="wb"
        ) as dst:
            shutil.copyfileobj(src, dst, 8 * 1024 * 1024)
        return cols, int(nrows)
    finally:
        for path in (csv_tmp.name, pq_tmp.name):
            try:
                os.unlink(path)
            except OSError:
                pass


def fetch_hmda_loan_records(node_id: str) -> None:
    """Nationwide HMDA loan/application register, one all-string Parquet batch
    per filing year. The transform globs `<node_id>-*`; identical per-year
    schemas (enforced here) make read_parquet's multi-file union clean."""
    years = _hmda_filing_years()
    first_cols: tuple[str, ...] | None = None
    total = 0
    for year in years:
        cols, nrows = _stream_hmda_year(node_id, year)
        if first_cols is None:
            first_cols = cols
        elif cols != first_cols:
            raise ValueError(
                f"{node_id}: {year} column schema differs from {years[0]} — "
                f"missing={set(first_cols) - set(cols)} extra={set(cols) - set(first_cols)}"
            )
        total += nrows
        print(f"  {node_id}: {year} -> {nrows:,} loan records")
    if total == 0:
        raise ValueError(f"{node_id}: 0 loan records across all years")
    print(f"  {node_id}: {total:,} loan records total across {len(years)} years")


DOWNLOAD_SPECS = [
    NodeSpec(id="cfpb-hmda-filers", fn=fetch_hmda_filers, kind="download"),
    NodeSpec(id="cfpb-hmda-loan-records", fn=fetch_hmda_loan_records, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=(spec.id,),
        sql=f'SELECT * FROM "{spec.id}"',
    )
    for spec in DOWNLOAD_SPECS
]
