"""Eurobarometer — the EU's public-opinion survey programme (DG Communication).

Two published subsets, mirroring the accepted collect entities:

* ``eurobarometer-surveys`` — one row per Eurobarometer survey dataset in the EU
  Open Data Portal catalog, enriched with the EC survey portal's own record
  (fieldwork window, series, themes, instrument, method). Reference table.
* ``eurobarometer-responses`` — the long-format aggregated results, harvested
  from each survey's "Volume A" workbook (weighted results by question). One row
  per (survey, question, banner column, answer): weighted N and the response
  share, plus the question's base N.

Enumeration goes through the catalog's CKAN-compatible ``package_search`` with
``sort=id asc`` — the relevance sort overlaps pages and silently drops records.
Only DG-Communication (COMMU) datasets are Eurobarometer; the same query also
matches third parties who merely cite it.

Volume A is the only aggregated-results artefact, and roughly three quarters of
the catalog ships one. The rest are excluded by the source, not by us: ~90 older
waves publish only .txt/.pdf/.doc tables or respondent-level microdata with no
codebook, and ~60 ship only Volume C (per-country demographic breakdowns).
``surveys.has_volume_a`` records which is which, so the gap is visible in the
data rather than implied by a row count.

Both nodes re-pull the full corpus each run (the source exposes no delta query).
``responses`` parses each Volume-A workbook in a **worker process**: the parse
(openpyxl / xlrd) is CPU-bound and holds the GIL, so a thread pool serialises it
and the ~800-workbook crawl overruns GitHub's six-hour job ceiling. A process
pool parses across every core, which brings the full crawl back inside one DAG
budget window — the orchestrator discards an interrupted node's staged fragments
(they only commit on clean completion), so the run must finish in one window to
land, not resume across a continuation.
"""
from __future__ import annotations

import datetime as dt
import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    list_raw_fragments,
    raw_asset_exists,
    save_raw_parquet,
)

from utils import (
    dataset_notes,
    dataset_title,
    download,
    enumerate_commu_datasets,
    fetch_survey_metadata,
    parse_volume_a,
    survey_id_of,
    volume_a_resources,
    volume_code,
)

RESPONSES_SCHEMA = pa.schema([
    ("survey_id", pa.string()),
    ("source_file", pa.string()),
    ("sheet_name", pa.string()),
    ("block_index", pa.int32()),
    ("question_code", pa.string()),
    ("question_en", pa.string()),
    ("question_fr", pa.string()),
    ("question_title", pa.string()),
    ("banner", pa.string()),
    ("country", pa.string()),
    ("answer", pa.string()),
    ("answer_fr", pa.string()),
    ("answer_index", pa.int32()),
    ("is_subtotal", pa.bool_()),
    ("weighted_n", pa.float64()),
    ("share", pa.float64()),
    ("base_n", pa.float64()),
])

SURVEYS_SCHEMA = pa.schema([
    ("survey_id", pa.string()),
    ("eb_survey_id", pa.int32()),
    ("survey_reference", pa.string()),
    ("title", pa.string()),
    ("description", pa.string()),
    ("survey_type", pa.string()),
    ("series", pa.string()),
    ("themes", pa.string()),
    ("instrument", pa.string()),
    ("method", pa.string()),
    ("directorate_general", pa.string()),
    ("fieldwork_start_date", pa.date32()),
    ("fieldwork_end_date", pa.date32()),
    ("publication_date", pa.date32()),
    ("catalog_created", pa.date32()),
    ("catalog_modified", pa.date32()),
    ("license_id", pa.string()),
    ("num_resources", pa.int32()),
    ("volume_codes", pa.string()),
    ("has_volume_a", pa.bool_()),
])

# The EC survey API is a secondary enrichment surface and a few dataset ids have
# no record there. A widespread miss means the API changed shape, not that the
# surveys vanished — so raise rather than ship a catalog of null fieldwork dates.
MAX_ENRICHMENT_MISS_FRACTION = 0.35

