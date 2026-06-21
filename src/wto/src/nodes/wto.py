"""WTO connector — bulk statistical trade datasets.

Mechanism (from research): anonymous bulk-download files. There is no catalog
API (the flagship Timeseries API is auth-gated), so the dataset list is the
fixed rank-accepted entity union. Each dataset is a single stable URL pointing
at a ZIP that wraps one CSV; TISMOS is two ZIPs (imports + exports) that share a
schema and publish as one table.

Fetch shape: stateless full re-pull (decision shape 1). These are static bulk
files overwritten in place each release; there is no incremental/since filter,
so every refresh re-downloads the whole file. Files are large (the BaTiS BPM6
zip is ~509MB), so each fetch streams: download the archive to a scratch
tempfile, then stream-parse the CSV row-by-row into a row-group-streamed parquet
via raw_parquet_writer (bounded memory). Raw columns are kept as strings — a
faithful copy of the source — and all typing/casting happens in the SQL
transform, which is the correctness gate.
"""

import csv
import io
import os
import tempfile
import zipfile

import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

_BATCH_ROWS = 100_000  # rows per parquet row-group flush

# --- file URLs per asset (one stable bulk URL each; TISMOS has two) -----------
_STATS = "https://stats.wto.org/assets/UserGuide"
_DAILY = "https://www.wto.org/english/res_e/statis_e/daily_update_e"

_MERCH_VALUES = [f"{_STATS}/merchandise_values_annual_dataset.zip"]
_MERCH_INDICES = [f"{_STATS}/merchandise_indices_annual_dataset.zip"]
_SERVICES = [f"{_STATS}/services_annual_dataset.zip"]
_BATIS = [f"{_DAILY}/OECD-WTO_BATIS_data_BPM6-1.zip"]
_TISMOS = [f"{_DAILY}/Tismos_imports.zip", f"{_DAILY}/Tismos_exports.zip"]


# --- transport ----------------------------------------------------------------


@transient_retry()
def _download_to_temp(url: str) -> str:
    """Download a (possibly large) archive to a scratch tempfile; return its path.

    The tempfile is intermediate scratch for unzipping — NOT a raw asset (raw is
    written via subsets_utils.raw_parquet_writer downstream)."""
    resp = get(url, timeout=(15.0, 600.0))
    resp.raise_for_status()
    fd, path = tempfile.mkstemp(suffix=".zip", prefix="wto-")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(resp.content)
    except BaseException:
        os.unlink(path)
        raise
    return path


def _sniff_encoding(zf: zipfile.ZipFile, member: str) -> str:
    """Detect a CSV member's text encoding from its first chunk.

    WTO bulk files are inconsistent: the stats.wto.org tidy CSVs are Windows-1252
    (e.g. 'Türkiye'), while the OECD-WTO services CSVs carry a UTF-8 BOM. Pick the
    right codec per file rather than assuming one."""
    with zf.open(member) as fh:
        head = fh.read(65536)
    if head.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    try:
        head.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "cp1252"


def _iter_zip_csv_rows(urls):
    """Yield CSV rows (list[str]) across all urls, validating a shared header.

    The first yielded item is ('header', header_list); every subsequent item is
    ('row', row_list). Later files must repeat the same header (e.g. TISMOS
    imports/exports) or it raises."""
    header = None
    for url in urls:
        path = _download_to_temp(url)
        try:
            zf = zipfile.ZipFile(path)
            members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            if not members:
                raise AssertionError(f"{url}: no .csv member in zip ({zf.namelist()})")
            enc = _sniff_encoding(zf, members[0])
            with zf.open(members[0]) as raw:
                # errors='replace' so a single odd byte never aborts a production run.
                text = io.TextIOWrapper(raw, encoding=enc, errors="replace", newline="")
                reader = csv.reader(text)
                this_header = next(reader)
                if header is None:
                    header = this_header
                    yield ("header", header)
                else:
                    assert this_header == header, (
                        f"{url}: header {this_header} != first header {header}"
                    )
                for row in reader:
                    yield ("row", row)
        finally:
            os.unlink(path)


def _fetch_asset(asset: str, urls) -> None:
    """Stream the CSV(s) behind `urls` into one all-string parquet raw asset."""
    rows = _iter_zip_csv_rows(urls)
    kind, header = next(rows)
    assert kind == "header"
    n = len(header)
    schema = pa.schema([(col, pa.string()) for col in header])

    cols = [[] for _ in range(n)]
    pending = 0
    with raw_parquet_writer(asset, schema) as writer:
        for _, row in rows:
            for i in range(n):
                cols[i].append(row[i] if i < len(row) else None)
            pending += 1
            if pending >= _BATCH_ROWS:
                writer.write_table(pa.table({header[i]: cols[i] for i in range(n)}, schema=schema))
                cols = [[] for _ in range(n)]
                pending = 0
        if pending:
            writer.write_table(pa.table({header[i]: cols[i] for i in range(n)}, schema=schema))


