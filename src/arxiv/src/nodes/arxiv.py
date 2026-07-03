"""arXiv connector — full paper-metadata corpus from the public GCS snapshot.

Mechanism: the whole-corpus arXiv metadata snapshot published anonymously in the
free, requester-pays-free Google Cloud Storage bucket `gs://arxiv-dataset`
(`metadata-v5/arxiv-metadata-oai.json`). This is the backing store of the
Kaggle `Cornell-University/arxiv` dataset: one JSON object per line, one line per
paper, covering the full corpus (~1.7M papers, arXiv id 0704.* onward plus the
pre-2007 archive/YYMMNNN ids back to 1991).

Why not OAI-PMH (the research-preferred path)? arXiv's OAI endpoint
(`oaipmh.arxiv.org`) sits behind a CDN that returns a hard `406 Not Acceptable`
to requests from datacenter IP ranges — every GitHub Actions runner. Verified:
the identical httpx client returns 200 from a residential IP and 406 from CI, so
no header/UA/retry change can unblock it. The Kaggle API (fresh weekly snapshot)
needs an auth token we don't have. The GCS snapshot is the only anonymous,
cloud-runnable, whole-corpus metadata source. Its limitation is freshness: the
public mirror is frozen at the 2020-08 snapshot, so coverage ends mid-2020.

Shape: single static file. There is no incremental window — every run streams
the whole snapshot and rewrites the raw parquet batches idempotently (same input
→ same deterministic batch ids), then the transform publishes one deduped table.

The snapshot carries no date fields (its `versions` are bare strings), so the
submission month is derived from the arXiv id, which deterministically encodes
YYMM (new-style `YYMM.NNNNN`; old-style `archive/YYMMNNN`).
"""
from __future__ import annotations

import json

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get_client, save_raw_parquet

# Anonymous, public, free (not requester-pays) HTTPS read of the GCS object.
SNAPSHOT_URL = (
    "https://storage.googleapis.com/arxiv-dataset/metadata-v5/arxiv-metadata-oai.json"
)

# Rows buffered before each parquet flush. ~1.7M rows / 100k ≈ 17 batches; keeps
# peak memory bounded (abstracts dominate, ~1-2 KB/row).
BATCH_ROWS = 100_000

# If more than this fraction of lines fail to parse, the download is corrupt —
# raise rather than publish a truncated corpus.
MAX_BAD_FRACTION = 0.01

SCHEMA = pa.schema(
    [
        ("arxiv_id", pa.string()),
        ("title", pa.string()),
        ("abstract", pa.string()),
        ("authors", pa.string()),
        ("submitter", pa.string()),
        ("primary_category", pa.string()),
        ("categories", pa.string()),
        ("doi", pa.string()),
        ("journal_ref", pa.string()),
        ("report_no", pa.string()),
        ("comments", pa.string()),
        ("num_versions", pa.int32()),
        ("created_date", pa.string()),
    ]
)


def _clean(val) -> str | None:
    if val is None:
        return None
    s = str(val).strip()
    return s or None


def _created_date(arxiv_id: str | None) -> str | None:
    """Month-granular submission date derived from the arXiv id.

    New-style ids are `YYMM.NNNNN` (April 2007 onward); old-style ids are
    `archive[.subclass]/YYMMNNN`. Both put the YYMM right after the optional
    `archive/` prefix. YY >= 91 maps to the 1900s (arXiv began 1991), else 2000s.
    """
    if not arxiv_id:
        return None
    tail = arxiv_id.split("/", 1)[1] if "/" in arxiv_id else arxiv_id
    token = tail.split(".", 1)[0][:4]
    if len(token) != 4 or not token.isdigit():
        return None
    yy, mm = int(token[:2]), int(token[2:])
    if not 1 <= mm <= 12:
        return None
    year = 1900 + yy if yy >= 91 else 2000 + yy
    return f"{year:04d}-{mm:02d}-01"


def _row(rec: dict) -> dict:
    cats = rec.get("categories")
    if isinstance(cats, list):
        cats = " ".join(c for c in cats if c)
    cats = _clean(cats)
    primary = cats.split()[0] if cats else None
    versions = rec.get("versions")
    arxiv_id = _clean(rec.get("id"))
    return {
        "arxiv_id": arxiv_id,
        "title": _clean(rec.get("title")),
        "abstract": _clean(rec.get("abstract")),
        "authors": _clean(rec.get("authors")),
        "submitter": _clean(rec.get("submitter")),
        "primary_category": primary,
        "categories": cats,
        "doi": _clean(rec.get("doi")),
        "journal_ref": _clean(rec.get("journal-ref")),
        "report_no": _clean(rec.get("report-no")),
        "comments": _clean(rec.get("comments")),
        "num_versions": len(versions) if isinstance(versions, list) else None,
        "created_date": _created_date(arxiv_id),
    }


def _flush(rows: list[dict], asset_base: str, batch_idx: int) -> None:
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, f"{asset_base}-{batch_idx:04d}")


def fetch_papers(node_id: str) -> None:
    asset_base = node_id  # "arxiv-papers" — also the view the transform reads
    client = get_client()

    rows: list[dict] = []
    batch_idx = 0
    seen = 0
    bad = 0

    with client.stream("GET", SNAPSHOT_URL, timeout=(30.0, 600.0)) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line or not line.strip():
                continue
            seen += 1
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            rows.append(_row(rec))
            if len(rows) >= BATCH_ROWS:
                _flush(rows, asset_base, batch_idx)
                batch_idx += 1
                rows = []

    if rows:
        _flush(rows, asset_base, batch_idx)
        batch_idx += 1

    if seen == 0:
        raise RuntimeError("arxiv: snapshot stream yielded no lines")
    if bad > seen * MAX_BAD_FRACTION:
        raise RuntimeError(
            f"arxiv: {bad}/{seen} lines failed to parse (> {MAX_BAD_FRACTION:.0%}) "
            "— snapshot likely truncated or corrupt"
        )
    print(f"  arxiv: streamed {seen:,} lines, {bad} bad, {batch_idx} batch(es)")


DOWNLOAD_SPECS = [
    NodeSpec(id="arxiv-papers", fn=fetch_papers, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="arxiv-papers-transform",
        deps=["arxiv-papers"],
        sql='''
            SELECT
                arxiv_id,
                title,
                abstract,
                authors,
                submitter,
                primary_category,
                categories,
                doi,
                journal_ref,
                report_no,
                comments,
                num_versions,
                TRY_CAST(created_date AS DATE) AS created_date
            FROM (
                SELECT
                    *,
                    row_number() OVER (PARTITION BY arxiv_id ORDER BY arxiv_id) AS _rn
                FROM "arxiv-papers"
                WHERE arxiv_id IS NOT NULL
            )
            WHERE _rn = 1
        ''',
        key=("arxiv_id",),
        temporal="created_date",
    ),
]
