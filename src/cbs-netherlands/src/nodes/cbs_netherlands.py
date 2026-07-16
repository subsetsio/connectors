"""CBS (Netherlands) — StatLine open data connector.

Source: Statistics Netherlands (CBS) StatLine, exposed as OData v3 plus the
CBS datasets bulk distributions.

Access strategy (per research): the catalog at
``https://opendata.cbs.nl/ODataCatalog/Tables`` enumerates every StatLine
table. For the data payload, prefer the newer CBS datasets CSV distribution
(``https://datasets.cbs.nl/csv/CBS/nl/{id}``) when present: large tables that
time out through JSON paging are served there as compact zip files. Fall back to
the OData **Feed** (``https://opendata.cbs.nl/ODataFeed/odata/{id}/TypedDataSet``)
only for tables without a bulk CSV distribution.

Fetch shape — **stateless full re-pull** (implement-prompt shape 1). CBS tables
are revised in place (provisional → revised → definite), so we never trust a
stored row-level high-water mark: each refresh re-snapshots the whole table
from the first page and overwrites the single raw asset. The TypedDataSet
endpoint exposes no row-level ``since``/``modifiedAfter`` filter, so genuine
incremental is not possible here; the only delta signal is table-level
``Modified`` on the catalog. The full crawl is therefore expensive, which is the
documented cost of having no row-level delta filter. Memory stays bounded by
streaming each row straight to a gzipped NDJSON file rather than buffering.

Re-pull is stateless but not unconditional: the *fetch fns* stay dumb (if one is
invoked, it fetches), while ``MAINTAIN_SPECS`` at the bottom of this module owns
"should this table run at all?" — a whole-snapshot age check against the raw
manifest. That split is what lets a ~19h corpus finish inside repeated ~5h45m
invocations; see the comment there, it is load-bearing.

Raw format — **CSV.GZ**. Every table has its own column set (each StatLine
table is a distinct dimension/topic schema), so a single shared parquet schema
is impossible; compressed CSV lets DuckDB infer each table independently while
matching the source's own bulk distribution. One raw asset per table.

Rows are the source's own wide ``TypedDataSet`` records, with two normalisations
applied in the fetch fn because raw is the contract and neither fact is
recoverable downstream:

* the serving-side row counter ``ID`` is dropped — it is not table content;
* every dimension code is stripped of CBS's fixed-width right padding
  (``"GM1680    "``) and paired with a ``<DimKey>_label`` column resolved from
  that dimension's own code-list entity set. Without it a published table reads
  ``WijkenEnBuurten = "GM1680"`` and nothing else.
"""

import csv
import io
import socket
import zipfile

from constants import ENTITY_IDS
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    raw_writer,
    transient_retry,
)

# ---------------------------------------------------------------------------
# Source surface
# ---------------------------------------------------------------------------

FEED_BASE = "https://opendata.cbs.nl/ODataFeed/odata"
CATALOG_BASE = "https://opendata.cbs.nl/ODataCatalog"
DATASETS_BASE = "https://datasets.cbs.nl/odata/v1/CBS"
MAX_PAGES = 200_000        # safety ceiling (~2e9 rows); raises, never silent

# One constant for the raw extension: the raw manifest addresses an asset by
# (id, ext) with an EXACT string match, so a writer/skip-check drift here would
# silently make every MaintainSpec check return False and re-crawl the corpus.
RAW_EXT = "csv.gz"

# Refresh window for the maintain skip — matches maintenance.json cadence_days.
REFRESH_DAYS = 7

# The theme taxonomy is a catalog-level entity set, not a StatLine table: it has
# no Feed endpoint, no dimensions and no TypedDataSet. It gets its own fetch fn.
THEMES_ENTITY_ID = "cbs-themes"

# DataProperties `Type` values that name a code-list entity set on the table.
DIMENSION_TYPES = frozenset({"Dimension", "GeoDimension", "GeoDetail", "TimeDimension"})

# The serving-side row counter on every TypedDataSet record.
ROW_ID_COLUMN = "ID"


def _node_id(entity_id: str) -> str:
    """Map a StatLine identifier to its download spec id (and asset name)."""
    return f"cbs-netherlands-{entity_id.lower().replace('_', '-')}"


# Reverse lookup: spec id -> original-case identifier (needed because the
# transform back from a lowercased/dash-normalised id is ambiguous, e.g.
# '7052_95'). Pure in-memory derivation, no I/O.
_EID_BY_NODE = {_node_id(eid): eid for eid in ENTITY_IDS}


# ---------------------------------------------------------------------------
# HTTP with honest retry semantics
# ---------------------------------------------------------------------------


# opendata.cbs.nl publishes both A and AAAA records, but the cloud runners have
# no IPv6 egress — connecting to the AAAA address raises ENETUNREACH ([Errno 101]
# Network is unreachable) and never falls back to IPv4. Force IPv4 resolution
# process-wide (each spec runs in its own subprocess; everything it talks to —
# CBS and R2 — is reachable over IPv4).
_orig_getaddrinfo = socket.getaddrinfo
_ipv4_forced = False


