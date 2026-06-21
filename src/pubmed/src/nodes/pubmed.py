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
import re
import xml.etree.ElementTree as ET

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    list_raw_files,
    save_state,
    transient_retry,
)

STATE_VERSION = 1
BASE_URL = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"
FILE_RE = re.compile(r"(pubmed\d{2}n\d{4})\.xml\.gz")

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


def fetch_citations(node_id: str) -> None:
    """Download every PubMed baseline file whose raw is not already present in
    THIS run's scope, writing one parquet batch per file. Loops until the whole
    baseline is drained — the supervisor bounds wall-clock by interrupting the
    node, and the per-file raw write makes resumption safe.

    Raw is run-scoped in cloud (<connector>/runs/<run_id>/raw/...), so the
    authoritative "already done" set is the raw that exists in the *current*
    run — NOT a globally-persisted `completed` list. Global state survives
    across distinct runs, so trusting it would make a fresh run skip every file
    (its raw scope starts empty), leaving the transform with no raw to read —
    exactly the failure we hit. Deriving completion from raw existence means a
    brand-new run re-fetches the whole corpus, while a self-retriggering chain
    (same RUN_ID, shared raw scope) resumes precisely where it left off. State
    is still written, but only as an observable record — never load-bearing.
    """
    prefix, nums = _discover_baseline()
    valid = set(nums)

    # Authoritative done-set: raw files already written in this run's scope.
    completed = set()
    for rel in list_raw_files(f"{node_id}-*.parquet"):
        m = re.search(r"-(\d{4})\.parquet$", rel)
        if m and int(m.group(1)) in valid:
            completed.add(int(m.group(1)))
    save_state(node_id, {
        "schema_version": STATE_VERSION,
        "release": prefix,
        "completed": sorted(completed),
    })

    pending = [n for n in nums if n not in completed]
    print(f"{prefix}: {len(completed)} present, {len(pending)} pending of {len(nums)}")

    for n in pending:
        filename = f"{prefix}{n:04d}.xml.gz"
        asset = f"{node_id}-{n:04d}"  # pure batch coordinate: the file number
        raw = _fetch_bytes(BASE_URL + filename)
        records = _parse_articles(gzip.decompress(raw))
        table = pa.Table.from_pylist(records, schema=SCHEMA)
        save_raw_parquet(table, asset)          # write raw first
        completed.add(n)
        save_state(node_id, {                    # then advance state
            "schema_version": STATE_VERSION,
            "release": prefix,
            "completed": sorted(completed),
        })
        print(f"  {filename}: {len(records):,} citations")


DOWNLOAD_SPECS = [
    NodeSpec(id="pubmed-citations", fn=fetch_citations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="pubmed-citations-transform",
        deps=["pubmed-citations"],
        sql='''
            SELECT
                pmid,
                title,
                abstract,
                journal,
                pub_date,
                TRY_CAST(regexp_extract(pub_date, '^(\\d{4})', 1) AS INTEGER) AS pub_year,
                authors,
                mesh_terms
            FROM "pubmed-citations"
            WHERE pmid IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY pmid ORDER BY pub_date DESC) = 1
        ''',
    ),
]
