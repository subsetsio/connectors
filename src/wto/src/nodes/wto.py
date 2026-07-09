"""WTO connector — bulk statistical trade datasets.

Mechanism (from research): anonymous bulk-download files. There is no catalog
API (the flagship Timeseries API is auth-gated), so the dataset list is the
fixed rank-accepted entity union. Each dataset is a single stable URL pointing
at a ZIP that wraps one CSV; TISMOS is two ZIPs (imports + exports) that share a
schema and publish as one table. The TISMOS FATS addendum is served as a bare
CSV rather than a ZIP.

Fetch shape: stateless full re-pull (decision shape 1). These are static bulk
files overwritten in place each release; there is no incremental/since filter,
so every refresh re-downloads the whole file. Files are large (the BaTiS BPM6
zip is ~509MB), so each fetch streams: download the archive to a scratch
tempfile, then stream-parse the CSV row-by-row into a row-group-streamed parquet
via raw_parquet_writer (bounded memory). Raw columns are kept as strings — a
faithful copy of the source — and all typing/casting happens in the SQL
transform, which is the correctness gate.
"""

import contextlib
import csv
import io
import os
import tempfile
import zipfile

import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    raw_parquet_writer,
    record_source_signature,
    source_unchanged,
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
_TISMOS_FATS = [f"{_DAILY}/Tismos_addendum_FATS.csv"]


# --- transport ----------------------------------------------------------------


@transient_retry()
def _download_to_temp(url: str) -> str:
    """Download a (possibly large) file to a scratch tempfile; return its path.

    The tempfile is intermediate scratch for unzipping/parsing — NOT a raw asset
    (raw is written via subsets_utils.raw_parquet_writer downstream)."""
    resp = get(url, timeout=(15.0, 600.0))
    resp.raise_for_status()
    fd, path = tempfile.mkstemp(prefix="wto-")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(resp.content)
    except BaseException:
        os.unlink(path)
        raise
    return path


def _sniff_encoding(head: bytes) -> str:
    """Detect a CSV's text encoding from its first chunk.

    WTO bulk files are inconsistent: the stats.wto.org tidy CSVs are Windows-1252
    (e.g. 'Türkiye'), while the OECD-WTO services CSVs carry a UTF-8 BOM. Pick the
    right codec per file rather than assuming one."""
    if head.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    try:
        head.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "cp1252"


@contextlib.contextmanager
def _open_csv_binary(path: str, url: str):
    """Open the CSV byte stream behind a downloaded file.

    A .zip is opened through its single .csv member; anything else is read
    directly (the TISMOS FATS addendum is served as a bare CSV)."""
    if url.lower().endswith(".zip"):
        zf = zipfile.ZipFile(path)
        members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not members:
            raise AssertionError(f"{url}: no .csv member in zip ({zf.namelist()})")
        with zf.open(members[0]) as fh:
            yield fh
    else:
        with open(path, "rb") as fh:
            yield fh


def _iter_csv_rows(urls):
    """Yield CSV rows (list[str]) across all urls, validating a shared header.

    The first yielded item is ('header', header_list); every subsequent item is
    ('row', row_list). Later files must repeat the same header (e.g. TISMOS
    imports/exports) or it raises."""
    header = None
    for url in urls:
        path = _download_to_temp(url)
        try:
            with _open_csv_binary(path, url) as probe:
                enc = _sniff_encoding(probe.read(65536))
            with _open_csv_binary(path, url) as raw:
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
    rows = _iter_csv_rows(urls)
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

    # Advance the freshness signature only after the whole asset landed, so a
    # failed fetch can never cause a later false skip. Only single-URL assets
    # have a MaintainSpec — one asset carries one signature.
    if len(urls) == 1:
        record_source_signature(asset, urls[0])


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


def fetch_tismos_fats(node_id: str) -> None:
    _fetch_asset(node_id, _TISMOS_FATS)


DOWNLOAD_SPECS = [
    NodeSpec(id="wto-merchandise-values-annual", fn=fetch_merchandise_values, kind="download"),
    NodeSpec(id="wto-merchandise-indices-annual", fn=fetch_merchandise_indices, kind="download"),
    NodeSpec(id="wto-services-annual", fn=fetch_services, kind="download"),
    NodeSpec(id="wto-batis-bpm6", fn=fetch_batis, kind="download"),
    NodeSpec(id="wto-tismos", fn=fetch_tismos, kind="download"),
    NodeSpec(id="wto-tismos-fats", fn=fetch_tismos_fats, kind="download"),
]


def _fresh(asset: str, url: str) -> bool:
    return source_unchanged(asset, url) and raw_asset_exists(asset, "parquet")


# Every file is overwritten in place at a stable URL and serves Last-Modified, so
# the signature is the freshness signal. `wto-tismos` is absent deliberately: it
# spans two URLs and one asset carries only one signature, and at ~6.5MB the
# unconditional refetch is cheap.
MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="wto-merchandise-values-annual",
        description="Annual release, revised in-year; observed via Last-Modified on https://stats.wto.org/assets/UserGuide/merchandise_values_annual_dataset.zip (cadence per https://www.wto.org/english/res_e/statis_e/trade_datasets_e.htm)",
        check=lambda aid: _fresh(aid, _MERCH_VALUES[0]),
    ),
    MaintainSpec(
        asset_id="wto-merchandise-indices-annual",
        description="Annual release, revised in-year; observed via Last-Modified on https://stats.wto.org/assets/UserGuide/merchandise_indices_annual_dataset.zip (cadence per https://www.wto.org/english/res_e/statis_e/trade_datasets_e.htm)",
        check=lambda aid: _fresh(aid, _MERCH_INDICES[0]),
    ),
    MaintainSpec(
        asset_id="wto-services-annual",
        description="Annual release, revised in-year; observed via Last-Modified on https://stats.wto.org/assets/UserGuide/services_annual_dataset.zip (cadence per https://www.wto.org/english/res_e/statis_e/trade_datasets_e.htm)",
        check=lambda aid: _fresh(aid, _SERVICES[0]),
    ),
    MaintainSpec(
        asset_id="wto-batis-bpm6",
        description="OECD-WTO BaTiS BPM6, annual vintage (last published 2025-12); observed via Last-Modified on the daily_update_e zip. Skipping an unchanged vintage avoids a ~509MB refetch.",
        check=lambda aid: _fresh(aid, _BATIS[0]),
    ),
    MaintainSpec(
        asset_id="wto-tismos-fats",
        description="TISMOS FATS addendum, a frozen 2005-2017 historical corpus (inferred - no published cadence); observed via Last-Modified on the daily_update_e CSV.",
        check=lambda aid: _fresh(aid, _TISMOS_FATS[0]),
    ),
]
