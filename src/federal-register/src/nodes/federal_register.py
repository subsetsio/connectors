"""Federal Register connector — REST API (https://www.federalregister.gov/api/v1).

Two published subsets:

- `federal-register-documents` — the full Federal Register document corpus
  (Rules, Proposed Rules, Notices, Presidential Documents, Corrections, Sunshine
  Act Documents), coverage 1994-present, ~25-30k documents/year. Fetched as a
  record-stream firehose: ONE parquet batch per publication YEAR
  (`federal-register-documents-{year}`). The API caps any single query window at
  10,000 results, and a full year exceeds that, so each year is fetched by
  iterating its 12 months (each ~2-3k docs) and accumulating into the year batch.
  State carries the highest fully-closed year already pulled; the current year is
  re-pulled every run to pick up new daily publications.

- `federal-register-agencies` — the ~470-record agency reference taxonomy
  (joinable to documents via agency id), returned in full from /agencies.json in
  a single request.

No auth. No documented rate limit; the site sits behind Cloudflare so requests
go through subsets_utils.get (descriptive ASCII User-Agent) with transient retry.
"""

import calendar
from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    load_state,
    save_state,
)

BASE = "https://www.federalregister.gov/api/v1"
STATE_VERSION = 1
SOURCE_MIN_YEAR = 1994          # FR API coverage begins 1994
PER_PAGE = 1000                 # max page size (verified)
WINDOW_CAP = 10000              # API hard cap on a single query window
MAX_PAGES_PER_MONTH = 40        # safety ceiling; ~3 pages expected per month

DOC_FIELDS = [
    "document_number", "type", "subtype", "title", "abstract",
    "publication_date", "signing_date", "citation",
    "start_page", "end_page", "page_length", "agencies", "president",
    "html_url", "pdf_url",
]

DOC_SCHEMA = pa.schema([
    ("document_number", pa.string()),
    ("type", pa.string()),
    ("subtype", pa.string()),
    ("title", pa.string()),
    ("abstract", pa.string()),
    ("publication_date", pa.string()),     # ISO YYYY-MM-DD; cast to DATE in transform
    ("signing_date", pa.string()),
    ("citation", pa.string()),
    ("start_page", pa.int64()),
    ("end_page", pa.int64()),
    ("page_length", pa.int64()),
    ("president_name", pa.string()),
    ("president_id", pa.string()),
    ("primary_agency_id", pa.int64()),
    ("primary_agency_name", pa.string()),
    ("agency_ids", pa.list_(pa.int64())),
    ("agency_names", pa.list_(pa.string())),
    ("html_url", pa.string()),
    ("pdf_url", pa.string()),
])

AGENCY_SCHEMA = pa.schema([
    ("id", pa.int64()),
    ("name", pa.string()),
    ("short_name", pa.string()),
    ("slug", pa.string()),
    ("description", pa.string()),
    ("parent_id", pa.int64()),
    ("agency_url", pa.string()),
    ("child_count", pa.int64()),
])


@transient_retry()
def _get_json(url, params=None):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _doc_row(doc: dict) -> dict:
    agencies = doc.get("agencies") or []
    agency_ids = [a.get("id") for a in agencies if a.get("id") is not None]
    agency_names = [a.get("name") for a in agencies if a.get("name")]
    president = doc.get("president") or {}
    return {
        "document_number": doc.get("document_number"),
        "type": doc.get("type"),
        "subtype": doc.get("subtype"),
        "title": doc.get("title"),
        "abstract": doc.get("abstract"),
        "publication_date": doc.get("publication_date"),
        "signing_date": doc.get("signing_date"),
        "citation": doc.get("citation"),
        "start_page": doc.get("start_page"),
        "end_page": doc.get("end_page"),
        "page_length": doc.get("page_length"),
        "president_name": president.get("name"),
        "president_id": president.get("identifier"),
        "primary_agency_id": agency_ids[0] if agency_ids else None,
        "primary_agency_name": agency_names[0] if agency_names else None,
        "agency_ids": agency_ids,
        "agency_names": agency_names,
        "html_url": doc.get("html_url"),
        "pdf_url": doc.get("pdf_url"),
    }


