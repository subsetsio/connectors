"""arXiv connector — full paper-metadata corpus from the weekly Kaggle snapshot.

Mechanism: the Cornell-University/arxiv Kaggle dataset's single file
`arxiv-metadata-oai-snapshot.json` — one JSON object per line, one line per
paper, the whole corpus (~2.9M papers, old-style archive/YYMMNNN ids from 1991
plus new-style YYMM.NNNNN from April 2007). Kaggle refreshes it roughly weekly
(verified: version 296, updated 2026-07-25, containing ids through 2607.*).

The single-file download endpoint

    https://www.kaggle.com/api/v1/datasets/download/Cornell-University/arxiv/
        arxiv-metadata-oai-snapshot.json

requires NO authentication: it 302-redirects to a signed storage.googleapis.com
URL and serves the raw NDJSON (not a zip; ~5.4 GB). Range requests work.

History / why not the alternatives:
- Until 2026-07 this connector read the anonymous GCS mirror
  `gs://arxiv-dataset/metadata-v5/arxiv-metadata-oai.json`, which is FROZEN at
  the 2020-08 snapshot — the published corpus ended April 2020 while weekly
  runs kept re-publishing it as "changed" (issues tracker problem 085).
- arXiv's OAI-PMH endpoint (`oaipmh.arxiv.org`) returns a hard 406 to
  datacenter IP ranges (every GitHub Actions runner) — verified previously;
  no header/UA change unblocks it.
- The authenticated Kaggle API needs a token; the anonymous single-file
  download above does not, and it serves the SAME weekly-refreshed object.

Freshness guard: a completed full pass raises unless the max v1-submission
date seen is recent — if Kaggle ever freezes this dataset the way the GCS
mirror froze, runs go red instead of silently re-publishing a stale corpus.
The published table additionally carries a `freshness` test on created_date.

Shape / continuation: every run streams the whole snapshot and writes the raw
as named parquet fragments of ONE asset (`arxiv-papers`, fragments
`part-0000`, `part-0001`, ... of BATCH_ROWS lines each, in file order). The
fragment layout makes the ingest resumable: fragments committed under the
current RUN_ID (earlier continuation legs, or an earlier in-process attempt)
are skipped by fast-forwarding the stream without JSON-parsing those lines,
and when the node's soft time budget expires at a batch boundary it returns
True so the run hands off as needs_continuation and the next leg resumes.
A full pass takes well under one leg (~30-60 min); the machinery is a
safety net, not the expected path.

Dates: new-style records carry `versions[0].created` (RFC-2822, the v1
submission timestamp) → `created_date` is the REAL submission date
(previously: month-granular YYYY-MM-01 derived from the id; the id-derived
month remains the fallback for the rare record without versions). Also
carried: `update_date` (Kaggle's last-metadata-touch date) and `license`.
"""
from __future__ import annotations

import json
import os
import re
import time
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, get_client, list_raw_fragments, save_raw_parquet

SNAPSHOT_URL = (
    "https://www.kaggle.com/api/v1/datasets/download/"
    "Cornell-University/arxiv/arxiv-metadata-oai-snapshot.json"
)
CATEGORY_TAXONOMY_URL = "https://arxiv.org/category_taxonomy"

# Rows per raw fragment. ~2.9M rows / 100k ≈ 29 fragments; keeps peak memory
# bounded (abstracts dominate, ~1-2 KB/row) and gives continuation legs a
# commit granularity to resume from.
BATCH_ROWS = 100_000

# If more than this fraction of parsed lines fail to parse, the download is
# corrupt — raise rather than publish a truncated corpus.
MAX_BAD_FRACTION = 0.01

# A complete snapshot is ~2.9M lines (2026-07). Anything far below this is a
# truncated stream, not the corpus.
MIN_TOTAL_LINES = 2_400_000

# A current corpus always contains papers submitted within the last few weeks
# (arXiv announces every weekday; the snapshot refreshes weekly). A completed
# full pass whose newest v1-submission date is older than this many days means
# the upstream snapshot has frozen — fail loudly (problem 085 was exactly this
# failure mode going unnoticed for six years).
MAX_STALENESS_DAYS = 60

# Soft per-node time budget (seconds). The cloud leg budget is 5h45m for the
# whole DAG; stopping this node at 5h leaves the transform leg headroom. At a
# batch boundary past the budget the node flushes, returns True, and the run
# continues in the next leg.
TIME_BUDGET_S = float(os.environ.get("ARXIV_TIME_BUDGET_S", 5 * 3600))

# Whole-stream retry attempts for transient network failures. Fragments
# flushed before the failure are visible via the in-process pending overlay of
# list_raw_fragments, so a retry fast-forwards past them.
STREAM_ATTEMPTS = 3

_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError,
)

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
        ("license", pa.string()),
        ("num_versions", pa.int32()),
        ("created_date", pa.string()),
        ("update_date", pa.string()),
    ]
)

