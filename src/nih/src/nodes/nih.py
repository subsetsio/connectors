"""NIH RePORTER ExPORTER connector.

Bulk grant-funding data from NIH RePORTER (Research Portfolio Online Reporting
Tools). Three published subsets, one per ExPORTER file group:

  - PROJECT      NIH/HHS award (project) records, ~46 columns.
  - ABSTRACT     project long abstracts (application_id + abstract_text).
  - PUBLICATION  publications associated with NIH-funded projects, ~15 columns.

Each group is published by the source as one zip (single CSV inside) per
fiscal/calendar year. Year is a column VALUE, not a schema split, so each group
is ONE subset. To keep memory bounded over the ~40-year, multi-GB corpus, every
year is written as its own NDJSON.gz batch asset (`nih-<group>-<year>`); the SQL
transform's dep view glob-unions the batches (`nih-<group>-*`). NDJSON is used
because the schema drifts across decades (FY1985 PROJECT is an 8-column funding
file; column-name casing varies e.g. FUNDING_ICs vs FUNDING_ICS) and DuckDB's
read_json_auto unions batch files by name, filling absent keys with NULL.

Mechanism: exporter_bulk.
  - List files:  POST /services/exporter/allFilesInfo  {"file_group": <GROUP>}
  - Download:    GET  /services/exporter/DownloadFromDocService?DocType=<dt>&KeyId=<id>
                 -> HTTP 302 -> tokenised public.era.nih.gov URL (get() follows redirects).
Each row is normalized to a canonical key set per group (so the unioned view has
a deterministic schema for every column the transform references) while any extra
upstream columns are preserved. Values are written as strings (empty -> null);
the transform casts. Stateless full re-pull each run — freshness is the maintain
step's concern.
"""

from __future__ import annotations

import csv
import io
import json
import re
import zipfile


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    post,
    raw_writer,
    transient_retry,
)

# Long free-text fields (abstracts, project terms) blow past csv's default cap.
csv.field_size_limit(10_000_000)

BASE = "https://reporter.nih.gov/services/exporter"

ENTITY_IDS = ["ABSTRACT", "PROJECT", "PUBLICATION"]

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
}


