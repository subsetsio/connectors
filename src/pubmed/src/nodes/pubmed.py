"""PubMed connector — biomedical citation corpus.

The PubMed/MEDLINE annual baseline is published as a set of gzipped XML files
(`pubmed<YY>n<NNNN>.xml.gz`) under https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/.
The 2026 release is 1,334 files, each ~5-37MB gzipped (~30k citations), ~38M+
citations total — far too large to hold in one file or finish in one run, so
this is a batched record-stream firehose: ONE entity (`citations`) whose raw is
written as one parquet batch per baseline file (`pubmed-citations-<NNNN>`).

The year prefix rotates annually (pubmed25n -> pubmed26n), so the file list and
prefix are discovered from the live directory listing each run rather than
hardcoded. State tracks the current release prefix plus the set of completed
file numbers; when the prefix changes (a new annual baseline), completed resets
and the whole corpus is re-fetched. No incremental record filter exists on the
bulk path — the corpus is re-pulled per annual release.
"""
import gzip
import io
import os
import re
import time
import xml.etree.ElementTree as ET

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    list_raw_fragments,
    save_state,
    transient_retry,
)

STATE_VERSION = 1
BASE_URL = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"
FILE_RE = re.compile(r"(pubmed\d{2}n\d{4})\.xml\.gz")

# Files fetched per invocation. The runner has no DAG_TIME_BUDGET, so the only
# continuation mechanism is a node returning True (-> exit 2 -> self-retrigger
# with the SAME RUN_ID, preserving run-scoped raw). We therefore bound each
# invocation to a batch and request continuation while files remain, rather
# than risk one ~38M-citation pass overrunning the 355-min GitHub job limit
# (which is a host SIGTERM -> run marked failed, NO retrigger). ~1,334 files /
# 250 ≈ 6 invocations.
FILES_PER_RUN = 250

# Politeness gap between file fetches. NCBI documents no hard cap on the FTP/
# HTTPS host and legacy production saw no 429s, but a small delay keeps us a
# good citizen; transient_retry still backs off any 429/5xx that does occur.
DOWNLOAD_DELAY = 0.5

SCHEMA = pa.schema([
    ("pmid", pa.string()),
    ("title", pa.string()),
    ("abstract", pa.string()),
    ("journal", pa.string()),
    ("pub_date", pa.string()),
    ("authors", pa.string()),
    ("mesh_terms", pa.string()),
])

_MONTH_MAP = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
    "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
}


@transient_retry()
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def _discover_baseline() -> tuple[str, list[int]]:
    """Return (release_prefix, sorted file numbers) from the live listing."""
    index = _fetch_text(BASE_URL)
    stems = sorted(set(FILE_RE.findall(index)))
    if not stems:
        raise AssertionError(f"no baseline files found at {BASE_URL}")
    prefixes = {s[:-4] for s in stems}  # strip the 4-digit file number
    if len(prefixes) != 1:
        raise AssertionError(f"expected one release prefix, got {sorted(prefixes)}")
    prefix = prefixes.pop()
    nums = sorted(int(s[-4:]) for s in stems)
    return prefix, nums


def _parse_date(date_elem) -> str | None:
    if date_elem is None:
        return None
    medline = date_elem.findtext("MedlineDate")
    if medline:
        parts = medline.split()
        return parts[0] if parts and len(parts[0]) == 4 and parts[0].isdigit() else medline
    year = date_elem.findtext("Year", "")
    if not year:
        return None
    month_raw = date_elem.findtext("Month", "")
    month = _MONTH_MAP.get(month_raw, month_raw.zfill(2) if month_raw.isdigit() else "")
    day = date_elem.findtext("Day", "")
    day = day.zfill(2) if day else ""
    if month and day:
        return f"{year}-{month}-{day}"
    if month:
        return f"{year}-{month}"
    return year


