"""DHS Office of Homeland Security Statistics (OHSS) connector.

Mechanism: bulk_xlsx (research's chosen mechanism). OHSS has no API; the data
surface is multi-sheet Excel workbooks linked from topic landing pages, behind
Akamai bot-manager (httpx's default TLS fingerprint is 403'd — see
utils.install_browser_client). Download URLs are point-in-time, so each fetch
re-discovers the current workbook by scraping the topic pages, then extracts and
parses its one target sheet.

Shape: stateless full re-pull (shape 1). Each entity is one sheet of one
workbook; both the Yearbook section workbooks and the Immigration Enforcement
monthly workbook are cumulative (a single current workbook holds the full
historical span per table), so one download per entity captures the whole series
— no watermark, no incremental query (the source exposes none). Many entities
share a workbook (all enforcement-* read the latest monthly workbook; each
yearbook section's tables share that section's workbook); independent download
nodes re-fetch it per entity, which is cheap at this corpus size.

Raw is NDJSON: each sheet has its own column set and mixed numeric/label types,
so the drifty-friendly writer fits; transform reads it straight back. parse_sheet
reconstructs each human-formatted table faithfully (header detection, newspaper-
column un-tiling, sparse-label forward-fill, numeric coercion).
"""

from constants import ENTITY_META
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import (
    install_browser_client,
    yearbook_workbook_url,
    enforcement_workbook_url,
    download_workbook,
    parse_sheet,
)

SLUG = "dhs-office-of-homeland-security-statistics"
PREFIX = SLUG + "-"


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len(PREFIX):]
    meta = ENTITY_META[entity]

    install_browser_client()  # browser-TLS client so Akamai doesn't 403 us
    if meta["section_kw"] is None:
        url = enforcement_workbook_url()
    else:
        url = yearbook_workbook_url(meta["section_kw"])

    content = download_workbook(url)
    _, rows = parse_sheet(content, meta["sheet"])
    if not rows:
        raise RuntimeError(
            f"{node_id}: parsed 0 rows from sheet {meta['sheet']!r} in {url}"
        )
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_META
]

# One published Delta table per subset: a thin pass-through of the faithfully
# parsed sheet (parse_sheet already did header detection / typing / reshape, so
# the SQL stays a straight projection). A 0-row result fails the node by design.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
