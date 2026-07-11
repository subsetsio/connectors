"""NIH RePORTER ExPORTER connector — downloads only.

Bulk grant-funding data from NIH RePORTER (Research Portfolio Online Reporting
Tools). Six published subsets, one per ExPORTER file group:

  - PROJECT       NIH/HHS award (project) records, ~46 columns.
  - ABSTRACT      project long abstracts (application_id + abstract_text).
  - PUBLICATION   publications associated with NIH-funded projects, ~15 columns.
  - LINK          publication-to-project link table (pmid + project_number).
  - PATENT        patents citing NIH support (patent_id, title, project, org).
  - CLINICALSTUDY ClinicalTrials.gov studies linked to NIH projects.

Two fetch shapes, both landing normalized NDJSON.gz raw:

  * Yearly groups (PROJECT, ABSTRACT, PUBLICATION, LINK) — the source publishes
    one zip (single CSV inside) per fiscal/calendar year. Year is a column
    VALUE, not a schema split, so each group is ONE subset. To keep memory
    bounded over the ~40-year, multi-GB corpus, every year is written as its
    own NDJSON.gz batch asset (`nih-<group>-<year>`); the transform's dep view
    glob-unions the batches. Enumerated via `POST allFilesInfo`.

  * Single all-years groups (PATENT, CLINICALSTUDY) — the source serves one
    CSV covering all years, streamed directly (NOT zipped) from a fixed
    DocType/KeyId. Written as one NDJSON.gz asset named exactly after the spec.

NDJSON is used because the schema drifts across decades (FY1985 PROJECT is an
8-column funding file; column-name casing varies e.g. FUNDING_ICs vs
FUNDING_ICS) and DuckDB's read_json_auto unions batch files by name, filling
absent keys with NULL. Each row is normalized to a canonical key set per group
(so the unioned view has a deterministic schema for every column the transform
references) while any extra upstream columns are preserved. Values are written
as strings (empty -> null); the transform casts. Stateless full re-pull each
run — freshness is the maintain step's concern.

Mechanism: exporter_bulk.
  - List files:  POST /services/exporter/allFilesInfo  {"file_group": <GROUP>}
  - Download:    GET  /services/exporter/DownloadFromDocService?DocType=<dt>&KeyId=<id>
                 -> HTTP 302 -> tokenised public.era.nih.gov URL (get() follows redirects).
                 Yearly groups redirect to a zip; single-file groups to a raw CSV.

Transforms are authored at the MODEL stage as compiled file pairs under
src/transforms/ — NOT here (module-level TRANSFORM_SPECS is retired).
"""

from __future__ import annotations

import csv
import io
import json
import re
import zipfile


from subsets_utils import (
    NodeSpec,
    get,
    post,
    raw_writer,
    transient_retry,
)

# Long free-text fields (abstracts, project terms) blow past csv's default cap.
csv.field_size_limit(10_000_000)

BASE = "https://reporter.nih.gov/services/exporter"

# Yearly (one-zip-per-year) groups — enumerated via allFilesInfo, fetched by fetch_one.
YEARLY_ENTITY_IDS = ["ABSTRACT", "PROJECT", "PUBLICATION", "LINK"]

# Single all-years groups — one raw CSV each at a fixed DocType/KeyId (getGroupDetails
# returns only a size summary, so the handle is hardcoded per research). The response
# is a bare CSV stream (content-type text/csv), NOT a zip.
SINGLE_FILES = {
    "nih-patent": {"group": "PATENT", "doc_type": "EXPPAT", "key_id": "1"},
    "nih-clinicalstudy": {"group": "CLINICALSTUDY", "doc_type": "EXPCS", "key_id": "1"},
}