def _parse_articles(xml_bytes: bytes) -> list[dict]:
    """Stream-parse one baseline XML file into citation rows, clearing each
    article element after use to keep memory bounded."""
    records = []
    for _event, article in ET.iterparse(io.BytesIO(xml_bytes), events=("end",)):
        if article.tag != "PubmedArticle":
            continue
        medline = article.find("MedlineCitation")
        if medline is None:
            article.clear()
            continue
        pmid_elem = medline.find("PMID")
        article_elem = medline.find("Article")
        if pmid_elem is None or not pmid_elem.text or article_elem is None:
            article.clear()
            continue

        title_elem = article_elem.find("ArticleTitle")
        title = "".join(title_elem.itertext()).strip() if title_elem is not None else None

        abstract_parts = []
        abstract_node = article_elem.find("Abstract")
        if abstract_node is not None:
            for at in abstract_node.findall("AbstractText"):
                text = "".join(at.itertext()).strip()
                if text:
                    label = at.get("Label")
                    abstract_parts.append(f"{label}: {text}" if label else text)
        abstract = " ".join(abstract_parts) if abstract_parts else None

        journal = article_elem.findtext("Journal/Title")
        pub_date = _parse_date(article_elem.find("Journal/JournalIssue/PubDate"))

        authors = []
        for author in article_elem.findall("AuthorList/Author"):
            lastname = author.findtext("LastName", "")
            forename = author.findtext("ForeName", "")
            collective = author.findtext("CollectiveName", "")
            if lastname:
                authors.append(f"{forename} {lastname}".strip())
            elif collective:
                authors.append(collective)

        mesh_terms = [
            m.text for m in medline.findall("MeshHeadingList/MeshHeading/DescriptorName")
            if m.text
        ]

        records.append({
            "pmid": pmid_elem.text,
            "title": title,
            "abstract": abstract,
            "journal": journal,
            "pub_date": pub_date,
            "authors": "|".join(authors) if authors else None,
            "mesh_terms": "|".join(mesh_terms) if mesh_terms else None,
        })
        article.clear()

    return records


def fetch_citations(node_id: str):
    """Fetch up to FILES_PER_RUN baseline files not already present in THIS
    run's scope, writing one parquet batch per file. Returns True while files
    remain so the runner self-retriggers (same RUN_ID) to drain the rest;
    returns None on the final batch so the transform publishes the full corpus.

    Why batch + continuation rather than one loop over everything: the runner
    sets no DAG_TIME_BUDGET, so there is no in-node deadline interrupt — the
    only continuation path is a node returning True (-> exit 2 -> self-retrigger
    with the SAME RUN_ID). A single pass over all ~1,334 files risks overrunning
    the 355-min GitHub job limit, which is a host SIGTERM that marks the run
    failed with NO retrigger. Bounding each invocation makes progress monotonic
    and the wall-clock per invocation predictable.

    The authoritative "already done" set is the raw manifest's fragments
    COMMITTED under the *current* RUN_ID — the commit log, not a directory
    listing and not the globally-persisted `completed` list. Global state
    survives across distinct runs, so trusting it would make a fresh run skip
    every file; a directory listing would resurrect a failed leg's discarded
    (never-committed) writes, which the manifest-first transform cannot see.
    Each completed leg commits its fragments, so a self-retriggering chain
    (same RUN_ID) resumes precisely where it left off, while a brand-new run
    re-fetches the whole corpus. State is written too, but only as an
    observable record — never load-bearing.
    """
    prefix, nums = _discover_baseline()
    valid = set(nums)

    # Authoritative done-set: fragments committed in this run.
    run_id = os.environ.get("RUN_ID", "unknown")
    completed = set()
    for frag, meta in list_raw_fragments(node_id, "parquet").items():
        if meta.get("run_id") == run_id and frag.isdigit() and int(frag) in valid:
            completed.add(int(frag))

    def _record_state():
        save_state(node_id, {
            "schema_version": STATE_VERSION,
            "release": prefix,
            "total": len(nums),
            "completed": sorted(completed),
        })

    _record_state()

    pending = [n for n in nums if n not in completed]
    if not pending:
        print(f"{prefix}: all {len(nums)} files present — corpus complete")
        return  # None -> download done -> transform publishes the full corpus

    batch = pending[:FILES_PER_RUN]
    print(
        f"{prefix}: {len(completed)} present, fetching {len(batch)} "
        f"of {len(pending)} pending ({len(nums)} total)"
    )

    for i, n in enumerate(batch):
        filename = f"{prefix}{n:04d}.xml.gz"
        raw = _fetch_bytes(BASE_URL + filename)
        records = _parse_articles(gzip.decompress(raw))
        table = pa.Table.from_pylist(records, schema=SCHEMA)
        # write raw first — the file number is the fragment key
        save_raw_parquet(table, node_id, fragment=f"{n:04d}")
        completed.add(n)
        _record_state()                          # then advance observable state
        print(f"  {filename}: {len(records):,} citations")
        if i + 1 < len(batch):
            time.sleep(DOWNLOAD_DELAY)

    remaining = len(pending) - len(batch)
    if remaining > 0:
        print(f"{remaining} files remaining — requesting continuation")
        return True  # needs_continuation -> retrigger with same RUN_ID
    print(f"{prefix}: corpus complete ({len(completed)}/{len(nums)} files)")
    # None -> download done -> transform runs against the full run-scoped raw


DOWNLOAD_SPECS = [
    NodeSpec(id="pubmed-citations", fn=fetch_citations, kind="download"),
]
