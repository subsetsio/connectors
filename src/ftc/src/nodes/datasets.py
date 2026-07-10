"""FTC bulk CSV datasets — the parametric flat single-table CSV family.

Stateless full re-pull each refresh. Every dataset is a single small CSV
(KB to low-MB) fetched whole; there is no incremental filter on the static
files, so we re-fetch the full corpus every run and overwrite. File slugs are
stable but carry an incrementing numeric suffix on revision (e.g. _2, _3), so we
resolve the current filename from the data-sets landing page at fetch time
rather than hardcoding it.
"""

import re

from subsets_utils import NodeSpec, save_raw_ndjson

from utils import BASE, _full_url, _get_bytes, _parse_csv

DATASETS_PAGE = BASE + "/policy-notices/open-government/data-sets"

# entity_id -> stable filename slug prefix on the data-sets page
# (without the version suffix or .csv extension).
DATASET_SLUGS = {
    "ftc_civil_penalty_actions": "ftc_civil_penalty_actions",
    "ftc_merger_enforcement_actions": "ftc_merger_enforcement_actions",
    "ftc_nonmerger_enforcement_actions": "ftc_nonmerger_enforcement_actions",
    "hsr_merger_transactions_by_month": "hsr_merger_transactions_by_month",
    "hsr_transactions_filings_second_requests_by_fy": "hsr_transactions_filings_second_requests_by_fy",
}


def _find_dataset_url(slug_prefix: str) -> str:
    html = _get_bytes(DATASETS_PAGE).decode("utf-8", "replace")
    hrefs = re.findall(r'href="([^"]*attachments/data-sets/[^"]+\.csv)"', html)
    pat = re.compile(rf"/{re.escape(slug_prefix)}(?:_\d+)?\.csv$")
    for h in hrefs:
        if "dictionary" in h:
            continue
        if pat.search(h):
            return _full_url(h)
    raise RuntimeError(f"no data-sets CSV link matching slug {slug_prefix!r}")


def fetch_dataset(node_id: str) -> None:
    """Fetch one flat single-table CSV dataset, resolving the current versioned
    filename from the landing page."""
    asset = node_id
    entity_id = node_id[len("ftc-"):].replace("-", "_")
    slug_prefix = DATASET_SLUGS[entity_id]
    url = _find_dataset_url(slug_prefix)
    rows = _parse_csv(_get_bytes(url))
    if not rows:
        raise RuntimeError(f"{asset}: parsed 0 rows from {url}")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="ftc-ftc-civil-penalty-actions", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-ftc-merger-enforcement-actions", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-ftc-nonmerger-enforcement-actions", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-hsr-merger-transactions-by-month", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-hsr-transactions-filings-second-requests-by-fy", fn=fetch_dataset, kind="download"),
]