def _normalize_col(name: str) -> str:
    """Upper-case, collapse non-alphanumeric runs to single underscores.

    Unifies cross-year header drift: 'OPPORTUNITY NUMBER' -> 'OPPORTUNITY_NUMBER',
    'FUNDING_ICs' -> 'FUNDING_ICS', 'PI_NAMEs' -> 'PI_NAMES'.
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
def _download_zip(doc_type: str, key_id: str) -> bytes:
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


def _write_year(asset: str, content: bytes, canonical: list[str]) -> int:
    """Unzip the single CSV, normalize, and stream it to an NDJSON.gz batch."""
    zf = zipfile.ZipFile(io.BytesIO(content))
    names = zf.namelist()
    if not names:
        raise RuntimeError(f"{asset}: empty zip archive")
    n = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        # ExPORTER CSVs are UTF-8 (some carry a BOM, even embedded mid-field).
        # Decode UTF-8 with errors="replace" so rare non-UTF-8 bytes in legacy
        # files degrade to U+FFFD instead of silently mojibaking the whole field
        # (decoding UTF-8 as latin-1 turns every Greek letter / accent into
        # double-byte garbage).
        with zf.open(names[0]) as fh:
            text = io.TextIOWrapper(fh, encoding="utf-8-sig", errors="replace")
            reader = csv.DictReader(text)
            for raw_row in reader:
                row = {c: None for c in canonical}
                for k, v in raw_row.items():
                    if k is None:
                        continue  # extra unnamed CSV fields (restkey)
                    col = _normalize_col(k)
                    if not col:
                        continue
                    if isinstance(v, str):
                        val = v.replace("﻿", "").strip()  # drop embedded BOMs
                    else:
                        val = v
                    row[col] = val if val not in (None, "") else None
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                n += 1
    return n


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
        content = _download_zip(doc_type, key_id)
        rows = _write_year(asset, content, canonical)
        total_rows += rows
        print(f"  [{node_id}] year {year}: {rows} rows")
    print(f"  [{node_id}] {len(files)} files, {total_rows} rows total")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"nih-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# --------------------------------------------------------------------------- #
# Transforms — one published Delta table per subset.
# Raw values are strings (empty -> null); TRY_CAST guards every numeric/date cast
# so a stray legacy value never fails the whole node.
#
# Each query is prefixed with `SET arrow_large_buffer_size=true` so DuckDB exports
# Arrow large_string (64-bit offsets) when streaming to the Delta writer. Without
# it, free-text columns (abstract_text spans ~40 years) overflow the 2GB regular
# string-buffer limit inside a single record batch and the node dies with
# "maximum total string size for regular string buffers is 2147483647".
# --------------------------------------------------------------------------- #

_SET_PREAMBLE = "SET arrow_large_buffer_size=true;\n"

_PROJECT_SQL = '''
    SELECT
        TRY_CAST(APPLICATION_ID AS BIGINT)            AS application_id,
        CORE_PROJECT_NUM                              AS core_project_num,
        FULL_PROJECT_NUM                              AS full_project_num,
        SUBPROJECT_ID                                 AS subproject_id,
        TRY_CAST(FY AS INTEGER)                       AS fiscal_year,
        ACTIVITY                                      AS activity_code,
        APPLICATION_TYPE                              AS application_type,
        ADMINISTERING_IC                              AS administering_ic,
        IC_NAME                                       AS ic_name,
        FUNDING_ICS                                   AS funding_ics,
        FUNDING_MECHANISM                             AS funding_mechanism,
        ARRA_FUNDED                                   AS arra_funded,
        ASSISTANCE_LISTING_NUMBER                     AS assistance_listing_number,
        OPPORTUNITY_NUMBER                            AS opportunity_number,
        PROJECT_TITLE                                 AS project_title,
        ORG_NAME                                      AS org_name,
        ORG_CITY                                      AS org_city,
        ORG_STATE                                     AS org_state,
        ORG_COUNTRY                                   AS org_country,
        ORG_ZIPCODE                                   AS org_zipcode,
        ORG_DEPT                                      AS org_dept,
        ORG_DUNS                                      AS org_duns,
        ED_INST_TYPE                                  AS ed_inst_type,
        PI_NAMES                                      AS pi_names,
        PI_IDS                                        AS pi_ids,
        PROGRAM_OFFICER_NAME                          AS program_officer_name,
        STUDY_SECTION                                 AS study_section,
        STUDY_SECTION_NAME                            AS study_section_name,
        TRY_CAST(SUPPORT_YEAR AS INTEGER)             AS support_year,
        TRY_CAST(BUDGET_START AS DATE)                AS budget_start,
        TRY_CAST(BUDGET_END AS DATE)                  AS budget_end,
        TRY_CAST(PROJECT_START AS DATE)               AS project_start,
        TRY_CAST(PROJECT_END AS DATE)                 AS project_end,
        TRY_CAST(AWARD_NOTICE_DATE AS DATE)           AS award_notice_date,
        TRY_CAST(DIRECT_COST_AMT AS DOUBLE)           AS direct_cost_amt,
        TRY_CAST(INDIRECT_COST_AMT AS DOUBLE)         AS indirect_cost_amt,
        TRY_CAST(TOTAL_COST AS DOUBLE)                AS total_cost,
        TRY_CAST(TOTAL_COST_SUB_PROJECT AS DOUBLE)    AS total_cost_sub_project,
        PHR                                           AS public_health_relevance
    FROM "nih-project"
    WHERE APPLICATION_ID IS NOT NULL
'''

_ABSTRACT_SQL = '''
    SELECT
        TRY_CAST(APPLICATION_ID AS BIGINT) AS application_id,
        ABSTRACT_TEXT                      AS abstract_text
    FROM "nih-abstract"
    WHERE APPLICATION_ID IS NOT NULL
'''

_PUBLICATION_SQL = '''
    SELECT
        TRY_CAST(PMID AS BIGINT)     AS pmid,
        PMC_ID                       AS pmc_id,
        PUB_TITLE                    AS pub_title,
        TRY_CAST(PUB_YEAR AS INTEGER) AS pub_year,
        PUB_DATE                     AS pub_date,
        AUTHOR_LIST                  AS author_list,
        AFFILIATION                  AS affiliation,
        COUNTRY                      AS country,
        JOURNAL_TITLE                AS journal_title,
        JOURNAL_TITLE_ABBR           AS journal_title_abbr,
        JOURNAL_VOLUME               AS journal_volume,
        JOURNAL_ISSUE                AS journal_issue,
        ISSN                         AS issn,
        PAGE_NUMBER                  AS page_number,
        LANG                         AS lang
    FROM "nih-publication"
    WHERE PMID IS NOT NULL
'''

_SQL_BY_ID = {
    "nih-project": _PROJECT_SQL,
    "nih-abstract": _ABSTRACT_SQL,
    "nih-publication": _PUBLICATION_SQL,
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_SET_PREAMBLE + _SQL_BY_ID[s.id],
    )
    for s in DOWNLOAD_SPECS
]
