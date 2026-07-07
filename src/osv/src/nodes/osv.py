"""OSV bulk export downloads.

OSV publishes a continuously updated public GCS export. The vulnerability
archive is large, so it is streamed to a temporary ZIP file and normalized to
gzip NDJSON one record at a time.
"""

import json
import re
import shutil
import tempfile
import urllib.request
import zipfile

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    raw_writer,
    record_source_signature,
    source_unchanged,
)

ALL_ZIP_URL = "https://storage.googleapis.com/osv-vulnerabilities/all.zip"
ECOSYSTEMS_URL = "https://osv.dev/"
MODIFIED_IDS_URL = "https://storage.googleapis.com/osv-vulnerabilities/modified_id.csv"
USER_AGENT = "subsets-osv-connector/1.0"


def _urlopen(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req, timeout=600)


def _write_json_line(out, row: dict) -> None:
    out.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def _ecosystem_from_path(path: str) -> str | None:
    if "/" not in path:
        return None
    return path.split("/", 1)[0]


def fetch_vulnerabilities(node_id: str) -> None:
    with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
        with _urlopen(ALL_ZIP_URL) as resp:
            shutil.copyfileobj(resp, tmp, length=1024 * 1024)
        tmp.flush()
        tmp.seek(0)

        with zipfile.ZipFile(tmp) as zf, raw_writer(
            node_id, "ndjson.gz", mode="wt", compression="gzip"
        ) as out:
            for member in zf.infolist():
                if member.is_dir() or not member.filename.endswith(".json"):
                    continue
                with zf.open(member) as src:
                    record = json.load(src)
                record["_source_path"] = member.filename
                record["_source_ecosystem"] = _ecosystem_from_path(member.filename)
                _write_json_line(out, record)

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

    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as out:
        for row in rows:
            _write_json_line(out, row)

    record_source_signature(node_id, ECOSYSTEMS_URL, response=resp)


def fetch_modified_ids(node_id: str) -> None:
    with _urlopen(MODIFIED_IDS_URL) as resp, raw_writer(
        node_id, "ndjson.gz", mode="wt", compression="gzip"
    ) as out:
        for raw_line in resp:
            line = raw_line.decode("utf-8").strip()
            if not line:
                continue
            modified, path = line.split(",", 1)
            row = {
                "modified": modified,
                "source_path": path,
                "source_ecosystem": _ecosystem_from_path(path),
                "osv_id": path.rsplit("/", 1)[-1],
            }
            _write_json_line(out, row)

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
        and raw_asset_exists(aid, "ndjson.gz"),
    ),
    MaintainSpec(
        asset_id="osv-ecosystems",
        description=(
            "OSV landing-page ecosystem counts; skip when page validators are "
            "unchanged."
        ),
        check=lambda aid: source_unchanged(aid, ECOSYSTEMS_URL)
        and raw_asset_exists(aid, "ndjson.gz"),
    ),
    MaintainSpec(
        asset_id="osv-modified-ids",
        description=(
            "Continuously exported OSV modified_id.csv; skip when GCS "
            "ETag/Last-Modified is unchanged."
        ),
        check=lambda aid: source_unchanged(aid, MODIFIED_IDS_URL)
        and raw_asset_exists(aid, "ndjson.gz"),
    ),
]