def _force_ipv4() -> None:
    global _ipv4_forced
    if _ipv4_forced:
        return

    def _ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
        return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

    socket.getaddrinfo = _ipv4_only
    _ipv4_forced = True


# opendata.cbs.nl answers deep pages but intermittently throws a transient 503
# under sustained load (observed mid-crawl on a large table), so a bare
# single-shot call crashes the whole DAG. Retry — but note this stacks
# MULTIPLICATIVELY with the shared client's own retry inside `get()` (4
# attempts, Retry-After honoured). The previous policy here (10 attempts,
# backoff to 300s) therefore meant 40 requests and a ~1073s wall per page: on
# the 2026-07-14 outage every spec burned ~18min before failing, and 10
# sequential specs tripped DAG_MAX_CONSECUTIVE_FAILURES after 3h having learned
# nothing. 5 outer attempts x 4 inner = 20 requests over ~5min still rides out a
# multi-minute wobble, fails a real outage ~4x sooner, and is a great deal
# gentler on a source whose docs ask clients to be considerate. Losing the DAG
# to a bad window is also no longer expensive: MAINTAIN_SPECS below means the
# next invocation resumes instead of re-crawling from table 1.
@transient_retry(attempts=5, min_wait=4, max_wait=60)
def _fetch_page(url: str, params: dict | None = None) -> dict:
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _strip(value):
    """CBS right-pads code values to a fixed width, in both code lists and data."""
    return value.strip() if isinstance(value, str) else value


def _dimension_labels(entity_id: str) -> dict[str, dict[str, str]]:
    """Per dimension key: {stripped code -> title}, from the table's own code lists."""
    properties = _fetch_page(
        f"{FEED_BASE}/{entity_id}/DataProperties", {"$format": "json"}
    )["value"]
    dimensions = [p["Key"] for p in properties if p.get("Type") in DIMENSION_TYPES]
    if not dimensions:
        raise RuntimeError(f"{entity_id}: DataProperties declares no dimensions")

    labels = {}
    for key in dimensions:
        rows = _fetch_page(f"{FEED_BASE}/{entity_id}/{key}", {"$format": "json"})["value"]
        labels[key] = {
            _strip(r["Key"]): r.get("Title") for r in rows if r.get("Key") is not None
        }
    return labels


def _csv_download_url(entity_id: str) -> tuple[str, str] | None:
    """Return (download_url, source_identifier) for the datasets bulk CSV.

    The datasets.cbs.nl v1 catalog currently exposes Dutch distributions. For
    English StatLine twins that are absent there, use the matching NED bulk
    file when the identifier convention is exact (85428ENG -> 85428NED). The
    values are the same statistical observations; the language-specific labels
    remain a known limitation of the bulk surface.
    """
    candidates = [entity_id]
    upper = entity_id.upper()
    if upper.endswith("ENG"):
        candidates.append(entity_id[:-3] + "NED")

    for candidate in candidates:
        payload = _fetch_page(
            f"{DATASETS_BASE}/Datasets",
            {"$format": "json", "$filter": f"Identifier eq '{candidate.upper()}'"},
        )
        for row in payload.get("value", []):
            for dist in row.get("Distributions", []):
                if str(dist.get("Format", "")).lower() == "csv" and dist.get("DownloadUrl"):
                    return dist["DownloadUrl"], row.get("Identifier") or candidate
    return None


def _write_observations_csv_from_zip(node_id: str, download_url: str) -> int:
    """Download a CBS bulk zip and save its Observations.csv as raw CSV.GZ."""
    resp = get(download_url, timeout=(10.0, 240.0))
    resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        name = next((n for n in zf.namelist() if n.endswith("Observations.csv")), None)
        if name is None:
            raise RuntimeError(f"{node_id}: CBS bulk zip has no Observations.csv")

        rows_written = 0
        with zf.open(name) as src, raw_writer(node_id, RAW_EXT, mode="wt", compression="gzip") as out:
            text = io.TextIOWrapper(src, encoding="utf-8-sig", newline="")
            reader = csv.reader(text, delimiter=";")
            writer = csv.writer(out)
            for row in reader:
                writer.writerow([_strip(v) for v in row])
                rows_written += 1

    # rows_written includes the header.
    return max(0, rows_written - 1)


