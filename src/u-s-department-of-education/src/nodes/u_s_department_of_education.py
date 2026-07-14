"""U.S. Department of Education Open Data Platform (data.ed.gov).

The portal is CKAN. Each accepted entity is one CKAN package, and each package
can contain several tabular resources with different local schemas. Fetching
normalizes every readable CSV/Excel/JSON member into NDJSON rows. Provenance
columns identify the package/resource/file/sheet; source columns are kept as
strings.

Resource bytes never pass through memory whole: every download is streamed to a
temp file under a hard size cap, and delimited files are parsed in row chunks.
The portal publishes single resources up to ~1 GB (ArcGIS geojson/kml exports,
shapefile archives, the CRDC bundles), and reading one of those whole is what
OOMs the runner.
"""

from __future__ import annotations

import csv
import json
import os
import re
import tempfile
import warnings
import zipfile
from collections.abc import Iterable
from contextlib import contextmanager
from pathlib import PurePosixPath

import pandas as pd

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, get_client, raw_writer, transient_retry

SLUG = "u-s-department-of-education"
PREFIX = f"{SLUG}-"
CKAN = "https://data.ed.gov/api/3/action"
USER_AGENT = "subsets.io u-s-department-of-education connector"

# Hard ceiling on any single resource we pull down. Bytes are streamed to disk,
# so this bounds bandwidth/time rather than memory. The fattest resource we
# actually want is the 2013-14 CRDC bundle (~592 MB).
MAX_RESOURCE_BYTES = 640 * 1024**2
# Formats we cannot parse incrementally (Excel, JSON) must be held whole, so
# they get a much tighter cap.
MAX_WHOLE_FILE_BYTES = 200 * 1024**2
# Rows per pandas chunk when parsing delimited text.
CHUNK_ROWS = 25_000
DOWNLOAD_CHUNK = 1 << 20

# CKAN `format` values are matched as exact normalized tokens, never as
# substrings: "dat" is a substring of the "/data/" in almost every ed.gov URL,
# so substring matching quietly rescues geojson/kml/html into the tabular set.
TABULAR_FORMATS = {
    "csv", "tsv", "txt", "text", "dat", "ascii", "json",
    "xls", "xlsx", "xlsm", "excel", "microsoft excel", "ms excel",
    "zip", "zipped csv", "zipped tsv", "zipped xls", "zipped xlsx",
    "zipped txt", "zipped text", "zipped dat", "zipped ascii", "zipped excel",
}
# Archives of binary statistical formats: fetchable, but nothing inside is
# something our readers understand, so skip rather than burn the bytes.
OPAQUE_FORMATS = {
    "sas", "sas7bdat", "spss", "sav", "stata", "dta", "mdb", "accdb",
    "zipped sas", "zipped sas7bdat", "zipped spss", "zipped sav",
    "zipped stata", "zipped dta", "zipped mdb", "zipped accdb",
    "zipped binary text",
}
SKIP_FORMATS = {
    "pdf", "doc", "docx", "word", "html", "htm", "xml", "rss", "api",
    "arcgis", "arcgis geoservices rest api", "geojson", "kml", "kmz",
    "gdb", "gpkg", "shp", "shapefile", "esri rest", "data explorer",
    "web page", "webpage", "url", "n/a", "",
}

# ArcGIS Hub geometry-export endpoints. These are matched on the URL *path*
# because their declared format lies: the 808 MB `.../featureCollection` export
# is tagged "txt". Deliberately NOT keyed on query params like `outSR=` — Hub
# appends those to the plain CSV attribute-table exports too (the ACS-ED
# school-district tables), and those are real tabular data we want.
GEO_URL_PATTERNS = (
    "/geojson", "/kml", "/geopackage", "/shapefile", "featurecollection",
    "f=geojson", "f=kml",
)

TEXT_EXTENSIONS = {".csv", ".tsv", ".txt", ".dat", ".asc", ".ascii"}
EXCEL_EXTENSIONS = {".xls", ".xlsx", ".xlsm"}
JSON_EXTENSIONS = {".json"}
PARSEABLE_EXTENSIONS = TEXT_EXTENSIONS | EXCEL_EXTENSIONS | JSON_EXTENSIONS


class UnsupportedResourceError(ValueError):
    """Resource is not something we can turn into rows."""


class ResourceTooLargeError(ValueError):
    """Resource exceeds the byte cap for its format."""


def _entity_id(node_id: str) -> str:
    if not node_id.startswith(PREFIX):
        raise ValueError(f"unexpected node id {node_id!r}; expected prefix {PREFIX!r}")
    return node_id[len(PREFIX):]


def _ckan(action: str, **params) -> dict:
    resp = get(
        f"{CKAN}/{action}",
        params=params,
        headers={"User-Agent": USER_AGENT},
        timeout=120.0,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"CKAN {action} failed: {data!r}")
    return data["result"]


def _normalize_format(value) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower()).lstrip(".")


