"""Tesouro Nacional CKAN bulk-resource connector.

Tesouro Transparente exposes a CKAN catalog where each accepted package has one
or more tabular resources. The node id maps 1:1 to a CKAN package slug; each run
resolves the package metadata fresh, downloads the selected CSV/Excel resources,
unpacks CSV/Excel files from ZIP/GZ containers, and writes one NDJSON stream per
package.

Two properties of this catalog drive the design:

* **Resources overlap.** A package typically publishes the same data three ways:
  one plain CSV per year, the same year as a ZIP, and a single consolidated
  GZ/ZIP archive spanning every year. Fetching all of them ingests each row two
  or three times. `_select_resources` picks exactly one representative per
  distinct payload — preferring the compressed form (6x less transfer) and
  dropping the consolidated archive when the per-year partition covers it.
* **Resources are large.** `investidores-do-tesouro-direto` alone is ~5.7 GB of
  CSV across its year partitions. Nothing here may hold a whole resource in
  memory: downloads stream to a temp file, parsing streams in row chunks, and
  rows are yielded rather than materialized.
"""

from __future__ import annotations

import gzip
import io
import json
import os
import re
import tempfile
import zipfile
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import IO, Any

import pandas as pd

from subsets_utils import MaintainSpec, NodeSpec, get, get_client, raw_asset_exists, raw_writer

try:
    from constants import ENTITY_IDS
except ModuleNotFoundError:  # local `python -m` imports load this as src.nodes.*
    from src.constants import ENTITY_IDS


SLUG = "tesouro-nacional"
CKAN = "https://www.tesourotransparente.gov.br/ckan/api/3/action"
TABULAR_FORMATS = {"CSV", "XLS", "XLSX", "ZIP", "GZ", "TSV", "ODS"}
MAX_SHEETS_PER_WORKBOOK = 50

# Rows per pandas chunk. Bounds peak RSS: a chunk of str cells plus its dict
# form is the only row-shaped memory alive at once.
CHUNK_ROWS = 50_000
DOWNLOAD_CHUNK_BYTES = 1 << 20
DOWNLOAD_ATTEMPTS = 3
RAW_EXT = "ndjson.gz"
MAINTAIN_MAX_AGE_DAYS = 7

ARCHIVE_EXTS = (".zip", ".gz")
PLAIN_EXTS = (".csv", ".tsv", ".txt")
EXCEL_EXTS = (".xls", ".xlsx", ".ods")
ALL_EXTS = ARCHIVE_EXTS + PLAIN_EXTS + EXCEL_EXTS

# A stem that another stem extends with a year-ish suffix ("...direto" vs
# "...direto2021" / "...diretoate2017") is the consolidated archive of the
# per-year partition — the same rows, once more.
PARTITION_SUFFIX = re.compile(r"^[_\-]?(ate|de|desde|until)?[_\-]?\d{4}")


def _entity_id_from_node(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id for {SLUG}: {node_id}")
    return node_id[len(prefix) :]


def _package_show(entity_id: str) -> dict[str, Any]:
    resp = get(f"{CKAN}/package_show", params={"id": entity_id}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        raise RuntimeError(f"CKAN package_show failed for {entity_id}: {payload}")
    return payload["result"]


def _resource_format(resource: dict[str, Any]) -> str:
    return str(resource.get("format") or "").strip().upper()


def _filename(resource: dict[str, Any]) -> str:
    url = str(resource.get("url") or "").split("?", 1)[0]
    return PurePosixPath(url).name


def _stem(filename: str) -> str:
    """Filename minus every trailing known extension: `foo.csv.gz` -> `foo`."""
    stem = filename.lower()
    while True:
        base, dot, ext = stem.rpartition(".")
        if dot and f".{ext}" in ALL_EXTS:
            stem = base
            continue
        return stem


def _preference(resource: dict[str, Any]) -> int:
    """Rank the encodings of one payload: compressed first (same rows, ~6x less
    transfer), then plain text, then a workbook."""
    name = _filename(resource).lower()
    if name.endswith(ARCHIVE_EXTS) or _resource_format(resource) in {"ZIP", "GZ"}:
        return 0
    if name.endswith(PLAIN_EXTS) or _resource_format(resource) in {"CSV", "TSV"}:
        return 1
    return 2


def _select_resources(package: dict[str, Any]) -> list[dict[str, Any]]:
    """One resource per distinct payload.

    Collapses `<stem>.csv` / `<stem>.zip` duplicates onto the cheapest encoding,
    then drops a consolidated archive that the per-year partition already covers.
    """
    candidates = [
        r
        for r in package.get("resources") or []
        if str(r.get("url") or "") and _resource_format(r) in TABULAR_FORMATS
    ]

    best_per_stem: dict[str, dict[str, Any]] = {}
    for resource in candidates:
        stem = _stem(_filename(resource))
        incumbent = best_per_stem.get(stem)
        if incumbent is None or _preference(resource) < _preference(incumbent):
            best_per_stem[stem] = resource

    stems = set(best_per_stem)
    kept = {
        stem: resource
        for stem, resource in best_per_stem.items()
        if not any(
            other != stem
            and other.startswith(stem)
            and PARTITION_SUFFIX.match(other[len(stem) :])
            for other in stems
        )
    }
    return [kept[stem] for stem in sorted(kept)]


def _safe_column(value: object, fallback: str) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^0-9a-zA-Z_]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    if not text:
        text = fallback
    if text[0].isdigit():
        text = f"col_{text}"
    return text[:120]


def _normalize_columns(columns: Iterable[object]) -> list[str]:
    seen: dict[str, int] = {}
    out: list[str] = []
    for idx, col in enumerate(columns, start=1):
        base = _safe_column(col, f"column_{idx}")
        count = seen.get(base, 0)
        seen[base] = count + 1
        out.append(base if count == 0 else f"{base}_{count + 1}")
    return out


def _clean_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, float) and pd.isna(value):
        return None
    return str(value)