# Characters that `str.splitlines()` treats as line boundaries but
# `json.dumps(ensure_ascii=False)` leaves RAW in the output (they are >= 0x20, so
# the JSON encoder does not escape them). Left in place they split one NDJSON
# record across physical lines, so the canonical Python reader
# (`load_raw_ndjson`, which does `text.splitlines()`) fails with "Unterminated
# string" mid-abstract. DuckDB's read_json_auto only splits on \n and is
# unaffected, but the raw must be safe for BOTH readers — normalize them to a
# space in every string value. (\v \f \x1c-\x1e and \r are < 0x20 and already
# escaped by json.dumps, so they need no handling here.)
_LINE_SEPARATORS = str.maketrans({" ": " ", " ": " ", "": " "})

# Canonical (modern) column set per group, normalized (upper, underscores). Every
# emitted row carries exactly these keys (missing -> null) PLUS any extra columns
# a given year's file happens to have. Guaranteeing presence makes the DuckDB
# view schema deterministic for every column the transform selects, independent
# of read_json_auto's file sampling.
_CANONICAL = {
    "PROJECT": [
        "APPLICATION_ID", "ACTIVITY", "ADMINISTERING_IC", "APPLICATION_TYPE",
        "ARRA_FUNDED", "AWARD_NOTICE_DATE", "BUDGET_START", "BUDGET_END",
        "ASSISTANCE_LISTING_NUMBER", "CORE_PROJECT_NUM", "ED_INST_TYPE",
        "OPPORTUNITY_NUMBER", "FULL_PROJECT_NUM", "FUNDING_ICS",
        "FUNDING_MECHANISM", "FY", "IC_NAME", "NIH_SPENDING_CATS", "ORG_CITY",
        "ORG_COUNTRY", "ORG_DEPT", "ORG_DISTRICT", "ORG_DUNS", "ORG_FIPS",
        "ORG_IPF_CODE", "ORG_NAME", "ORG_STATE", "ORG_ZIPCODE", "PHR", "PI_IDS",
        "PI_NAMES", "PROGRAM_OFFICER_NAME", "PROJECT_START", "PROJECT_END",
        "PROJECT_TERMS", "PROJECT_TITLE", "SERIAL_NUMBER", "STUDY_SECTION",
        "STUDY_SECTION_NAME", "SUBPROJECT_ID", "SUFFIX", "SUPPORT_YEAR",
        "DIRECT_COST_AMT", "INDIRECT_COST_AMT", "TOTAL_COST",
        "TOTAL_COST_SUB_PROJECT",
    ],
    "ABSTRACT": ["APPLICATION_ID", "ABSTRACT_TEXT"],
    "PUBLICATION": [
        "AFFILIATION", "AUTHOR_LIST", "COUNTRY", "ISSN", "JOURNAL_ISSUE",
        "JOURNAL_TITLE", "JOURNAL_TITLE_ABBR", "JOURNAL_VOLUME", "LANG",
        "PAGE_NUMBER", "PMC_ID", "PMID", "PUB_DATE", "PUB_TITLE", "PUB_YEAR",
    ],
    "LINK": ["PMID", "PROJECT_NUMBER"],
    "PATENT": ["PATENT_ID", "PATENT_TITLE", "PROJECT_ID", "PATENT_ORG_NAME"],
    "CLINICALSTUDY": [
        "CORE_PROJECT_NUMBER", "CLINICALTRIALS_GOV_ID", "STUDY", "STUDY_STATUS",
    ],
}


def _normalize_col(name: str) -> str:
    """Upper-case, collapse non-alphanumeric runs to single underscores.

    Unifies cross-year header drift: 'OPPORTUNITY NUMBER' -> 'OPPORTUNITY_NUMBER',
    'FUNDING_ICs' -> 'FUNDING_ICS', 'PI_NAMEs' -> 'PI_NAMES',
    'ClinicalTrials.gov ID' -> 'CLINICALTRIALS_GOV_ID'.
    """
    return re.sub(r"[^0-9A-Z]+", "_", name.strip().upper()).strip("_")