def _resource_is_tabular(resource: dict) -> bool:
    """Decide from the declared format, falling back to the URL extension.

    Exact-token matching only — see TABULAR_FORMATS.
    """
    url = str(resource.get("url") or "")
    lowered = url.lower()
    if any(pattern in lowered for pattern in GEO_URL_PATTERNS):
        return False

    fmt = _normalize_format(resource.get("format"))
    if fmt in SKIP_FORMATS or fmt in OPAQUE_FORMATS:
        return False
    if fmt in TABULAR_FORMATS:
        return True

    # Unknown/blank format token: trust the URL's extension, nothing else.
    suffix = PurePosixPath(lowered.split("?", 1)[0]).suffix
    return suffix in PARSEABLE_EXTENSIONS | {".zip"}


@contextmanager
def _temp_path(suffix: str = ""):
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    try:
        yield path
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


@transient_retry()
def _stream_to_file(url: str, path: str, cap: int) -> int:
    """Stream `url` into `path`, aborting past `cap` bytes. Returns bytes written."""
    client = get_client()
    written = 0
    with client.stream(
        "GET",
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=240.0,
        follow_redirects=True,
    ) as resp:
        resp.raise_for_status()
        declared = resp.headers.get("content-length")
        if declared and declared.isdigit() and int(declared) > cap:
            raise ResourceTooLargeError(f"content-length {declared} exceeds cap {cap}")
        with open(path, "wb") as fh:
            for chunk in resp.iter_bytes(DOWNLOAD_CHUNK):
                written += len(chunk)
                if written > cap:
                    raise ResourceTooLargeError(f"stream exceeded cap {cap}")
                fh.write(chunk)
    return written


def _clean_col(value, pos: int) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        text = f"column_{pos + 1}"
    return text


def _unique_columns(columns) -> list[str]:
    cols = [_clean_col(c, i) for i, c in enumerate(columns)]
    seen: dict[str, int] = {}
    unique: list[str] = []
    for col in cols:
        n = seen.get(col, 0) + 1
        seen[col] = n
        unique.append(col if n == 1 else f"{col}_{n}")
    return unique


