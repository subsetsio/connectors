"""OSV bulk export downloads.

OSV publishes a continuously updated public GCS export. The vulnerability
archive is large, so it is streamed to a temporary ZIP file and normalized to
typed Parquet batches.
"""

import json
import re
import shutil
import tempfile
import urllib.request
import zipfile
from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_parquet_writer,
    raw_asset_exists,
    record_source_signature,
    save_raw_parquet,
    source_unchanged,
)

ALL_ZIP_URL = "https://storage.googleapis.com/osv-vulnerabilities/all.zip"
ECOSYSTEMS_URL = "https://osv.dev/"
MODIFIED_IDS_URL = "https://storage.googleapis.com/osv-vulnerabilities/modified_id.csv"
USER_AGENT = "subsets-osv-connector/1.0"
BATCH_SIZE = 5000

VULNERABILITY_SCHEMA = pa.schema(
    [
        pa.field("id", pa.string()),
        pa.field("schema_version", pa.string()),
        pa.field("published", pa.timestamp("us")),
        pa.field("modified", pa.timestamp("us")),
        pa.field("withdrawn", pa.timestamp("us")),
        pa.field("source_path", pa.string()),
        pa.field("source_ecosystem", pa.string()),
        pa.field("aliases", pa.string()),
        pa.field("related", pa.string()),
        pa.field("summary", pa.string()),
        pa.field("details", pa.string()),
        pa.field("severity", pa.string()),
        pa.field("affected", pa.string()),
        pa.field("references", pa.string()),
        pa.field("credits", pa.string()),
        pa.field("database_specific", pa.string()),
    ]
)

ECOSYSTEM_SCHEMA = pa.schema(
    [
        pa.field("ecosystem", pa.string()),
        pa.field("vulnerability_count", pa.int64()),
    ]
)

MODIFIED_IDS_SCHEMA = pa.schema(
    [
        pa.field("modified", pa.timestamp("us")),
        pa.field("source_path", pa.string()),
        pa.field("source_ecosystem", pa.string()),
        pa.field("osv_id", pa.string()),
    ]
)


def _urlopen(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req, timeout=600)


def _ecosystem_from_path(path: str) -> str | None:
    if "/" not in path:
        return None
    return path.split("/", 1)[0]


def _ts(value: str | None) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    if "." in text:
        head, tail = text.split(".", 1)
        tz_pos = min([p for p in (tail.find("+"), tail.find("-")) if p >= 0] or [len(tail)])
        frac = tail[:tz_pos][:6].ljust(6, "0")
        text = f"{head}.{frac}{tail[tz_pos:]}"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


def _json_or_none(value) -> str | None:
    if value in (None, [], {}):
        return None
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _vulnerability_row(path: str, record: dict) -> dict:
    return {
        "id": record.get("id"),
        "schema_version": record.get("schema_version"),
        "published": _ts(record.get("published")),
        "modified": _ts(record.get("modified")),
        "withdrawn": _ts(record.get("withdrawn")),
        "source_path": path,
        "source_ecosystem": _ecosystem_from_path(path),
        "aliases": _json_or_none(record.get("aliases")),
        "related": _json_or_none(record.get("related")),
        "summary": record.get("summary"),
        "details": record.get("details"),
        "severity": _json_or_none(record.get("severity")),
        "affected": _json_or_none(record.get("affected")),
        "references": _json_or_none(record.get("references")),
        "credits": _json_or_none(record.get("credits")),
        "database_specific": _json_or_none(record.get("database_specific")),
    }


def _write_batch(writer, rows: list[dict], schema: pa.Schema) -> None:
    if not rows:
        return
    writer.write_table(pa.Table.from_pylist(rows, schema=schema))
    rows.clear()