@transient_retry()
def _list_files(group: str) -> list[dict]:
    resp = post(f"{BASE}/allFilesInfo", json={"file_group": group}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    files = resp.json()
    if not isinstance(files, list) or not files:
        raise RuntimeError(f"allFilesInfo returned no files for group {group!r}")
    return files


@transient_retry()
def _download_doc(doc_type: str, key_id: str) -> bytes:
    # 302-redirects to a tokenised public.era.nih.gov URL; get() follows redirects.
    resp = get(
        f"{BASE}/DownloadFromDocService",
        params={"DocType": doc_type, "KeyId": str(key_id)},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    content = resp.content
    if not content:
        raise RuntimeError(f"empty download for DocType={doc_type} KeyId={key_id}")
    return content


def _stream_rows(asset: str, reader: csv.DictReader, canonical: list[str]) -> int:
    """Normalize each CSV row to the canonical key set and stream to NDJSON.gz."""
    n = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for raw_row in reader:
            row = {c: None for c in canonical}
            for k, v in raw_row.items():
                if k is None:
                    continue  # extra unnamed CSV fields (restkey)
                col = _normalize_col(k)
                if not col:
                    continue
                if isinstance(v, str):
                    val = v.replace("﻿", "").translate(_LINE_SEPARATORS).strip()  # drop embedded BOMs + normalize stray line separators
                else:
                    val = v
                row[col] = val if val not in (None, "") else None
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def _write_year(asset: str, content: bytes, canonical: list[str]) -> int:
    """Unzip the single CSV, normalize, and stream it to an NDJSON.gz batch."""
    zf = zipfile.ZipFile(io.BytesIO(content))
    names = zf.namelist()
    if not names:
        raise RuntimeError(f"{asset}: empty zip archive")
    # ExPORTER CSVs are UTF-8 (some carry a BOM, even embedded mid-field). Decode
    # UTF-8 with errors="replace" so rare non-UTF-8 bytes in legacy files degrade
    # to U+FFFD instead of silently mojibaking the whole field (decoding UTF-8 as
    # latin-1 turns every Greek letter / accent into double-byte garbage).
    with zf.open(names[0]) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8-sig", errors="replace")
        return _stream_rows(asset, csv.DictReader(text), canonical)


def _write_csv(asset: str, content: bytes, canonical: list[str]) -> int:
    """Normalize a bare (non-zipped) CSV byte stream to a single NDJSON.gz asset."""
    text = io.TextIOWrapper(io.BytesIO(content), encoding="utf-8-sig", errors="replace")
    return _stream_rows(asset, csv.DictReader(text), canonical)


def fetch_one(node_id: str) -> None:
    """Fetch every yearly file for one ExPORTER group, one NDJSON.gz batch/year.

    The runtime passes the spec id (e.g. 'nih-project'); the group is recovered
    from it. Batch asset ids are 'nih-<group>-<year>' so the transform view
    glob-unions them.
    """
    group = node_id[len("nih-"):].upper()
    canonical = _CANONICAL[group]
    files = _list_files(group)

    total_rows = 0
    for f in files:
        doc_type = f["doc_type_code"]
        key_id = f.get("doc_key_id") or f.get("fy")
        year = f.get("fy") or f.get("doc_key_id")
        if doc_type is None or key_id is None or year is None:
            raise RuntimeError(f"{node_id}: incomplete file record {f}")
        asset = f"{node_id}-{year}"
        content = _download_doc(doc_type, key_id)
        rows = _write_year(asset, content, canonical)
        total_rows += rows
        print(f"  [{node_id}] year {year}: {rows} rows")
    print(f"  [{node_id}] {len(files)} files, {total_rows} rows total")


def fetch_single(node_id: str) -> None:
    """Fetch one all-years ExPORTER group served as a bare CSV (PATENT, CLINICALSTUDY).

    Written as one NDJSON.gz asset named exactly after the spec id.
    """
    meta = SINGLE_FILES[node_id]
    canonical = _CANONICAL[meta["group"]]
    content = _download_doc(meta["doc_type"], meta["key_id"])
    rows = _write_csv(node_id, content, canonical)
    print(f"  [{node_id}] all-years file: {rows} rows")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"nih-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in YEARLY_ENTITY_IDS
] + [
    NodeSpec(id=node_id, fn=fetch_single, kind="download")
    for node_id in SINGLE_FILES
]
