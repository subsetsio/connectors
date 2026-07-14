"""London Datastore connector.

Each download node is one accepted CKAN package. A package can contain one or
more tabular resources with different schemas, so the raw asset is normalized
to a fixed string-typed row table: package/resource metadata plus `data_json`,
the original source row encoded as JSON.

Every resource is streamed to disk and parsed in bounded batches: a package's
rows are never all resident at once. The catalog's heavy tail makes that
load-bearing rather than tidy — the median accepted package is ~0.2 MB, but the
largest declares ~2.4 GB across 205 resources, and single resources reach a
1.4 GB zip and a 390 MB spreadsheet.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import time
import zipfile
from collections.abc import Iterable, Iterator
from pathlib import PurePosixPath

import httpx
import openpyxl
import pandas as pd
import pyarrow as pa
from openpyxl.cell.cell import TYPE_ERROR, TYPE_NUMERIC

from constants import ENTITY_IDS
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    get_client,
    raw_asset_exists,
    raw_parquet_writer,
)

SLUG = "london-datastore"
PREFIX = f"{SLUG}-"
API = "https://data.london.gov.uk/api/action"

SUPPORTED_EXTENSIONS = {".csv", ".xls", ".xlsx", ".json"}
TABULAR_FORMATS = {"csv", "xls", "xlsx", "json", "zip"}
BASE_COLUMNS = [
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_url",
    "member_path",
    "sheet_name",
    "source_row_number",
    "data_json",
]

# Rows per parquet batch. The cap on resident rows, so it bounds peak memory
# across every resource shape below.
BATCH_ROWS = 20_000
# The portal rate-limits (429) despite documenting no limit; a DAG walking
# 2500+ resources trips it, so downloads back off rather than tear.
DOWNLOAD_ATTEMPTS = 6
MAX_BACKOFF_S = 60.0
RAW_SCHEMA = pa.schema([(col, pa.string()) for col in BASE_COLUMNS])


def _api(action: str, **params):
    resp = get(f"{API}/{action}", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"CKAN {action} returned success!=true for {params}")
    return body["result"]


def _retry_after(resp: httpx.Response, fallback: float) -> float:
    raw = (resp.headers.get("Retry-After") or "").strip()
    if raw.isdigit():
        return min(float(raw), MAX_BACKOFF_S)
    return fallback


def _stream_to_file(url: str, dest: str) -> None:
    """Stream a resource to disk. Multi-hundred-MB resources are routine here,
    so the body never becomes a bytes object.

    get_client() is the raw httpx client: unlike get(), it carries NO retry, so
    the backoff below is ours to own. The portal does rate-limit (429) despite
    publishing no documented limit, and a DAG walking 2500+ resources trips it
    readily — without this, a 429 would surface as a torn resource."""
    for attempt in range(DOWNLOAD_ATTEMPTS):
        last = attempt == DOWNLOAD_ATTEMPTS - 1
        backoff = min(2.0 ** attempt, MAX_BACKOFF_S)
        try:
            with get_client().stream(
                "GET", url, timeout=httpx.Timeout(300.0, connect=10.0)
            ) as resp:
                if resp.status_code == 429 or resp.status_code >= 500:
                    if last:
                        resp.raise_for_status()
                    time.sleep(_retry_after(resp, backoff))
                    continue
                resp.raise_for_status()
                with open(dest, "wb") as handle:
                    for chunk in resp.iter_bytes(1 << 20):
                        handle.write(chunk)
            return
        except (httpx.TransportError, httpx.TimeoutException):
            if last:
                raise
            time.sleep(backoff)


def _extension(url_or_name: str) -> str:
    path = PurePosixPath(str(url_or_name).split("?", 1)[0].lower())
    suffix = path.suffix
    if suffix == ".gz":
        return PurePosixPath(path.stem).suffix
    return suffix


def _resource_format(resource: dict) -> str:
    fmt = str(resource.get("format") or "").strip().lower()
    if fmt:
        return fmt
    ext = _extension(resource.get("url") or "")
    return ext.lstrip(".")


def _is_supported_resource(resource: dict) -> bool:
    fmt = _resource_format(resource)
    if fmt in TABULAR_FORMATS:
        return True
    return _extension(resource.get("url") or "") in SUPPORTED_EXTENSIONS


def _safe_name(raw: object, fallback: str) -> str:
    name = re.sub(r"[^0-9A-Za-z_]+", "_", str(raw or "").strip().lower())
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        name = fallback
    if name[0].isdigit():
        name = f"col_{name}"
    return name


def _dedupe(names: Iterable[object]) -> list[str]:
    used: set[str] = set()
    out: list[str] = []
    for i, raw in enumerate(names):
        base = _safe_name(raw, f"col_{i + 1}")
        candidate = base
        n = 1
        while candidate in used or candidate in BASE_COLUMNS:
            n += 1
            candidate = f"{base}_{n}"
        used.add(candidate)
        out.append(candidate)
    return out


def _stringify(value: object) -> str | None:
    if pd.isna(value):
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=True, sort_keys=True)
    text = str(value).strip()
    return text or None


def _batched(rows: list[dict]) -> Iterator[list[dict]]:
    for start in range(0, len(rows), BATCH_ROWS):
        yield rows[start:start + BATCH_ROWS]


def _frame_rows(
    frame: pd.DataFrame,
    *,
    sheet_name: str | None,
    member_path: str | None,
    start_number: int,
) -> tuple[list[dict], int]:
    """Rows for one frame (or one chunk of one). `start_number` continues
    `source_row_number` across chunks of the same resource, so a chunked read
    numbers rows exactly as a whole-file read would."""
    number = start_number
    if frame.empty:
        return [], number
    frame = frame.dropna(how="all")
    if frame.empty:
        return [], number
    frame.columns = _dedupe(frame.columns)
    rows: list[dict] = []
    for record in frame.to_dict(orient="records"):
        row = {col: _stringify(value) for col, value in record.items()}
        if any(value is not None for value in row.values()):
            row["source_row_number"] = str(number)
            row["sheet_name"] = sheet_name
            row["member_path"] = member_path
            rows.append(row)
        number += 1
    return rows, number


def _csv_row_batches(path: str, member_path: str | None) -> Iterator[list[dict]]:
    reader = pd.read_csv(
        path,
        dtype=str,
        keep_default_na=False,
        na_values=[],
        encoding_errors="replace",
        chunksize=BATCH_ROWS,
        low_memory=False,
    )
    number = 1
    with reader:
        for frame in reader:
            rows, number = _frame_rows(
                frame, sheet_name=None, member_path=member_path, start_number=number
            )
            if rows:
                yield rows


def _cell_value(cell):
    """One cell, converted the way pandas' openpyxl reader converts it.

    Excel error cells (#N/A, #REF!, ...) become NaN — keyed off the cell TYPE,
    not the text, so a text cell that literally reads "#N/A" is left alone.
    Integral numerics narrow to int, because Excel stores every number as a
    double and pandas renders 655.0 as "655", not "655.0"."""
    if cell.data_type == TYPE_ERROR:
        return float("nan")
    value = cell.value
    if cell.data_type == TYPE_NUMERIC and isinstance(value, float):
        try:
            narrowed = int(value)
        except (OverflowError, ValueError):  # inf / nan
            return value
        if narrowed == value:
            return narrowed
    return value


def _cell_values(cells) -> list:
    return [_cell_value(cell) for cell in cells]


def _mangle_dupes(columns: list) -> list:
    """pandas' duplicate-header mangling (`_maybe_dedup_names`): a repeated
    header becomes `Name.1`, `Name.2`, ... Reproduced here because the readers
    apply it before our own `_dedupe` runs, and the two disagree on the suffix
    (`back_to_contents_1` vs `back_to_contents_2`) for the same sheet."""
    counts: dict = {}
    out = []
    for col in columns:
        count = counts.get(col, 0)
        while count > 0:
            counts[col] = count + 1
            col = f"{col}.{count}"
            count = counts.get(col, 0)
        out.append(col)
        counts[col] = count + 1
    return out


def _chunk_rows(
    chunk: list[list],
    columns: list,
    sheet_title: str,
    member_path: str | None,
    number: int,
) -> tuple[list[dict], int]:
    return _frame_rows(
        # dtype=object or pandas infers one dtype per column and upcasts a
        # mixed int/float column to float64 — rendering 655 as "655.0".
        pd.DataFrame(chunk, columns=columns, dtype=object),
        sheet_name=str(sheet_title),
        member_path=member_path,
        start_number=number,
    )


def _xlsx_row_batches(path: str, member_path: str | None) -> Iterator[list[dict]]:
    """Stream an .xlsx sheet-by-sheet, row-by-row. pandas would hold every sheet
    at once, which the 390 MB workbooks in this catalog cannot afford.

    Each chunk is handed to _frame_rows as a frame, so this reproduces the
    pandas read path the .xls/.csv readers use rather than a lookalike of it.
    Matching pandas exactly takes three rules, each verified against workbooks
    in this catalog:
      * only an ABSENT header cell becomes `Unnamed: <i>` — a blank-but-present
        one ("  ") keeps its value and falls back to `col_<i>` downstream;
      * an Excel error cell (#N/A, #REF!, ...) is NaN, keyed off the cell TYPE
        so a text cell that literally reads "#N/A" survives as text;
      * an empty cell is "" (what `keep_default_na=False` yields), so blank rows
        still consume a `source_row_number` instead of vanishing.
    """
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        for sheet in workbook.worksheets:
            records = sheet.iter_rows()
            header = next(records, None)
            if header is None:
                continue
            columns = _mangle_dupes(
                [
                    f"Unnamed: {i}" if pd.isna(value) else value
                    for i, value in enumerate(_cell_values(header))
                ]
            )
            width = len(columns)
            number = 1
            chunk: list[list] = []
            for record in records:
                values = _cell_values(record)[:width]
                values += [None] * (width - len(values))
                chunk.append(["" if value is None else value for value in values])
                if len(chunk) >= BATCH_ROWS:
                    rows, number = _chunk_rows(
                        chunk, columns, sheet.title, member_path, number
                    )
                    if rows:
                        yield rows
                    chunk = []
            if chunk:
                rows, _ = _chunk_rows(
                    chunk, columns, sheet.title, member_path, number
                )
                if rows:
                    yield rows
    finally:
        workbook.close()


def _xls_row_batches(path: str, member_path: str | None) -> Iterator[list[dict]]:
    # Legacy .xls caps at 65k rows/sheet, so a whole-workbook read stays bounded.
    workbook = pd.read_excel(path, sheet_name=None, dtype=str, keep_default_na=False)
    for sheet_name, frame in workbook.items():
        rows, _ = _frame_rows(
            frame,
            sheet_name=str(sheet_name),
            member_path=member_path,
            start_number=1,
        )
        yield from _batched(rows)


def _json_row_batches(path: str, member_path: str | None) -> Iterator[list[dict]]:
    with open(path, "rb") as handle:
        data = json.loads(handle.read().decode("utf-8-sig"))
    if isinstance(data, dict):
        for key in ("result", "results", "data", "records", "rows"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
    if not isinstance(data, list):
        data = [data]
    frame = pd.json_normalize(data, sep="_")
    rows, _ = _frame_rows(
        frame, sheet_name=None, member_path=member_path, start_number=1
    )
    yield from _batched(rows)


def _file_row_batches(
    path: str, name: str, member_path: str | None = None
) -> Iterator[list[dict]]:
    ext = _extension(name)
    if ext == ".csv":
        yield from _csv_row_batches(path, member_path)
    elif ext == ".xlsx":
        yield from _xlsx_row_batches(path, member_path)
    elif ext == ".xls":
        yield from _xls_row_batches(path, member_path)
    elif ext == ".json":
        yield from _json_row_batches(path, member_path)


def _zip_row_batches(path: str, tmpdir: str) -> Iterator[list[dict]]:
    with zipfile.ZipFile(path) as archive:
        for member in archive.infolist():
            ext = _extension(member.filename)
            if member.is_dir() or ext not in SUPPORTED_EXTENSIONS:
                continue
            # Spill the member to disk rather than read() it: members reach
            # multi-GB, and .xlsx needs a seekable file anyway.
            dest = os.path.join(tmpdir, f"member{ext}")
            with archive.open(member) as src, open(dest, "wb") as out:
                shutil.copyfileobj(src, out, 1 << 20)
            try:
                yield from _file_row_batches(
                    dest, member.filename, member_path=member.filename
                )
            finally:
                if os.path.exists(dest):
                    os.remove(dest)


def _parse_resource(resource: dict, path: str, tmpdir: str) -> Iterator[list[dict]]:
    url = str(resource.get("url") or "")
    if _resource_format(resource) == "zip" or _extension(url) == ".zip":
        yield from _zip_row_batches(path, tmpdir)
    else:
        yield from _file_row_batches(path, url)


def _metadata_row(status: str, message: str) -> dict:
    return {
        "_subsets_status": status,
        "_subsets_message": message,
    }


def _table_from_rows(rows: list[dict]) -> pa.Table:
    normalized = []
    for row in rows:
        data = {
            key: value
            for key, value in row.items()
            if key not in BASE_COLUMNS and value is not None
        }
        normalized.append(
            {
                **{col: row.get(col) for col in BASE_COLUMNS if col != "data_json"},
                "data_json": json.dumps(data, ensure_ascii=True, sort_keys=True),
            }
        )
    return pa.Table.from_pylist(normalized, schema=RAW_SCHEMA)


def _write_rows(writer, rows: list[dict], package: dict, resource: dict) -> None:
    for row in rows:
        row.update(
            {
                "package_id": package["package_id"],
                "package_title": package["package_title"],
                "resource_id": str(resource.get("id") or ""),
                "resource_name": str(resource.get("name") or ""),
                "resource_format": _resource_format(resource),
                "resource_url": str(resource.get("url") or ""),
                "member_path": row.get("member_path"),
                "sheet_name": row.get("sheet_name"),
                "source_row_number": row.get("source_row_number"),
            }
        )
    writer.write_table(_table_from_rows(rows))


def _write_resource(writer, resource: dict, identity: dict, tmpdir: str) -> None:
    """Fetch + parse one resource, emitting at least one row for it.

    Raises only on a transient fetch failure, which fails the whole spec by
    design; anything permanent about the resource is recorded as a row."""
    url = str(resource.get("url") or "")
    if not url:
        _write_rows(
            writer,
            [_metadata_row("metadata_only", "resource has no url")],
            identity,
            resource,
        )
        return

    is_zip = _resource_format(resource) == "zip" or _extension(url) == ".zip"
    dest = os.path.join(tmpdir, f"resource{'.zip' if is_zip else _extension(url)}")
    try:
        _stream_to_file(url, dest)
    except httpx.HTTPStatusError as exc:
        # A dead link (404/403/410) is a fact about the package, so it becomes a
        # row like any other unusable resource. A 429/5xx that outlived the
        # backoff is NOT: recording it would bake a temporary outage into the
        # published table for the whole maintain window, so let it fail the spec
        # and leave the package to retry-failed-specs.
        if exc.response.status_code == 429 or exc.response.status_code >= 500:
            raise
        _write_rows(
            writer,
            [_metadata_row("resource_error", f"{type(exc).__name__}: {exc}")],
            identity,
            resource,
        )
        return

    wrote = False
    try:
        for batch in _parse_resource(resource, dest, tmpdir):
            _write_rows(writer, batch, identity, resource)
            wrote = True
    except Exception as exc:  # noqa: BLE001 - a real, per-resource defect
        # Only parse failures land here: the resource is malformed for us, which
        # is a fact about the data, not about the run. Batches already written
        # stay — partial rows plus an explicit error row beat discarding what the
        # resource did yield.
        _write_rows(
            writer,
            [_metadata_row("resource_error", f"{type(exc).__name__}: {exc}")],
            identity,
            resource,
        )
        return
    finally:
        if os.path.exists(dest):
            os.remove(dest)

    if not wrote:
        _write_rows(
            writer,
            [
                _metadata_row(
                    "metadata_only",
                    "supported resource contained no CSV/XLS/XLSX/JSON rows",
                )
            ],
            identity,
            resource,
        )


def fetch_one(node_id: str) -> None:
    entity_id = node_id[len(PREFIX):]
    package = _api("package_show", id=entity_id)
    resources = [
        resource
        for resource in package.get("resources") or []
        if _is_supported_resource(resource)
    ]
    identity = {
        "package_id": str(package.get("name") or entity_id),
        "package_title": str(package.get("title") or ""),
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        with raw_parquet_writer(node_id, RAW_SCHEMA) as writer:
            for resource in resources:
                _write_resource(writer, resource, identity, tmpdir)
            # Every resource above emits at least one row, so an empty table can
            # only mean the package had nothing supported to begin with.
            if not resources:
                writer.write_table(
                    _table_from_rows(
                        [
                            {
                                **_metadata_row(
                                    "metadata_only", "package has no supported resources"
                                ),
                                **identity,
                            }
                        ]
                    )
                )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]

# Each package is a stateless full re-pull (fetch_one overwrites its raw parquet
# whole every run — picks up CKAN revisions for free). With 757 slow packages
# (some resources take minutes), a single cloud leg can't fetch them all before
# the DAG time budget, so the run self-retriggers in a continuation chain. The
# MaintainSpec bounds the cross-leg cost: a package whose raw parquet already
# exists and is younger than the refresh window is skipped pre-spawn, so the
# backfill is resumable across legs (each leg only spawns not-yet-fetched
# packages, and the chain advances instead of re-validating done work) and
# scheduled weekly refreshes (maintenance cadence 7d) re-pull only what aged out.
MAINTAIN_MAX_AGE_DAYS = 7

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "London Datastore CKAN packages update on their own irregular cadence; "
            f"reuse raw parquet for up to {MAINTAIN_MAX_AGE_DAYS} days (inferred weekly "
            "factory cadence, source portal https://data.london.gov.uk/). Resumable backfill."
        ),
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=MAINTAIN_MAX_AGE_DAYS),
    )
    for spec in DOWNLOAD_SPECS
]