def _stringify(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return str(value)


def _records_from_frame(df: pd.DataFrame, provenance: dict, start_row: int) -> Iterable[dict]:
    """Yield one record per row. `start_row` continues numbering across chunks."""
    if df.empty:
        return
    df = df.dropna(how="all")
    unique_cols = _unique_columns(df.columns)
    for offset, row in enumerate(df.itertuples(index=False, name=None)):
        out = dict(provenance)
        out["row_number"] = start_row + offset
        out.update({col: _stringify(value) for col, value in zip(unique_cols, row)})
        yield out


def _sniff_delimiter(path: str, filename: str) -> str:
    if filename.lower().endswith(".tsv"):
        return "\t"
    with open(path, "rb") as fh:
        sample = fh.read(8192).decode("utf-8-sig", "replace")
    try:
        return csv.Sniffer().sniff(sample, delimiters=",\t|;").delimiter
    except csv.Error:
        return ","


def _read_delimited(path: str, filename: str, provenance: dict) -> Iterable[dict]:
    """Parse delimited text in chunks: peak memory is one chunk, not one file."""
    delimiter = _sniff_delimiter(path, filename)
    for engine in ("c", "python"):
        try:
            reader = pd.read_csv(
                path,
                sep=delimiter,
                dtype=str,
                engine=engine,
                on_bad_lines="skip",
                encoding="utf-8-sig",
                encoding_errors="replace",
                chunksize=CHUNK_ROWS,
            )
            row_number = 1
            for chunk in reader:
                for record in _records_from_frame(chunk, provenance, row_number):
                    yield record
                    row_number += 1
            return
        except (pd.errors.ParserError, pd.errors.EmptyDataError, ValueError, UnicodeDecodeError):
            # The C engine is strict about ragged rows; retry once on the
            # tolerant python engine before falling back to raw lines.
            if engine == "python":
                break
            continue

    # Unparseable as a table — keep the raw lines rather than dropping the file.
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        for row_number, line in enumerate(fh, start=1):
            out = dict(provenance)
            out["row_number"] = row_number
            out["line"] = line.rstrip("\n")
            yield out


def _read_excel(path: str, provenance: dict) -> Iterable[dict]:
    size = os.path.getsize(path)
    if size > MAX_WHOLE_FILE_BYTES:
        raise ResourceTooLargeError(
            f"excel file {size} exceeds whole-file cap {MAX_WHOLE_FILE_BYTES}"
        )
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Unknown extension is not supported")
        # One sheet at a time: sheet_name=None materializes every sheet at once.
        with pd.ExcelFile(path) as book:
            for sheet_name in book.sheet_names:
                df = book.parse(sheet_name, dtype=str)
                sheet_provenance = {**provenance, "sheet_name": str(sheet_name)}
                yield from _records_from_frame(df, sheet_provenance, 1)


def _read_json(path: str, provenance: dict) -> Iterable[dict]:
    size = os.path.getsize(path)
    if size > MAX_WHOLE_FILE_BYTES:
        raise ResourceTooLargeError(
            f"json file {size} exceeds whole-file cap {MAX_WHOLE_FILE_BYTES}"
        )
    with open(path, "rb") as fh:
        data = json.loads(fh.read().decode("utf-8-sig"))
    if isinstance(data, list):
        iterable = data
    elif isinstance(data, dict):
        iterable = data.get("data") or data.get("results") or data.get("records") or [data]
    else:
        iterable = [{"value": data}]
    for row_number, item in enumerate(iterable, start=1):
        out = dict(provenance)
        out["row_number"] = row_number
        if isinstance(item, dict):
            out.update({str(k): _stringify(v) for k, v in item.items()})
        else:
            out["value"] = _stringify(item)
        yield out


def _looks_like_html(path: str) -> bool:
    with open(path, "rb") as fh:
        head = fh.read(512).lstrip().lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html")


def _read_member(path: str, filename: str, provenance: dict) -> Iterable[dict]:
    suffix = PurePosixPath(filename.split("?", 1)[0]).suffix.lower()
    if _looks_like_html(path):
        raise UnsupportedResourceError("resource returned HTML")
    if suffix in EXCEL_EXTENSIONS:
        yield from _read_excel(path, provenance)
    elif suffix in JSON_EXTENSIONS:
        yield from _read_json(path, provenance)
    else:
        yield from _read_delimited(path, filename, provenance)


def _read_zip(path: str, provenance: dict) -> Iterable[dict]:
    """Extract parseable members one at a time; never hold the archive in memory."""
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename
            suffix = PurePosixPath(name).suffix.lower()
            if suffix not in PARSEABLE_EXTENSIONS:
                continue
            if info.file_size > MAX_RESOURCE_BYTES:
                continue
            member_provenance = {**provenance, "archive_member": name}
            with _temp_path(suffix) as member_path:
                with zf.open(info) as src, open(member_path, "wb") as dst:
                    while True:
                        block = src.read(DOWNLOAD_CHUNK)
                        if not block:
                            break
                        dst.write(block)
                try:
                    yield from _read_member(member_path, name, member_provenance)
                except (UnsupportedResourceError, ResourceTooLargeError):
                    continue


def _error_record(package: dict, resource: dict | None, message: str) -> dict:
    return {
        "_subsets_record_type": "resource_error",
        "package_id": package.get("name") or package.get("id"),
        "package_title": package.get("title") or package.get("name") or package.get("id"),
        "resource_id": (resource or {}).get("id"),
        "resource_name": (resource or {}).get("name"),
        "resource_format": (resource or {}).get("format"),
        "resource_position": (resource or {}).get("position"),
        "error": message,
    }


def _package_record(package_id: str, package: dict, skipped: int) -> dict:
    return {
        "_subsets_record_type": "package_metadata",
        "package_id": package_id,
        "package_title": package.get("title") or package_id,
        "package_name": package.get("name") or package_id,
        "metadata_modified": package.get("metadata_modified"),
        "resource_count": len(package.get("resources") or []),
        "skipped_resource_count": skipped,
    }


def _write_ndjson_row(fh, row: dict) -> None:
    fh.write(json.dumps(row, separators=(",", ":"), ensure_ascii=False))
    fh.write("\n")


def _resource_rows(url: str, provenance: dict) -> Iterable[dict]:
    filename = url.rsplit("/", 1)[-1] or str(provenance.get("resource_name") or "resource")
    suffix = PurePosixPath(filename.split("?", 1)[0]).suffix.lower()
    with _temp_path(suffix) as path:
        _stream_to_file(url, path, MAX_RESOURCE_BYTES)
        is_zip = suffix == ".zip" or (
            suffix not in EXCEL_EXTENSIONS and zipfile.is_zipfile(path)
        )
        if is_zip:
            yield from _read_zip(path, provenance)
        else:
            yield from _read_member(path, filename, provenance)


def fetch_one(node_id: str) -> None:
    package_id = _entity_id(node_id)
    try:
        package = _ckan("package_show", id=package_id)
    except Exception as exc:
        package = {"name": package_id, "id": package_id}
        with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
            _write_ndjson_row(fh, _error_record(package, None, f"package_show failed: {exc}"))
        return

    rows_written = 0
    skipped = 0

    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for resource in package.get("resources") or []:
            url = resource.get("url")
            if not url or not _resource_is_tabular(resource):
                skipped += 1
                continue

            provenance = {
                "package_id": package_id,
                "package_title": package.get("title") or package_id,
                "resource_id": resource.get("id"),
                "resource_name": resource.get("name"),
                "resource_format": resource.get("format"),
                "resource_position": resource.get("position"),
            }
            try:
                for row in _resource_rows(url, provenance):
                    _write_ndjson_row(fh, row)
                    rows_written += 1
            except (UnsupportedResourceError, ResourceTooLargeError):
                skipped += 1
                continue
            except Exception as exc:
                _write_ndjson_row(fh, _error_record(package, resource, str(exc)))
                rows_written += 1

        if rows_written == 0:
            _write_ndjson_row(fh, _package_record(package_id, package, skipped))


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for entity_id in ENTITY_IDS
]
