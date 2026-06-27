"""MIT Election Lab (MEDSL) connector.

MEDSL publishes its data as datasets on Harvard Dataverse under the 'medsl'
collection. This is a heterogeneous catalog: one accepted Dataverse dataset =
one published Delta table. We fetch via the Dataverse Native + Data Access API
(the research-chosen 'dataverse_api' mechanism).

Fetch shape: stateless full re-pull (shape 1). Each refresh re-resolves the
dataset's current dataFile ids (they change across versions) and re-downloads
the data. No incremental filter exists; corpora are small-to-large single files
republished irregularly (per election cycle).

Per-dataset file handling. A dataset's latest version carries tabular data
file(s) plus codebooks/READMEs/PDFs we ignore. Some datasets split ONE logical
table across many per-state files (e.g. 51 `YYYY-XX-precinct-general.{tab,csv}`)
— those share a header and must concatenate. Other datasets bundle several
files of DIFFERENT schemas (a main returns table + a small 'sources' table, or a
county feed + a state feed). Since each dataset publishes exactly one table, we:

  1. list tabular files, peek each file's header line,
  2. group files by their (delimiter-independent) column-name signature,
  3. choose the group with the most bytes — the dataset's primary table,
  4. download every file in that group, each as its own ndjson batch.

The SQL transform unions the batches (`<asset>-*`) and publishes them. Values
are kept verbatim as strings: MEDSL tables mix true numerics (votes, year) with
zero-padded codes (state_fips, county_fips, jurisdiction_fips) where coercion
would corrupt the data, so typing is deliberately left to downstream curation.

Guestbook: the Election Returns datasets sit behind Dataverse guestbook 458; a
plain file GET returns HTTP 400/403 with a "Guestbook response required"
message. No API token is needed — POST a guestbook response to get a one-hour
signed URL, then stream that. Non-gated datasets (e.g. EPI) stream directly.
"""

from __future__ import annotations

import csv
import io
import json

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    post,
    get_client,
    raw_writer,
    transient_retry,
)
from constants import ENTITY_IDS, ENTITY_DOIS

SLUG = "mit-election-lab"
PREFIX = f"{SLUG}-"
BASE = "https://dataverse.harvard.edu/api"

# Extensions that denote a tabular data file (the publishable payload).
TABULAR_EXTS = (".csv", ".tab", ".tsv")

# Anonymous guestbook response — clears guestbook 458 (Name/Email/Institution/
# Position are all required). No account or token involved.
GUESTBOOK = {
    "guestbookResponse": {
        "name": "subsets.io",
        "email": "data@subsets.io",
        "institution": "subsets.io",
        "position": "data engineer",
    }
}

# Generous per-request timeout: precinct files reach a few GB and stream slowly.
DL_TIMEOUT = 600.0
META_TIMEOUT = 120.0


# --------------------------------------------------------------------------- #
# Dataverse API helpers
# --------------------------------------------------------------------------- #
@transient_retry()
def _list_tabular_files(doi: str) -> list[dict]:
    """Return the latest version's tabular data files: [{id,label,size}]."""
    r = get(
        f"{BASE}/datasets/:persistentId/versions/:latest/files",
        params={"persistentId": doi},
        timeout=META_TIMEOUT,
    )
    r.raise_for_status()
    out = []
    for f in r.json()["data"]:
        df = f["dataFile"]
        label = f.get("label") or df.get("filename") or ""
        if label.lower().endswith(TABULAR_EXTS):
            out.append(
                {"id": df["id"], "label": label, "size": int(df.get("filesize") or 0)}
            )
    return out


def _is_guestbook_block(resp) -> bool:
    if resp.status_code not in (400, 403):
        return False
    try:
        return "guestbook" in resp.read().decode("utf-8", "ignore").lower()
    except Exception:
        return False


@transient_retry()
def _signed_url(file_id: int) -> str:
    """Clear the guestbook and return a one-hour signed download URL."""
    r = post(f"{BASE}/access/datafile/{file_id}", json=GUESTBOOK, timeout=META_TIMEOUT)
    r.raise_for_status()
    return r.json()["data"]["signedUrl"]


def _first_line(resp) -> str:
    for line in resp.iter_lines():
        if line:
            return line
    return ""


