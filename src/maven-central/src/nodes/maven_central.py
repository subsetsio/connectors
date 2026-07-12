"""Maven Central artifact catalog download.

The public Solr search API is useful for spot checks but rate-blocks long
GitHub-hosted crawls. For full-corpus extraction, use the official repository
index published under repo1's .index directory. The packed index is a gzip
stream of Maven Indexer records; each artifact record carries compact `u`
(groupId|artifactId|version|classifier) and `i` metadata fields.
"""

from __future__ import annotations

import gzip
import struct
from collections.abc import Iterator

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, raw_parquet_writer

INDEX_URL = "https://repo1.maven.org/maven2/.index/nexus-maven-repository-index.gz"
USER_AGENT = (
    "Mozilla/5.0 (compatible; subsets.io Maven Central connector; "
    "+https://subsets.io)"
)

SCHEMA = pa.schema(
    [
        ("group_id", pa.string()),
        ("artifact_id", pa.string()),
        ("latest_version", pa.string()),
        ("packaging", pa.string()),
        ("version_count", pa.int64()),
        ("repository_id", pa.string()),
        ("last_updated", pa.timestamp("ms")),
    ]
)

BATCH_SIZE = 50_000


class _IteratorReader:
    """Minimal read(size) adapter around httpx.iter_bytes for gzip.GzipFile."""

    def __init__(self, chunks: Iterator[bytes]) -> None:
        self._chunks = chunks
        self._buffer = bytearray()
        self._eof = False

    def read(self, size: int = -1) -> bytes:
        if size is None or size < 0:
            parts = [bytes(self._buffer)]
            self._buffer.clear()
            parts.extend(self._chunks)
            self._eof = True
            return b"".join(parts)

        while len(self._buffer) < size and not self._eof:
            try:
                self._buffer.extend(next(self._chunks))
            except StopIteration:
                self._eof = True

        out = bytes(self._buffer[:size])
        del self._buffer[:size]
        return out


def _read_exact(stream, size: int) -> bytes:
    data = stream.read(size)
    if len(data) != size:
        raise EOFError(f"expected {size} bytes, got {len(data)}")
    return data


def _decode_modified_utf8(data: bytes) -> str:
    # Maven coordinates and compact field names are ASCII in practice. Python's
    # UTF-8 decoder handles that path directly; the replacement fallback avoids
    # failing the whole corpus on a non-coordinate descriptive field we ignore.
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace").replace("\x00", "")


def _read_utf_short(stream) -> str:
    length = struct.unpack(">H", _read_exact(stream, 2))[0]
    return _decode_modified_utf8(_read_exact(stream, length))


def _read_utf_int(stream) -> str:
    length = struct.unpack(">i", _read_exact(stream, 4))[0]
    if length < 0:
        raise ValueError(f"negative string length in Maven index: {length}")
    return _decode_modified_utf8(_read_exact(stream, length))


def _iter_index_records():
    timeout = httpx.Timeout(connect=30.0, read=600.0, write=30.0, pool=30.0)
    headers = {"User-Agent": USER_AGENT, "Accept": "application/gzip,*/*"}
    with httpx.stream(
        "GET",
        INDEX_URL,
        headers=headers,
        timeout=timeout,
        follow_redirects=True,
    ) as response:
        response.raise_for_status()
        reader = _IteratorReader(response.iter_bytes(chunk_size=1024 * 1024))
        with gzip.GzipFile(fileobj=reader, mode="rb") as gz:
            _read_exact(gz, 1)  # transfer format version
            _read_exact(gz, 8)  # index timestamp, milliseconds since epoch
            while True:
                raw_count = gz.read(4)
                if not raw_count:
                    break
                if len(raw_count) != 4:
                    raise EOFError("truncated Maven index record field count")
                field_count = struct.unpack(">i", raw_count)[0]
                record = {}
                for _ in range(field_count):
                    _read_exact(gz, 1)  # field flags, not needed for extraction
                    name = _read_utf_short(gz)
                    value = _read_utf_int(gz)
                    record[name] = value
                yield record


def _artifact_from_record(record: dict[str, str]) -> tuple[str, str, str, str | None, int | None] | None:
    uinfo = record.get("u")
    if not uinfo or "del" in record:
        return None

    parts = uinfo.split("|")
    if len(parts) < 3:
        return None

    group_id, artifact_id, version = parts[:3]
    if not group_id or not artifact_id or not version:
        return None

    packaging = None
    modified = None
    info = record.get("i")
    if info:
        info_parts = info.split("|")
        if info_parts and info_parts[0] != "NA":
            packaging = info_parts[0] or None
        if len(info_parts) > 1 and info_parts[1]:
            try:
                modified = int(info_parts[1])
            except ValueError:
                modified = None

    if packaging is None and len(parts) > 4 and parts[4] != "NA":
        packaging = parts[4] or None

    return group_id, artifact_id, version, packaging, modified


def _to_batches(artifacts: dict[tuple[str, str], dict]) -> Iterator[pa.RecordBatch]:
    rows = sorted(artifacts.items())
    for start in range(0, len(rows), BATCH_SIZE):
        chunk = rows[start : start + BATCH_SIZE]
        group_id = []
        artifact_id = []
        latest_version = []
        packaging = []
        version_count = []
        repository_id = []
        last_updated = []
        for (group, artifact), rec in chunk:
            group_id.append(group)
            artifact_id.append(artifact)
            latest_version.append(rec["latest_version"])
            packaging.append(rec["packaging"])
            version_count.append(len(rec["versions"]))
            repository_id.append("central")
            last_updated.append(rec["last_updated"])

        yield pa.RecordBatch.from_arrays(
            [
                pa.array(group_id, pa.string()),
                pa.array(artifact_id, pa.string()),
                pa.array(latest_version, pa.string()),
                pa.array(packaging, pa.string()),
                pa.array(version_count, pa.int64()),
                pa.array(repository_id, pa.string()),
                pa.array(last_updated, pa.int64()).cast(pa.timestamp("ms")),
            ],
            schema=SCHEMA,
        )


def fetch_artifacts(node_id: str) -> None:
    artifacts: dict[tuple[str, str], dict] = {}
    records_seen = 0

    for record in _iter_index_records():
        parsed = _artifact_from_record(record)
        if parsed is None:
            continue

        group_id, artifact_id, version, packaging, modified = parsed
        key = (group_id, artifact_id)
        current = artifacts.get(key)
        if current is None:
            artifacts[key] = {
                "latest_version": version,
                "packaging": packaging,
                "last_updated": modified,
                "versions": {version},
            }
        else:
            current["versions"].add(version)
            current_ts = current["last_updated"]
            if modified is not None and (current_ts is None or modified >= current_ts):
                current["latest_version"] = version
                current["packaging"] = packaging or current["packaging"]
                current["last_updated"] = modified
        records_seen += 1

    if len(artifacts) < 400_000:
        raise AssertionError(
            f"{node_id}: parsed only {len(artifacts)} artifacts from {records_seen} index records"
        )

    with raw_parquet_writer(node_id, SCHEMA) as writer:
        for batch in _to_batches(artifacts):
            writer.write_batch(batch)

    print(f"  {node_id}: wrote {len(artifacts)} artifacts from {records_seen} index records")


DOWNLOAD_SPECS = [
    NodeSpec(id="maven-central-artifacts", fn=fetch_artifacts, kind="download"),
]