CATEGORY_SCHEMA = pa.schema(
    [
        ("category_id", pa.string()),
        ("category_name", pa.string()),
        ("group_name", pa.string()),
        ("archive_id", pa.string()),
        ("archive_name", pa.string()),
        ("description", pa.string()),
        ("source_url", pa.string()),
    ]
)


class _CategoryTaxonomyParser(HTMLParser):
    """Extract category rows from arXiv's taxonomy page.

    The page is a sequence of accordion group headings plus category rows:
    h2 = group, optional h3 = physics archive, h4 = category id/name, p =
    description.
    """

    _CATEGORY_RE = re.compile(r"^([^\s()]+)\s*\((.+)\)$")
    _ARCHIVE_RE = re.compile(r"^(.*?)\s*\(([^()]+)\)$")

    def __init__(self) -> None:
        super().__init__()
        self._in_taxonomy = False
        self._capture: str | None = None
        self._parts: list[str] = []
        self._group_name: str | None = None
        self._archive_name: str | None = None
        self._archive_id: str | None = None
        self._pending_category: tuple[str, str] | None = None
        self.rows: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs_dict = dict(attrs)
        if tag == "div" and attrs_dict.get("id") == "category_taxonomy_list":
            self._in_taxonomy = True
        if self._in_taxonomy and tag in {"h2", "h3", "h4", "p"}:
            self._capture = tag
            self._parts = []

    def handle_endtag(self, tag: str) -> None:
        if not self._in_taxonomy or tag != self._capture:
            return
        text = " ".join("".join(self._parts).split())
        if tag == "h2" and text:
            self._group_name = text
            self._archive_name = None
            self._archive_id = None
        elif tag == "h3" and text:
            match = self._ARCHIVE_RE.match(text)
            self._archive_name = match.group(1).strip() if match else text
            self._archive_id = match.group(2).strip() if match else None
        elif tag == "h4" and text:
            match = self._CATEGORY_RE.match(text)
            if match:
                self._pending_category = (match.group(1).strip(), match.group(2).strip())
        elif tag == "p" and self._pending_category:
            category_id, category_name = self._pending_category
            archive_id = self._archive_id or (
                category_id.split(".", 1)[0] if "." in category_id else category_id
            )
            self.rows.append(
                {
                    "category_id": category_id,
                    "category_name": category_name,
                    "group_name": self._group_name,
                    "archive_id": archive_id,
                    "archive_name": self._archive_name or self._group_name,
                    "description": text,
                    "source_url": CATEGORY_TAXONOMY_URL,
                }
            )
            self._pending_category = None
        self._capture = None
        self._parts = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._parts.append(data)


def _clean(val) -> str | None:
    if val is None:
        return None
    s = str(val).strip()
    return s or None