# A Volume-A workbook that parses to nothing is a layout we do not understand.
# Around 23% of them are: legacy .txt/.pdf/.doc tables and respondent-level
# microdata dressed as Volume A. This is the catastrophe guard, not the coverage
# check — the tests/ spec pins the real floor at 600 distinct surveys.
MAX_EMPTY_FRACTION = 0.40
RESPONSE_WORKERS = int(os.environ.get("EUROBAROMETER_RESPONSE_WORKERS", "8"))
MAINTAIN_MAX_AGE_DAYS = 30


def _survey_type(reference, title):
    ref = (reference or "").upper()
    if ref.startswith("STD"):
        return "Standard"
    if ref.startswith(("EBS", "SP")):
        return "Special"
    if ref.startswith("FL"):
        return "Flash"
    low = (title or "").lower()
    for name in ("standard", "special", "flash"):
        if low.startswith(name):
            return name.capitalize()
    return None


def _dictish(value):
    return value.get("description") if isinstance(value, dict) else value


def _date(value):
    """The portal mixes bare ISO dates with full timestamps; keep the day."""
    if not value:
        return None
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def fetch_surveys(node_id: str) -> None:
    """Catalog snapshot, one row per COMMU Eurobarometer dataset."""
    datasets = enumerate_commu_datasets()
    print(f"[surveys] {len(datasets)} DG-Communication datasets enumerated")

    rows, missed = [], 0
    for dataset_id, rec in sorted(datasets.items()):
        resources = rec.get("resources") or []
        codes = sorted({c for c in (volume_code(r) for r in resources) if c})
        eb_id = survey_id_of(dataset_id)

        meta = fetch_survey_metadata(eb_id) if eb_id is not None else None
        if meta is None:
            missed += 1
        meta = meta or {}

        themes = meta.get("themes") or []
        reference = meta.get("reference")
        title = dataset_title(rec)
        fieldwork_start = _date(meta.get("fieldworkStartDate"))
        fieldwork_end = _date(meta.get("fieldworkEndDate"))
        if fieldwork_start and fieldwork_end and fieldwork_start > fieldwork_end:
            fieldwork_start, fieldwork_end = fieldwork_end, fieldwork_start

        rows.append({
            "survey_id": dataset_id,
            "eb_survey_id": eb_id,
            "survey_reference": reference,
            "title": title,
            "description": dataset_notes(rec),
            "survey_type": _survey_type(reference, title),
            "series": _dictish(meta.get("serie")),
            "themes": "; ".join(t["description"] for t in themes
                                if t.get("description")) or None,
            "instrument": _dictish(meta.get("instrument")),
            "method": _dictish(meta.get("method")),
            "directorate_general": _dictish(meta.get("dg")),
            "fieldwork_start_date": fieldwork_start,
            "fieldwork_end_date": fieldwork_end,
            "publication_date": _date(meta.get("publicationFirstDate")),
            "catalog_created": _date(rec.get("metadata_created")),
            "catalog_modified": _date(rec.get("metadata_modified")),
            "license_id": rec.get("license_id"),
            "num_resources": len(resources),
            "volume_codes": ",".join(codes) or None,
            "has_volume_a": "A" in codes,
        })

    if rows and missed > len(rows) * MAX_ENRICHMENT_MISS_FRACTION:
        raise RuntimeError(
            f"[surveys] survey/get/one returned no record for {missed} of "
            f"{len(rows)} datasets — the EC survey API changed shape")

    print(f"[surveys] {len(rows)} rows, {missed} without an EC survey record, "
          f"{sum(r['has_volume_a'] for r in rows)} with a Volume A workbook")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=SURVEYS_SCHEMA), node_id)


def _fetch_response_rows(dataset_id: str, resources: list[tuple[str, str]]) -> tuple[str, list[dict], int]:
    rows = []
    failed = 0
    for title, url in resources:
        try:
            payload = download(url)
        except Exception as exc:
            # A dead distribution link is the source's problem, not a bug:
            # isolate it so one 404 cannot sink the whole crawl.
            print(f"[responses] {dataset_id}: download failed {title!r} "
                  f"{type(exc).__name__}: {exc}")
            failed += 1
            continue
        for row in parse_volume_a(payload, title):
            row["survey_id"] = dataset_id
            rows.append(row)
    return dataset_id, rows, failed