def _write_typed_dataset_csv(node_id: str, entity_id: str) -> int:
    """Fallback path: stream the OData TypedDataSet as CSV.GZ."""
    labels = _dimension_labels(entity_id)

    url = f"{FEED_BASE}/{entity_id}/TypedDataSet"
    params = {"$format": "json"}

    pages = 0
    rows_written = 0
    fieldnames: list[str] | None = None
    with raw_writer(node_id, RAW_EXT, mode="wt", compression="gzip") as fh:
        writer = None
        while url is not None:
            if pages >= MAX_PAGES:
                raise RuntimeError(
                    f"{node_id}: exceeded MAX_PAGES={MAX_PAGES} (source grew "
                    f"past expectations) - investigate before raising the cap"
                )
            payload = _fetch_page(url, params)
            params = None  # nextLink already carries $skip/$format
            rows = payload.get("value", [])
            if rows and fieldnames is None:
                first = {k: _strip(v) for k, v in rows[0].items() if k != ROW_ID_COLUMN}
                for key in labels:
                    first[f"{key}_label"] = None
                fieldnames = list(first)
                writer = csv.DictWriter(fh, fieldnames=fieldnames)
                writer.writeheader()

            for row in rows:
                record = {k: _strip(v) for k, v in row.items() if k != ROW_ID_COLUMN}
                for key, lookup in labels.items():
                    record[f"{key}_label"] = lookup.get(record.get(key))
                writer.writerow({k: record.get(k) for k in fieldnames})
                rows_written += 1
            pages += 1
            url = payload.get("odata.nextLink") or payload.get("@odata.nextLink")
    return rows_written


# ---------------------------------------------------------------------------
# Download — one stateless full snapshot per StatLine table
# ---------------------------------------------------------------------------

def fetch_one(node_id: str) -> None:
    """Write a StatLine table's full observations to one gzipped CSV asset.

    Stateless: re-fetches from the first page every run and overwrites, so
    in-place revisions are always picked up.
    """
    _force_ipv4()
    entity_id = _EID_BY_NODE[node_id]

    bulk = _csv_download_url(entity_id)
    if bulk is not None:
        download_url, source_identifier = bulk
        rows_written = _write_observations_csv_from_zip(node_id, download_url)
        source = f"bulk csv {source_identifier}"
    else:
        rows_written = _write_typed_dataset_csv(node_id, entity_id)
        source = "OData TypedDataSet fallback"

    if rows_written == 0:
        raise RuntimeError(
            f"{node_id}: source served no rows — the catalog lists this table "
            "as live, so an empty response is a source fault, not an empty table"
        )

    print(f"  {node_id}: wrote {rows_written} rows from {source}")


def fetch_themes(node_id: str) -> None:
    """The StatLine subject taxonomy — joinable reference data for the tables.

    Served whole by the catalog service; one row per theme, `ParentID` giving
    the tree. Small enough that paging never engages, but the nextLink loop is
    shared with the table path anyway.
    """
    _force_ipv4()

    url = f"{CATALOG_BASE}/Themes"
    params = {"$format": "json"}

    rows_written = 0
    with raw_writer(node_id, RAW_EXT, mode="wt", compression="gzip") as fh:
        writer = None
        while url is not None:
            payload = _fetch_page(url, params)
            params = None
            for row in payload.get("value", []):
                record = {k: _strip(v) for k, v in row.items()}
                if writer is None:
                    writer = csv.DictWriter(fh, fieldnames=list(record))
                    writer.writeheader()
                writer.writerow(record)
                rows_written += 1
            url = payload.get("odata.nextLink") or payload.get("@odata.nextLink")

    if rows_written == 0:
        raise RuntimeError(f"{node_id}: the Themes entity set served no rows")

    print(f"  {node_id}: wrote {rows_written} themes")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=_node_id(eid),
        fn=fetch_themes if eid == THEMES_ENTITY_ID else fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# ---------------------------------------------------------------------------
# Maintain — the freshness policy, and the only thing that makes this corpus
# finishable at all
# ---------------------------------------------------------------------------
#
# This connector crawls ~1531 tables at roughly 45s each (~19h of fetch), but a
# cloud invocation gets DAG_TIME_BUDGET ~5h45m and the orchestrator treats every
# main.py invocation as a FRESH DAG — cross-invocation node-state resume was
# deliberately removed from the library. So without a maintain skip each run
# restarts at the first table, gets ~460 tables in, and dies at the deadline
# having re-fetched exactly what the last run already had: the corpus can never
# complete. (Observed: run 20260709-112646 committed 462 assets; the 20260713
# re-dispatch then began again at table 1 and made zero progress.)
#
# `raw_asset_exists` resolves through the CONNECTOR-scoped raw manifest, not the
# run-scoped raw dir, so a snapshot committed by an earlier run still counts as
# fresh under a new run_id. That turns each invocation into the next slice of one
# backfill, and once the corpus is whole the same window makes the weekly refresh
# re-pull it — which is what we want, since CBS revises tables in place and the
# TypedDataSet endpoint offers no row-level `since` filter to be cleverer with.
# FORCE_REFRESH=1 bypasses every check.
MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=_node_id(eid),
        description=(
            f"CBS revises StatLine tables in place and exposes no row-level delta "
            f"filter, so freshness is whole-snapshot age: refetch this table when "
            f"its raw snapshot is older than {REFRESH_DAYS}d "
            f"(maintenance.json cadence_days=7). Younger than that, skip — which "
            f"is also how the ~1531-table backfill advances across invocations."
        ),
        check=lambda asset_id: raw_asset_exists(
            asset_id, RAW_EXT, max_age_days=REFRESH_DAYS
        ),
    )
    for eid in ENTITY_IDS
]