def fetch_vulnerabilities(node_id: str) -> None:
    with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
        with _urlopen(ALL_ZIP_URL) as resp:
            shutil.copyfileobj(resp, tmp, length=1024 * 1024)
        tmp.flush()
        tmp.seek(0)

        rows = []
        count = 0
        with zipfile.ZipFile(tmp) as zf, raw_parquet_writer(
            node_id, VULNERABILITY_SCHEMA
        ) as writer:
            for member in zf.infolist():
                if member.is_dir() or not member.filename.endswith(".json"):
                    continue
                with zf.open(member) as src:
                    record = json.load(src)
                rows.append(_vulnerability_row(member.filename, record))
                count += 1
                if len(rows) >= BATCH_SIZE:
                    _write_batch(writer, rows, VULNERABILITY_SCHEMA)
            _write_batch(writer, rows, VULNERABILITY_SCHEMA)

    if count == 0:
        raise RuntimeError("parsed 0 vulnerability records from OSV archive")

    record_source_signature(node_id, ALL_ZIP_URL)


def fetch_ecosystems(node_id: str) -> None:
    resp = get(ECOSYSTEMS_URL, timeout=(10.0, 60.0))
    resp.raise_for_status()

    rows = []
    pattern = re.compile(
        r'<dt class="ecosystem-name">(?P<name>.*?)</dt>\s*'
        r'<dd class="ecosystem-count-wrapper">.*?'
        r'<span class="ecosystem-count"[^>]*>\s*(?P<count>[0-9,]+)',
        re.DOTALL,
    )
    for match in pattern.finditer(resp.text):
        rows.append(
            {
                "ecosystem": match.group("name").strip(),
                "vulnerability_count": int(match.group("count").replace(",", "")),
            }
        )

    if not rows:
        raise RuntimeError("failed to parse ecosystem counts from OSV landing page")

    save_raw_parquet(pa.Table.from_pylist(rows, schema=ECOSYSTEM_SCHEMA), node_id)

    record_source_signature(node_id, ECOSYSTEMS_URL, response=resp)


def fetch_modified_ids(node_id: str) -> None:
    rows = []
    count = 0
    with _urlopen(MODIFIED_IDS_URL) as resp, raw_parquet_writer(
        node_id, MODIFIED_IDS_SCHEMA
    ) as writer:
        for raw_line in resp:
            line = raw_line.decode("utf-8").strip()
            if not line:
                continue
            modified, path = line.split(",", 1)
            rows.append(
                {
                    "modified": _ts(modified),
                    "source_path": path,
                    "source_ecosystem": _ecosystem_from_path(path),
                    "osv_id": path.rsplit("/", 1)[-1],
                }
            )
            count += 1
            if len(rows) >= BATCH_SIZE:
                _write_batch(writer, rows, MODIFIED_IDS_SCHEMA)
        _write_batch(writer, rows, MODIFIED_IDS_SCHEMA)

    if count == 0:
        raise RuntimeError("parsed 0 rows from OSV modified_id.csv")

    record_source_signature(node_id, MODIFIED_IDS_URL)


DOWNLOAD_SPECS = [
    NodeSpec(id="osv-vulnerabilities", fn=fetch_vulnerabilities, kind="download"),
    NodeSpec(id="osv-ecosystems", fn=fetch_ecosystems, kind="download"),
    NodeSpec(id="osv-modified-ids", fn=fetch_modified_ids, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="osv-vulnerabilities",
        description=(
            "Continuously exported OSV bulk archive; skip when GCS "
            "ETag/Last-Modified is unchanged for all.zip."
        ),
        check=lambda aid: source_unchanged(aid, ALL_ZIP_URL)
        and raw_asset_exists(aid, "parquet"),
    ),
    MaintainSpec(
        asset_id="osv-ecosystems",
        description=(
            "OSV landing-page ecosystem counts; skip when page validators are "
            "unchanged."
        ),
        check=lambda aid: source_unchanged(aid, ECOSYSTEMS_URL)
        and raw_asset_exists(aid, "parquet"),
    ),
    MaintainSpec(
        asset_id="osv-modified-ids",
        description=(
            "Continuously exported OSV modified_id.csv; skip when GCS "
            "ETag/Last-Modified is unchanged."
        ),
        check=lambda aid: source_unchanged(aid, MODIFIED_IDS_URL)
        and raw_asset_exists(aid, "parquet"),
    ),
]