def fetch_responses(node_id: str) -> None:
    """Parse every Volume-A workbook into long format, one fragment per dataset."""
    datasets = enumerate_commu_datasets()
    run_id = os.environ.get("RUN_ID", "unknown")
    # GitHub's six-hour deadline can finalize a crawl before the DAG's same-run
    # continuation chain completes. Treat manifest-committed Volume-A fragments
    # as durable work: the corpus is historical, and re-enumeration below still
    # discovers and fetches new surveys that do not have a fragment yet.
    committed = set(list_raw_fragments(node_id, "parquet"))
    if committed:
        print(f"[responses] resuming run {run_id}: {len(committed)} fragments already committed")

    targets = {d: volume_a_resources(rec) for d, rec in sorted(datasets.items())}
    targets = {d: r for d, r in targets.items() if r}
    print(f"[responses] {len(targets)} of {len(datasets)} datasets ship a Volume A")

    written = resumed = failed = empty = 0
    pending = []
    for dataset_id, resources in targets.items():
        if dataset_id in committed:
            resumed += 1
            continue
        pending.append((dataset_id, resources))

    workers = min(RESPONSE_WORKERS, max(1, len(pending)))
    # Parse in worker PROCESSES: openpyxl/xlrd hold the GIL, so a thread pool
    # would parse one workbook at a time and the crawl overruns the job ceiling.
    # fork inherits the imported parser + HTTP session; the node process holds no
    # threads at this point, so forking is clean. save_raw_parquet stays in the
    # parent — the worker only downloads + parses and ships back plain rows.
    ctx = multiprocessing.get_context("fork")
    print(f"[responses] parsing {len(pending)} pending datasets with {workers} worker processes")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        futures = {pool.submit(_fetch_response_rows, dataset_id, resources): dataset_id
                   for dataset_id, resources in pending}
        for future in as_completed(futures):
            try:
                dataset_id, rows, failures = future.result()
            except Exception as exc:
                # A worker that died parsing one workbook (crash, unpicklable
                # payload) must not sink the whole crawl — count it and move on.
                print(f"[responses] {futures[future]}: worker failed "
                      f"{type(exc).__name__}: {exc}")
                failed += 1
                continue
            failed += failures
            if not rows:
                empty += 1
                continue
            save_raw_parquet(pa.Table.from_pylist(rows, schema=RESPONSES_SCHEMA),
                             node_id, fragment=dataset_id)
            written += 1

    print(f"[responses] done: {written} fragments written, {resumed} resumed, "
          f"{empty} parsed to nothing, {failed} downloads failed")
    if written + resumed == 0:
        raise RuntimeError("[responses] no dataset produced any rows — the catalog "
                           "shape or the Volume-A parser is broken")
    if empty > len(targets) * MAX_EMPTY_FRACTION:
        raise RuntimeError(
            f"[responses] {empty} of {len(targets)} Volume-A workbooks parsed to zero "
            "rows — the banner layout changed and the parser is dropping the corpus")


DOWNLOAD_SPECS = [
    NodeSpec(id="eurobarometer-surveys", fn=fetch_surveys, kind="download"),
    NodeSpec(id="eurobarometer-responses", fn=fetch_responses, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="eurobarometer-surveys",
        description=(
            "Eurobarometer catalog and survey metadata are re-observed monthly; "
            "skip when the raw survey snapshot is under 30 days old, matching "
            "maintenance.json's inferred cadence."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "parquet", max_age_days=MAINTAIN_MAX_AGE_DAYS),
    ),
    MaintainSpec(
        asset_id="eurobarometer-responses",
        description=(
            "Volume-A workbooks are historical with no delta endpoint; re-pull "
            "monthly to catch newly published waves while skipping a fresh full "
            "response corpus."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "parquet", max_age_days=MAINTAIN_MAX_AGE_DAYS),
    ),
]
