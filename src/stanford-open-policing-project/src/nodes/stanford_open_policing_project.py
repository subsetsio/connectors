"""Stanford Open Policing Project raw downloads.

The source publishes one ZIP-compressed CSV per standardized location on the
project data page, backed by Stanford Stacks file URLs. Files can be large and
location schemas vary, so each download node streams its ZIP to a temporary file,
then streams CSV rows to gzip-compressed NDJSON with a few provenance columns.
Transforms type and select columns after profiling the real raw assets.
"""

from __future__ import annotations

import csv
import html
import json
import re
import tempfile
import zipfile
from pathlib import Path

import httpx

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, raw_writer, transient_retry

SLUG = "stanford-open-policing-project"
PREFIX = f"{SLUG}-"
DATA_PAGE = "https://openpolicing.stanford.edu/data/"
HEADERS = {"User-Agent": "subsets-factory/1.0"}


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
        with zf.open(member) as raw, raw_writer(
            asset, "ndjson.gz", mode="wt", compression="gzip"
        ) as out:
            text = (line.decode("utf-8-sig", errors="replace") for line in raw)
            reader = csv.DictReader(text)
            if not reader.fieldnames:
                raise RuntimeError(f"{zip_path.name}: CSV has no header")
            fieldnames = _dedupe_headers(reader.fieldnames)
            reader.fieldnames = fieldnames
            written = 0
            for row_number, row in enumerate(reader, start=1):
                rec = {
                    "_source_entity_id": entity_id,
                    "_source_file": source_file,
                    "_source_member": member,
                    "_row_number": row_number,
                }
                for key in fieldnames:
                    value = row.get(key)
                    rec[key] = value if value != "" else None
                out.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")))
                out.write("\n")
                written += 1
    return written


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
