"""Stanford Open Policing Project raw downloads.

The source publishes one ZIP-compressed CSV per standardized location on the
project data page, backed by Stanford Stacks file URLs. Files can be large and
location schemas vary, so each download node streams its ZIP to a temporary file,
then streams CSV rows to a Parquet file with a few provenance columns.
Transforms type and select columns after profiling the real raw assets.

Raw is Parquet with every source column typed `string`, so the read side does
no type inference at all, and the source's `NA` is decoded to null.

Both details are load-bearing. The CSVs are R exports, so a missing cell is the
literal `NA` — in numeric columns too (`lat`, `subject_age`), where it cannot
be a value. Under NDJSON that was fatal: read_json_auto infers types from a
sample of the file head, so a column whose first rows all parse as times was
bound TIME and the scan then died on the first `NA` deeper in the file (3 such
rows out of 36845 killed vt-burlington). No SQL cast can help — the failure is
in the read, before the cast. Parquet is self-describing, so the declared
string type IS the read type, for every file and every future run.

Decoding `NA` to null then lets the model verify pure casts on the full scan
(it exempts nulls but not sentinels), which is what recovers real DATE/DOUBLE
types downstream instead of stranding every column at VARCHAR. Only the exact
uppercase `NA` is a sentinel: `na` and `N/A` occur as ordinary free text and
are left alone, as are genuine empty cells, which are distinct from `NA` here
(mt-statewide carries both).
"""

from __future__ import annotations

import csv
import html
import re
import tempfile
import zipfile
from pathlib import Path

import httpx
import pyarrow as pa
import pyarrow.parquet as pq

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, raw_writer, transient_retry

SLUG = "stanford-open-policing-project"
PREFIX = f"{SLUG}-"
DATA_PAGE = "https://openpolicing.stanford.edu/data/"
HEADERS = {"User-Agent": "subsets-factory/1.0"}
_BATCH_ROWS = 50_000
# R's missing literal, and empty cells. Exact case only — "na"/"N/A" are data.
_NULL_VALUES = frozenset({"", "NA"})


def fetch_one(node_id: str) -> None:
    entity_id = node_id[len(PREFIX):]
    url = _csv_url_by_entity()[entity_id]

    with tempfile.TemporaryDirectory(prefix="opp_") as tmpdir:
        zip_path = Path(tmpdir) / f"{entity_id}.csv.zip"
        _download_to_file(url, zip_path)
        written = _emit_zip_csv(zip_path, node_id, entity_id, url.rsplit("/", 1)[-1])

    if written == 0:
        raise RuntimeError(f"{node_id}: parsed 0 rows from {url}")


def _csv_url_by_entity() -> dict[str, str]:
    resp = get(DATA_PAGE, headers=HEADERS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    urls = re.findall(r'https://stacks\.stanford\.edu/file/[^" ]+?\.csv\.zip', resp.text)
    out = {}
    for url in urls:
        entity_id = _entity_id_from_filename(url.rsplit("/", 1)[-1])
        out[entity_id] = html.unescape(url)
    missing = sorted(set(ENTITY_IDS) - set(out))
    if missing:
        raise RuntimeError(f"data page missing CSV URLs for {len(missing)} entities: {missing[:5]}")
    return out


@transient_retry()
def _download_to_file(url: str, path: Path) -> None:
    timeout = httpx.Timeout(connect=20.0, read=900.0, write=60.0, pool=60.0)
    with httpx.Client(follow_redirects=True, headers=HEADERS, timeout=timeout) as client:
        with client.stream("GET", url) as resp:
            resp.raise_for_status()
            with path.open("wb") as out:
                for chunk in resp.iter_bytes(chunk_size=1024 * 1024):
                    if chunk:
                        out.write(chunk)
    if path.stat().st_size == 0:
        raise RuntimeError(f"{url}: downloaded empty ZIP")


def _emit_zip_csv(zip_path: Path, asset: str, entity_id: str, source_file: str) -> int:
    with zipfile.ZipFile(zip_path) as zf:
        csv_members = [name for name in zf.namelist() if name.lower().endswith(".csv")]
        if len(csv_members) != 1:
            raise RuntimeError(f"{zip_path.name}: expected one CSV member, got {csv_members}")
        member = csv_members[0]
        with zf.open(member) as raw:
            text = (line.decode("utf-8-sig", errors="replace") for line in raw)
            reader = csv.DictReader(text)
            if not reader.fieldnames:
                raise RuntimeError(f"{zip_path.name}: CSV has no header")
            fieldnames = _dedupe_headers(reader.fieldnames)
            reader.fieldnames = fieldnames
            schema = pa.schema(
                [
                    pa.field("_source_entity_id", pa.string()),
                    pa.field("_source_file", pa.string()),
                    pa.field("_source_member", pa.string()),
                    pa.field("_row_number", pa.int64()),
                ]
                + [pa.field(name, pa.string()) for name in fieldnames]
            )
            with raw_writer(asset, "parquet") as out:
                writer = pq.ParquetWriter(out, schema, compression="zstd")
                try:
                    written = _write_rows(reader, writer, schema, fieldnames, entity_id,
                                          source_file, member)
                finally:
                    writer.close()
    return written


def _write_rows(reader, writer, schema, fieldnames, entity_id, source_file, member) -> int:
    """Stream CSV rows into `writer` in batches — these files don't fit in memory."""
    buf: dict[str, list] = {name: [] for name in schema.names}
    written = 0
    for row_number, row in enumerate(reader, start=1):
        buf["_source_entity_id"].append(entity_id)
        buf["_source_file"].append(source_file)
        buf["_source_member"].append(member)
        buf["_row_number"].append(row_number)
        for key in fieldnames:
            value = row.get(key)
            buf[key].append(None if value in _NULL_VALUES else value)
        written += 1
        if len(buf["_row_number"]) >= _BATCH_ROWS:
            _flush(writer, schema, buf)
    _flush(writer, schema, buf)
    return written


def _flush(writer, schema, buf: dict[str, list]) -> None:
    if not buf["_row_number"]:
        return
    writer.write_table(pa.Table.from_pydict(buf, schema=schema))
    for values in buf.values():
        values.clear()


def _dedupe_headers(headers: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out = []
    for raw in headers:
        name = (raw or "").strip()
        if not name:
            name = "unnamed"
        count = seen.get(name, 0)
        seen[name] = count + 1
        out.append(name if count == 0 else f"{name}_{count + 1}")
    return out


def _entity_id_from_filename(filename: str) -> str:
    name = filename.split("_", 1)[-1]
    name = re.sub(r"_\d{4}_\d{2}_\d{2}\.csv\.zip$", "", name)
    return name.replace("_", "-")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