@transient_retry()
def _peek_header(file_id: int) -> tuple[str, bool]:
    """Return (first header line, gated?) for a datafile, handling guestbook."""
    client = get_client()
    direct = f"{BASE}/access/datafile/{file_id}"
    with client.stream("GET", direct, timeout=DL_TIMEOUT) as resp:
        if not _is_guestbook_block(resp):
            resp.raise_for_status()
            return _first_line(resp), False
    url = _signed_url(file_id)
    with client.stream("GET", url, timeout=DL_TIMEOUT) as resp:
        resp.raise_for_status()
        return _first_line(resp), True


def _sniff_delim(header_line: str) -> str:
    return "\t" if header_line.count("\t") > header_line.count(",") else ","


def _signature(header_line: str, delim: str) -> tuple:
    return tuple(c.strip().strip('"').lower() for c in header_line.split(delim))


class _ByteIterStream(io.RawIOBase):
    """Adapt an httpx byte-chunk iterator into a readable binary stream so
    csv.reader (via TextIOWrapper) parses quoted fields with embedded newlines
    correctly — splitting on raw lines would corrupt them."""

    def __init__(self, chunks):
        self._chunks = chunks
        self._buf = b""

    def readable(self) -> bool:
        return True

    def readinto(self, b) -> int:
        while not self._buf:
            try:
                self._buf = next(self._chunks)
            except StopIteration:
                return 0
        n = min(len(b), len(self._buf))
        b[:n] = self._buf[:n]
        self._buf = self._buf[n:]
        return n


@transient_retry()
def _download_file_to_batch(file_id: int, delim: str, gated: bool, batch_asset: str) -> int:
    """Stream one source file → one ndjson.gz batch (string values, verbatim).
    Idempotent: a retry truncates and rewrites the batch from scratch."""
    client = get_client()
    url = _signed_url(file_id) if gated else f"{BASE}/access/datafile/{file_id}"
    n_rows = 0
    with raw_writer(batch_asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        with client.stream("GET", url, timeout=DL_TIMEOUT) as resp:
            resp.raise_for_status()
            text = io.TextIOWrapper(
                _ByteIterStream(resp.iter_bytes()), encoding="utf-8", newline=""
            )
            reader = csv.reader(text, delimiter=delim)
            try:
                header = next(reader)
            except StopIteration:
                return 0
            header = [h.strip().strip('"') for h in header]
            for row in reader:
                if not row:
                    continue
                rec = {header[i]: row[i] for i in range(min(len(header), len(row)))}
                out.write(json.dumps(rec, ensure_ascii=False))
                out.write("\n")
                n_rows += 1
    return n_rows


# --------------------------------------------------------------------------- #
# Fetch
# --------------------------------------------------------------------------- #
def fetch_one(node_id: str) -> None:
    eid = node_id[len(PREFIX):] if node_id.startswith(PREFIX) else node_id
    doi = ENTITY_DOIS[eid]

    files = _list_tabular_files(doi)
    if not files:
        raise ValueError(f"{node_id}: dataset {doi} has no tabular data files")

    # Group files by header signature; each file keeps its own delimiter
    # (a single logical table can ship as .csv (comma) AND .tab (tab) per state).
    groups: dict[tuple, dict] = {}
    for f in files:
        line, gated = _peek_header(f["id"])
        if not line:
            continue
        delim = _sniff_delim(line)
        sig = _signature(line, delim)
        g = groups.setdefault(sig, {"bytes": 0, "files": []})
        g["bytes"] += f["size"]
        g["files"].append({**f, "delim": delim, "gated": gated})

    if not groups:
        raise ValueError(f"{node_id}: no readable headers among {len(files)} files")

    chosen = max(groups.values(), key=lambda g: (g["bytes"], len(g["files"])))
    chosen["files"].sort(key=lambda f: f["label"])

    total = 0
    for i, f in enumerate(chosen["files"]):
        batch = f"{node_id}-{i:04d}"
        total += _download_file_to_batch(f["id"], f["delim"], f["gated"], batch)
    print(f"  {node_id}: wrote {total} rows from {len(chosen['files'])} file(s)")
    if total == 0:
        raise ValueError(f"{node_id}: all source files were empty")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published table per subset: pass the unioned raw rows through verbatim.
# The transform is the correctness gate (it fails on 0 rows / unreadable raw);
# typing is intentionally deferred (see module docstring).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
