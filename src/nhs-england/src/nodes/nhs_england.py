"""NHS England statistics — one download node per accepted statistical work area.

Each work area's landing page (and its same-section sub-pages) is scraped for
the current .xls/.xlsx workbook URLs (research: scrape_index -> bulk_files; the
file URLs are point-in-time, so they are re-discovered every refresh, never
hardcoded). The chosen workbooks — preferring the full-history "time series"
workbook — are extracted to a uniform tidy table (see src/utils.py):

    source_file | sheet | series | period (DATE) | value (DOUBLE)

Full re-pull each refresh (stateless): the time-series workbooks already carry
the complete history, and the source exposes no incremental/`since` filter.
"""
import pyarrow as pa
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    raw_asset_exists,
    raw_parquet_writer,
)

from constants import ENTITY_IDS
from utils import (
    SCHEMA,
    discover_files,
    iter_sheets,
    select_files,
    tidy_sheet,
)

SLUG = "nhs-england"
_BATCH = 50000

NO_WORKBOOK_IDS = {
    "child-immunisation",
    "dental-commissioning",
    "diagnostic-imaging-dataset",
    "gp-patient-survey",
    "gpps-dental-statistics",
    "marthas-rule",
    "nhs-staff-survey-in-england",
    "patient-safety-data",
    "patient-surveys",
    "proms",
    "screening",
    "under-16-cancer-patient-experience-survey",
}


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    slug = node_id.removeprefix(f"{SLUG}-")

    files = discover_files(slug)
    chosen = select_files(slug, files)
    if not chosen:
        if slug in NO_WORKBOOK_IDS:
            with raw_parquet_writer(asset, SCHEMA):
                pass
            return
        # Some work areas publish only PDFs, or host their data on a separate
        # site — no on-site machine-readable workbook to fetch.
        raise RuntimeError(
            f"{slug}: no .xls/.xlsx workbook found on the landing page or its "
            f"sub-pages ({len(files)} total links) — nothing to fetch"
        )

    total = 0
    with raw_parquet_writer(asset, SCHEMA) as writer:
        batch = []
        for url in chosen:
            for source_file, sheet, raw in iter_sheets(url):
                rows = tidy_sheet(raw, source_file, sheet)
                if not rows:
                    continue
                batch.extend(rows)
                total += len(rows)
                while len(batch) >= _BATCH:
                    writer.write_table(pa.Table.from_pylist(batch[:_BATCH], schema=SCHEMA))
                    batch = batch[_BATCH:]
        if batch:
            writer.write_table(pa.Table.from_pylist(batch, schema=SCHEMA))

    if total == 0:
        raise RuntimeError(
            f"{slug}: workbooks {[u.rsplit('/', 1)[-1] for u in chosen]} "
            "produced 0 tidy rows — no date-indexed table detected"
        )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# NHS England statistical releases are mostly monthly/quarterly. The workbook
# URLs are point-in-time (a new file each release), so ETag/Last-Modified on a
# stable URL is unavailable — fall back to age-based freshness sized to the
# fastest (monthly) cadence: refetch when the local raw is older than 25 days.
MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "NHS England statistics refresh monthly/quarterly "
            "(https://www.england.nhs.uk/statistics/statistical-work-areas/); "
            "point-in-time file URLs, so age-based (inferred — no stable validator)"
        ),
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=25),
    )
    for spec in DOWNLOAD_SPECS
]