# --- one fetch fn per asset (runtime calls fn(spec_id); spec_id IS the asset) -

def fetch_merchandise_values(node_id: str) -> None:
    _fetch_asset(node_id, _MERCH_VALUES)


def fetch_merchandise_indices(node_id: str) -> None:
    _fetch_asset(node_id, _MERCH_INDICES)


def fetch_services(node_id: str) -> None:
    _fetch_asset(node_id, _SERVICES)


def fetch_batis(node_id: str) -> None:
    _fetch_asset(node_id, _BATIS)


def fetch_tismos(node_id: str) -> None:
    _fetch_asset(node_id, _TISMOS)


DOWNLOAD_SPECS = [
    NodeSpec(id="wto-merchandise-values-annual", fn=fetch_merchandise_values, kind="download"),
    NodeSpec(id="wto-merchandise-indices-annual", fn=fetch_merchandise_indices, kind="download"),
    NodeSpec(id="wto-services-annual", fn=fetch_services, kind="download"),
    NodeSpec(id="wto-batis-bpm6", fn=fetch_batis, kind="download"),
    NodeSpec(id="wto-tismos", fn=fetch_tismos, kind="download"),
]


# --- transforms — one published Delta table per subset ------------------------
# All three WTO Stats files share the same tidy 23-column schema; only the
# IndicatorCategory/Unit values differ, so they share one SELECT template.

def _tidy_sql(view: str) -> str:
    return f'''
        SELECT
            IndicatorCategory            AS indicator_category,
            IndicatorCode                AS indicator_code,
            Indicator                    AS indicator,
            ReporterCode                 AS reporter_code,
            ReporterISO3A                AS reporter_iso3,
            Reporter                     AS reporter,
            PartnerCode                  AS partner_code,
            PartnerISO3A                 AS partner_iso3,
            Partner                      AS partner,
            ProductClassificationCode    AS product_classification_code,
            ProductClassification        AS product_classification,
            ProductCode                  AS product_code,
            Product                      AS product,
            FrequencyCode                AS frequency_code,
            Frequency                    AS frequency,
            UnitCode                     AS unit_code,
            Unit                         AS unit,
            TRY_CAST(Year AS INTEGER)    AS year,
            ValueFlagCode                AS value_flag_code,
            ValueFlag                    AS value_flag,
            TRY_CAST(Value AS DOUBLE)    AS value
        FROM "{view}"
        WHERE TRY_CAST(Year AS INTEGER) IS NOT NULL
          AND TRY_CAST(Value AS DOUBLE) IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wto-merchandise-values-annual-transform",
        deps=["wto-merchandise-values-annual"],
        sql=_tidy_sql("wto-merchandise-values-annual"),
    ),
    SqlNodeSpec(
        id="wto-merchandise-indices-annual-transform",
        deps=["wto-merchandise-indices-annual"],
        sql=_tidy_sql("wto-merchandise-indices-annual"),
    ),
    SqlNodeSpec(
        id="wto-services-annual-transform",
        deps=["wto-services-annual"],
        sql=_tidy_sql("wto-services-annual"),
    ),
    SqlNodeSpec(
        id="wto-batis-bpm6-transform",
        deps=["wto-batis-bpm6"],
        sql='''
            SELECT
                Reporter                            AS reporter,
                type_Reporter                       AS reporter_type,
                Partner                             AS partner,
                type_Partner                        AS partner_type,
                Flow                                AS flow,
                Item_code                           AS item_code,
                type_Item                           AS item_type,
                TRY_CAST(Year AS INTEGER)           AS year,
                TRY_CAST(Reported_value AS DOUBLE)  AS reported_value,
                TRY_CAST(Final_value AS DOUBLE)     AS final_value,
                Final_value_methodology             AS final_value_methodology,
                TRY_CAST(Balanced_value AS DOUBLE)  AS balanced_value
            FROM "wto-batis-bpm6"
            WHERE TRY_CAST(Year AS INTEGER) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="wto-tismos-transform",
        deps=["wto-tismos"],
        sql='''
            SELECT
                FLOW                        AS flow,
                REPORTER                    AS reporter,
                PARTNER                     AS partner,
                INDICATOR                   AS indicator,
                TRY_CAST(YEAR AS INTEGER)   AS year,
                MODE                        AS mode_of_supply,
                TRY_CAST(VALUE AS DOUBLE)   AS value,
                METH                        AS method
            FROM "wto-tismos"
            WHERE TRY_CAST(YEAR AS INTEGER) IS NOT NULL
              AND TRY_CAST(VALUE AS DOUBLE) IS NOT NULL
        ''',
    ),
]