def _month_from_id(arxiv_id: str | None) -> str | None:
    """Fallback month-granular submission date derived from the arXiv id.

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


def _created_date(rec: dict, arxiv_id: str | None) -> str | None:
    """Day-granular v1 submission date from `versions[0].created` (RFC-2822);
    id-derived YYYY-MM-01 when versions are absent/unparseable."""
    versions = rec.get("versions")
    if isinstance(versions, list) and versions:
        created = (versions[0] or {}).get("created") if isinstance(versions[0], dict) else None
        if created:
            try:
                return parsedate_to_datetime(created).date().isoformat()
            except (ValueError, TypeError):
                pass
    return _month_from_id(arxiv_id)


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
        "license": _clean(rec.get("license")),
        "num_versions": len(versions) if isinstance(versions, list) else None,
        "created_date": _created_date(rec, arxiv_id),
        "update_date": _clean(rec.get("update_date")),
    }


def _fragment(idx: int) -> str:
    return f"part-{idx:04d}"


def _done_fragments(asset: str) -> set[str]:
    """Fragments already committed (or staged by this process) under the
    current RUN_ID — the resume set for continuation legs and in-process
    retries. Fragments from OTHER runs are not skipped: a new run means a new
    (possibly newer) snapshot, so everything is re-fetched and re-written."""
    run_id = os.environ.get("RUN_ID", "unknown")
    frags = list_raw_fragments(asset, "parquet")
    return {f for f, m in frags.items() if m.get("run_id") == run_id}


class _Budget:
    def __init__(self, seconds: float):
        self.deadline = time.monotonic() + seconds

    def expired(self) -> bool:
        return time.monotonic() > self.deadline


def _stream_once(asset: str, budget: _Budget) -> tuple[bool, int, int, int, str]:
    """One full pass over the snapshot stream.

    Returns (needs_continuation, total_lines_seen, parsed, bad, max_created).
    Fragment boundaries are LINE-INDEX boundaries (fragment part-K holds the
    parseable lines [K*BATCH_ROWS, (K+1)*BATCH_ROWS)), so the layout is
    deterministic for a given snapshot regardless of bad lines. Batches whose
    fragment is already committed for this RUN_ID are fast-forwarded
    (counted, not parsed, not re-written).
    """
    done = _done_fragments(asset)
    if done:
        print(f"  arxiv: resuming — {len(done)} fragment(s) already committed for this run")

    client = get_client()
    rows: list[dict] = []
    open_idx: int | None = None  # batch currently accumulating
    line_no = 0        # non-empty lines seen (== global row index)
    parsed = 0
    bad = 0
    flushed = 0
    max_created = ""

    def _flush(idx: int) -> None:
        nonlocal rows, flushed
        table = pa.Table.from_pylist(rows, schema=SCHEMA)
        save_raw_parquet(table, asset, fragment=_fragment(idx))
        flushed += 1
        rows = []

    with client.stream("GET", SNAPSHOT_URL, timeout=httpx.Timeout(30.0, read=600.0),
                       follow_redirects=True) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line or not line.strip():
                continue
            idx = line_no // BATCH_ROWS
            line_no += 1
            if _fragment(idx) in done:
                continue  # fast-forward: already committed this run
            if open_idx is not None and idx != open_idx:
                _flush(open_idx)
                if budget.expired():
                    print(f"  arxiv: time budget expired after fragment "
                          f"{_fragment(open_idx)} — handing off for continuation")
                    return True, line_no, parsed, bad, max_created
            open_idx = idx
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            row = _row(rec)
            parsed += 1
            if row["created_date"] and row["created_date"] > max_created:
                max_created = row["created_date"]
            rows.append(row)

    if open_idx is not None:
        _flush(open_idx)

    print(f"  arxiv: streamed {line_no:,} lines ({parsed:,} parsed, {bad} bad), "
          f"wrote {flushed} fragment(s), max created_date {max_created or 'n/a'}")
    return False, line_no, parsed, bad, max_created


def fetch_papers(node_id: str) -> bool | None:
    asset = node_id  # "arxiv-papers" — also the view the transform reads
    budget = _Budget(TIME_BUDGET_S)
    started_fresh = not _done_fragments(asset)

    last_exc: Exception | None = None
    for attempt in range(1, STREAM_ATTEMPTS + 1):
        try:
            cont, seen, parsed, bad, max_created = _stream_once(asset, budget)
            break
        except _TRANSIENT_EXC as exc:
            last_exc = exc
            print(f"  arxiv: transient stream failure (attempt {attempt}/{STREAM_ATTEMPTS}): {exc}")
            if budget.expired():
                # Flushed fragments are staged; hand off rather than burn the leg.
                return True
            time.sleep(min(60, 5 * attempt))
    else:
        raise RuntimeError(f"arxiv: stream failed {STREAM_ATTEMPTS} times") from last_exc

    if cont:
        return True  # needs_continuation — next leg resumes past committed fragments

    # Completed pass — validate before letting the transform publish.
    if seen == 0:
        raise RuntimeError("arxiv: snapshot stream yielded no lines")
    if seen < MIN_TOTAL_LINES:
        raise RuntimeError(
            f"arxiv: only {seen:,} lines (< {MIN_TOTAL_LINES:,}) — snapshot truncated?"
        )
    if parsed and bad > parsed * MAX_BAD_FRACTION:
        raise RuntimeError(
            f"arxiv: {bad}/{parsed} parsed lines failed (> {MAX_BAD_FRACTION:.0%}) "
            "— snapshot likely corrupt"
        )
    if started_fresh and max_created:
        from datetime import date, timedelta
        floor = (date.today() - timedelta(days=MAX_STALENESS_DAYS)).isoformat()
        if max_created < floor:
            raise RuntimeError(
                f"arxiv: newest v1 submission {max_created} is older than "
                f"{MAX_STALENESS_DAYS}d — the Kaggle snapshot appears frozen "
                "(refusing to re-publish a stale corpus; see problem 085)"
            )
    return None


def fetch_categories(node_id: str) -> None:
    resp = get_client().get(CATEGORY_TAXONOMY_URL, timeout=30.0)
    resp.raise_for_status()

    parser = _CategoryTaxonomyParser()
    parser.feed(resp.text)
    rows = sorted(parser.rows, key=lambda r: str(r["category_id"]))
    if len(rows) < 150:
        raise RuntimeError(
            f"arxiv: parsed only {len(rows)} category taxonomy rows "
            f"from {CATEGORY_TAXONOMY_URL}"
        )
    if len({r["category_id"] for r in rows}) != len(rows):
        raise RuntimeError("arxiv: duplicate category ids in taxonomy parse")

    table = pa.Table.from_pylist(rows, schema=CATEGORY_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="arxiv-categories", fn=fetch_categories, kind="download"),
    NodeSpec(id="arxiv-papers", fn=fetch_papers, kind="download"),
]
