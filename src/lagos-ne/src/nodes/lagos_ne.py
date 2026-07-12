"""LAGOS-NE lake water clarity connector (EDI package edi.101, LAGOS-NE-LIMNO).

Source: Environmental Data Initiative PASTA+ REST API
(https://pasta.lternet.edu/package). The package is LAGOS-NE-LIMNO -- in-situ
measurements of lake water quality (Secchi clarity, chlorophyll, nutrients) plus
a lake identifier/morphometry reference table, for thousands of US lakes.

Fetch shape: stateless full re-pull (shape 1). Each EDI revision is immutable, so
there is no incremental delta to chase -- every run resolves the latest revision,
finds each target dataTable's data-object hash from the EML, downloads the full
CSV in one request, and overwrites raw. The data-object hashes change across
revisions, so they are resolved at fetch time from the EML (never hardcoded);
only the package scope/identifier (edi/101) and the table entityName are stable.

Raw format: parquet via pyarrow's CSV reader. These are single immutable
snapshots (one full table per revision, never batched), the CSVs are clean and
well-typed, and "NA"/"" are the only missing-value tokens -- so pyarrow's type
inference (with those tokens declared null) is deterministic and correct here,
giving int64 ids, date32 sampledate, and double measurements without a 92-column
hand-written schema. The transform then re-asserts types via the test specs.
"""

import io
import re
import xml.etree.ElementTree as ET

import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

SLUG = "lagos-ne"
BASE = "https://pasta.lternet.edu/package"
SCOPE_ID = "edi/101"  # EDI scope=edi identifier=101 == LAGOS-NE-LIMNO

# Published subsets (the rank-accepted entity union). Each is the slug of a
# dataTable entityName in the EDI EML; the download fn maps it to that revision's
# data-object hash at fetch time.
PROGRAMS = f"{SLUG}-data-source-and-program-information"
MEAS = f"{SLUG}-in-situ-measurements-of-epilimnetic-nutrients-and-secchi-data"
MORPH = f"{SLUG}-lake-identifiers-and-morphometry"


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _slug(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"\.[a-z0-9]+$", "", s)          # drop trailing extension
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


@transient_retry()
def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _latest_revision() -> int:
    body = _get_text(f"{BASE}/eml/{SCOPE_ID}")
    revs = [int(line.strip()) for line in body.splitlines() if line.strip().isdigit()]
    if not revs:
        raise AssertionError(f"no revisions returned for {SCOPE_ID}: {body!r}")
    return max(revs)


def _entity_hash_map(rev: int) -> dict:
    """Map slug(entityName) -> data-object hash for every dataTable in the EML."""
    xml = _get_bytes(f"{BASE}/metadata/eml/{SCOPE_ID}/{rev}")
    root = ET.fromstring(xml)
    out = {}
    for dt in root.iter():
        if _local(dt.tag) != "dataTable":
            continue
        name = None
        for c in dt:
            if _local(c.tag) == "entityName":
                name = (c.text or "").strip()
                break
        url = None
        for e in dt.iter():
            if _local(e.tag) == "url" and e.text and "/data/eml/" in e.text:
                url = e.text.strip()
                break
        if name and url:
            out[_slug(name)] = url.rsplit("/", 1)[-1]
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id                       # spec id IS the asset name
    entity = node_id[len(SLUG) + 1:]      # strip "lagos-ne-" prefix
    rev = _latest_revision()
    hashes = _entity_hash_map(rev)
    if entity not in hashes:
        raise AssertionError(
            f"entity {entity!r} not found among dataTables of {SCOPE_ID}/{rev}; "
            f"available: {sorted(hashes)}"
        )
    content = _get_bytes(f"{BASE}/data/eml/{SCOPE_ID}/{rev}/{hashes[entity]}")
    convert = pacsv.ConvertOptions(null_values=["NA", ""], strings_can_be_null=True)
    table = pacsv.read_csv(io.BytesIO(content), convert_options=convert)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=PROGRAMS, fn=fetch_one, kind="download"),
    NodeSpec(id=MEAS, fn=fetch_one, kind="download"),
    NodeSpec(id=MORPH, fn=fetch_one, kind="download"),
]