def _rows_from_frame(df: pd.DataFrame) -> Iterator[dict[str, Any]]:
    df = df.dropna(how="all")
    df.columns = _normalize_columns(df.columns)
    for record in df.to_dict(orient="records"):
        yield {key: _clean_value(value) for key, value in record.items()}


def _download_to_temp(url: str) -> Path:
    """Stream a resource to disk. Never holds the body in memory — these run to
    a gigabyte apiece."""
    client = get_client()
    last_error: Exception | None = None
    for attempt in range(1, DOWNLOAD_ATTEMPTS + 1):
        handle, path_str = tempfile.mkstemp(prefix="tesouro-", suffix=".bin")
        path = Path(path_str)
        try:
            with os.fdopen(handle, "wb") as sink:
                with client.stream("GET", url, timeout=(10.0, 900.0)) as resp:
                    resp.raise_for_status()
                    for chunk in resp.iter_bytes(DOWNLOAD_CHUNK_BYTES):
                        sink.write(chunk)
            return path
        except Exception as exc:
            path.unlink(missing_ok=True)
            last_error = exc
            if attempt == DOWNLOAD_ATTEMPTS:
                break
    raise RuntimeError(f"could not download {url}: {last_error}") from last_error


def _sniff(sample: bytes, source_file: str | None) -> tuple[str, str, int]:
    """Encoding, delimiter, and header offset from a sample.

    Tesouro publishes latin-1 semicolon CSVs, UTF-8 CSVs, and UTF-16 report
    exports with title/filter preambles. Detect the real header line so those
    report exports do not parse as a one-column title followed by skipped rows.
    """
    if sample.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = sample.decode("utf-16")
        encoding = "utf-16"
    else:
        try:
            text = sample.decode("utf-8-sig")
            encoding = "utf-8-sig"
        except UnicodeDecodeError:
            text = sample.decode("latin1")
            encoding = "latin1"

    if source_file and source_file.lower().endswith(".tsv"):
        return encoding, "\t", 0

    lines = text.splitlines()
    candidates = [(idx, line) for idx, line in enumerate(lines) if line.strip()]
    if not candidates:
        return encoding, ",", 0

    separators = (";", ",", "\t", "|")
    header_idx, header = max(
        candidates,
        key=lambda item: (max(item[1].count(sep) for sep in separators), -item[0]),
    )
    separator = max(separators, key=header.count)
    if header.count(separator) == 0:
        separator = ","
        header_idx = 0
    return encoding, separator, header_idx


def _iter_csv_stream(
    open_binary: Callable[[], IO[bytes]], source_file: str | None
) -> Iterator[tuple[str | None, dict[str, Any]]]:
    """Chunked parse of one CSV byte stream. `open_binary` must return a fresh
    reader each call — the header is sniffed from one, the parse consumes another."""
    with open_binary() as probe:
        sample = probe.read(65536)
    if not sample.strip():
        return
    encoding, separator, skiprows = _sniff(sample, source_file)

    with open_binary() as reader:
        frames = pd.read_csv(
            reader,
            dtype=str,
            encoding=encoding,
            encoding_errors="replace",
            sep=separator,
            skiprows=skiprows,
            chunksize=CHUNK_ROWS,
            on_bad_lines="skip",
            low_memory=False,
        )
        for frame in frames:
            for row in _rows_from_frame(frame):
                yield None, row


def _iter_excel(content: bytes, source_file: str | None) -> Iterator[tuple[str | None, dict[str, Any]]]:
    sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, dtype=str, engine=None)
    if len(sheets) > MAX_SHEETS_PER_WORKBOOK:
        raise RuntimeError(
            f"{source_file or 'workbook'} has {len(sheets)} sheets; expected <= {MAX_SHEETS_PER_WORKBOOK}"
        )
    for sheet_name, frame in sheets.items():
        for row in _rows_from_frame(frame):
            yield str(sheet_name), row