def _fetch_month(year: int, month: int) -> list[dict]:
    """All documents published in one calendar month. Page-paginates by
    following next_page_url (keyset cursor embedded) until exhausted. A month
    holds ~2-3k docs, comfortably under the 10k window cap."""
    last_day = calendar.monthrange(year, month)[1]
    params = [
        ("conditions[publication_date][gte]", f"{year}-{month:02d}-01"),
        ("conditions[publication_date][lte]", f"{year}-{month:02d}-{last_day:02d}"),
        ("per_page", str(PER_PAGE)),
        ("order", "oldest"),
    ] + [("fields[]", f) for f in DOC_FIELDS]

    data = _get_json(f"{BASE}/documents.json", params=params)
    reported = data.get("count") or 0
    if reported >= WINDOW_CAP:
        # Monthly windowing is no longer fine-grained enough — refuse rather
        # than silently truncate at the 10k window cap.
        raise RuntimeError(
            f"{year}-{month:02d}: reported count {reported} >= window cap "
            f"{WINDOW_CAP}; need sub-monthly windowing"
        )

    rows: list[dict] = []
    pages = 0
    while True:
        results = data.get("results") or []
        rows.extend(results)
        pages += 1
        next_url = data.get("next_page_url")
        if not next_url or not results:
            break
        if pages > MAX_PAGES_PER_MONTH:
            raise RuntimeError(
                f"{year}-{month:02d}: exceeded {MAX_PAGES_PER_MONTH} pages "
                "(source grew unexpectedly)"
            )
        data = _get_json(next_url)
    return rows


def fetch_documents(node_id: str) -> None:
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    watermark_year = state.get("watermark_year")  # highest CLOSED year done
    current_year = datetime.now(tz=timezone.utc).year
    start_year = (watermark_year + 1) if watermark_year else SOURCE_MIN_YEAR

    for year in range(start_year, current_year + 1):
        rows: list[dict] = []
        for month in range(1, 13):
            rows.extend(_fetch_month(year, month))
        table = pa.Table.from_pylist([_doc_row(d) for d in rows], schema=DOC_SCHEMA)
        save_raw_parquet(table, f"{node_id}-{year}")          # raw FIRST
        if year < current_year:
            # Closed year is immutable — advance the watermark so we never
            # re-pull it. The current (open) year is intentionally NOT recorded,
            # so every run re-fetches it to capture new daily publications.
            save_state(node_id, {
                "schema_version": STATE_VERSION,
                "watermark_year": year,
            })


def fetch_agencies(node_id: str) -> None:
    agencies = _get_json(f"{BASE}/agencies.json")
    rows = [{
        "id": a.get("id"),
        "name": a.get("name"),
        "short_name": a.get("short_name"),
        "slug": a.get("slug"),
        "description": a.get("description"),
        "parent_id": a.get("parent_id"),
        "agency_url": a.get("agency_url"),
        "child_count": len(a.get("child_ids") or []),
    } for a in agencies]
    table = pa.Table.from_pylist(rows, schema=AGENCY_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="federal-register-documents", fn=fetch_documents, kind="download"),
    NodeSpec(id="federal-register-agencies", fn=fetch_agencies, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="federal-register-documents-transform",
        deps=["federal-register-documents"],
        sql='''
            SELECT
                document_number,
                type,
                subtype,
                title,
                abstract,
                CAST(publication_date AS DATE)  AS publication_date,
                TRY_CAST(signing_date AS DATE)  AS signing_date,
                citation,
                start_page,
                end_page,
                page_length,
                president_name,
                president_id,
                primary_agency_id,
                primary_agency_name,
                agency_ids,
                agency_names,
                html_url,
                pdf_url
            FROM "federal-register-documents"
            WHERE document_number IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY document_number ORDER BY publication_date
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="federal-register-agencies-transform",
        deps=["federal-register-agencies"],
        sql='''
            SELECT
                CAST(id AS BIGINT)         AS id,
                name,
                short_name,
                slug,
                description,
                CAST(parent_id AS BIGINT)  AS parent_id,
                agency_url,
                child_count
            FROM "federal-register-agencies"
            WHERE id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY id ORDER BY slug) = 1
        ''',
    ),
]
