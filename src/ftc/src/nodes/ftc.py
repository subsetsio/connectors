"""FTC bulk CSV datasets.

Every accepted dataset is a small, flat CSV linked from the FTC data-sets page.
The FTC appends revision suffixes to filenames, so fetches resolve the current
URL from the landing page at run time.
"""

import re

from subsets_utils import NodeSpec, save_raw_ndjson

from utils import BASE, _full_url, _get_bytes, _parse_csv

DATASETS_PAGE = BASE + "/policy-notices/open-government/data-sets"

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
    for href in hrefs:
        if "dictionary" in href:
            continue
        if pat.search(href):
            return _full_url(href)
    raise RuntimeError(f"no data-sets CSV link matching slug {slug_prefix!r}")


def fetch_dataset(node_id: str) -> None:
    entity_id = node_id[len("ftc-") :].replace("-", "_")
    url = _find_dataset_url(DATASET_SLUGS[entity_id])
    rows = _parse_csv(_get_bytes(url))
    if not rows:
        raise RuntimeError(f"{node_id}: parsed 0 rows from {url}")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ftc-ftc-civil-penalty-actions", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-ftc-merger-enforcement-actions", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-ftc-nonmerger-enforcement-actions", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-hsr-merger-transactions-by-month", fn=fetch_dataset, kind="download"),
    NodeSpec(id="ftc-hsr-transactions-filings-second-requests-by-fy", fn=fetch_dataset, kind="download"),
]