def _iter_zip(path: Path) -> Iterator[tuple[str, str | None, dict[str, Any]]]:
    with zipfile.ZipFile(path) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            name = member.filename
            lower = name.lower()
            if lower.endswith((".csv", ".txt", ".tsv")):
                yield from (
                    (name, sheet, row)
                    for sheet, row in _iter_csv_stream(lambda m=member: archive.open(m), name)
                )
            elif lower.endswith(EXCEL_EXTS):
                # Workbooks are small; openpyxl needs the whole member anyway.
                for sheet, row in _iter_excel(archive.read(member), name):
                    yield name, sheet, row


def _container(resource: dict[str, Any]) -> str:
    """How to open this payload.

    The filename extension wins over CKAN's declared `format`, which is
    routinely wrong — `retencao-de-tributos-federais` declares an `.xlsx`
    workbook as `CSV`. Fall back to the format only when the name carries no
    extension we recognize.
    """
    lower = _filename(resource).lower()
    if lower.endswith(".zip"):
        return "zip"
    if lower.endswith(".gz"):
        return "gz"
    if lower.endswith(EXCEL_EXTS):
        return "excel"
    if lower.endswith(PLAIN_EXTS):
        return "csv"

    fmt = _resource_format(resource)
    if fmt == "ZIP":
        return "zip"
    if fmt == "GZ":
        return "gz"
    if fmt in {"XLS", "XLSX", "ODS"}:
        return "excel"
    return "csv"


def _iter_resource(
    resource: dict[str, Any], path: Path
) -> Iterator[tuple[str | None, str | None, dict[str, Any]]]:
    filename = _filename(resource)
    kind = _container(resource)

    if kind == "zip":
        yield from _iter_zip(path)
    elif kind == "gz":
        inner = filename[:-3] if filename.lower().endswith(".gz") else filename
        for sheet, row in _iter_csv_stream(lambda: gzip.open(path, "rb"), inner):
            yield inner, sheet, row
    elif kind == "excel":
        for sheet, row in _iter_excel(path.read_bytes(), filename):
            yield filename, sheet, row
    else:
        for sheet, row in _iter_csv_stream(lambda: path.open("rb"), filename):
            yield filename, sheet, row


@contextmanager
def _fetched(resource: dict[str, Any]) -> Iterator[Path]:
    path = _download_to_temp(str(resource.get("url") or ""))
    try:
        yield path
    finally:
        path.unlink(missing_ok=True)


def fetch_one(node_id: str) -> None:
    entity_id = _entity_id_from_node(node_id)
    package = _package_show(entity_id)
    resources = _select_resources(package)
    if not resources:
        formats = sorted({_resource_format(r) for r in package.get("resources") or []})
        raise RuntimeError(f"{entity_id}: no tabular CKAN resources found; formats={formats}")

    # A package can carry hundreds of resources (retencao-de-tributos-federais
    # publishes 235 monthly workbooks, one of which is a 217-byte stub). Let a
    # few individual payloads fail without sinking the package, but fail loudly
    # once the failures stop looking incidental — a source-wide format change
    # must not pass as a thin-but-successful asset.
    failure_budget = max(1, len(resources) // 10)
    failures: list[str] = []
    rows_written = 0

    with raw_writer(node_id, RAW_EXT, mode="wt", compression="gzip") as handle:
        for resource in resources:
            resource_id = resource.get("id")
            name = _filename(resource)
            try:
                with _fetched(resource) as path:
                    resource_rows = 0
                    for source_file, sheet_name, row in _iter_resource(resource, path):
                        resource_rows += 1
                        record = {
                            "source_entity_id": entity_id,
                            "source_resource_id": resource_id,
                            "source_file": source_file,
                            "source_sheet": sheet_name,
                            "source_row_number": resource_rows,
                        }
                        record.update(row)
                        handle.write(
                            json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
                        )
            except Exception as exc:
                failures.append(f"{name}: {type(exc).__name__}: {exc}")
                print(f"  !! {entity_id}: skipped {name} — {type(exc).__name__}: {exc}")
                if len(failures) > failure_budget:
                    raise RuntimeError(
                        f"{entity_id}: {len(failures)} of {len(resources)} resources failed to parse "
                        f"(budget {failure_budget}); first failures: {failures[:3]}"
                    ) from exc
                continue

            rows_written += resource_rows
            print(f"  -> {entity_id}: {resource_rows} rows from {name}")

        if rows_written == 0:
            raise RuntimeError(f"{entity_id}: parsed tabular resources but wrote zero rows")


# Each package is independent: one CKAN slug in, one NDJSON asset out. The DAG
# already runs nodes one at a time (DAG_PARALLELISM defaults to 1) in forked,
# memory-isolated subprocesses, so chaining specs buys no serialization — it only
# means one node's failure blocks every node after it.
DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id}", fn=fetch_one, kind="download")
    for entity_id in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Tesouro Transparente CKAN packages refresh at dataset-specific cadences; "
            "production maintenance checks for an existing raw NDJSON asset and "
            "re-fetches at least every 7 days per connector maintenance cadence."
        ),
        check=lambda asset_id: raw_asset_exists(
            asset_id, RAW_EXT, max_age_days=MAINTAIN_MAX_AGE_DAYS
        ),
    )
    for spec in DOWNLOAD_SPECS
]
